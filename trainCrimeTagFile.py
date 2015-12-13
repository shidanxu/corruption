#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import re
import os
import baselineSentenceRecognizer

def tagTxt(ftxt, fann, path = './corruption annotated data/'):
    chars = []
    alltags = []
    word_list = []
    new_sentences = []
    sentence_anchor = []


    with codecs.open(path + ftxt, 'r', encoding='utf-8') as txt:
        with codecs.open(path + fann, 'r', encoding='utf-8') as ann:

            document = txt.read()
            word_list, new_sentences, sentence_anchor = baselineSentenceRecognizer.sentence_index(document)
            # print "original encoding: ", soup.originalEncoding
            for char in document:
                # print "HAHAHAHAHHAHA", type(char), char
                chars.append(char)
                alltags.append("0")
                # exit(0)
            print "Length of chars", len(chars)



            annotation = ann.readlines()
            print "".join(annotation)

            for line in annotation:
                if line:
                    # print line
                    tagLineNumber, tagBulk, tagTxt = line.split("\t")
                    numPlusTag, startIndex, endIndex = tagBulk.split()
                    startIndex = int(startIndex)
                    endIndex = int(endIndex)
                    num = numPlusTag[:1]
                    tag = numPlusTag[1:]
                    # print "line: ", tagLineNumber, tag, startIndex, endIndex, tagTxt
                    for i in range(startIndex, endIndex):
                        # print i
                        char = chars[i]

                        if tag != "Event":
                            alltags[i] = tag
                        # print chars[i]
                        # print tagTxt[i-startIndex]
    with codecs.open(path + ftxt + ".train", 'w', encoding='utf-8') as writeFile:
        for char, tag in zip(chars, alltags):
            # print char, tag
            tag = str(tag)
            writeFile.write(char + "\t" + tag + "\n")

    # Here we use a words approach
    words = []
    with codecs.open(path + ftxt, 'r', encoding='utf-8') as txt:
        words = re.split(r"(\s+)", txt.read())
        words = [(word, "0", 0, 0) for word in words]

        currentLength = 0
        for ii in range(len(words)):
            item = words[ii]
            # print item
            (word, tag, start, end) = item
            # print word, len(word)
            start = currentLength
            currentLength += len(word)
            end = currentLength

            words[ii] = (word, tag, start, end)

        print len(words), currentLength
        print words

    with codecs.open(path + fann, 'r', encoding='utf-8') as ann:
        annotation = ann.readlines()
        print "".join(annotation)

        for line in annotation:
            if line:
                # print line
                tagLineNumber, tagBulk, tagTxt = line.split("\t")
                numPlusTag, startIndex, endIndex = tagBulk.split()
                startIndex = int(startIndex)
                endIndex = int(endIndex)
                num = numPlusTag[:1]
                tagAnn = numPlusTag[1:]
                # print "line: ", tagLineNumber, tag, startIndex, endIndex, tagTxt

                # if tag == "Crime":
                if tagAnn != "Event":
                    startFound = False
                    endFound = False
                    print "Found crime: ", ''.join(chars[startIndex : endIndex])
                    print startIndex, endIndex
                    for ii in range(len(words)):
                        (word, tag, start, end) = words[ii]

                        if not startFound:
                            # print "start, end, startIndex, endIndex:", start, end, startIndex, endIndex
                            if startIndex < end:
                                tag = tagAnn
                                startFound = True
                            words[ii] = (word, tag, start, end)
                            continue

                        if startFound:
                            print "Start found, ", start, end, startIndex, endIndex
                            tag = tagAnn
                            if endIndex <= start:
                                endFound = True
                                break
                            words[ii] = (word, tag, start, end)


    # Here we only want the words in the tagged sentences
    print words
    relevantSentences = []
    for [start, end] in sentence_anchor:
        sentence = words[start:end]
        print "This sentence is: ", ''.join([word[0] for word in sentence])
        for (word, tag, start, end) in sentence:
            if tag != "0":
                # any nonzero tag makes us want the sentence
                relevantSentences.extend(sentence)
                break





    with codecs.open(path + ftxt + ".train", 'w', encoding='utf-8') as writeFile:
        with codecs.open(path + ftxt + ".train.full", 'w', encoding='utf-8') as writeFile2:

            for (word, tag, start, end) in words:
                if word.split():
                    tag = str(tag)
                    writeFile2.write(word + "\t" + tag + "\n")
            
            print relevantSentences
            # raw_input()
            for (word, tag, start, end) in relevantSentences:
                if word.split():
                    tag = str(tag)
                    writeFile.write(word + "\t" + tag + "\n")



if __name__ == '__main__':
    foldername = "corruption annotated data/"


    filesInFolder = os.listdir(foldername)
    for filename in filesInFolder:
        if filename.endswith(".ann"):
            try:
                tagTxt(filename[:-4]+".txt", filename)
            except Exception, e:
                print e
                continue
