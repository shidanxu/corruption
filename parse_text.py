#!/usr/bin/python
#-*- coding: utf-8 -*-

import os, sys
import numpy as np
import urllib, urllib2
from bosonnlp import BosonNLP
from sets import Set


token1 = "O8M_j1Nd.4200.wIlhsL46w9-C"
def bosonNer(text, sensitivity):
    nlp = BosonNLP('qJWJc-f3.4334.MamzfHZ-9wUL')
    return nlp.ner(text, sensitivity)

def recognize_names(original_text):
    result = bosonNer(original_text, 2)
    # print "result from boson:"
    string = ' '.join(result[0]['word'])
    # print "segmentation:", string
    entities = '; '.join(map(' '.join, map(str,result[0]['entity'])))
    # print "entities:", entities
    # entities is of format [(中方， org_name)]

    # entities = []
    # myresults = []
    # # print "Type of result is: ", type(result), len(result)
    # old_endIndex = 0
    # for startIndex, endIndex, entityName in result[0]['entity']:
    #     entities.append((''.join(result[0]['word'][startIndex:endIndex]), entityName))

    #     if startIndex>old_endIndex:
    #         myresults.append((result[0]['word'][old_endIndex:startIndex],'unknown'))
    #     myresults.append(([''.join(result[0]['word'][startIndex:endIndex])],entityName))
    #     old_endIndex = endIndex

    # if endIndex < len(result[0]['word']):
    #     myresults.append(([result[0]['word'][endIndex:]],'unknown'))

    # return myresults, entities
    return result[0]


if __name__ == '__main__':
    results = recognize_names("中央情报局局长许诗旦予以强烈谴责。 白宫表示同意。北京")

    print 'words: '
    words = results['word']
    sentence = ''
    for word in words:
        # print word
        sentence += word
    entities = results['entity']
    for entity in entities:
        tmp = entity[:2]
        ent = words[tmp[0]]
        for ii in range(tmp[0]+1,tmp[1]):
            ent += words[ii]
        print ent
        print 'len of entity word = ', len(ent)
    print 'find position=', sentence.find(unicode("长谴",'utf-8'))


