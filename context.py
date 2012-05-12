#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : context.py
# Creation Date : 12-05-2012
# Last Modified : Sat 12 May 2012 09:25:05 PM EEST
# Created By : Greg Liras <gregliras@gmail.com>
#_._._._._._._._._._._._._._._._._._._._._.*/


class GlobalLookupError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LocalLookupError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class context(object):
    def __init__(self,name,parent=None):
        self.__name = name
        self.__parent = parent
        self.__entries = {}

    def add(self,entry):
        try:
            sth = self.__entries[entry.name]
        except:
            self.__entries[entry.name] = entry

    def lookupGL(self,st):
        try:
            return self.__entries[st]
        except:
            try:
                return self.__parent.lookupGL(st)
            except:
                raise GlobalLookupError

    def lookupCR(self,st):
        try:
            return self.__entries[st]
        except:
            raise LocalLookupError

    def pop(self):
        return self.__parent

