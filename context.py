#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : context.py
# Creation Date : 12-05-2012
# Last Modified : Sat 12 May 2012 01:30:59 AM EEST
# Created By : Greg Liras <gregliras@gmail.com>
#_._._._._._._._._._._._._._._._._._._._._.*/


class context(object):
    def __init__(self,name,parent=None):
        self.__name = name
        self.__parent = parent
        if parent:
            self.__entries = parent.getEntries()
        else:
            self.__entries = {}
    def add(self,entry):
        self.__entries[entry.name] = entry

    def lookup(self,st):
        try:
            return self.__entries[st]
        except:
            raise KeyError("ContextError"):

    def pop(self):
        return self.__parent

