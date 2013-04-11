from setuptools import setup, find_packages

import sys
if sys.version_info[0] >= 3 or sys.version_info <= (2,5):
	raise Exception("This module only supports Python 2.6 or 2.7")

requirements = ["termcolor"]
try:
	import argparse
except ImportError, err:
	requirements.append("argparse")
try:
	from OrderedDict import OrderedDict
except ImportError:
	requirements.append("OrderedDict")

import platform
if platform.system().lower() == "windows":
	requirements.append("colorama")

setup(
	name = "py.Lang",
	version = "0.5.1",
	description = "Common modules that probably should have been included in the Python standard library but weren't",
	author = "Jesse Cowles",
	author_email = "jcowles@indigital.net",
	url = "http://projects.indigitaldev.net/py.Lang",
	
	package_dir = {"":"src"},
	packages = find_packages("src"),
	zip_safe = False,
	install_requires = requirements,
	classifiers = [
		# http://pypi.python.org/pypi?%3Aaction=list_classifiers
		"Development Status :: 4 - Beta",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Operating System :: OS Independent",
	],
)
