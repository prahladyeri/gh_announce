![pypi](https://img.shields.io/pypi/v/cfgsaver.svg)
![license](https://img.shields.io/github/license/prahladyeri/cfgsaver.svg)
![last-commit](https://img.shields.io/github/last-commit/prahladyeri/cfgsaver.svg)
[![donate](https://img.shields.io/badge/-Donate-blue.svg?logo=paypal)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU)
[![follow](https://img.shields.io/twitter/follow/prahladyeri.svg?style=social)](https://twitter.com/prahladyeri)

# gh-announce

![project logo](https://raw.githubusercontent.com/prahladyeri/gh_announce/master/logo.png)

Twitter bot that posts a tweet each time you make a release on github!

# Synopsis

I happen to maintain a lot of python projects on github such as [distroverify](https://github.com/prahladyeri/distroverify) and [vtscan](https://github.com/prahladyeri/vtscan), and each time I make a tagged release on Github, I have to make a status tweet to let people know. This tool is for automating this process, [read this article to know more details](https://prahladyeri.com/blog/2019/06/announcing-gh_announce-a-python-bot-that-posts-a-tweet-each-time-you-make-a-release-on-github.html).

# Installation

	pip install gh_announce

# Usage

	gh_announce --config # (first time only to configure your github username & twitter api details)
	
	gh_announce # (set as a cron job using crontab -e, etc.)