#!/usr/bin/python
# -*- coding: utf-8 -*-

from sets import Set
import difflib
import os
import json
import matplotlib.pyplot as plt

# This method returns the tags in a file in the format
# dictionary['Shidan'] = {'Crime': '贪污', 'Punish': '无期徒刑'}
def process(filename, fields = ['Person', 'Crime', 'Money_Person', 'Punish', 'Position', 'Time', 'location', 'Province', 'City', 'Year_Disc', 'Year_Crime'], printing=False):
    dictionary = {}
    outputDict = {}
    if printing:
        print "WORKING ON FILE: ", filename
    with open(filename, 'r') as f:
        document = []
        if filename.endswith('.machine'):
            document = json.load(f)['content']
        else:
            document = unicode(f.read(), 'utf-8')
        
        if printing:
            print "type of document " + filename, " :", type(document)

        # print document
        listtags = document.split("\n")
        if printing:
            for item in listtags:
                print item
            print "\n"
        # print listtags
        # print "type of document", type(document)
        
        # print "listtags: ", listtags

        # print listtags
        # try 

        for line in listtags:
            if line.strip():
                # print line
                tagType, value = "", ""
                try:
                    tag, tagType, value = line.split("\t")
                    tagType = tagType.split(" ")[0]
                    tagIndex, tagType = int(tagType[:1]), tagType[1:]
                except Exception:
                    tagType, value = line.split("\t")
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
            # print "DICTIONARY[INDEX]: ", list(dictionary[index])
            if 'Person' not in dictionary[index]:
                return -1
            name = list(dictionary[index]['Person'])[0]
            name = name.replace(" ", "")
            outputDict[name] = {}
            for key in dictionary[index]:
                if key != 'Person':
                    outputDict[name][key] = dictionary[index][key]
            
            # The human annotation may have location in separate entries, we combine them
            location = ""
            if 'Province' in dictionary[index]:
                # print "Found province: ", ''.join(list(dictionary[index]['Province']))
                location += ''.join(list(dictionary[index]['Province']))
            if 'City' in dictionary[index]:
                # print "Found city: ", ''.join(list(dictionary[index]['City']))
                location += ''.join(list(dictionary[index]['City']))
            if location != "":
                # print "Corrected Location: ", location
                outputDict[name]['location'] = location
    if printing:
        print "\n\n\n"

    return outputDict

# This baseline specifies whether we want the element or the set element to be compared to
def maxScore(element, compareSet, baseline):
    comparisonScores = []

    # Remove spaces for comparison
    element = "".join(element.split())
    lengthLongest = len(element)
    # print "element is:", element
    if len(element) == 0:
        return 0
    for item in compareSet:
        # Remove spaces for comparison
        item = "".join(item.split())
        # if baseline == 0:
            # lengthLongest = len(item)
        # else:
            # lengthLongest = len(element)


        s = difflib.SequenceMatcher(None, element, item)
        m = s.find_longest_match(0, len(element), 0, len(item))

        # print "Comparing: ", item, element, min(1.0, float(m.size) / lengthLongest)

        comparisonScores.append(min(1.0, float(m.size) / lengthLongest))

    # print comparisonScores
    # print "\n"
    return max(comparisonScores)

def maxScoreEntire(element, setOfSet):
    comparisonScores = []
    # Clean up string
    element = "".join(element.split())
    lengthLongest = len(element)

    # print "element is:", element
    if len(element) == 0:
        return 0

    for dictionary in setOfSet:
        for key, value in setOfSet[dictionary].iteritems():
            # value is a set
            for item in value:
                # First clean up
                item = ''.join(item.split())
                s = difflib.SequenceMatcher(None, element, item)
                m = s.find_longest_match(0, len(element), 0, len(item))

                # print "Comparing MAX Entire: ", item, element, min(1.0, float(m.size) / lengthLongest)
                comparisonScores.append(min(1.0, float(m.size) / lengthLongest))
    # print "\n"
    return max(comparisonScores)



def evaluate(human, machine, fields = ['Person', 'Crime', 'Money_Person', 'Punish', 'Position', 'Year_Disc', 'Year_Crime'], printing = False):
    # Calculate a precision score and a recall score
    # recall: exact matches in humanDict that are also in machineDict
    # Precision: line exact matches in machineDict that are also found in humanDict
    totalScore = 0.0
    possibleScore = 0.0

    recallTagScoreDict = {}
    precisionTagScoreDict = {}


    humanDict = process(human, printing = printing)
    machineDict = process(machine, printing = printing)

    if humanDict == -1 or machineDict == -1:
        return -1


    # print humanDict
    # for person in humanDict:
    #   print person
    #   for item in humanDict[person]:
    #       print item, humanDict[person][item]

    # 每一个UROP找到的人 总分是行数
    for person in humanDict:
        # 1 Extra point for finding the person
        possibleScore += len(humanDict[person]) + 1
        # 如果这个人机器也找到了
        if person in machineDict:
            # 如果所有数据相等 直接给分
            if machineDict[person] == humanDict[person]:
                totalScore += len(humanDict[person]) + 1
            else:
                totalScore += 1
                # 每个UROP找到的entry
                for item in humanDict[person]:
                    # 如果机器也找到了
                    if item in machineDict[person]:
                        # Here want approximate matching
                        # humanDict[person][item] is a Set
                        # 总分等于人类找到的行数
                        total = len(humanDict[person][item])
                        # print "total is:", total
                        # print "item is:", item
                        hit = 0.0
                        # 对人类找到的每一行 机器找到的最好结果是几分 机器／人类长度
                        for element in humanDict[person][item]:
                            hit += maxScore(element, machineDict[person][item], 0)
                        totalScore += hit / total

                        # totalScore += int(humanDict[person][item] == machineDict[person][item])
    if possibleScore == 0:
        return -1
    recallScore = totalScore / possibleScore

    totalScore = 0.0
    possibleScore = 0.0

    # 对每个机器找到的人
    for person in machineDict:
        possibleScore += len(machineDict[person]) + 1
        # 如果人类也找到了这个人
        if person in humanDict:
            if machineDict[person] == humanDict[person]:
                totalScore += len(humanDict[person]) + 1
            else:
                # 对于机器找到的所有关于这个人的信息
                totalScore += 1
                for item in machineDict[person]:
                    # 如果人类也有
                    if item in humanDict[person]:
                        # 看机器总共几行
                        total = len(machineDict[person][item])
                        hit = 0.0
                        # 看机器的每一行 是不是真的阳性
                        for element in machineDict[person][item]:
                            hit += maxScore(element, humanDict[person][item], 1)

                        totalScore += hit / total
                        # totalScore += int(humanDict[person][item] == machineDict[person][item])
    
    if possibleScore == 0:
        return -1
    precisionScore = totalScore / possibleScore


    # 宽泛的recall
    totalScore = 0.0
    possibleScore = 0.0
    for person in humanDict:
        # 1 extra pt for finding the person
        possibleScore += len(humanDict[person]) + 1

        if person in machineDict:
            totalScore += 1
        
        for item in humanDict[person]:
            total = len(humanDict[person][item])
            hit = 0.0
            for element in humanDict[person][item]:
                hit += maxScoreEntire(element, machineDict)
            totalScore += hit / total
            # print "add this many pts:", hit, total, hit/total

    if possibleScore == 0:
        return -1
    infoExtractionRecall = totalScore / possibleScore

    # 宽泛的precision
    totalScore = 0.0
    possibleScore = 0.0
    for person in machineDict:
        # 1 extra pt for finding the person
        possibleScore += len(machineDict[person]) + 1

        if person in humanDict:
            totalScore += 1
        
        for item in machineDict[person]:
            total = len(machineDict[person][item])
            hit = 0.0
            for element in machineDict[person][item]:
                hit += maxScoreEntire(element, humanDict)
            totalScore += hit / total
            # print "add this many pts:", hit, total, hit/total

    if possibleScore == 0:
        return -1

    infoExtractionPrecision = totalScore / possibleScore



    # Per tag recall
    for person in humanDict:
        # 1 Extra point for finding the person
        possibleScore += len(humanDict[person]) + 1
        # 如果这个人机器也找到了
        if person in machineDict:
            # 如果所有数据相等 直接给分
            totalScore += 1
            # 每个UROP找到的entry
            for item in humanDict[person]:
                if item not in recallTagScoreDict:
                    recallTagScoreDict[item] = {"possibleScore": 0.0, "score": 0.0}
                
                recallTagScoreDict[item]["possibleScore"] += len(humanDict[person][item])

                if item in machineDict[person]:
                    hit = 0.0
                    for element in humanDict[person][item]:
                        hit += maxScore(element, machineDict[person][item], 0)
                    recallTagScoreDict[item]["score"] += hit
                    
    # Per tag precision
    for person in machineDict:
        # 1 Extra point for finding the person
        possibleScore += len(machineDict[person]) + 1
        # 如果这个人机器也找到了
        if person in humanDict:
            # 如果所有数据相等 直接给分
            totalScore += 1
            # 每个UROP找到的entry
            for item in machineDict[person]:
                if item not in precisionTagScoreDict:
                    precisionTagScoreDict[item] = {"possibleScore": 0.0, "score": 0.0}
                
                precisionTagScoreDict[item]["possibleScore"] += len(machineDict[person][item])

                if item in humanDict[person]:
                    hit = 0.0
                    for element in machineDict[person][item]:
                        hit += maxScore(element, humanDict[person][item], 0)
                    precisionTagScoreDict[item]["score"] += hit
                    
             
   



    return recallScore, precisionScore, infoExtractionRecall, infoExtractionPrecision, recallTagScoreDict, precisionTagScoreDict



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
                try:
                    evaluationValues = evaluate(foldername + filename, foldername + filename+suffix)
                    if evaluationValues != -1: 
                        if min(evaluationValues) > 0.5:
                            print evaluationValues
                            evaluate(foldername + filename, foldername + filename+suffix, printing = True)
                        else:
                            scores.append(evaluationValues)
                except Exception, e:
                    print e
                    continue
                
    # Prints scores list, average precision, avg recall
    print scores
    strict_recall = sum([pair[0] for pair in scores]) / len(scores)
    strict_precision = sum([pair[1] for pair in scores]) / len(scores)
    extraction_recall = sum([pair[2] for pair in scores]) / len(scores)
    extraction_precision = sum([pair[3] for pair in scores]) / len(scores)
    recallTagDict = [pair[4] for pair in scores]
    precisionTagDict = [pair[5] for pair in scores]

    recallCrimeDict = [dictItem for dictItem in recallTagDict if u'Crime' in dictItem]
    recallCrime = sum([dictItem[u'Crime']['score'] /dictItem[u'Crime']['possibleScore'] for dictItem in recallCrimeDict]) / len(recallCrimeDict)
    
    recallPositionDict = [dictItem for dictItem in recallTagDict if u'Position' in dictItem]
    recallPosition = sum([dictItem[u'Position']['score'] /dictItem[u'Position']['possibleScore'] for dictItem in recallPositionDict]) / len(recallPositionDict)
    
    recallPunishDict = [dictItem for dictItem in recallTagDict if u'Punish' in dictItem]
    recallPunish = sum([dictItem[u'Punish']['score'] /dictItem[u'Punish']['possibleScore'] for dictItem in recallPunishDict]) / len(recallPunishDict)
    
    recallMoneyDict = [dictItem for dictItem in recallTagDict if u'Money_Person' in dictItem]
    recallMoney = sum([dictItem[u'Money_Person']['score'] /dictItem[u'Money_Person']['possibleScore'] for dictItem in recallMoneyDict]) / len(recallMoneyDict)
    
    precisionCrimeDict = [dictItem for dictItem in precisionTagDict if u'Crime' in dictItem]
    precisionCrime = sum([dictItem[u'Crime']['score'] /dictItem[u'Crime']['possibleScore'] for dictItem in precisionCrimeDict]) / len(precisionCrimeDict)
    
    precisionPositionDict = [dictItem for dictItem in precisionTagDict if u'Position' in dictItem]
    precisionPosition = sum([dictItem[u'Position']['score'] /dictItem[u'Position']['possibleScore'] for dictItem in precisionPositionDict]) / len(precisionPositionDict)
    
    precisionPunishDict = [dictItem for dictItem in precisionTagDict if u'Punish' in dictItem]
    precisionPunish = sum([dictItem[u'Punish']['score'] /dictItem[u'Punish']['possibleScore'] for dictItem in precisionPunishDict]) / len(precisionPunishDict)
    
    precisionMoneyDict = [dictItem for dictItem in precisionTagDict if u'Money_Person' in dictItem]
    precisionMoney = sum([dictItem[u'Money_Person']['score'] /dictItem[u'Money_Person']['possibleScore'] for dictItem in precisionMoneyDict]) / len(precisionMoneyDict)
    

    print "AVG Recall: ", strict_recall
    print "AVG Precision: ", strict_precision
    print "AVG Extraction Recall: ", extraction_recall
    print "AVG Extraction Precision: ", extraction_precision
    print "Normalized Precision: ", strict_precision / extraction_precision
    print "Normalized Recall: ", strict_recall / extraction_recall


    print "AVG Recall Crime: ", recallCrime
    print "AVG Recall Position: ", recallPosition
    print "AVG Recall Punish: ", recallPunish
    print "AVG Recall Money: ", recallMoney

    print "AVG Precision Crime: ", precisionCrime
    print "AVG Precision Position: ", precisionPosition
    print "AVG Precision Punish: ", precisionPunish
    print "AVG Precision Money: ", precisionMoney
    # print "AVG Recall Year_Disc: ", recallYearD


    # Plotting
    xvalues = [pair[0] / pair[2] for pair in scores]
    yvalues = [pair[1] / pair[3] for pair in scores]

    plt.subplot(2,2, 1)
    plt.plot(xvalues, yvalues, 'ro')
    plt.xlabel('Recall Normalized')
    plt.ylabel('Precision Normalized')

    plt.plot([0, 1], [0, 1])
    plt.plot([0, 1], [1,1], 'b--')

    plt.subplot(2, 2, 2)

    n_bins = 20
    strict_recall_output = [pair[0] for pair in scores]
    plt.hist(strict_recall_output, n_bins)

    plt.subplot(2, 2, 3)

    n_bins = 20
    strict_precision_output = [pair[1] for pair in scores]
    plt.hist(strict_precision_output, n_bins)

    plt.subplot(2, 2, 4)

    n_bins = 20
    extraction_recall_output = [pair[2] for pair in scores]
    plt.hist(extraction_recall_output, n_bins)

    plt.show()
    