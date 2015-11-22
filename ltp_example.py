# -*- coding: utf-8 -*-
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

import sys, os

# Set your own model path
MODELDIR="/home/shidan/Desktop/corruption/3.3.0/ltp_data"


sentence = "陕西政协原副主席祝作利一审被判处有期徒刑11年."

segmentor = Segmentor()
segmentor.load(os.path.join(MODELDIR, "cws.model"))
words = segmentor.segment(sentence)
print "\t".join(words)

postagger = Postagger()
postagger.load(os.path.join(MODELDIR, "pos.model"))
postags = postagger.postag(words)
# list-of-string parameter is support in 0.1.5
#postags = postagger.postag(["中国","进出口","银行","与","中国银行","加强","合作"])
print "\t".join(postags)

parser = Parser()
parser.load(os.path.join(MODELDIR, "parser.model"))
arcs = parser.parse(words, postags)

print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)

recognizer = NamedEntityRecognizer()
recognizer.load(os.path.join(MODELDIR, "ner.model"))
netags = recognizer.recognize(words, postags)
print "\t".join(netags)

labeller = SementicRoleLabeller()
labeller.load(os.path.join(MODELDIR, "srl/"))

roles = labeller.label(words, postags, netags, arcs)

for role in roles:
    print role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])