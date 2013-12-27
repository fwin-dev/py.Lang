from Lang.FuncTools import getArgs

from termcolor import colored
import platform
if platform.system().lower() == "windows":
	from colorama import init
	init()

class FormattedText(str):
	def __new__(cls, text, color=None, background=None,
				bold=None, dark=None, underline=None, blink=None, reverse=None, concealed=None):
		return str.__new__(cls, text)
	
	def __init__(self, text, color=None, background=None,
				bold=None, dark=None, underline=None, blink=None, reverse=None, concealed=None):
		self.rawText = str(text)
		self.color = color
		self.background = background
		self.bold = bold
		self.dark = dark
		self.underline = underline
		self.blink = blink
		self.reverse = reverse
		self.concealed = concealed
		
		self._termcolorAttrs = getArgs(excludeList=["text", "color", "background"])
		self.coloredText = self._generateColored()
		self.data = self.rawText
	
	def asColored(self):
		return self.coloredText
	def asUncolored(self):
		return self.rawText
	def __str__(self):
		return self.asColored()
	def __repr__(self):
		return self.asUncolored()
	
	def _generateColored(self):
		kwargs = {"text": self.rawText}
		if self.color != None:
			kwargs["color"] = self.color
		if self.background != None:
			kwargs["on_color"] = "on_" + self.background
		
		for name, value in self._termcolorAttrs.iteritems():
			if value != True:
				del self._termcolorAttrs[name]
		return colored(attrs=self._termcolorAttrs, **kwargs)
	
	def __getattribute__(self, attrName):
		""" This is necessary to return objects with the extra attributes defined in this class """
		func = super(FormattedText, self).__getattribute__(attrName)
		# any function in this class which returns a string instance must be listed here to avoid infinite recursion
		if not callable(func) or attrName in ["_generateColored", "asColored", "asUncolored"]:   # if it's a property, not a method
			return func
		
		def changeReturnFunc(*args, **kwargs):
			result = func(*args, **kwargs)
			if isinstance(result, basestring):
				return FormattedText(result, color=self.color, background=self.background, bold=self.bold, dark=self.dark,
								   underline=self.underline, blink=self.blink, reverse=self.reverse, concealed=self.concealed)
			else:
				return result
		return changeReturnFunc
	
	def __add__(self, other):
		if isinstance(other, FormattedText):
			return self.asColored() + other.asColored()
		else:
			return self.asColored() + other
