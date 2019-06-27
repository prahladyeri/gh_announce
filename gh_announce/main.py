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

def tw_announce(tag_name, repo_name, repo_url):
	ss = "I have" if (config['Full_Name'] == None or config['Full_Name'] == "") else config["Full_Name"] + " has"
	ss += " just released version %s of %s on Github. Check it out! %s" % (tag_name, repo_name.split("/")[1], repo_url)
	#print("TWEETING: " + ss)

	if config['twitter_consumer_api_key'] == "":
		print("twitter api credentials missing")
		return
	auth = tweepy.OAuthHandler(config['twitter_consumer_api_key'], 
		config['twitter_consumer_secret'],
		)
	auth.set_access_token(config['twitter_access_token'], config['twitter_access_token_secret'])
	api = tweepy.API(auth)
	api.update_status(ss)
	print("successfully updated status for repo: %s, tag: %s" % (repo_name, tag_name))
	

def check_activity():
	url = "https://api.github.com/users/%s/events" % config['github_username']
	resp = requests.get(url)
	acts = json.loads(resp.text)
	if len(acts) == 0:
		print("Zero events found, is this the correct github repo I'm looking at?")
		print("Run the program again with --config parameter to set the correct values")
		return
	for i in range(len(acts)):
		act = acts[i]
		if act['type'] == 'CreateEvent': #latest tag
			payload = act['payload']
			if payload['ref_type'] != 'tag':
				continue
			repo = act['repo']
			repo_url = "https://github.com/" + repo['name']
			tag_name = payload['ref']
			
			dt = parse_date(act['created_at'])
			delta = datetime.now() - dt
			days = delta.days
			hrs = delta.seconds // 3600
			mins = (delta.seconds // 60) % 60
			
			if delta.days >= 2: #this push is more than two days old, so just ignore
				continue
				
			tweet = False
			#check local config data to know whether we've already tweeted for this release
			if not 'pushes' in config:
				pushes = [act['id']]
				tweet = True
			else:
				pushes = config['pushes']
				if act['id'] in pushes:
					pass #do nothing
				else:
					tweet = True
					pushes.append(act['id'])
			if tweet:
				try:
					tw_announce(tag_name, repo['name'], repo_url)
				except Exception as ex:
					print("Error occurred: ", str(ex))
			config['pushes'] = pushes
			cfgsaver.save(pkg_name, config)
				 
			#TODO: housekeep the pushes list occasionally
			

def parse_date(dt):
    format = "%Y-%m-%dT%H:%M:%S"
    if dt[-6] in ('+', '-'):
        return datetime.strptime(dt, format + '%z')
    elif dt[-1] == 'Z':
        return datetime.strptime(dt, format + 'Z')
    return datetime.strptime(dt, format)
	
def main(args):
	global config
	if '-v' in args or '--version' in args:
		print("%s version %s" % (__title__, __version__))
		return
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--version', help='Version', action='store_true')
	parser.add_argument('-c', '--config',  default=False, action='store_true', help='setup the app configuration')
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
		if args.config:
			return
	check_activity()

if __name__ == "__main__":
	main(sys.argv[1:])