# gh-announce
Twitter bot that posts a tweet each time you make a release on github!

# Synopsis

I happen to maintain a lot of python projects on github such as [distroverify](https://github.com/prahladyeri/distroverify) and [vtscan](https://github.com/prahladyeri/vtscan), and each time I make a tagged release on Github, I have to make a status tweet to let people know. This tool is for automating this process, [read this article to know more details](https://prahladyeri.com/blog/2019/06/announcing-gh_announce-a-python-bot-that-posts-a-tweet-each-time-you-make-a-release-on-github.html).

# Installation

	pip install gh_announce

# Usage

	gh_configure --config # (first time only to configure your github username & twitter api details)
	
	gh_announce # (set as a cron job using crontab -e, etc.)