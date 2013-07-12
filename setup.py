from setuptools import setup, find_packages
from setuptools.command.install import install as _install

import sys

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

class InstallHook(_install):
	def run(self):
		self.preInstall()
		_install.run(self)
	def preInstall(self):
		if sys.version_info[0] >= 3 or sys.version_info <= (2,5):
			raise Exception("This module only supports Python 2.6 or 2.7")

setup(
	cmdclass = {"install": InstallHook},
	name = "py.Lang",
	version = "1.0.1",
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
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Operating System :: OS Independent",
	],
)
