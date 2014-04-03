from Lang.Struct import OrderedSet

_vars_ = vars	# backup reference to built-in function

def vars(cls):
	"""Like the built-in function `vars`, but also works with slotted classes"""
	if not hasattr(cls, "__slots__"):
		return _vars_(cls)
	allVars = OrderedSet()
	for cls in cls.__mro__:
		for varName in getattr(cls, "__slots__", tuple()):
			allVars.add(varName)
	return allVars
