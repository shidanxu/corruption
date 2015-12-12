#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import re
import nltk
import pycrfsuite

def mytrain():
    # mycrftagger = CRFTagger()
    train_sents = read_traindata("L_R_1990_3420.txt.train")

    
    # print mytrainingData


    # Turn training set to feature X
    X_train = [sent2features(train_sents)]
    print X_train, len(X_train)
    Y_train = [[getY(each) for each in train_sents]]
    print Y_train, len(Y_train)

    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, Y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,
        'c2': 1e-3,
        'max_iterations': 500
        })

    trainer.train('output.crfModel')

    tagger = pycrfsuite.Tagger()
    tagger.open('output.crfModel')

    X_test = X_train
    pred = tagger.tag(X_test[0])

    print type(pred), len(pred)
    print pred
    # for ii, item in enumerate(pred):
    #     print type(item), item, ii
    # print 'finish enumerate.\n'
    # print "Correct:", ' '.join([item for item in Y_train])




def word2features(word):
    features = ["regex_punish="+feature1(word), "regex_crime="+feature2(word)]
    return features

def sent2features(sent):
    return [word2features(word) for word in sent]

def feature1(word_tuple):
    txt, tag = word_tuple
    print "word is:", txt
    punish_regex_string = unicode('有期徒刑(\d+|[一二三四五六七八九十]+)年|缓刑(\d+|[一二三四五六七八九十]+)年', 'utf-8')
    punish_regex_string += unicode('|(\d+|[一二三四五六七八九十]+)年 有期徒刑','utf-8')
    punish_regex_string += unicode('|死刑|死缓|开除公职|依法逮捕|双规|没收个人财产|剥夺政治权利(终身|(\d+|[一二三四五六七八九十]+)年)+','utf-8')
    punish_regex_string += unicode('|免去|开除|撤销','utf-8')


    PUNISH_REGEX = re.compile(punish_regex_string, flags = re.UNICODE)

    if re.search(PUNISH_REGEX, txt):
        return "1"
    return "0"

def feature2(word_tuple):
    
    print "word is:", word_tuple
    txt, tag = word_tuple
    crime_regex_string = unicode('诈骗罪|贪污受贿|经济犯罪|挪用公款|盗窃|贿赂|贪污|行贿|销赃|受贿|假捐赠|倒卖|走私|索贿|报复陷害','utf-8')
    crime_regex_string += unicode('|失职|渎职|以权谋私|嫖娼','utf-8')


    CRIME_REGEX = re.compile(crime_regex_string, flags = re.UNICODE)

    if re.search(CRIME_REGEX, txt):
        return "1"
    return "0"

def getY(tuples):
    a, tag = tuples
    return tag

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