import pkgutil as _pkgutil
from modulefinder import ModuleFinder
import os.path, sys, imp


# filters local file paths from system file paths (for python modules)
from distutils.sysconfig import get_python_lib
SYSTEM_FOLDERS = [os.path.split(get_python_lib())[0]]
CUSTOM_PATHS = [os.path.realpath(".")]
for testPath in sys.path:
	for realSysPath in SYSTEM_FOLDERS:
		if os.path.commonprefix([testPath, realSysPath]) != realSysPath:
			CUSTOM_PATHS.append(testPath)


class PkgUtil:
	"""Provides information about python packages."""
	@classmethod
	def isBuiltin(cls, moduleObj):
		"""
		@return bool:	`True` if the module object is builtin (when its source is not in a file)
		""" 
		return not hasattr(moduleObj, "__file__") or moduleObj.__file__ == None
	
	@classmethod
	def isStock(cls, moduleObj):
		"""Returns true when moduleObj comes as part of the stock python install or a readily available extra module"""
		for sysFolder in SYSTEM_FOLDERS:
			if os.path.commonprefix([moduleObj.__file__, sysFolder]) == sysFolder:
				return True
		return False
	
	@classmethod
	def isModule(cls, moduleObj):
		return not cls.isPackage(moduleObj)
	
	@classmethod
	def isPackage(cls, moduleObj):
		return hasattr(moduleObj, "__path__") and moduleObj.__path__ != None
	
	@classmethod
	def getImported_all(cls, moduleObj, isRecursive):
		"""
		@return list:	Modules and packages imported by moduleObj, in a flat list
		"""
		# first, must get all packages referenced by the imports
		
		#packageFolders = []
		#for pkg in cls.getImported_packages(moduleObj, isRecursive):
		#	packageFolders.append(os.path.split(os.path.realpath(pkg.__file__))[0]) 
		result = cls._getImported_all(moduleObj, isRecursive, [])
		return result
	
	@classmethod
	def _getImported_all(cls, moduleObj, isRecursive, allSubs=[]):
		if cls.isBuiltin(moduleObj) or cls.isStock(moduleObj):
			return
		if moduleObj.__name__ == "__main__":
			return
		for i in allSubs:
			if i.__name__ == moduleObj.__name__ and i.__file__ == moduleObj.__file__:
				return
#		print("adding " + str(moduleObj))
		allSubs.append(moduleObj)
		
		if isRecursive or allSubs == []:
			# add path relative to current module
			newPaths = [os.path.split(cls.convert_objectToFullPath(moduleObj))[0]] + sys.path
			finder = ModuleFinder(path=newPaths)
			finder.run_script(cls.convert_objectToFullPath(moduleObj))
			for subModuleName, subModuleObj in finder.modules.iteritems():
#				print("discovered " + str(subModuleObj))
				cls._getImported_all(subModuleObj, True, allSubs)
		
		return allSubs
	
	@classmethod
	def getImported_packages(cls, moduleObj, isRecursive):
		for sub in cls._getImported_all(moduleObj, isRecursive):
			if cls.isPackage(sub):
				yield sub
	
	@classmethod
	def convert_fullPathToRelative(cls, fullPath):
		"""
		@return str:	A path relative to the executed script
		"""
		allSysPaths = sys.path
		allSysPaths.append(os.path.dirname(sys.argv[0]))
		bestRelPath = None	 # lower is better
		
		for sysPathFolder in allSysPaths:
			if os.path.commonprefix([sysPathFolder, fullPath]) == sysPathFolder:
				currentRelPath = os.path.relpath(fullPath, sysPathFolder)
				if bestRelPath == None or currentRelPath.count("/") < bestRelPath.count("/"):
					bestRelPath = currentRelPath
		return bestRelPath
	
	@classmethod
	def convert_objectToFullPath(cls, moduleObj):
		"""
		@return Full path of the imported module
		"""
		if cls.isBuiltin(moduleObj):
			return None
		_str = moduleObj.__file__
		if _str.endswith(".pyc"):
			_str = _str[:-1]
		return _str
	
	@classmethod
	def convert_fullPathToObject(cls, fullPath):
		"""
		@return An imported object from the filesystem path
		"""
		filename = os.path.basename(fullPath).replace(".py","").replace(".pyc","")
		return imp.load_source(filename, fullPath)
	
	@classmethod
	def convert_nameToObject(cls, moduleName):
		"""
		@return A module object, given the name
		"""
		mod = __import__(moduleName)
		components = moduleName.split(".")
		for comp in components[1:]:
			mod = getattr(mod, comp)
		return mod
	
	@classmethod
	def convert_objectToName(cls, moduleObj):
		"""
		@return str:	The name of a module
		"""
		return moduleObj.__name__
