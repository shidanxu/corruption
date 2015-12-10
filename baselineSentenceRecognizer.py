#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sets import Set
import re
from parse_text import recognize_names
from tags import TAGS, EVAL_TAGS
import json
import copy
import nltk
from sklearn import linear_model
import features


# label the sentence with 1 of the following 3
# 1. crime
# 2. punishment
# 3. amount
# 4. unknown
punish_regex_string = unicode('有期徒刑(\d+|[一二三四五六七八九十]+)年|缓刑(\d+|[一二三四五六七八九十]+)年', 'utf-8')
punish_regex_string += unicode('|(\d+|[一二三四五六七八九十]+)年 有期徒刑','utf-8')
punish_regex_string += unicode('|死刑|死缓|开除公职|依法逮捕|双规|没收个人财产|剥夺政治权利(终身|(\d+|[一二三四五六七八九十]+)年)+','utf-8')
punish_regex_string += unicode('|免去|开除|撤销','utf-8')

crime_regex_string = unicode('诈骗罪|贪污受贿|经济犯罪|挪用公款|盗窃|贿赂|贪污|行贿|销赃|受贿|假捐赠|倒卖|走私|索贿|报复陷害','utf-8')
crime_regex_string += unicode('|失职|渎职|以权谋私|嫖娼','utf-8')

amount_regex_string = unicode('(英镑|美金|港币|人民币|日元|欧元)?[ ]?((\d+|[一二三四五六七八九十]+)[\.]?(\d+|[一二三四五六七八九十]+)?[ ]?[多余]?[ ]?[万千个十百亿]*[多余]?[ ]?[美|日|欧|港]?元)','utf-8')
amount_regex_string += unicode('|(英镑|美金|港币|[美日欧]!元)[数]?[万千个十百亿]+[元]?','utf-8')
amount_regex_string += unicode('|(英镑|美金|港币|[美日欧]!元)((\d+|[一二三四五六七八九十]+)[万千个十百亿]+)+[元]?','utf-8')


amount_regex_string += unicode('|共计折合|茅台酒','utf-8')
amount_regex_string += unicode('|数[万千个十百亿]+[美日欧港]?元','utf-8')

# time_regex_string = unicode('(\d+[ ]?年[ ]?\d+[ ]?月[ ]?\d+[ ]?日)+([ ]?[下午|上午|傍晚|凌晨][ ]?(\d+[ ]?时)?([ ]?[\d+]分)?([ ]?[\d+]秒)?[左右]?)?', 'utf-8')
time_regex_string = unicode('((\d{4}|[一二三四五六七八九十]{4})[ ]?年[ ]?)', 'utf-8')


good_position_regex_string = unicode('记者|副检察长|纪委副书记|法院副院长|法官|检察长|纪委书记|法院院长|通讯员','utf-8')
neutral_position_regex_string = unicode('', 'utf-8')
bad_position_regex_string = unicode('特派员|办事员|收款员|会计|出纳|', 'utf-8')

bad_position_regex_string += unicode('([副]?(局长|书记|党支部书记|市委书记|市长|县委书记|县长','utf-8')
bad_position_regex_string += unicode('|股长|地委书记|厅长|省长|省委书记|区长|区委书记','utf-8')
bad_position_regex_string += unicode('|秘书长|秘书|部长|常委|预算员|社长|科长|部长|经理|总经理|董事长|主任|处长|厂长))','utf-8')


# position regex includes good and bad

position_regex_string = good_position_regex_string + "|" +  bad_position_regex_string

PUNISH_REGEX = re.compile(punish_regex_string, flags = re.UNICODE)
CRIME_REGEX = re.compile(crime_regex_string, flags = re.UNICODE)
AMOUNT_REGEX = re.compile(amount_regex_string, flags = re.UNICODE)
TIME_REGEX = re.compile(time_regex_string, flags = re.UNICODE)
POSITION_REGEX = re.compile(position_regex_string, flags = re.UNICODE)

GOOD_REGEX = re.compile(good_position_regex_string, flags=re.UNICODE)

def labelSentence(sentence):
    try:
        sentence = ' '.join(sentence)
    except Exception, e:
        pass
    crimeScore = 0
    punishmentScore = 0
    amountScore = 0
    timeScore = 0
    positionScore = 0
    unknownScore = 0.99
    # words = sentence.split(" ")
    # for word in words:

    # print "sentence=", sentence

    word_tag_monotone = []

    if re.search(CRIME_REGEX, sentence):
        found = re.search(CRIME_REGEX, sentence)
        allfound = re.finditer(CRIME_REGEX, sentence)
        for found in allfound:
            # print "Crime found: ", found.group()
            crimeScore += len(found.group())
            word_tag_monotone.append((found.group(), found.span(), "Crime"))

    if re.search(PUNISH_REGEX, sentence):
        found = re.search(PUNISH_REGEX, sentence)
        allfound = re.finditer(PUNISH_REGEX, sentence)

        for found in allfound:
            # print "Punish found: ", found.group()
            punishmentScore += len(found.group())
            word_tag_monotone.append((found.group(), found.span(), "Punish"))

    if re.search(AMOUNT_REGEX, sentence):
        found = re.search(AMOUNT_REGEX, sentence)
        allfound = re.finditer(AMOUNT_REGEX, sentence)

        for found in allfound:
            # print "Amount found: ", found.group()
            amountScore += len(found.group())
            word_tag_monotone.append((found.group(), found.span(), "Money_Person"))

    if re.search(TIME_REGEX, sentence):
        found = re.search(TIME_REGEX, sentence)
        allfound = re.finditer(TIME_REGEX, sentence)

        for found in allfound:
            print "Time found: ", found.group()
            timeScore += len(found.group())
            word_tag_monotone.append((found.group(), found.span(), "Time"))

    if re.search(POSITION_REGEX, sentence):
        found = re.search(POSITION_REGEX, sentence)
        allfound = re.finditer(POSITION_REGEX, sentence)

        for found in allfound:
            # print "Position found: ", found.group()
            positionScore += len(found.group())
            word_tag_monotone.append((found.group(), found.span(), "Position"))


    tagScoreDict = {'Crime': crimeScore, 'Punish': punishmentScore, 'Money_Person': amountScore, 'Time': timeScore, 'Position': positionScore, 'unknown': unknownScore}

    # if max(tagScoreDict, key = tagScoreDict.get) != 'unknown':
    #     print sentence, max(tagScoreDict, key = tagScoreDict.get)

    word_tag_monotone = sorted(word_tag_monotone, key = lambda x: x[1][0])

    # print word_tag_monotone

    output_monotone = [[item[0], item[2]] for item in word_tag_monotone]
    # print output_monotone
    for item in word_tag_monotone:
        # print ''.join(item[0]) + "; " + str(item[1][0]) + ", " + str(item[1][1]) + " " + " ".join(item[2]) + "\n"
        pass
    # print crimes, punishes, amounts
    # return max(tagScoreDict, key=tagScoreDict.get)
    return tagScoreDict, output_monotone

def labelTime(sentence):
    try:
        sentence = ' '.join(sentence)
    except Exception, e:
        pass

    timeScore = 0
    unknownScore = 0.99

    # print "sentence=", sentence

    word_tag_monotone = []


    if re.search(TIME_REGEX, sentence):
        found = re.search(TIME_REGEX, sentence)
        allfound = re.finditer(TIME_REGEX, sentence)

        for found in allfound:
            print "Time found: ", found.group()
            timeScore += len(found.group())
            word_tag_monotone.append((found.group(), found.span(), "Time"))


    tagScoreDict = {'Time': timeScore, 'unknown': unknownScore}

    # if max(tagScoreDict, key = tagScoreDict.get) != 'unknown':
    #     print sentence, max(tagScoreDict, key = tagScoreDict.get)

    word_tag_monotone = sorted(word_tag_monotone, key = lambda x: x[1][0])

    # print word_tag_monotone

    output_monotone = [[item[0], item[2]] for item in word_tag_monotone]
    # print output_monotone
    for item in word_tag_monotone:
        # print ''.join(item[0]) + "; " + str(item[1][0]) + ", " + str(item[1][1]) + " " + " ".join(item[2]) + "\n"
        pass
    # print crimes, punishes, amounts
    # return max(tagScoreDict, key=tagScoreDict.get)
    return tagScoreDict, output_monotone

BIAODIAN = (unicode('。', 'utf-8'), unicode('；', 'utf-8'),unicode('，', 'utf-8'),unicode('：', 'utf-8'),unicode('？', 'utf-8'),)

def sentence_index(paragraph):
    sentences = re.split(unicode('(。|；|，|：|？|\n)', 'utf-8'), paragraph, flags=re.UNICODE)
    # print "\n\n\nFIRST SENTENCE: ", sentences[0]
    new_sentences = []
    current_sentence = []
    for x in sentences:
        # print "WOrking on X=", x.strip()
        if not x.strip():
            continue
        if x in BIAODIAN:
            current_sentence.append(x)
            new_sentences.append(current_sentence)
            current_sentence = []
            # print "NEW SENTENCE NOW: ", '\n'.join(' '.join(sentence) for sentence in new_sentences)

        else:
            if current_sentence:
                # print "current_sentence:", current_sentence
                current_sentence.extend(unicode('。', 'utf-8'))
                # print "\n\nCurrent Sentence ends without a period: ", " ".join(current_sentence)
                new_sentences.append(current_sentence)
                current_sentence = filter(None, re.split(unicode('\s+'), x))
                continue
            x = re.split(unicode('\s+'), x)
            x = filter(None, x)
            current_sentence = x
            # print "Current Sentence: ", " ".join(current_sentence)

    if current_sentence:
        new_sentences.append(current_sentence)
    # print 'new sentence: ', new_sentences
    print 'new_sentences = ', '\n'.join(' '.join(sentence) for sentence in new_sentences)

    word_list = []
    start = 0
    stop = 0
    sentence_anchor = []
    # new_sentences = []
    for sentence in new_sentences:
        # sentenceToWords = re.split('\s+', sentence, flags = re.UNICODE)
        # sentenceToWords = filter(None, sentenceToWords)
        if sentence:
            stop += len(sentence)
            # print "sentence: ", sentence
            sentence_anchor.append([start, stop])
            word_list.extend(sentence)
            # new_sentences.append(sentenceToWords)
            assert(word_list[sentence_anchor[-1][0]:sentence_anchor[-1][1]]==sentence)
            start += len(sentence)
    # word_list = re.split('\s+', paragraph, flags=re.UNICODE)
    # print "word list="
    # print word_list[24:25]
    # print "\n".join(word_list)

    # print "\n\n\n\nAligning checkup: word_list, new_sentences, sentence_anchor"
    for ii, s1 in enumerate(new_sentences):
        # print "word_list: ", word_list[sentence_anchor[ii][0] : sentence_anchor[ii][1]]
        # print "Sentence: ", s1
        pass
    return word_list, new_sentences, sentence_anchor

def findAllFiles(directory = "./corruption annotated data/"):
    filesInFolder = os.listdir(directory)
    files = []
    for filename in filesInFolder:
        if filename.endswith(".ann"):
            if filename[:-4]+".txt" in filesInFolder:
                # This file has both .txt and .ann
                files.append((filename[:-4]+".txt", filename))
    print files
    return files

# Returns the found tag in annotation file
def tagTime(year, time_anchor, annotation_file, fields = ['Year_Disc', 'Year_Crime']):
    # First process the annotaiton file
    annotated_times = []
    with open(annotation_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip():
                tagType, value = "", ""

                try:
                    tag, tagType, value = line.split("\t")
                    tagType = tagType.split(" ")[0]
                    tagIndex, tagType = int(tagType[:1]), tagType[1:]
                    print "tagIndex: ", tagIndex
                    if tagType in fields:
                        annotated_times.append((tagIndex, tagType, value))
                except Exception, e:
                    print e
                    # tagType, value = line.split("\t")
                    # tagType = tagType.split(" ")[0]
                    # tagIndex, tagType = int(tagType[:1]), tagType[1:]

    print annotated_times

    # Only keep current year
    output = []
    for (tagIndex, tagType, value) in annotation_times:
    	if value == year:
    		output.append((tagIndex, tagType, value, abs(tagIndex[0] - time_anchor[0])))
    
    if output == []:
        print "Found tag: None ", year
        return "None"
    else:
        tagReturn = min(output, key=lambda x: x[-1])[2]
        print "Found tag: ", tagReturn
        return tagReturn

def annotate_paragraph(paragraph):
    print "\n\nin annotate_paragraph\n"
    word_list, sentences, sentence_anchor = sentence_index(paragraph)
    annotation_dict = {}
    # annotation_dict['person_name']=[]
    # annotation_dict['org_name']=[]
    # annotation_dict['company_name']=[]
    # annotation_dict['location']=[]
    # annotation_dict['time']=[]
    # annotation_dict['product_name']=[]
    for tag in EVAL_TAGS:
        annotation_dict[tag]=[]
    for tag in TAGS:
        annotation_dict[tag]=[]

    for ii, sentence in enumerate(sentences):
        # print ii, len(sentences)
        # print 'sentence=', sentence
        # print 'encoded:', [sentence]
        anchor = sentence_anchor[ii]

        # tag = labelSentence(sentence)
        tagScoreDict, tagged_items = labelSentence(sentence)
        # print "tagged_items:", tagged_items
        # print "sentence:", sentence
        if max(tagScoreDict, key = tagScoreDict.get) == 'unknown':
            continue
        else:
            # print "IM HERE!!!"
            old_pos = anchor[0]
            for item in tagged_items:
                # print "DEALING WITH ITEM: ", item
                entity_word = item[0]
                tag = item[1]

                # print "ENTITY WORD: ", entity_word, "TAG: ", tag
                tag_anchor = align_words_debug(word_list, sentence_anchor, old_pos, entity_word)

                # print "TAG_ANCHOR: ", tag_anchor
                if tag_anchor[1]!=-1:
                    annotation_dict[tag].append(tag_anchor)
                    old_pos = tag_anchor[1]
            # print "I FINISHED!!"

    ner_results = recognize_names(paragraph)
    name_entities = ner_results['entity']
    ner_words = ner_results['word']
    displace = 0
    # old_pos=-1
    old_pos = 0
    for entity in name_entities:
        tag = entity[2]
        anchor = entity[:2]
        # print "\n\ntag = ", tag
        # print "anchor = ", anchor
        # print "type of anchor=", type(anchor)
        anchor = align_words_debug(word_list, sentence_anchor, old_pos, ner_words, anchor)
        # anchor = align_words(ner_words, anchor, word_list, old_pos)
        if tag=="person_name":
            # print "found person_name %s. anchor=%d-%d\n\n" % (''.join(word_list[anchor[0]:anchor[1]]), anchor[0], anchor[1])
            pass
        if anchor[1]!=-1:
            annotation_dict[tag].append(anchor)
            old_pos = anchor[1]

    return annotation_dict, word_list, sentences, sentence_anchor

def align_words(ner_words, anchor, word_list, old_pos):
    start = anchor[0]
    stop = anchor[1]
    search_range = 5
    entity_word = ner_words[start]
    for ii in range(start+1,stop):
        entity_word += ner_words[ii]
    # print '\nentity_word=',entity_word

    start = old_pos
    stop = start
    flag = 1
    string = ''
    # print 'start=', start,'; word=', word_list[start]
    while flag:
        word = word_list[start]
        if word in entity_word:
            # print 'found a starting word %s.' % word
            stop = start + 1
            string = word
            if entity_word in string:
                flag = 0
            while flag:
                if stop>len(word_list)-1:
                    flag = -1
                    break
                string += word_list[stop]
                print 'now using word %s.' % string
                stop += 1
                if entity_word in string:
                    flag = 0
        elif entity_word in word:
            print 'found a word %s containing the entity.' % word

            flag = 0
            string = word
            stop = start+1
        else:
            print 'this word is not matched: ', word

        if flag==0:
            break
        start += 1
        if start>len(word_list)-1:
            flag = -1
            break
    if flag==0:
        print 'entity %s recovered as %s. at %d-%d' % (entity_word, string, start, stop)
        return [start, stop]
    else:
        print 'entity %s not recovered!' % entity_word
        # exit(0)
        return -1, -1
# '''

def align_words_debug(word_list, sentence_anchor, old_pos, ner_words, anchor=None):
    if anchor:
        start = anchor[0]
        stop = anchor[1]
        search_range = 5
        entity_word = ner_words[start]
        for ii in range(start+1,stop):
            entity_word += ner_words[ii]
    else:
        entity_word = re.sub('\s+','', ner_words)
    # print '\nentity_word=',entity_word
    # ind = -1
    start = -1
    stop = -1
    match_flag = 0

    # if old_pos>896:
    #     exit(0)
    for ii in sentence_anchor:
        if match_flag:
            break
        if ii[1]<=old_pos:
            continue
        small = ii[0]
        # print 'temp sentence_anchor:', ii
        # print 'found the corresponding sentence, anchor=',ii
        if ii[0]<old_pos:
            small = old_pos
            # print "starting from word %s at %d:\n" % (word_list[old_pos], old_pos)
            current_sentence = word_list[old_pos:ii[1]]
        else:
            current_sentence = word_list[ii[0]:ii[1]]

        current_sentence_str = ''.join(current_sentence)
        # print 'current_sentence: ', current_sentence_str
        if entity_word in current_sentence_str:
            # do something;

            # print "Entity word contained in current_sentence_str!!!!"
            ind = 0
            index = [ind]
            pos = ind
            char_ind = current_sentence_str.index(entity_word)
            for jj in range(small+1,ii[1]):
                # print 'looping over the remaining part of the sentence. jj=', jj
                # current_sentence += word_list[jj]
                pos+=len(word_list[jj-1])
                index.append(pos)
            # print 'index=', index
            # print 'current_sentence=', current_sentence
            start = 0
            stop = 0
            # print 'char_ind=', char_ind
            ll=len(entity_word)
            # print 'll=',ll
            tmp_str = ''
            for pos, jj in enumerate(index):
                if match_flag:
                    # print '\n\nmatch_flag=1, break from index enumeration.'
                    # print 'start=',start,', stop=',stop
                    break
                # pos is the index of word in this sentence. starting from 0.
                # jj is the character index of pos_th word in this sentence.
                # print 'old_pos-ii[0], pos, jj=', old_pos-ii[0], pos, ',', jj
                # print 'ii[0]=%d, pos=%d, jj=%d' % (ii[0],pos, jj)
                if jj>char_ind:
                    # print 'jj>char_ind'
                    start = small+pos-1
                    stop = start+1
                    tmp_str = ''.join(word_list[start:stop])
                    while True:
                        # print 'tmp_str=', tmp_str
                        # print 'word_list[start:stop]=%d-%d:%s' % (start, stop, ''.join(word_list[start:stop]))
                        if entity_word in tmp_str:
                            # print 'entity_word in tmp_str'
                            match_flag = 1
                            break
                        tmp_str += word_list[stop]
                        stop += 1
                if jj==char_ind:
                    # print 'jj==char_ind'
                    start = small+pos
                    stop = start+1
                    tmp_str = ''.join(word_list[start:stop])
                    while True:
                        # print 'tmp_str=', tmp_str
                        # print 'word_list[start:stop]=%d-%d:%s' % (start, stop, ''.join(word_list[start:stop]))
                        # print 'its repr = ', repr(''.join(word_list[start:stop]))
                        if entity_word in tmp_str:
                            # print 'entity_word in tmp_str'
                            match_flag = 1
                            break
                        # print 'entity_word not in tmp_str'
                        tmp_str += word_list[stop]
                        stop += 1
        else:
            continue
    if start<0:
        print "\n\n\nentity_word %s not recovered!\n\n\n\n" % entity_word
        # exit(0)
        # raw_input()
        return [start, stop]
    # print '\nrecovered the entity_word at ', start, stop, ' word=', ''.join(word_list[start:stop]), '\n'

    return [start, stop]
# '''

# the time anaylse part:
TimeTags = (
    'Year_Crime',
    'Year_Disc',
    'None',
    )

class MyRecognizer(object):
    """docstring for MyRecognizer"""
    def __init__(self, word_list, sentences_anchor, time_anchors):
        super(MyRecognizer, self).__init__()
        self.word_list = word_list
        self.sentences_anchor = sentences_anchor
        self.time_anchors = time_anchors
        self.crime_features = self.tolist()
        self.disc_features = self.tolist()

    def tolist(self):
        d=[]
        d.append(self.feature1)
        d.append(self.feature2)
        d.append(self.feature3)
        d.append(self.feature4)
        d.append(self.feature5)
        d.append(self.feature6)
        d.append(self.feature7)
        return d

# the feature functions:
    def feature1(self, time_anchor):
        if features.isStartOfArticle(time_anchor, self.sentences_anchor):
            return 1
        else:
            return 0

    def feature2(self,time_anchor):
        if features.nearCaughtKeywords(time_anchor, self.sentences_anchor, self.word_list):
            return 1
        else:
            return 0

    def feature3(self,time_anchor):
        if features.nearReportKeywords(time_anchor, self.sentences_anchor, self.word_list):
            return 1
        else:
            return 0

    def feature4(self,time_anchor):
        if features.nearCrime(time_anchor, self.sentences_anchor, self.word_list):
            return 1
        else:
            return 0

    def feature5(self,time_anchor):
        time = ''.join(self.word_list[time_anchor[0]:time_anchor[1]])
        if features.timeSentenceByItself(time, time_anchor, self.sentences_anchor, self.word_list):
            return 1
        else:
            return 0

    def feature6(self,time_anchor):
        time = ''.join(self.word_list[time_anchor[0]:time_anchor[1]])
        if features.earliestTime(time, times):
            return 1
        else:
            return 0

    def feature7(self,time_anchor):
        time = ''.join(self.word_list[time_anchor[0]:time_anchor[1]])
        if features.latestTime(time, times):
            return 1
        else:
            return 0

    def feature8(self, time_anchor):
        lasttime_anchor = self.time_anchors[-1]
        if time_anchor==lasttime_anchor:
            return 0
        ind = self.time_anchors.index(time_anchor)
        time2_anchor = self.time_anchors[ind+1]
        if features.isStartOfTimePeriod(time1_anchor, time2_anchor, self.sentences_anchor, self.word_list):
            return 1
        else:
            return 0
#######################################


class MyTrainer(object):
    """docstring for MyTrainer"""
    def __init__(self):
        super(MyTrainer, self).__init__()
        self.n_features_disc = 7
        self.n_features_crime = 7
        self.mylr_crime = linear_model.LogisticRegression()
        self.mylr_disc = linear_model.LogisticRegression()
        self.feature_vector_crime = []
        self.feature_vector_disc = []
        self.all_tags_crime = []
        self.all_tags_disc = []
        self.myrecognizer = MyRecognizer()

    def gen_feature_disc(self, time_anchor):
        feature_vector = npy.zeros(self.n_features_disc)

        feature_vector[0]=self.myrecognizer.feature1(time_anchor)
        feature_vector[1]=self.myrecognizer.feature2(time_anchor)
        feature_vector[2]=self.myrecognizer.feature3(time_anchor)
        feature_vector[3]=self.myrecognizer.feature4(time_anchor)
        feature_vector[4]=self.myrecognizer.feature5(time_anchor)
        feature_vector[5]=self.myrecognizer.feature6(time_anchor)
        feature_vector[6]=self.myrecognizer.feature7(time_anchor)

        return feature_vector

    def gen_feature_crime(self, time_anchor):
        feature_vector = npy.zeros(self.n_features_crime)

        feature_vector[0]=self.myrecognizer.feature1(time_anchor)
        feature_vector[1]=self.myrecognizer.feature2(time_anchor)
        feature_vector[2]=self.myrecognizer.feature3(time_anchor)
        feature_vector[3]=self.myrecognizer.feature4(time_anchor)
        feature_vector[4]=self.myrecognizer.feature5(time_anchor)
        feature_vector[5]=self.myrecognizer.feature6(time_anchor)
        feature_vector[6]=self.myrecognizer.feature7(time_anchor)

        return feature_vector

    def train(self):
        path = './corruption annotated data/'
        for ftxt, fann in findAllFiles():
            with open(path + ftxt, 'r') as f:
                paragraph = f.read()
                paragraph = unicode(paragraph, 'utf-8')
                # for paragraph in paragraphs:
                word_list, sentences, sentences_anchor = sentence_index(paragraph)
                self.myrecognizer.word_list = word_list
                self.myrecognizer.sentences_anchor = sentences_anchor

                # get the time_anchors:
                time_anchors, all_tags = self.get_time_anchors_train(word_list, sentences, sentences_anchor)
                self.myrecognizer.time_anchors = time_anchors
                # append the feature vectors and tags to self.**
                for ii, time_anchor in enumerate(time_anchors):
                    tmp_feature_vector_crime = self.gen_feature_crime(time_anchor)
                    tmp_feature_vector_disc = self.gen_feature_disc(time_anchor)
                    self.feature_vector_disc.append(tmp_feature_vector_disc)
                    self.feature_vector_crime.append(tmp_feature_vector_crime)
                    curr_tag = all_tags[ii]
                    if curr_tag=="Year_Disc":
                        self.all_tags_disc.append(curr_tag)
                        self.all_tags_crime.append('None')
                    elif curr_tag=="Year_Crime":
                        self.all_tags_disc.append('None')
                        self.all_tags_crime.append(curr_tag)
                    else:
                        self.all_tags_disc.append('None')
                        self.all_tags_crime.append('None')
        # now fit
        self.mylr_crime.fit(self.feature_vector_crime, self.all_tags_crime)
        self.mylr_disc.fit(self.feature_vector_disc, self.all_tags_disc)

    def get_time_anchors_train(self, word_list, sentences, sentences_anchor):
        time_anchors = []
        all_tags = []
        for ii, sentence in enumerate(sentences):
            anchor = sentence_anchor[ii]
            tagScoreDict, tagged_items = labelTime(sentence)
            if max(tagScoreDict, key = tagScoreDict.get) == 'unknown':
                continue
            else:
                # print "IM HERE!!!"
                old_pos = anchor[0]
                for item in tagged_items:
                    # print "DEALING WITH ITEM: ", item
                    entity_word = item[0]
                    tag = item[1]

                    # print "ENTITY WORD: ", entity_word, "TAG: ", tag
                    tag_anchor = align_words_debug(word_list, sentence_anchor, old_pos, entity_word)

                    # print "TAG_ANCHOR: ", tag_anchor
                    if tag_anchor[1]!=-1:
                        time_anchors.append(tag_anchor)
                        old_pos = tag_anchor[1]
                # print "I FINISHED!!"
                    year = re.match('.*年', entity_word)
                    tmptag = tagTime(year, tag_anchor, path+fann)
                    all_tags.append(tmptag)

        return time_anchors, all_tags

    def get_time_anchors_test(self, word_list, sentences, sentences_anchor):

        time_anchors = []
        for ii, sentence in enumerate(sentences):
            anchor = sentence_anchor[ii]
            tagScoreDict, tagged_items = labelTime(sentence)
            if max(tagScoreDict, key = tagScoreDict.get) == 'unknown':
                continue
            else:
                # print "IM HERE!!!"
                old_pos = anchor[0]
                for item in tagged_items:
                    # print "DEALING WITH ITEM: ", item
                    entity_word = item[0]
                    tag = item[1]

                    # print "ENTITY WORD: ", entity_word, "TAG: ", tag
                    tag_anchor = align_words_debug(word_list, sentence_anchor, old_pos, entity_word)

                    # print "TAG_ANCHOR: ", tag_anchor
                    if tag_anchor[1]!=-1:
                        time_anchors.append(tag_anchor)
                        old_pos = tag_anchor[1]
                # print "I FINISHED!!"

        return time_anchors

    def predict_tag(self, time_anchor):
        features_disc = self.gen_feature_disc(time_anchor)
        features_crime = self.gen_feature_crime(time_anchor)

        return self.mylr_disc.predict(features_disc), self.mylr_crime.predict(features_crime)


    def analyse_time(self, word_list, sentences, sentences_anchor):
        self.myrecognizer.word_list = word_list
        self.myrecognizer.sentences_anchor = sentences_anchor
        time_anchors = self.get_time_anchors_test(word_list, sentences, sentences_anchor)
        self.myrecognizer.time_anchors = time_anchors
        tags = []
        for time_anchor in time_anchors:
            tag1, tag2 = self.predict_tag(time_anchor)
            if tag1=="None":
                tags.append((time_anchor,tag2))
            else:
                tags.append((time_anchor,tag1))
        return tags

# main part

def test_baselineRecognizer1(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(path + filename, 'r') as f:
                paragraphs = f.readlines()

                for paragraph in paragraphs:
                    lines = re.split('。|；|，|：|、', paragraph, flags=re.UNICODE)

                    for line in lines:
                        if line.strip():
                            if labelSentence(line) != 'unknown':
                                print line, labelSentence(line)

def calculate_dist(anchor, list_anchors):
    scores = [10000]*len(list_anchors)
    mean_pos0 = sum(anchor)/2.0
    for ii, person_anchor in enumerate(list_anchors):
        if person_anchor is None:
            continue
        mean_pos = sum(person_anchor)/2.0
        score = (mean_pos-mean_pos0)*(mean_pos-mean_pos0)
        scores[ii] = score
    mean_score = min(scores)
    return scores.index(mean_score)

def test_baselineRecognizer(path, filename, mytrainer):
    outputDict = {}
    persons = []
    with open(path + filename, 'r') as f:
        paragraph = f.read()
        paragraph = unicode(paragraph, 'utf-8')
        print paragraph
        # for paragraph in paragraphs:
        annotation_dict, word_list, sentences, sentences_anchor = annotate_paragraph(paragraph)
        if len(annotation_dict['person_name']) == 0:
            return -1

        time_analysis = mytrainer.analyse_time(word_list, sentences, sentences_anchor)
        annotation_dict['']
        for time_tag in time_analysis:
            time_anchor = time_tag[0]
            tmptag = time_tag[1]
            if tmptag=="None":
                continue
            if tmptag=="Year_Crime":
                annotation_dict['Year_Crime'].append(time_anchor)
            if tmptag=="Year_Disc":
                annotation_dict['Year_Disc'].append(time_anchor)

        persons_ind = [0]*len(annotation_dict['person_name'])
        # print "\n\nannotation_dict=", annotation_dict
        # print "\n\nwords:\n", word_list
        ind = 0

        for ii, anchor in enumerate(annotation_dict['person_name']):
            # print 'anchor=', anchor
            name = word_list[anchor[0]:anchor[1]]
            name = ''.join(name)
            # print 'name=', name, '\n'
            if name not in persons:
                persons.append(name)
                outputDict[name]={}
                persons_ind[ii] = ind
                ind += 1
            else:
                persons_ind[ii] = persons.index(name)
            # print 'persons_ind[%d]=%d, name is %s' % (ii, persons_ind[ii], persons[persons_ind[ii]])

        # print 'persons:'
        for name in persons:
            # print name
            pass
        # exit(0)
        new_annotation_dict = copy.deepcopy(annotation_dict)

        anchors = annotation_dict['Position']
        good_man_list = []
        for anchor in anchors:
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
            if 'Position' not in outputDict[name]:
                outputDict[name]['Position']=[]
                if re.search(GOOD_REGEX, newlist):
                    # print 'found a good man: ', newlist
                    good_man_list.append(name)
            # print "current name=", name, '; at ', annotation_dict['person_name'][ind]
            # print 'found position =', newlist, '; at ', anchor, '\n\n'

            outputDict[name]['Position'].append((anchor,newlist))

        good_man_list = set(good_man_list)
        for x in good_man_list:
            # print x
            pass
        # raw_input()
        for ii, ind in enumerate(persons_ind):
            # print '\n\nnow person is ', persons[ind]
            if persons[ind] in good_man_list:
                # print 'this person is a goodman.'
                new_annotation_dict['person_name'][ii]=None

        # exit(0)

        for ii,x in enumerate(new_annotation_dict['person_name']):
            if x is not None:
                # print persons[persons_ind[ii]]
                pass
        # print '\n\n'
        # new_annotation_dict['person_name'] = filter(None, new_annotation_dict['person_name'])

        # print "annotation_dict", annotation_dict.keys()
        for tag in EVAL_TAGS:
            if tag=="Position":
                continue
            anchors = annotation_dict[tag]
            # print "tag=", tag
            # print "anchors=", anchors
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
                try:
                    ind = calculate_dist(anchor, new_annotation_dict['person_name'])
                except Exception, e:
                    print e
                    print 'new_annotation_dict: ', new_annotation_dict['person_name']
                    print 'original annotation_dict: ', annotation_dict['person_name']
                    exit(0)
                    # raw_input()
                name = persons[persons_ind[ind]]
                # print 'ER = ', newlist
                # print 'name=', name
                # print "\n\ncurrent outputDict[name]=", outputDict[name]
                if tag not in outputDict[name]:
                    # print '\n\ntag=', tag
                    outputDict[name][tag]=[]
                    # print "outputDict[name] = ", outputDict[name]
                outputDict[name][tag].append((anchor,newlist))
                # print newlist
                # print word_list[anchor[0]:anchor[1]]

    for name in good_man_list:
        del outputDict[name]

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
                # print "\n\n\ntag = ", tag
                # print 'outputDict[person] = ', outputDict[person]
                if tag in outputDict[person]:
                    for item in outputDict[person][tag]:
                        anchor_tmp = item[0]
                        tmpstr = numbered_tag+" "+str(anchor_tmp[0])+" "+str(anchor_tmp[1])+"\t"+item[1]+"\n"
                        total_str += tmpstr
            ind += 1
        # f.write(total_str.decode(encoding='utf-8'))
        print "\n\n"
        print total_str
        data = {'content': total_str}
        json.dump(data, f)

if __name__ == '__main__':
    path = "./corruption annotated data/"

    count = 1
    # count = 0
    mytrainer = MyTrainer()
    mytrainer.train()

    for filename in os.listdir(path):
        # filename = "L_R_1990_3438.txt"
        print 'filename=', filename
        if count == 0:
            break

        if filename.endswith(".txt"):
            outputfilename = filename[:-4] + ".ann.machine"
            outputDict = test_baselineRecognizer(path, filename, mytrainer)
            if outputDict == -1:
                continue
            # print "\n\n\n\noutputDict:"
            # print outputDict
            print "\n\n\n"
            output(outputDict, path+outputfilename)
            count -= 1
            # count += 1

        # raw_input()

    print 'total # of articles: ', count

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

