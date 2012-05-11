#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : tree.py
# Creation Date : 26-04-2012
# Last Modified : Fri 11 May 2012 09:44:48 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/

def fixme(stuff):
    ls = []
    for i in stuff.keys():
        ls.append(' {0}="{1}"'.format(i,stuff[i]))
    return "".join(ls)


class node(object):
    def __init__(self,name,stuff,children):
        self._name = name
        self._attrs = stuff
        self._attrsShow = fixme(stuff)
        if children:
            self._children = children
        else:
            self._children = []
        self._type = stuff['type']
    def __repr__(self):
        kids = "".join(map(repr,self._children))
        kids = filter(lambda x: repr(x) != 'None',kids)
        self._attrs['type'] = self.type()
        self._attrsShow = fixme(self._attrs)
        return "<{0} {1}>\n{2}</{0}>\n".format(self._name,self._attrsShow,kids)
        #return "{0}: {1}\n\t{2}".format(self._name,self._attrsShow,self._children)
    def __iter__(self):
        return iter(self._children)
    def symbol(self):
        return self._attrs['symbol']
    def value(self):
        return self._name
    def type(self):
        return self._type





