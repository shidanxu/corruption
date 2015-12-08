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
punish_regex_string = unicode('有期徒刑(\d+|[一二三四五六七八九十]+)年|缓刑(\d+|[一二三四五六七八九十]+)年', 'utf-8')
punish_regex_string += unicode('|(\d+|[一二三四五六七八九十]+)年 有期徒刑','utf-8')
punish_regex_string += unicode('|死刑|死缓|开除公职|依法逮捕|双规|没收个人财产|剥夺政治权利(终身|(\d+|[一二三四五六七八九十]+)年)+','utf-8')
punish_regex_string += unicode('|免去|开除|撤销','utf-8')

crime_regex_string = unicode('诈骗罪|经济犯罪|挪用公款|盗窃|贿赂|贪污|行贿|销赃|贪污受贿|假捐赠|倒卖|走私|索贿|报复陷害','utf-8')
crime_regex_string += unicode('|失职|渎职|以权谋私|嫖娼','utf-8')

amount_regex_string = unicode('((\d+|[一二三四五六七八九十]+)[\.]?(\d+|[一二三四五六七八九十]+)?[ ]?[多余]?[ ]?[万千个十百亿]*[多余]?[美|日|欧|港]?元)','utf-8')
amount_regex_string += unicode('|共计折合|茅台酒','utf-8')
amount_regex_string += unicode('|数[万千个十百亿]+[美日欧港]?元','utf-8')

time_regex_string = unicode('(\d+[ ]?年[ ]?\d+[ ]?月[ ]?\d+[ ]?日)+([ ]?[下午|上午|傍晚|凌晨][ ]?(\d+[ ]?时)?([ ]?[\d+]分)?([ ]?[\d+]秒)?[左右]?)?', 'utf-8')

good_position_regex_string = unicode('记者|法官|检察长|纪委书记|法院院长|通讯员|','utf-8')
neutral_position_regex_string = unicode('', 'utf-8')
bad_position_regex_string = unicode('特派员|办事员|收款员|', 'utf-8')

bad_position_regex_string += unicode('([副]?(局长|书记|党支部书记|市委书记|市长|县委书记|县长','utf-8')
bad_position_regex_string += unicode('|股长|地委书记|厅长|省长|省委书记|区长|区委书记','utf-8')
bad_position_regex_string += unicode('|秘书长|秘书|部长|常委|预算员|社长|科长|部长|经理|总经理|董事长|主任|处长))','utf-8')



# position regex includes good and bad

position_regex_string = good_position_regex_string + bad_position_regex_string

PUNISH_REGEX = re.compile(punish_regex_string, flags = re.UNICODE)
CRIME_REGEX = re.compile(crime_regex_string, flags = re.UNICODE)
AMOUNT_REGEX = re.compile(amount_regex_string, flags = re.UNICODE)
TIME_REGEX = re.compile(time_regex_string, flags = re.UNICODE)
POSITION_REGEX = re.compile(position_regex_string, flags = re.UNICODE)



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
        # print "Crime found: ", found.group()
        crimeScore += len(found.group())
        word_tag_monotone.append((found.group(), "Crime"))

    if re.search(PUNISH_REGEX, sentence):
        found = re.search(PUNISH_REGEX, sentence)
        # print "Punish found: ", found.group()
        punishmentScore += len(found.group())
        word_tag_monotone.append((found.group(), "Punish"))

    if re.search(AMOUNT_REGEX, sentence):
        found = re.search(AMOUNT_REGEX, sentence)
        # print "Amount found: ", found.group()
        amountScore += len(found.group())
        word_tag_monotone.append((found.group(), "Money_Person"))

    if re.search(TIME_REGEX, sentence):
        found = re.search(TIME_REGEX, sentence)
        # print "Time found: ", found.group()
        timeScore += len(found.group())
        word_tag_monotone.append((found.group(), "Time"))

    if re.search(POSITION_REGEX, sentence):
        found = re.search(POSITION_REGEX, sentence)
        print "Position found: ", found.group()
        positionScore += len(found.group())
        word_tag_monotone.append((found.group(), "Position"))


    tagScoreDict = {'Crime': crimeScore, 'Punish': punishmentScore, 'Money_Person': amountScore, 'Time': timeScore, 'Position': positionScore, 'unknown': unknownScore}

    # if max(tagScoreDict, key = tagScoreDict.get) != 'unknown':
    #     print sentence, max(tagScoreDict, key = tagScoreDict.get)


    # print word_tag_monotone

    # print crimes, punishes, amounts
    # return max(tagScoreDict, key=tagScoreDict.get)
    return tagScoreDict, word_tag_monotone

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
    # print 'new_sentences = ', '\n'.join(' '.join(sentence) for sentence in new_sentences)

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

    return annotation_dict, word_list

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
        exit(0)
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
        return [start, stop]
    # print '\nrecovered the entity_word at ', start, stop, ' word=', ''.join(word_list[start:stop]), '\n'

    return [start, stop]
# '''

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
        if len(annotation_dict['person_name']) == 0:
            return -1

        persons_ind = [0]*len(annotation_dict['person_name'])
        # print "\n\nannotation_dict=", annotation_dict
        # print "\n\nwords:\n", word_list
        ind = 0

        for ii, anchor in enumerate(annotation_dict['person_name']):
            print 'anchor=', anchor
            name = word_list[anchor[0]:anchor[1]]
            name = ''.join(name)
            print 'name=', name, '\n'
            if name not in persons:
                persons.append(name)
                outputDict[name]={}
                persons_ind[ii] = ind
                ind += 1
            else:
                persons_ind[ii] = persons.index(name)

        anchors = annotation_dict['Position']
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
            print "\n\ncurrent name=", name, '; at ', annotation_dict['person_name'][ind]
            print 'found position =', newlist, '; at ', anchor

            outputDict[name]['Position'].append((anchor,newlist))

        # print "annotation_dict", annotation_dict.keys()
        for tag in EVAL_TAGS:
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
                ind = calculate_dist(anchor, annotation_dict['person_name'])
                name = persons[persons_ind[ind]]
                # print "\n\ncurrent outputDict[name]=", outputDict[name]
                if tag not in outputDict[name]:
                    # print '\n\ntag=', tag
                    outputDict[name][tag]=[]
                    # print "outputDict[name] = ", outputDict[name]
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


    count = 8
    for filename in os.listdir(path):
        # filename = "L_R_1990_3399.txt"
        print 'filename=', filename
        if count == 0:
            break

        if filename.endswith(".txt"):
            outputfilename = filename[:-4] + ".ann.machine"

            outputDict = test_baselineRecognizer(path, filename)
            if outputDict == -1:
                continue
            # print "\n\n\n\noutputDict:"
            # print outputDict
            print "\n\n\n"
            output(outputDict, path+outputfilename)
            count -= 1
        # raw_input()


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





