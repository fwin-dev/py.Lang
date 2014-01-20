"""Provides a better implementation of ArgParse, using man-like help"""

import sys, os
import argparse

class Bool3Way:
	"""3 way boolean - can be `True`, `False`, or `None`"""
	choices = [None, True, False]
	
	def __init__(self):
		self.index = 0
	def __iter__(self):
		return self
	def next(self):
		if self.index >= len(self.choices):
			raise StopIteration
		else:
			value = self.choices[self.index]			
			self.index += 1
			return value

class _HelpFormatter(argparse.RawDescriptionHelpFormatter):
	"""Man-page-like formatter for getting help of a python script"""
	def __init__(self, prog, indent_increment=2, max_help_position=24):
		if sys.stdin.isatty():
			rows, cols = [int(i) for i in os.popen("stty size", "r").read().split()]  # returns rows, columns when connected to a tty
		else:   # when not connected to a tty
			cols = 160
		super(_HelpFormatter, self).__init__(prog=prog, indent_increment=indent_increment, max_help_position=max_help_position, width=cols)
	def _format_usage(self, usage, actions, groups, prefix):
		_str = argparse.HelpFormatter._format_usage(self, usage, actions, groups, "Usage:")
		_str = _str.replace("Usage:", "Usage:\n  ")
		return _str
	
	def add_argument(self, action):
		if action.help is argparse.SUPPRESS:
			return
		
		# find all invocations
		get_invocation = self._format_action_invocation
		invocations = [get_invocation(action)]
		for subaction in self._iter_indented_subactions(action):
			invocations.append(get_invocation(subaction))
		
		# update the maximum item length
		invocation_length = len(invocations[0])
		action_length = invocation_length + self._current_indent
		self._action_max_length = max(self._action_max_length, action_length)
		
		# add the item to the list
		self._add_item(self._format_action, [action])
	
	def _format_action_calcWidths(self, useSameLine):
		# determine the required width and the entry label
		if useSameLine:
			help_position = min(self._action_max_length + 2, self._max_help_position)
			action_width = help_position - self._current_indent - 2
		else:
			help_position = len("	  ".expandtabs())
			action_width = help_position - self._current_indent - 2
		help_width = self._width - help_position
		return help_position, help_width, action_width
	
	def _format_action(self, action):
		action_header = self._format_action_invocation(action)
		help_position, help_width, action_width = self._format_action_calcWidths(True)
		
		# no help; start on same line and add a final newline
		if not action.help:
			tup = self._current_indent, "", action_header
			action_header = "%*s%s\n" % tup
		
		# short action name; start on the same line and pad two spaces
#		elif len(action_header) <= action_width:
#			tup = self._current_indent, "", action_width, action_header
#			action_header = "%*s%-*s  " % tup
#			indent_first = 0
		
		# long action name; start on the next line
		else:
			help_position, help_width, action_width = self._format_action_calcWidths(False)
			tup = self._current_indent, "", action_header
			action_header = "%*s%s\n" % tup
			indent_first = help_position
		
		# collect the pieces of the action help
		parts = [action_header]
		
		# if there was help for the action, add lines of help text
		if action.help:
			help_text = self._expand_help(action)
			help_lines = self._split_lines(help_text, help_width)
			parts.append("%*s%s\n" % (indent_first, "", help_lines[0]))
			for line in help_lines[1:]:
				parts.append("%*s%s\n" % (help_position, "", line))
			parts.append("\n")
		
		# or add a newline if the description doesn't end with one
		elif not action_header.endswith("\n"):
			parts.append("\n")
		
		# if there are any sub-actions, add their help as well
		for subaction in self._iter_indented_subactions(action):
			parts.append(self._format_action(subaction))
		
		# return a single string
		return self._join_parts(parts)
	
	
	def _format_action_invocation(self, action):
		if not action.option_strings:
			metavar, = self._metavar_formatter(action, action.dest)(1)
			return metavar
		else:
			parts = []

			# if the Optional doesn't take a value, format is:
			#	-s, --long
			if action.nargs == 0:
				parts.extend(action.option_strings)

			# if the Optional takes a value, format is:
			#	-s, --long ARGS
			else:
				default = action.dest.upper()
				args_string = self._format_args(action, default)
				for option_string in action.option_strings:
					parts.append(option_string)
				parts.append(args_string)
			
			_str = parts[0] + " " + parts[1]
			if len(parts) == 3:
				_str = parts[0] + ", " + parts[1] + " " + parts[2]
			return _str


class ActionsContainer(argparse._ActionsContainer):
	def add_argument(self, *args, **kwargs):
		if "type" in kwargs and "choices" not in kwargs:
			if kwargs["type"] == bool:
				kwargs["choices"] = [True, False]
			try:
				kwargs["choices"] = [i for i in kwargs["type"]()]
			except TypeError:
				pass
		return super(ActionsContainer, self).add_argument(*args, **kwargs)


class ArgParser(ActionsContainer, argparse.ArgumentParser):
	"""Supports positional arguments, named required arguments, and named optional arguments, with help in man-page-like format."""
	def __init__(self, description=None, argument_default=None, add_help=True, prog=None, usage=None,
				 epilog=None, parents=[], conflict_handler="error", prefix_chars="-", fromfile_prefix_chars=None):
		ActionsContainer.__init__(self, description=description, prefix_chars=prefix_chars, argument_default=argument_default, conflict_handler=conflict_handler)
		argparse.ArgumentParser.__init__(self, description=description, epilog=epilog, prog=prog, usage=usage, argument_default=argument_default, parents=parents, prefix_chars=prefix_chars, conflict_handler=conflict_handler,
										 formatter_class=_HelpFormatter, add_help=False)
		
		self._action_groups = []
		self._positionals = self.add_argument_group("Required positional parameters")	# do not rename variable name
		self._named_requireds = self.add_argument_group("Required named parameters")
		self._named_optionals = self.add_argument_group("Optional named parameters")
		
		if add_help:
			default_prefix = "-" if "-" in prefix_chars else prefix_chars[0]
			self.add_argument(default_prefix+"h", default_prefix*2+"help", action="help", default=argparse.SUPPRESS, help="Show this help message and exit")
	
	def error(self, message):
		"""argparse never gives details about parameters when user doesn't enter parameter correctly"""
		sys.stderr.write("error: %s\n\n" % message)
		self.print_help()
		sys.exit(2)
	
	def _add_action(self, action):
		if action.option_strings:
			if action.required:
				self._named_requireds._add_action(action)
			else:
				self._named_optionals._add_action(action)
		else:
			self._positionals._add_action(action)
		return action
	

