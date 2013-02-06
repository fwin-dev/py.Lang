from setuptools import setup, find_packages

import sys
if sys.version_info[0] >= 3 or sys.version_info <= (2,5):
	raise Exception("This module only supports Python 2.6 or 2.7")

requirements = ["termcolor"]
try:
	import argparse
except ImportError, err:
	requirements.append("argparse")

setup(
	name = "py.Lang",
	version = "0.5.0",
	description = "Common modules that probably should have been included in the Python standard library but weren't",
	author = "Jesse Cowles",
	author_email = "jcowles@indigital.net",
	url = "http://projects.indigitaldev.net/py.Lang",
	
	package_dir = {"":"src"},
	packages = find_packages("src"),
	zip_safe = False,
	install_requires = requirements,
#	dependency_links = ["http://projects.indigitaldev.net/master#egg=py.OS-0.5.0"],
)
