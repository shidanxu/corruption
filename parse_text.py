#!/usr/bin/python
#-*- coding: utf-8 -*-

import os, sys
import numpy as np
import urllib, urllib2
from bosonnlp import BosonNLP
from sets import Set


def bosonNer(text, sensitivity):
    nlp = BosonNLP('O8M_j1Nd.4200.wIlhsL46w9-C')
    return nlp.ner(text, sensitivity)

def parsed_text(original_text):
    result = bosonNer(original_text, 3)
    # entities is of format [(中方， org_name)]
    entities = []
    # print "Type of result is: ", type(result), len(result)
    for startIndex, endIndex, entityName in result[0]['entity']:
    	entities.append([''.join(result[0]['word'][startIndex:endIndex]), entityName])
    	result[0]['word'][startIndex:endIndex] = ((''.join(result[0]['word'][startIndex: endIndex]), entityName))


    
    return result[0]['word'], entities
if __name__ == '__main__':
	print(parsed_text("中央情报局予以强烈谴责。白宫表示同意。"))