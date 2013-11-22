class ResourceIsFullException(Exception):
	pass

class ResourceAlreadyReleasedException(Exception):
	pass

import abstract
import decorators
import _Threading as Threading
import FileSystem
