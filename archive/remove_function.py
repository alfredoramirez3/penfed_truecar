#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 19:26:37 2020

@author: ar3
"""


def remove(text, chars):
    if chars: return remove(text.replace(chars[0], ""), chars[1:])
    return text

