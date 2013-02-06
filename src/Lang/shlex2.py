import re
import shlex

def split(_str, charSplitList=[], excludeComments=True):
    _list = shlex.split(_str, comments=excludeComments)
    expandedList = []
    for i in _list:
        expandedList += strSplitMultiDelim(i, charSplitList)
    return expandedList

def strSplitMultiDelim(_str, delimList):
    delimList = [re.escape(i) for i in delimList]
    result = re.split("(" + "|".join(delimList) + ")", _str)
    return filter(lambda x: x != "", result)
