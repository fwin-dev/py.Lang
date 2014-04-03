# <a name="terminal"></a>Terminal

Utilities for improving terminal interaction with the user.

## Asking the user a question

	from Lang import Terminal
	if Terminal.askYesNo("Do you like Star Trek?") == True:
		print("Awesome!")
	else:
		print("Your nerd credit has been lowered")

## Using formatted text on the terminal

	from Lang.Terminal import FormattedText

`FormattedText` returns a subclass of the built-in python `str` type. It adds terminal formatting codes when
the `str` function is called on it:

	boldStr = str(FormattedText("I'm in bold", bold=True))

`boldStr` will contain some funny looking characters which enable formatting, but these characters do not influence
any other function of the string. For example:

	char = boldStr[2]

will store `m` into `char`. Similarly, `len` and other functions will act the same as if the string were a direct
instantiation of `str`.
 
Many more text attributes are available, including coloring - see the source for more information.

## Tables

Printing tabular data to the terminal is very common. This implementation of a table has a couple extras with it.
Here is an example:

	from Terminal import Table
	table = Table()
	table.setColHeaders(("First Name", "Last Name Initial", "Number"))	# optional
	table.setColMaxLens([None] * 3)			# enables automatic column sizing for the 3 columns
	table.addRow(["Jesse", "C", str(1234)])	# explicitly convert all elements to strings
	table.printLive()						# prints all rows (and headers) that haven't been printed before

If another row is added to the table, another call to `printLive()` will only print only that new row.

## An improved ArgParser

In addition to the plethora of features in [python's built-in argparse module](https://docs.python.org/2.7/library/argparse.html), a few more are added in here:

* Improved help formatting, similar to `man`
* Addition of 3 way booleans (`True`, `False`, `None`) and automatic handling of any other iterable type
* Required named parameters - the built-in ArgParser only supports required positional arguments and optional named parameters

The new `ArgParser` uses the same interface as the old one, so see the built-in `ArgParser` documentation.

Example:

	from Lang.ArgParser import ArgParser
    parser = ArgParser(argument_default=None, add_help=True, description="Adds a user to a linux machine")
    parser.add_argument("username")
	parser.add_argument("-p", "--password", required=False, help="Prompt for password if this is not given")
	parser.add_argument("-H", "--create-home", type=Bool3Way, required=True,
		help="Controls home directory creation for user. None uses the default behavior which varies between machines.")
	args = parser.parse_args()
