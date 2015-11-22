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
    print "result from boson=", result
    # entities is of format [(中方， org_name)]
    entities = []
    myresults = []
    # print "Type of result is: ", type(result), len(result)
    old_endIndex = 0
    for startIndex, endIndex, entityName in result[0]['entity']:
        entities.append((''.join(result[0]['word'][startIndex:endIndex]), entityName))

        if startIndex>old_endIndex:
            myresults.append((result[0]['word'][old_endIndex:startIndex],'unknown'))
        myresults.append(([''.join(result[0]['word'][startIndex:endIndex])],entityName))
        old_endIndex = endIndex

    if endIndex < len(result[0]['word']):
        myresults.append(([result[0]['word'][endIndex:]],'unknown'))

    return myresults, entities


if __name__ == '__main__':
    results, entities = parsed_text("中央情报局局长许诗旦予以强烈谴责。白宫表示同意。")
    print entities
    print results
