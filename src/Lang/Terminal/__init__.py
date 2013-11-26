from __future__ import print_function

from _formatted_text import FormattedText
from _table import Table

def askYesNo(question):
	"""Print a question to the terminal for the user. Expects a yes or no response. Returns True if yes, False if no."""
	return raw_input(question + " [y/n]: ").lower() in ["y", "yes"]
