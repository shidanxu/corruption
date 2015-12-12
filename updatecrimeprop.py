import os
import re


def main():
    filedir='./train/'
    files = [f for f in os.listdir(filedir) if os.path.isfile(os.path.join(filedir,f))]
    files_str = ''
    for f in files:
        files_str += filedir+f
    with open('crime.prop.base','r') as f:
        content = f.read
    newcontent = re.sub('trainFile = train.txt', files_str, content)
    with open('crime.prop', 'w') as f:
        f.write(newcontent)
