#!/usr/bin/python
#-*- coding: utf-8 -*-

import os, sys
import numpy as np
import urllib, urllib2
import parse_text.parse_text

class NameQueue(object):
    """docstring for ClassName"""
    def __init__(self):
        super(NameQueue, self).__init__()
        self.queue = []

    def add_name_to_queue(self, name):
        self.queue.append(name)

    def pop_name_from_queue(self, name):
        self.queue.remove(name)

    def move_name_to_last(self, name):
        self.pop_name_from_queue(name)
        self.add_name_to_queue(name)


output_dict = {}


def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        original_text = f.read()
    # parse the text from the file:
    # should annotate names, crimes, time, amount, penalty
    parsed_text = parse_text(original_text)
    # below is the naive sequence correspondence as a baseline
    # name_queue = NameQueue()
    crimes =[]
    for ii in range(len(parsed_text)):
        current_word = parsed_text[ii]
        if current_word['tag']=='name':
            tmp_name = current_word['word']
            if tmp_name not in output_dict:
                output_dict[tmp_name] = {}
                output_dict[tmp_name]['crimes']=[]
                if len(crimes):
                    output_dict[tmp_name]['crimes'].extend(crimes)
                    crimes = []
                output_dict[tmp_name]['amount']=[]
                output_dict[tmp_name]['time']=[]
                output_dict[tmp_name]['penalty']=[]
        if current_word['tag']=='crime':
            if tmp_name:
                output_dict[tmp_name]['crimes'].append(current_word)
            else:
                crimes.append(current_word)






