# <a name="pypkgutil"></a>PyPkgUtil

Provides details about python packages and modules. Python can provide a lot of information about a package and a lot of
different ways of loading packages, but the functions and code to accomplish this is scattered and sometimes not obvious.
This `PkgUtil` module provides everything in one location.

	from PyPkgUtil import PkgUtil

## Is it built-in?

A built-in module is one who's source is not defined in a `.py` file.

	PkgUtil.isBuiltin(moduleObj)

## Is it included in a stock python distibution?

	PkgUtil.isStock(moduleObj)

## Is an object a module or a package?

	PkgUtil.isModule(obj)
	PkgUtil.isPackage(obj)

## Getting all modules and packages imported by a module

	PkgUtil.getImported_all(moduleObj, isRecursive)

Returns a flat list with all modules and packages.

## Getting all packages imported by a module

	PkgUtil.getImported_packages(moduleObj, isRecursive)

Returns a flat list.

## Full module path -> Relative module path

Convert the full file path of a module to a relative path, which can be used for importing:

	relPath = PkgUtil.convert_fullPathToRelative(fullPath)

## Object -> Full path

Get the full file path of a module or package object:

	fullPath = PkgUtil.convert_objectToFullPath(obj)

## Full path -> Object

Get the module or package object from a full path, aka import a module or package at the specified path:

	obj = PkgUtil.convert_fullPathToObject(fullPath)

## Name string -> Object

Import an object by its name:

	obj = PkgUtil.convert_nameToObject("moduleName")

## Object -> Name string

Get the name of a module or package:

	name = PkgUtil.convert_objectToName(obj)
