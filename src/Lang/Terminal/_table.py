class Table(object):
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
		if self.getColHeaders() != None:
			self._updateColMaxLens(self.getColHeaders())
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
	
	def _computeColMaxLen(self, colNum):
		"""On the fly computation for maximum length of columns"""
# 		print([str(self.colHeaders[colNum])] + [str(row[colNum]) for row in self.rows])
		return max([len(str(self.colHeaders[colNum]))] + [len(str(row[colNum])) for row in self.rows])
	
	def _fmtRow(self, row):
		str_ = ""
		for colNum in range(0, len(row)):
			value = row[colNum]
			if not isinstance(value, str):		# don't always call str(), so it's compatible with FormattedText and any other custom string class
				value = str(value)
			if self.colMaxLens == None or self.colMaxLens[colNum] == None:
				maxLen = self._computeColMaxLen(colNum)
			else:
				maxLen = self.colMaxLens[colNum]
			str_ += value.ljust(maxLen) + "  "
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
