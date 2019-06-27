#!/usr/bin/env python3
import os
import gh_announce
from gh_announce import pkg_name, __version__, __author__, __email__, __description__
from setuptools import setup, find_packages

# class PostInstallCommand(install):
	# """Post-installation for installation mode."""
	# def run(self):
		# install.run(self)
		# fpath = os.path.join(self.install_lib, pkg_name)
		# fpath = os.path.join(fpath, "cfg.json")
		# cfg_dir = os.path.join(os.path.expanduser("~"), ".config/%s" % pkg_name)
		# if not os.path.isdir(cfg_dir): os.makedirs(cfg_dir)
		# tpath = os.path.join(cfg_dir, "cfg.json")
		# shutil.move(fpath, tpath)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

s = setup(
	name=pkg_name,
	version=__version__,
	license='MIT',
	description=__description__,
	long_description=read("README.md"),
	long_description_content_type='text/markdown',
	keywords="github,twitter,internet",
	url='https://github.com/prahladyeri/' + pkg_name,
	packages=find_packages(),
	include_package_data=True,
	entry_points={
		"console_scripts": [
			"gh_announce = gh_announce.gh_announce:main",
		],
	},
	install_requires=['requests','tweepy'],
	author=__author__,
	author_email=__email__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	# cmdclass={
		# 'install': PostInstallCommand,
	# },
	)
