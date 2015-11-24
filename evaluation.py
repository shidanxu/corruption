#!/usr/bin/python
# -*- coding: utf-8 -*-

from sets import Set
import difflib
import os

# This method returns the tags in a file in the format
# dictionary['Shidan'] = {'Crime': '贪污', 'Punish': '无期徒刑'}
def process(filename, fields = ['Person', 'Crime', 'Money_Person', 'Punish', 'Position']):
    dictionary = {}
    outputDict = {}
    with open(filename, 'r') as f:
        listtags = f.readlines()

        for line in listtags:
            tag, tagType, value = line.split("\t")
            tagType = tagType.split(" ")[0]
            tagIndex, tagType = int(tagType[:1]), tagType[1:]

            if tagType in fields:
                if tagIndex in dictionary:
                    if tagType in dictionary[tagIndex]:
                        dictionary[tagIndex][tagType].add(value)
                    else:
                        dictionary[tagIndex][tagType] = Set([value])
                else:
                    dictionary[tagIndex] = {}
                    dictionary[tagIndex][tagType] = Set([value])

        for index in dictionary:
            name = list(dictionary[index]['Person'])[0]
            outputDict[name] = {}
            for key in dictionary[index]:
                if key != 'Person':
                    outputDict[name][key] = dictionary[index][key]

    return outputDict

# This baseline specifies whether we want the element or the set element to be compared to
def maxScore(element, compareSet, baseline):
    comparisonScores = []
    for item in compareSet:
        if baseline == 0:
            lengthLongest = len(item)
        else:
            lengthLongest = len(element)

        s = difflib.SequenceMatcher(None, element, item)
        m = s.find_longest_match(0, len(element), 0, len(item))

        comparisonScores.append(min(1.0, float(m.size) / lengthLongest))

    # print comparisonScores
    return max(comparisonScores)



def evaluate(human, machine, fields = ['Person', 'Crime', 'Money_Person', 'Punish', 'Position']):
    # Calculate a precision score and a recall score
    # recall: exact matches in humanDict that are also in machineDict
    # Precision: line exact matches in machineDict that are also found in humanDict
    totalScore = 0.0
    possibleScore = 0.0

    humanDict = process(human)
    machineDict = process(machine)

    # print humanDict
    # for person in humanDict:
    #   print person
    #   for item in humanDict[person]:
    #       print item, humanDict[person][item]

    for person in humanDict:
        possibleScore += len(humanDict[person])
        if person in machineDict:
            if machineDict[person] == humanDict[person]:
                totalScore += len(humanDict[person])
            else:
                for item in humanDict[person]:
                    if item in machineDict[person]:
                        # Here want approximate matching
                        # humanDict[person][item] is a Set
                        total = len(humanDict[person][item])
                        hit = 0.0
                        for element in humanDict[person][item]:
                            hit += maxScore(element, machineDict[person][item], 0)
                        totalScore += hit / total

                        # totalScore += int(humanDict[person][item] == machineDict[person][item])
    recallScore = totalScore / possibleScore

    totalScore = 0.0
    possibleScore = 0.0

    for person in machineDict:
        possibleScore += len(machineDict[person])
        if person in humanDict:
            if machineDict[person] == humanDict[person]:
                totalScore += len(humanDict[person])
            else:
                for item in machineDict[person]:
                    if item in humanDict[person]:
                        total = len(machineDict[person][item])
                        hit = 0.0
                        for element in machineDict[person][item]:
                            hit += maxScore(element, humanDict[person][item], 1)

                        totalScore += hit / total
                        # totalScore += int(humanDict[person][item] == machineDict[person][item])
    precisionScore = totalScore / possibleScore

    return precisionScore, recallScore

if __name__ == '__main__':
    foldername = "corruption annotated data/"
    # file1 = "corruption annotated data/L_R_1990_3420.ann"
    # file2 = "corruption annotated data/L_R_1990_3420_mod.machine"

    scores = []
    suffix = ".machine"

    filesInFolder = os.listdir(foldername)
    for filename in filesInFolder:
        if filename.endswith(".ann"):
            if filename + suffix in filesInFolder:
                scores.append(evaluate(foldername + filename, foldername + filename+suffix))


    # Prints scores list, average precision, avg recall
    print scores
    print "AVG Precision: ", sum([pair[0] for pair in scores]) / len(scores)
    print "AVG Recall: ", sum([pair[1] for pair in scores]) / len(scores)
    # print(evaluate(file1, file2))
