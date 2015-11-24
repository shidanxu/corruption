#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sets import Set
import re
from parse_text import recognize_names
from tags import TAGS, EVAL_TAGS
import json

# label the sentence with 1 of the following 3
# 1. crime
# 2. punishment
# 3. amount
# 4. unknown
punish_regex_string = unicode('有期徒刑 (\d+|[一二三四五六七八九十]+)年|缓刑 (\d+|[一二三四五六七八九十]+)年', 'utf-8')
punish_regex_string += unicode('|(\d+|[一二三四五六七八九十]+)年 有期徒刑','utf-8')
punish_regex_string += unicode('|死刑|死缓|开除公职|依法逮捕|双规|没收个人财产|剥夺政治权利(终身|(\d+|[一二三四五六七八九十]+)年)+','utf-8')
punish_regex_string += unicode('|免去|开除|撤销','utf-8')

crime_regex_string = unicode('诈骗罪|经济犯罪|挪用公款|盗窃|贿赂|贪污|行贿|销赃|贪污受贿|假捐赠|倒卖|走私|索贿|报复陷害','utf-8')
crime_regex_string += unicode('|失职|渎职|以权谋私|嫖娼','utf-8')

amount_regex_string = unicode('(\d+|[一二三四五六七八九十]+)[ ]?[多|余]?[万|千|个|十|百|亿]+[余]?[美|日|欧|港]?元','utf-8')
amount_regex_string += unicode('|共计折合|茅台酒','utf-8')
amount_regex_string += unicode('|数[万千个十百亿]+[美日欧港]?元','utf-8')

PUNISH_REGEX = re.compile(punish_regex_string, flags = re.UNICODE)
CRIME_REGEX = re.compile(crime_regex_string, flags = re.UNICODE)
AMOUNT_REGEX = re.compile(amount_regex_string, flags = re.UNICODE)

def labelSentence(sentence):
    try:
        sentence = unicode(sentence, 'utf-8')
    except Exception, e:
        pass
    crimeScore = 0
    punishmentScore = 0
    amountScore = 0
    unknownScore = 0.99
    # words = sentence.split(" ")
    # for word in words:

    if re.search(CRIME_REGEX, sentence):
        found = re.search(CRIME_REGEX, sentence)
        # print found.group()
        crimeScore += len(found.group())
    if re.search(PUNISH_REGEX, sentence):
        found = re.search(PUNISH_REGEX, sentence)
        # print found.group()
        punishmentScore += len(found.group())
    if re.search(AMOUNT_REGEX, sentence):
        found = re.search(AMOUNT_REGEX, sentence)
        # print found.group()
        amountScore += len(found.group())
    d = {'Crime': crimeScore, 'Punish': punishmentScore, 'Money_Person': amountScore, 'unknown': unknownScore}
    return max(d, key=d.get)


def sentence_index(paragraph):
    sentences = re.split(unicode('。 | ；| ，| ：| 、', 'utf-8'), paragraph, flags=re.UNICODE)

    word_list = re.split('\s+', paragraph, flags=re.UNICODE)
    sentence_anchor = []
    start = 0
    stop = 0
    for sentence in sentences:
        split_sentence = re.split('\s+', sentence, flags=re.UNICODE)
        stop += len(split_sentence)
        stop += 1
        anchor = [start, stop]
        sentence_anchor.append(anchor)
        start = stop
    return word_list, sentences, sentence_anchor

def annotate_paragraph(paragraph):
    print "\n\nin annotate_paragraph\n"
    word_list, sentences, sentence_anchor = sentence_index(paragraph)
    annotation_dict = {}
    annotation_dict['person_name']=[]
    annotation_dict['org_name']=[]
    annotation_dict['company_name']=[]
    annotation_dict['location']=[]
    annotation_dict['time']=[]
    for tag in EVAL_TAGS:
        annotation_dict[tag]=[]


    for ii, sentence in enumerate(sentences):
        # print 'sentence=', sentence
        # print 'encoded:', [sentence]
        anchor = sentence_anchor[ii]
        tag = labelSentence(sentence)
        if tag=="unknown":
            # print "tag=unknown"
            continue
        else:
            pass
            # print "tag=", tag
        # print "\n\ntag = ", tag
        # print "anchor = ", anchor
        # print "type of anchor=", type(anchor)

        annotation_dict[tag].append(anchor)

    name_entities = recognize_names(paragraph)
    for entity in name_entities:
        tag = entity[2]
        anchor = entity[:2]
        # print "tag = ", tag
        # print "anchor = ", anchor
        # print "type of anchor=", type(anchor)
        if tag=="person_name":
            print "\n\nfound person_name. anchor=", anchor
        annotation_dict[tag].append(anchor)

    return annotation_dict, word_list


def test_baselineRecognizer1(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(path + filename, 'r') as f:
                paragraphs = f.readlines()

                for paragraph in paragraphs:
                    lines = re.split('。 | ； | ， | ： | 、', paragraph, flags=re.UNICODE)

                    for line in lines:
                        if line.strip():
                            if labelSentence(line) != 'unknown':
                                print line, labelSentence(line)

def calculate_dist(anchor, list_anchors):
    scores = [0]*len(list_anchors)
    mean_pos0 = sum(anchor)/2.0
    for ii, person_anchor in enumerate(list_anchors):
        mean_pos = sum(person_anchor)/2.0
        score = (mean_pos-mean_pos0)*(mean_pos-mean_pos0)
        scores[ii] = score
    mean_score = min(scores)
    return scores.index(mean_score)

def test_baselineRecognizer(path, filename):
    outputDict = {}
    persons = []
    with open(path + filename, 'r') as f:
        paragraph = f.read()
        paragraph = unicode(paragraph, 'utf-8')
        print paragraph
        # for paragraph in paragraphs:
        annotation_dict, word_list = annotate_paragraph(paragraph)
        persons_ind = [0]*len(annotation_dict['person_name'])
        print "\n\nannotation_dict=", annotation_dict
        # print "\n\nwords:\n", word_list
        ind = 0
        for ii, anchor in enumerate(annotation_dict['person_name']):
            print 'anchor=', anchor
            name = word_list[anchor[0]:anchor[1]]
            name = ''.join(name)
            if name not in persons:
                persons.append(name)
                print 'new name=', name
                outputDict[name]={}
                persons_ind[ii] = ind
                ind += 1
            else:
                persons_ind[ii] = persons.index(name)
        print "annotation_dict", annotation_dict.keys()
        for tag in EVAL_TAGS:
            anchors = annotation_dict[tag]
            print "tag=", tag
            print "anchors=", anchors
            for anchor in anchors:
                # print "anchor=", anchor
                # print "type of anchor[1]=", type(anchor[1])
                # print [unicode(x, 'utf-8') for x in word_list[anchor[0]:anchor[1]]]
                newlist = []
                for x in word_list[anchor[0]:anchor[1]]:
                    try:
                        x = unicode(x,'utf-8')
                    except Exception, e:
                        pass
                    newlist.append(x)
                    # print x
                newlist = ''.join(newlist)
                ind = calculate_dist(anchor, annotation_dict['person_name'])
                name = persons[persons_ind[ind]]
                print "\n\ncurrent outputDict[name]=", outputDict[name]
                if tag not in outputDict[name]:
                    print '\n\ntag=', tag
                    outputDict[name][tag]=[]
                    print "outputDict[name] = ", outputDict[name]
                outputDict[name][tag].append((anchor,newlist))
                # print newlist
                # print word_list[anchor[0]:anchor[1]]
    return outputDict

def output(outputDict, filename):
    total_str = ''
    with open(filename, 'w') as f:
        ind = 1
        for person in outputDict:
            numbered_person = str(ind)+"Person"
            print numbered_person
            tmpstr = numbered_person+"\t"+person+"\n"
            total_str += tmpstr
            for tag in EVAL_TAGS:
                numbered_tag = str(ind)+tag
                print "\n\n\ntag = ", tag
                print 'outputDict[person] = ', outputDict[person]
                if tag in outputDict[person]:
                    for item in outputDict[person][tag]:
                        tmpstr = numbered_tag+"\t"+item[1]+"\n"
                        total_str += tmpstr
            ind += 1
        # f.write(total_str.decode(encoding='utf-8'))
        print "\n\n"
        print total_str
        data = {'content': total_str}
        json.dump(data, f)

if __name__ == '__main__':
    filename = "L_R_1994_4643.txt"
    path = "./corruption annotated data/"

    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            outputfilename = filename[:-4] + ".ann.machine"

            outputDict = test_baselineRecognizer(path, filename)
            print "\n\n\n\noutputDict:"
            print outputDict
            print "\n\n\n"
            output(outputDict, path+outputfilename)


    # with open(path + filename, 'r') as f:
    #     paragraph = f.read()
    #     sentences = re.split('[。 | ； | ， | ： | 、]+', paragraph, flags=re.UNICODE)
    #     for sentence in sentences:
    #         word_list = re.split('\s+', sentence, flags=re.UNICODE)
    #         print "\nwords in sentence:"
    #         for word in word_list:
    #             try:
    #                 word = unicode(word, 'utf-8')
    #             except Exception, e:
    #                 pass
    #             print word





