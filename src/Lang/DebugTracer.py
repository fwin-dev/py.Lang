import sys, inspect, os.path

_SETTINGS = {}

def _trace(frame, event, arg):
    depth = len(inspect.getouterframes(inspect.currentframe()))
    if depth < _SETTINGS["minFuncDepth"] or depth > _SETTINGS["maxFuncDepth"]:
        return
    file = os.path.basename(frame.f_code.co_filename)
    functionName = frame.f_code.co_name
    lineNum = frame.f_lineno
    parentFrameLineNum = frame.f_back.f_lineno
    
    if event == "call":
        if not _SETTINGS["showFunctions"]:
            return
        event = "line " + str(parentFrameLineNum) + " called " + functionName + "(...)"
    elif event == "line":
        if not _SETTINGS["showLines"]:
            return
        event = "executing line"
    elif event == "return":
        if not _SETTINGS["showReturns"]:
            return
        event = "returning"
    
    print("depth " + str(depth) + ": " + file + ", line " + str(lineNum) + ": " + event)
    return _trace

def setTraceOn(showFunctions=True, showLines=False, showReturns=False, minFuncDepth=0, maxFuncDepth=30, limitToFiles=[]):
    _SETTINGS["showFunctions"] = showFunctions
    _SETTINGS["showLines"] = showLines
    _SETTINGS["showReturns"] = showReturns
    _SETTINGS["minFuncDepth"] = minFuncDepth
    _SETTINGS["maxFuncDepth"] = maxFuncDepth
    _SETTINGS["limitToFiles"] = limitToFiles
    
    if len(filter(lambda x: x == True, _SETTINGS.values())) != 0:
        sys.settrace(_trace)
    else:
        sys.settrace(None)

def setTraceOff():
    setTraceOn(False, False)

