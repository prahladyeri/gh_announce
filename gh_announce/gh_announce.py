import requests
import argparse
import os, sys
from datetime import datetime
from cfgsaver import cfgsaver
import json
import tweepy
from gh_announce import pkg_name, __title__, __description__, __version__

config = cfgsaver.get(pkg_name)

config_keys = [
	'github_username',
	'twitter_consumer_api_key',
	'twitter_consumer_secret',
	'twitter_access_token',
	'twitter_access_token_secret',
	'Full_Name',
	]
	
opt_keys = ['Full_Name']

dry_run = False
refresh_tags = False

def fetch_topics(repo_name):
	try:
		# GET /repos/:owner/:repo/topics
		url = "https://api.github.com/repos/%s/topics" % repo_name
		resp = requests.get(url, headers={'Accept':'application/vnd.github.mercy-preview+json'})
		data = json.loads(resp.text)
		names = ["#" + name.replace('-', '_') for name in data['names']]
		print("topics fetched for %s:" % repo_name, names)
		return names
		# if len(acts) == 0:
			# print("Zero events found, is this the correct github repo I'm looking at?")
			# print("Run the program again with --config parameter to set the correct values")
			# return
		# twcnt = 0
		# for i in range(len(acts)):
	except Exception as ex:
		print("Error occurred while fetching topics: " + str(ex))
		return []
		
def do_refresh_tags():
	try:
		# GET /repos/:owner/:repo/topics
		url = "https://api.github.com/users/%s/repos" % config['github_username']
		#print("URL: ",url)
		resp = requests.get(url) #headers={'Accept':'application/vnd.github.mercy-preview+json'}
		data = json.loads(resp.text)
		print("%d repos fetched" % len(data))
		#print("data: ",data)
		if not 'topics' in config: config['topics'] = {}
		for repo in data:
			print("refreshing tags for %s..." % repo['full_name'])
			if not dry_run:
				topics = fetch_topics(repo['full_name'])
				print("%d tags fetched" % len(topics))
				config['topics'][repo['full_name']] = topics
				cfgsaver.save(pkg_name, config)
				print("")
	except Exception as ex:
		print("Error occurred: " + str(ex))
		#raise
	


def tw_announce(id, tag_name, repo_name, repo_url, topics):
	proj_name = repo_name.split("/")[1]
	hash_tags = " ".join(topics)
	ss = "I have" if (config['Full_Name'] == None or config['Full_Name'] == "") else config["Full_Name"] + " has"
	ss += " just released version %s of %s on Github. Check it out! %s %s" % (tag_name, proj_name, repo_url, hash_tags)
	if len(ss) > 280: 
		print("skipped %s as string length is greater than 280" % repo_name)
		return
	if config['twitter_consumer_api_key'] == "":
		print("twitter api credentials missing")
		return
	if not dry_run:
		auth = tweepy.OAuthHandler(config['twitter_consumer_api_key'], 
			config['twitter_consumer_secret'],
			)
		auth.set_access_token(config['twitter_access_token'], config['twitter_access_token_secret'])
		api = tweepy.API(auth)
		api.update_status(ss)
		print("%s: successfully updated status for repo %s, tag: %s" % (id, repo_name, tag_name))
	else:
		print("%s: skipped update: status for repo: %s, tag: %s" % (id, repo_name, tag_name))
	

def check_activity():
	url = "https://api.github.com/users/%s/events" % config['github_username']
	resp = requests.get(url)
	acts = json.loads(resp.text)
	if len(acts) == 0:
		print("Zero events found, is this the correct github repo I'm looking at?")
		print("Run the program again with --config parameter to set the correct values")
		return
	twcnt = 0
	recently_updated = []
	for i in range(len(acts)):
		act = acts[i]
		if act['type'] == 'CreateEvent': #latest tag
			payload = act['payload']
			if payload['ref_type'] != 'tag':
				continue
			repo = act['repo']
			repo_url = "https://github.com/" + repo['name'] #prahladyeri/gh_announce
			tag_name = payload['ref']
			
			dt = parse_date(act['created_at'])
			delta = datetime.now() - dt
			days = delta.days
			hrs = delta.seconds // 3600
			mins = (delta.seconds // 60) % 60
			
			if delta.days >= 2: #this push is more than two days old, so just ignore
				continue
				
			#try to fetch topics
			if not 'topics' in config: config['topics'] = {}
			if repo['name'] not in config['topics'].keys():
				config['topics'][repo['name']] = fetch_topics(repo['name'])
				
			tweet = False
			#check local config data to know whether we've already tweeted for this release
			if not 'pushes' in config:
				pushes = [] #[act['id']]
				tweet = True
			else:
				pushes = config['pushes']
				if not act['id'] in pushes:
					tweet = True
			if tweet: # @todo: check whether dry_run even works or not
				if not dry_run: pushes.append(act['id'])
				try:
					if repo['name'] not in recently_updated:
						tw_announce(act['id'], tag_name, repo['name'], repo_url, config['topics'][repo['name']])
						twcnt += 1
					recently_updated.append(repo['name'])
				except Exception as ex:
					print("Error occurred: ", str(ex))
			config['pushes'] = pushes #TODO: housekeep the pushes list occasionally
			cfgsaver.save(pkg_name, config)
			
	if twcnt == 0: print("no status to update right now")
			

def parse_date(dt):
    format = "%Y-%m-%dT%H:%M:%S"
    if dt[-6] in ('+', '-'):
        return datetime.strptime(dt, format + '%z')
    elif dt[-1] == 'Z':
        return datetime.strptime(dt, format + 'Z')
    return datetime.strptime(dt, format)
	
def announce(args=[]):
	global config, dry_run, refresh_tags
	if '-v' in args or '--version' in args:
		print("%s version %s" % (__title__, __version__))
		return
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--version', help='Version', action='store_true')
	parser.add_argument('-c', '--config',  default=False, action='store_true', help='setup the app configuration')
	parser.add_argument('-n', '--dry-run',  default=False, action='store_true', help='dry run mode')
	parser.add_argument('-r', '--refresh-tags',  default=False, action='store_true', help='refresh tags')
	args = parser.parse_args(args)
	
	if args.config or config == None:
		print("""You need to add some configuration data. Things you'll need:

[1] Your github username (eg: prahladyeri)
[2] Your twitter API credentials. To get those, visit
https://developer.twitter.com/en/apps and register an 
app for yourself. After that, visit the "Keys and tokens" 
section and note down the following four kinds of keys:

(i) Consumer API Key.
(ii) Consumer Secret.
(iii) Access Token.
(iv) Access Token Secret.

Once you have the above information, you can enter the configuration values below.

""")
		config = cfgsaver.get_from_cmd(pkg_name, config_keys, opt_keys)
		if config == None:
			print("Cound't read config values, please start the program again using --config parameter")
			return
		elif args.config:
			return
	dry_run = args.dry_run
	if dry_run: print("running in %s mode" % ("dry run" if dry_run else "normal"))
	if args.refresh_tags:
		refresh_tags = True
		do_refresh_tags()
	else:
		check_activity()
	
def main():
	announce(sys.argv[1:])

if __name__ == "__main__":
	main()