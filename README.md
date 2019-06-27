# gh-announce
Twitter bot that posts a tweet each time you make a release on github!

# Installation

	pip install gh_announce

# Usage

	gh_configure --config # (first time only to configure your github username & twitter api details)
	
	gh_announce # (set as a cron job using crontab -e, etc.)