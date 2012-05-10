#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : tree.py
# Creation Date : 26-04-2012
# Last Modified : Thu 10 May 2012 07:32:48 PM EEST
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
    def __repr__(self):
        kids = "".join(map(repr,self._children))
        kids = filter(lambda x: repr(x) != 'None',kids)
        return "<{0} {1}>\n{2}</{0}>\n".format(self._name,self._attrsShow,kids)
    def __iter__(self):
        return iter(self._children)
    def sumbol(self):
        return self._attrs['symbol']




