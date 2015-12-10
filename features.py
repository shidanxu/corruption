#!/usr/bin/python
# -*- coding: utf-8 -*-

import dateparser
import re
import os

caughtKeywords = ['逮捕', '破获', '捉拿归案', '反映']
caughtKeywords = [unicode(item, 'utf-8') for item in caughtKeywords]
reportKeywords = ['举报', '揭露', '报案', '告发', '上访', '揭发', '状告', '申冤']
reportKeywords = [unicode(item, 'utf-8') for item in reportKeywords]

crime_regex_string = unicode('诈骗罪|贪污受贿|经济犯罪|挪用公款|盗窃|贿赂|贪污|行贿|销赃|受贿|假捐赠|倒卖|走私|索贿|报复陷害','utf-8')
crime_regex_string += unicode('|失职|渎职|以权谋私|嫖娼','utf-8')
CRIME_REGEX = re.compile(crime_regex_string, flags = re.UNICODE)


def isStartOfArticle(time_anchor, sentences_anchor):
    threshold = 0.1
    return time_anchor[0] < len(sentences_anchor) * threshold

# nearCaughtKeywords check whether time is within the same sentence of some keywords
# that indicate caught time
def nearCaughtKeywords(time_anchor, sentences_anchor, word_list):
    sentence = findCompleteSentence(time_anchor, sentences_anchor, word_list)
    sentence = [eachWord.strip() for eachWord in sentence]
    sentence = ''.join(sentence)
    for word in caughtKeywords:
        if word in sentence:
            return True
    return False

def nearReportKeywords(time_anchor, sentences_anchor, word_list):
    sentence = findCompleteSentence(time_anchor, sentences_anchor, word_list)
    sentence = [eachWord.strip() for eachWord in sentence]
    sentence = ''.join(sentence)
    for word in reportKeywords:
        if word in sentence:
            return True
    return False

def nearCrime(time_anchor, sentences_anchor, word_list):
    sentence = findCompleteSentence(time_anchor, sentences_anchor, word_list)
    sentence = [eachWord.strip() for eachWord in sentence]
    sentence = ''.join(sentence)
    if re.search(CRIME_REGEX, sentence):
        print "time near crime"
        return True
    return False

def timeSentenceByItself(time, time_anchor, sentences_anchor, word_list):
    sentence = findCompleteSentence(time_anchor, sentences_anchor, word_list)
    sentence = [eachWord.strip() for eachWord in sentence]
    sentence = ''.join(sentence)
    time = ''.join([item.strip() for item in time.split()])

    if time.strip() == sentence.strip():
        return True
    return False

def earliestTime(time, times):
    parsedTimes = []
    try:
        parsedTimes = [dateparser.parse(thisTime) for thisTime in times]
        parsedTimes = filter(None, parsedTimes)
    except Exception:
        return False
    # print "parsedTimes:=", parsedTimes

    try:
        myTime = dateparser.parse(time)
    except Exception:
        return False

    if parsedTimes == []:
        return False
    if myTime == None:
        return False

    return min(parsedTimes) == myTime

def latestTime(time, times):
    parsedTimes = []
    try:
        parsedTimes = [dateparser.parse(thisTime) for thisTime in times]
        parsedTimes = filter(None, parsedTimes)
    except Exception:
        return False
    # print "parsedTimes:=", parsedTimes

    try:
        myTime = dateparser.parse(time)
    except Exception:
        return False

    if parsedTimes == []:
        return False
    if myTime == None:
        return False

    return max(parsedTimes) == myTime

# returns the anchors of complete sentence in word list
def findCompleteSentence(time_anchor, sentences_anchor, word_list):
    completeSentence = []
    for ii, sent_anchor in enumerate(sentences_anchor):
        if time_anchor[1] <= sent_anchor[1]:
            head = ii
            completeSentence = [sent_anchor[0], sent_anchor[1]]
            jj = ii
            # while not word_list[completeSentence[-1]].endswith(("。", "？")):
            if ii != len(sentences_anchor):
                # print "len(word_list):", len(word_list)
                # print "sentence:", ''.join(word_list[sent_anchor[0] : sent_anchor[1]])
                
                while not word_list[completeSentence[1]-1].endswith((unicode("。", 'utf-8'), unicode("？", 'utf-8'))):
                    # print "completeSentence[1]: ", completeSentence[1]
                    # print "wrod list:", word_list[68]
                    jj+=1
                    sent_anchor = sentences_anchor[jj]
                    completeSentence[-1] = sent_anchor[1]
            if ii != 0:
                jj = ii
                # while not word_list[completeSentence[0]-1].endswith(("。", "？")):
                while not word_list[completeSentence[0]-1].endswith((unicode('。', 'utf-8'), unicode('？', 'utf-8'))):
                    jj -=1
                    sent_anchor = sentences_anchor[jj]
                    completeSentence[0] = sent_anchor[0]
            break
    return word_list[completeSentence[0] : completeSentence[1]]

def isStartOfTimePeriod(time1_anchor, time2_anchor, sentences_anchor, word_list):
    sentence1 = findCompleteSentence(time1_anchor, sentences_anchor, word_list)
    sentence2 = findCompleteSentence(time2_anchor, sentences_anchor, word_list)
    if sentence1 == sentence2:
        return (time1_anchor[1] - time2_anchor[0]) <= 2
    return False
