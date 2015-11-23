#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sets import Set
import re

# label the sentence with 1 of the following 3
# 1. crime
# 2. punishment
# 3. amount
# 4. unknown
punish_regex_string = '有期徒刑 (\d+|[一二三四五六七八九十]+)年|缓刑 (\d+|[一二三四五六七八九十]+)年'
punish_regex_string += '|(\d+|[一二三四五六七八九十]+)年 有期徒刑'
punish_regex_string += '|死刑|死缓|开除公职|依法逮捕|双规|没收个人财产|剥夺政治权利(终身|(\d+|[一二三四五六七八九十]+)年)+'
punish_regex_string += '|免去|开除|撤销'

crime_regex_string = '诈骗罪|经济犯罪|挪用公款|盗窃|贿赂|贪污|行贿|销赃|贪污受贿|假捐赠|倒卖|走私|索贿|报复陷害'
crime_regex_string += '|失职|渎职|以权谋私|嫖娼'

amount_regex_string = '(\d+|[一二三四五六七八九十]+)[ ]?[多|余]?[万|千|个|十|百|亿]+[余]?[美|日|欧|港]?元'
amount_regex_string += '|共计折合|茅台酒'
amount_regex_string += '|数[万千个十百亿]+[美日欧港]?元'

PUNISH_REGEX = re.compile(punish_regex_string, flags = re.UNICODE)
CRIME_REGEX = re.compile(crime_regex_string, flags = re.UNICODE)
AMOUNT_REGEX = re.compile(amount_regex_string, flags = re.UNICODE)

def labelSentence(sentence):
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
	d = {'crime': crimeScore, 'punishment': punishmentScore, 'amount': amountScore, 'unknown': unknownScore}
	return max(d, key=d.get)


prefix = "./corruption annotated data/"
for filename in os.listdir("./corruption annotated data/"):
	if filename.endswith(".txt"):
		with open(prefix + filename, 'r') as f:
			paragraphs = f.readlines()
			
			for paragraph in paragraphs:
				lines = re.split('。 | ；| ，| ：| 、', paragraph, flags=re.UNICODE)

				for line in lines:
					if line.strip():
						if labelSentence(line) != 'unknown':
							print line, labelSentence(line)

