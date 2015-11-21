#!/usr/bin/python
#-*- coding: utf-8 -*-

import os, sys
import numpy as np
import urllib, urllib2
from bosonnlp import BosonNLP


def bosonNer(text, sensitivity):
    nlp = BosonNLP('O8M_j1Nd.4200.wIlhsL46w9-C')
    return nlp.ner(text, sensitivity)

def parsed_text(original_text):
    result = bosonNer(original_text, 3)
    # entities is of format [(中方， org_name)]
    entities = []
    # print "Type of result is: ", type(result), len(result)
    for startIndex, endIndex, entityName in result[0]['entity']:
    	entities.append((''.join(result[0]['word'][startIndex:endIndex]), entityName))
    
    # result[0]['word'] = ['中方'， ‘予以’， ‘强烈’， ’谴责‘]
    # result[0]['entity'] = [[0, 1, org_name]], 
    # meaning first entry in result[0]['word'] is an org
    return entities, result[0]['word'], result[0]['entity']

if __name__ == '__main__': 
	print(parsed_text("中方予以强烈谴责。"))