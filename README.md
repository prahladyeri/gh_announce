![pypi](https://img.shields.io/pypi/v/cfgsaver.svg)
![license](https://img.shields.io/github/license/prahladyeri/cfgsaver.svg)
![last-commit](https://img.shields.io/github/last-commit/prahladyeri/cfgsaver.svg)
[![patreon](https://img.shields.io/badge/Patreon-brown.svg?logo=patreon)](https://www.patreon.com/prahladyeri)
[![paypal](https://img.shields.io/badge/PayPal-blue.svg?logo=paypal)](https://paypal.me/prahladyeri)
[![follow](https://img.shields.io/twitter/follow/prahladyeri.svg?style=social)](https://twitter.com/prahladyeri)

# gh-announce

![project logo](https://raw.githubusercontent.com/prahladyeri/gh_announce/master/logo.png)

Twitter bot that posts a tweet each time you make a release on github!

# Synopsis

I happen to maintain a lot of python projects on github such as [distroverify](https://github.com/prahladyeri/distroverify) and [vtscan](https://github.com/prahladyeri/vtscan), and each time I make a tagged release, I have to make a status tweet to let people know. This tool is for automating this process, [read this article to know more details](https://prahladyeri.github.io/blog/2019/06/announcing-gh_announce-a-python-bot-that-posts-a-tweet-each-time-you-make-a-release-on-github.html).

# Installation

	pip install gh_announce

# Usage

* First time only to configure your github username & twitter api details:

		> gh_announce --config

* Testing the app:
	
		> gh_announce
		successfully updated status for repo: prahladyeri/distroverify, tag: 1.0.4
		
* Result:

[![sample screen](https://raw.githubusercontent.com/prahladyeri/gh_announce/master/screen.png)](https://twitter.com/prahladyeri/status/1144223088201986049)

* Set as a cron job by running `crontab -e`:

		* 12 * * * gh_announce