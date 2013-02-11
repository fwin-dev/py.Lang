from _lang import getArgs

from termcolor import colored

def askYesNo(question):
	"""Print a question to the terminal for the user. Expects a yes or no response. Returns True if yes, False if no."""
	return raw_input(question + " [y/n]: ").lower() in ["y", "yes"]

class FormattedText(str):
	def __new__(cls, text, color=None, background=None,
				bold=None, dark=None, underline=None, blink=None, reverse=None, concealed=None):
		return str.__new__(cls, text)
	
	def __init__(self, text, color=None, background=None,
				bold=None, dark=None, underline=None, blink=None, reverse=None, concealed=None):
		self.rawText = text
		self.color = color
		self.background = background
		self.bold = bold
		self.dark = dark
		self.underline = underline
		self.blink = blink
		self.reverse = reverse
		self.concealed = concealed
		
		self._termcolorAttrs = getArgs(useKwargFormat=True, excludeList=["text", "color", "background"])
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
			kwargs["on_color"] = self.background
		
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
	

class Table:
	"""Prints data in a table format to the terminal."""
	def __init__(self):
		self.rows = []
		self.autoResizeCols = True
		self.colMaxLens = None
		self.colHeaders = None
		self._lastPrintedRow = -1
	
	def setColHeaders(self, headers):
		"""
		Column headers will be printed at the top of the table.
		
		@param headers	tuple or list of str:	Headers from left to right
		"""
		self.colHeaders = headers
		self._updateColMaxLens(headers)
	
	def setColMaxLens(self, maxLens):
		"""
		Call before adding rows to set the max lengths of each column.
		
		@param maxLens	iterable of (int or None):	Maximum lengths for each column. Use None for any column for automatic sizing based on column contents and header.
		"""
		self.colMaxLens = maxLens
		self.autoResizeCols = [True if maxLen == None else False for maxLen in self.colMaxLens]
		for row in self.rows:
			self._updateColMaxLens(row)
	
	def getColHeaders(self):
		return self.colHeaders
	def getColMaxLens(self):
		return self.colMaxLens
	def addRow(self, row):
		"""
		@param row	list of str:	Values for each column for the row.
		"""
		self.rows.append(row)
		self._updateColMaxLens(row)
	
	def _updateColMaxLens(self, newRow):
		if self.colMaxLens == None:
			return
		for i in range(0, len(self.colMaxLens)):
			if i < len(newRow):
				if self.autoResizeCols == True or self.autoResizeCols[i] == True:
					self.colMaxLens[i] = max((self.colMaxLens[i], len(newRow[i])))
	
	def _fmtRow(self, row):
		str_ = ""
		for colNum in range(0, len(row)):
			if self.colMaxLens[colNum] != None:
				colStr = row[colNum].ljust(self.colMaxLens[colNum])
			else:
				colStr = row[colNum].ljust(max([len(col) for col in [self.colheaders] + self.rows]))
			str_ += colStr + "  "
		return str_[:-2]
	def __str__(self):
		str_ = ""
		for row in self.rows:
			str_ += self._fmtRow(row)
		return str
	def printLive(self):
		"""Prints any rows not printed before, such as those that have been added since the last call to this function."""
		if self._lastPrintedRow == -1 and self.colHeaders != None:
			print(self._fmtRow(self.colHeaders))
		for rowNum in range(self._lastPrintedRow + 1, len(self.rows)):
			print(self._fmtRow(self.rows[rowNum]))
		self._lastPrintedRow = len(self.rows) - 1
