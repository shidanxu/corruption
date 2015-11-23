import os
from sets import Set

crimes = Set()
punish = Set()

prefix = "./corruption annotated data/"
for filename in os.listdir("./corruption annotated data/"):
	if filename.endswith(".ann"):
		with open(prefix + filename, 'r') as f:
			lines = f.readlines()
			for line in lines:
				values = line.split("\t")
				if len(values) > 1:
					tag = values[1]
					value = values[-1]

					mytag = tag.split(" ")[0].strip()[1:]
					
					if mytag == "Punish":
						punish.add(value)
					if mytag == "Crime":
						crimes.add(value)

with open("crimes_auto.txt", 'w') as f:
	for item in crimes:
		f.write(item)

with open("punish_auto.txt", 'w') as f:
	for item in punish:
		f.write(item)
# for item in punish:
# 	print item