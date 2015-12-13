#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import re
import nltk
import pycrfsuite
import os

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

    X_train = []
    Y_train = []
    foldername = "corruption annotated data/"

    filesInFolder = os.listdir(foldername)
    for filename in filesInFolder:
        if filename.endswith(".train"):
            train_sents = read_traindata(filename)

    
            # print mytrainingData


            # Turn training set to feature X
            X_train.append(sent2features(train_sents))
            # print X_train, len(X_train)
            # print "\n\n\n\n\n\n"
            # for item in X_train[0]:
            #     if 'regex_time=1' in item:
            #         print item
            # print "DONe.\n\n\n"
            Y_train.append([getY(each) for each in train_sents])
            # print Y_train, len(Y_train)

    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, Y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 0.1,
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
    print "Correct:", ' '.join([item for item in Y_train[0]])




def word2features(preword, word, wordnext):
    features = ["regex_punish="+feature1(preword, word, wordnext), "regex_crime="+feature2(preword, word, wordnext), "regex_amount="+feature3(preword, word, wordnext), "regex_time="+feature4(preword, word, wordnext), "regex_position="+feature5(preword, word, wordnext)]
    features.append("feature6"+"="+feature6(preword, word, wordnext))
    features.append("feature7"+"="+feature7(preword, word, wordnext))
    features.append("feature8"+"="+feature8(preword, word, wordnext))
    features.append("feature9"+"="+feature9(preword, word, wordnext))
    features.append("feature10"+"="+feature10(preword, word, wordnext))
    features.append("feature11"+"="+feature11(preword, word, wordnext))
    features.append("feature12"+"="+feature12(preword, word, wordnext))
    features.append("feature13"+"="+feature13(preword, word, wordnext))
    features.append("feature14"+"="+feature14(preword, word, wordnext))
    features.append("feature15"+"="+feature15(preword, word, wordnext))
    features.append("feature16"+"="+feature16(preword, word, wordnext))
    features.append("feature17"+"="+feature17(preword, word, wordnext))
    features.append("feature18"+"="+feature18(preword, word, wordnext))
    features.append("feature19"+"="+feature19(preword, word, wordnext))
    features.append("feature20"+"="+feature20(preword, word, wordnext))
    features.append("feature21"+"="+feature21(preword, word, wordnext))
    features.append("feature22"+"="+feature22(preword, word, wordnext))
    features.append("feature23"+"="+feature23(preword, word, wordnext))
    features.append("feature24"+"="+feature24(preword, word, wordnext))
    features.append("feature25"+"="+feature25(preword, word, wordnext))
    features.append("feature26"+"="+feature26(preword, word, wordnext))
    features.append("feature27"+"="+feature27(preword, word, wordnext))
    features.append("feature28"+"="+feature28(preword, word, wordnext))
    features.append("feature29"+"="+feature29(preword, word, wordnext))
    features.append("feature30"+"="+feature30(preword, word, wordnext))
    features.append("feature31"+"="+feature31(preword, word, wordnext))
    features.append("feature32"+"="+feature32(preword, word, wordnext))
    features.append("feature33"+"="+feature33(preword, word, wordnext))
    features.append("feature34"+"="+feature34(preword, word, wordnext))
    features.append("feature35"+"="+feature35(preword, word, wordnext))
    features.append("feature36"+"="+feature36(preword, word, wordnext))
    features.append("feature37"+"="+feature37(preword, word, wordnext))
    features.append("feature38"+"="+feature38(preword, word, wordnext))
    features.append("feature39"+"="+feature39(preword, word, wordnext))
    features.append("feature40"+"="+feature40(preword, word, wordnext))
    features.append("feature41"+"="+feature41(preword, word, wordnext))
    features.append("feature42"+"="+feature42(preword, word, wordnext))
    features.append("feature43"+"="+feature43(preword, word, wordnext))
    features.append("feature44"+"="+feature44(preword, word, wordnext))
    features.append("feature45"+"="+feature45(preword, word, wordnext))
    features.append("feature46"+"="+feature46(preword, word, wordnext))
    features.append("feature47"+"="+feature47(preword, word, wordnext))
    features.append("feature48"+"="+feature48(preword, word, wordnext))
    features.append("feature49"+"="+feature49(preword, word, wordnext))
    features.append("feature50"+"="+feature50(preword, word, wordnext))
    features.append("feature51"+"="+feature51(preword, word, wordnext))
    features.append("feature52"+"="+feature52(preword, word, wordnext))
    features.append("feature53"+"="+feature53(preword, word, wordnext))
    features.append("feature54"+"="+feature54(preword, word, wordnext))
    features.append("feature55"+"="+feature55(preword, word, wordnext))
    features.append("feature56"+"="+feature56(preword, word, wordnext))
    features.append("feature57"+"="+feature57(preword, word, wordnext))
    features.append("feature58"+"="+feature58(preword, word, wordnext))
    features.append("feature59"+"="+feature59(preword, word, wordnext))
    features.append("feature60"+"="+feature60(preword, word, wordnext))
    features.append("feature61"+"="+feature61(preword, word, wordnext))
    features.append("feature62"+"="+feature62(preword, word, wordnext))
    features.append("feature63"+"="+feature63(preword, word, wordnext))
    features.append("feature64"+"="+feature64(preword, word, wordnext))
    features.append("feature65"+"="+feature65(preword, word, wordnext))
    features.append("feature66"+"="+feature66(preword, word, wordnext))
    features.append("feature67"+"="+feature67(preword, word, wordnext))
    features.append("feature68"+"="+feature68(preword, word, wordnext))
    features.append("feature69"+"="+feature69(preword, word, wordnext))
    features.append("feature70"+"="+feature70(preword, word, wordnext))
    features.append("feature71"+"="+feature71(preword, word, wordnext))
    features.append("feature72"+"="+feature72(preword, word, wordnext))
    features.append("feature73"+"="+feature73(preword, word, wordnext))
    features.append("feature74"+"="+feature74(preword, word, wordnext))
    features.append("feature75"+"="+feature75(preword, word, wordnext))
    features.append("feature76"+"="+feature76(preword, word, wordnext))
    features.append("feature77"+"="+feature77(preword, word, wordnext))
    features.append("feature78"+"="+feature78(preword, word, wordnext))
    features.append("feature79"+"="+feature79(preword, word, wordnext))
    features.append("feature80"+"="+feature80(preword, word, wordnext))
    features.append("feature81"+"="+feature81(preword, word, wordnext))
    features.append("feature82"+"="+feature82(preword, word, wordnext))
    features.append("feature83"+"="+feature83(preword, word, wordnext))
    features.append("feature84"+"="+feature84(preword, word, wordnext))
    features.append("feature85"+"="+feature85(preword, word, wordnext))
    features.append("feature86"+"="+feature86(preword, word, wordnext))
    features.append("feature87"+"="+feature87(preword, word, wordnext))
    features.append("feature88"+"="+feature88(preword, word, wordnext))
    
    # print features
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
        # print "word is:", word_tuple, ". Feature 3 is 1"
        return "1"
    return "0"

def feature4(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    if re.search(TIME_REGEX, pretxt+txt+nextxt):
        # print "word is:", word_tuple, ". Feature 4 is 1"
        return "1"
    return "0"

def feature5(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    if re.search(POSITION_REGEX, pretxt+txt+nextxt):
        # print "word is:", word_tuple, ". Feature 5 is 1"
        return "1"
    return "0"

def feature6(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('有期徒刑', 'utf-8') in newword:
        return "1"
    return "0"

def feature7(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('缓刑', 'utf-8') in newword:
        return "1"
    return "0"

def feature8(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('死刑', 'utf-8') in newword:
        return "1"
    return "0"


def feature9(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('死缓', 'utf-8') in newword:
        return "1"
    return "0"

def feature10(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('开除公职', 'utf-8') in newword:
        return "1"
    return "0"

def feature11(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('依法逮捕', 'utf-8') in newword:
        return "1"
    return "0"

def feature12(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('双规', 'utf-8') in newword:
        return "1"
    return "0"

def feature13(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('没收个人财产', 'utf-8') in newword:
        return "1"
    return "0"

def feature14(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('剥夺政治权利', 'utf-8') in newword:
        return "1"
    return "0"

def feature15(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('免去', 'utf-8') in newword:
        return "1"
    return "0"

def feature16(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('开除', 'utf-8') in newword:
        return "1"
    return "0"

def feature17(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('撤销', 'utf-8') in newword:
        return "1"
    return "0"

def feature18(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('诈骗罪', 'utf-8') in newword:
        return "1"
    return "0"
def feature19(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('贪污受贿', 'utf-8') in newword:
        return "1"
    return "0"
def feature20(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('经济犯罪', 'utf-8') in newword:
        return "1"
    return "0"
def feature21(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('挪用公款', 'utf-8') in newword:
        return "1"
    return "0"
def feature22(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('盗窃', 'utf-8') in newword:
        return "1"
    return "0"

def feature23(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('贿赂', 'utf-8') in newword:
        return "1"
    return "0"
def feature24(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('贪污', 'utf-8') in newword:
        return "1"
    return "0"

def feature25(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('行贿', 'utf-8') in newword:
        return "1"
    return "0"
def feature26(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('销赃', 'utf-8') in newword:
        return "1"
    return "0"

def feature27(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('受贿', 'utf-8') in newword:
        return "1"
    return "0"
def feature28(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('假捐赠', 'utf-8') in newword:
        return "1"
    return "0"
def feature29(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('倒卖', 'utf-8') in newword:
        return "1"
    return "0"
def feature30(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('走私', 'utf-8') in newword:
        return "1"
    return "0"
def feature31(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('索贿', 'utf-8') in newword:
        return "1"
    return "0"
def feature32(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('报复陷害', 'utf-8') in newword:
        return "1"
    return "0"



def feature33(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('失职', 'utf-8') in newword:
        return "1"
    return "0"


def feature34(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('渎职', 'utf-8') in newword:
        return "1"
    return "0"

def feature35(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('以权谋私', 'utf-8') in newword:
        return "1"
    return "0"

def feature36(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('嫖娼', 'utf-8') in newword:
        return "1"
    return "0"

def feature37(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('英镑', 'utf-8') in newword:
        return "1"
    return "0"

def feature38(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('美金', 'utf-8') in newword:
        return "1"
    return "0"

def feature39(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('港币', 'utf-8') in newword:
        return "1"
    return "0"
def feature40(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('人民币', 'utf-8') in newword:
        return "1"
    return "0"

def feature41(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('日元', 'utf-8') in newword:
        return "1"
    return "0"

def feature42(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('欧元', 'utf-8') in newword:
        return "1"
    return "0"


def feature43(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('共计折合', 'utf-8') in newword:
        return "1"
    return "0"


def feature44(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('茅台酒', 'utf-8') in newword:
        return "1"
    return "0"

def feature45(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('法郎', 'utf-8') in newword:
        return "1"
    return "0"


def feature46(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('年', 'utf-8') in newword:
        return "1"
    return "0"

def feature47(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('月', 'utf-8') in newword:
        return "1"
    return "0"

def feature48(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('日', 'utf-8') in newword:
        return "1"
    return "0"

def feature49(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('法郎', 'utf-8') in newword:
        return "1"
    return "0"

def feature50(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('记者', 'utf-8') in newword:
        return "1"
    return "0"

def feature51(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('检察长', 'utf-8') in newword:
        return "1"
    return "0"


def feature52(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('纪委书记', 'utf-8') in newword:
        return "1"
    return "0"


def feature53(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('法院副院长', 'utf-8') in newword:
        return "1"
    return "0"


def feature54(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('法官', 'utf-8') in newword:
        return "1"
    return "0"


def feature55(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('检察长', 'utf-8') in newword:
        return "1"
    return "0"


def feature56(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('纪委书记', 'utf-8') in newword:
        return "1"
    return "0"


def feature57(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('法院院长', 'utf-8') in newword:
        return "1"
    return "0"


def feature58(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('通讯员', 'utf-8') in newword:
        return "1"
    return "0"


def feature59(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('特派员', 'utf-8') in newword:
        return "1"
    return "0"


def feature60(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('办事员', 'utf-8') in newword:
        return "1"
    return "0"


def feature61(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('收款员', 'utf-8') in newword:
        return "1"
    return "0"


def feature62(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('会计', 'utf-8') in newword:
        return "1"
    return "0"


def feature63(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('出纳', 'utf-8') in newword:
        return "1"
    return "0"


def feature64(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('局长', 'utf-8') in newword:
        return "1"
    return "0"


def feature65(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('书记', 'utf-8') in newword:
        return "1"
    return "0"


def feature66(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('党支部书记', 'utf-8') in newword:
        return "1"
    return "0"


def feature67(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('市委书记', 'utf-8') in newword:
        return "1"
    return "0"


def feature68(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('市长', 'utf-8') in newword:
        return "1"
    return "0"


def feature69(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('县委书记', 'utf-8') in newword:
        return "1"
    return "0"


def feature70(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('县长', 'utf-8') in newword:
        return "1"
    return "0"
###
def feature71(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('股长', 'utf-8') in newword:
        return "1"
    return "0"


def feature72(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('地委书记', 'utf-8') in newword:
        return "1"
    return "0"




def feature73(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('厅长', 'utf-8') in newword:
        return "1"
    return "0"


def feature74(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('省长', 'utf-8') in newword:
        return "1"
    return "0"

def feature75(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('省委书记', 'utf-8') in newword:
        return "1"
    return "0"

def feature76(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('区长', 'utf-8') in newword:
        return "1"
    return "0"

def feature77(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('区委书记', 'utf-8') in newword:
        return "1"
    return "0"

def feature78(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('秘书', 'utf-8') in newword:
        return "1"
    return "0"

def feature79(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('部长', 'utf-8') in newword:
        return "1"
    return "0"


def feature80(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('常委', 'utf-8') in newword:
        return "1"
    return "0"
def feature81(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('预算员', 'utf-8') in newword:
        return "1"
    return "0"
def feature82(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('社长', 'utf-8') in newword:
        return "1"
    return "0"
def feature83(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('科长', 'utf-8') in newword:
        return "1"
    return "0"
def feature84(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('经理', 'utf-8') in newword:
        return "1"
    return "0"
def feature85(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('董事长', 'utf-8') in newword:
        return "1"
    return "0"
def feature86(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('主任', 'utf-8') in newword:
        return "1"
    return "0"
def feature87(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('处长', 'utf-8') in newword:
        return "1"
    return "0"
def feature88(preword_tuple, word_tuple, nextword_tuple):
    txt, tag = word_tuple
    pretxt, pretag = preword_tuple
    nextxt, nextag = nextword_tuple

    newword = pretxt+txt + nextxt
    if unicode('厂长', 'utf-8') in newword:
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