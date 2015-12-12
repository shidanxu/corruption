#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import re
import nltk
import pycrfsuite


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



def mytrain():
    # mycrftagger = CRFTagger()
    train_sents = read_traindata("L_R_1990_3420.txt.train")

    
    # print mytrainingData


    # Turn training set to feature X
    X_train = [sent2features(train_sents)]
    # print X_train, len(X_train)
    print "\n\n\n\n\n\n"
    for item in X_train[0]:
        if 'regex_time=1' in item:
            print item
    print "DONe.\n\n\n"
    Y_train = [[getY(each) for each in train_sents]]
    # print Y_train, len(Y_train)

    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, Y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,
        'c2': 1e-3,
        'max_iterations': 5000
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
    print "Correct:", ' '.join([item for item in Y_train[0]])




def word2features(preword, word, wordnext):
    features = ["regex_punish="+feature1(preword, word, wordnext), "regex_crime="+feature2(preword, word, wordnext), "regex_amount="+feature3(preword, word, wordnext), "regex_time="+feature4(preword, word, wordnext), "regex_position="+feature5(preword, word, wordnext)]
    return features

def sent2features(sent):
    output = []
    for ii in range(len(sent)):
        output.append(word2features(sent[max(0, ii-1)], sent[ii], sent[min(ii+1, len(sent)-1)]))

    return output

def feature1(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple
    # print "word is:", txt
    
    if re.search(PUNISH_REGEX, pretxt+txt+nextxt):
        return "1"
    return "0"

def feature2(preword_tuple, word_tuple, nextword_tuple):
    # print "word is:", word_tuple
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    if re.search(CRIME_REGEX, pretxt+txt+nextxt):
        return "1"
    return "0"

def feature3(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    if re.search(AMOUNT_REGEX, pretxt+txt+nextxt):
        print "word is:", word_tuple, ". Feature 3 is 1"
        return "1"
    return "0"

def feature4(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    if re.search(TIME_REGEX, pretxt+txt+nextxt):
        print "word is:", word_tuple, ". Feature 4 is 1"
        return "1"
    return "0"

def feature5(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    if re.search(POSITION_REGEX, pretxt+txt+nextxt):
        print "word is:", word_tuple, ". Feature 5 is 1"
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