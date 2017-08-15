#!/usr/bin/python
# -*- coding: utf-8 -*-
import re,os

filter_keywords = ["&nbsp;", "&amp;", "\t", "\n", "\r", "&quot;", "&middot;"]

def replace():
    src = '  jj\t  1 '
    src = src.strip()
    print src
    src2 = re.sub('\s+', '', src)
    #src = re.sub(r'<[\S\s]*?>','',src)
    print src2
    print src


