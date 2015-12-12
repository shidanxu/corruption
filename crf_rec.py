#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import re
import nltk
# import pycrfsuite

def mytrain():
    # mycrftagger = CRFTagger()
    mytrainingData = read_traindata("L_R_1990_3420.txt.train")
    print mytrainingData


def read_traindata(fname, path = "./corruption annotated data/"):
    output = []
    with codecs.open(path + fname, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            word, tag = line.split("\t")
            output.append((word, tag.strip()))
    return output


if __name__ == '__main__':
    mytrain()