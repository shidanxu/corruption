#!/usr/bin/python
# -*- coding: utf-8 -*-

# This method returns the tags in a file in the format
# dictionary['Shidan'] = {'Crime': '贪污', 'Punish': '无期徒刑'}
def process(listtags):
	dictionary = {}
	outputDict = {}
	for line in listtags:
		tag, tagType, value = line.split("\t")
		tagType = tagType.split(" ")[0]
		tagIndex, tagType = int(tagType[:1]), tagType[1:]

		if tagIndex in dictionary:
			if tagType in dictionary[tagIndex]:
				dictionary[tagIndex][tagType] += (value)
			else:
				dictionary[tagIndex][tagType] = value
		else:
			dictionary[tagIndex] = {}
			dictionary[tagIndex][tagType] = value

	for index in dictionary:
		name = dictionary[index]['Person']
		outputDict[name] = {}
		for key in dictionary[index]:
			if key != 'Person':
				outputDict[name][key] = dictionary[index][key]

	return outputDict

def evaluate(human, machine):
	# Calculate a precision score and a recall score
	# recall: exact matches in humanDict that are also in machineDict
	# Precision: line exact matches in machineDict that are also found in humanDict
	totalScore = 0.0
	possibleScore = 0.0
	with open(human, 'r') as f:
		with open(machine, 'r') as g:
			humanLabeled = f.readlines()
			machineLabeled = g.readlines()
			humanDict = process(humanLabeled)
			machineDict = process(machineLabeled)

			# print humanDict
			# for person in humanDict:
			# 	print person
			# 	for item in humanDict[person]:
			# 		print item, humanDict[person][item]

			for person in humanDict:
				possibleScore += len(humanDict[person])
				if person in machineDict:
					if machineDict[person] == humanDict[person]:
						totalScore += len(humanDict[person])
					else:
						for item in humanDict[person]:
							if item in machineDict[person]:
								totalScore += int(humanDict[person][item] == machineDict[person][item])
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
								totalScore += int(humanDict[person][item] == machineDict[person][item])
			precisionScore = totalScore / possibleScore

	return precisionScore, recallScore

if __name__ == '__main__':
	file1 = "corruption annotated data/L_R_1990_3420.ann"
	file2 = "corruption annotated data/L_R_1990_3420_mod.ann"
	print(evaluate(file1, file2))