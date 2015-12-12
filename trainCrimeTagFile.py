#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import re

def tagTxt(ftxt, fann, path = './corruption annotated data/'):
    chars = []
    alltags = []
    with codecs.open(path + ftxt, 'r', encoding='utf-8') as txt:
        with codecs.open(path + fann, 'r', encoding='utf-8') as ann:

            document = txt.read()
            # print "original encoding: ", soup.originalEncoding
            for char in document:
                # print "HAHAHAHAHHAHA", type(char), char
                chars.append(char)
                alltags.append("Unknown")
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
        words = [(word, "Unknown", 0, 0) for word in words]

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



    print words
    with codecs.open(path + ftxt + ".train", 'w', encoding='utf-8') as writeFile:
        for (word, tag, start, end) in words:
            if word.split():
                tag = str(tag)
                writeFile.write(word + "\t" + tag + "\n")



if __name__ == '__main__':
    tagTxt("L_R_1990_3420.txt", "L_R_1990_3420.ann")
