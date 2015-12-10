import numpy as npy
import os, sys
from sklearn import linear_model
import features


TimeTags = (
    'Year_Crime',
    'Year_Disc',
    'None',
    )

class MyRecognizer(object):
    """docstring for MyRecognizer"""
    def __init__(self, word_list, sentences_anchor, time_anchors):
        super(MyRecognizer, self).__init__()
        self.word_list = word_list
        self.sentences_anchor = sentences_anchor
        self.time_anchors = time_anchors
        self.crime_features = self.tolist()
        self.disc_features = self.tolist()

    def tolist(self):
        d=[]
        d.append(self.feature1)
        d.append(self.feature2)
        d.append(self.feature3)
        d.append(self.feature4)
        d.append(self.feature5)
        d.append(self.feature6)
        d.append(self.feature7)
        return d

# the feature functions:
    def feature1(self, time_anchor):
        if features.isStartOfArticle(time_anchor, self.sentences_anchor):
            return 1
        else:
            return 0

    def feature2(self,time_anchor):
        if features.nearCaughtKeywords(time_anchor, self.sentences_anchor, self.word_list)
            return 1
        else:
            return 0

    def feature3(self,time_anchor):
        if features.nearReportKeywords(time_anchor, self.sentences_anchor, self.word_list)
            return 1
        else:
            return 0

    def feature4(self,time_anchor):
        if features.nearCrime(time_anchor, self.sentences_anchor, self.word_list)
            return 1
        else:
            return 0

    def feature5(self,time_anchor):
        time = ''.join(self.word_list[time_anchor[0]:time_anchor[1]])
        if features.timeSentenceByItself(time, time_anchor, self.sentences_anchor, self.word_list)
            return 1
        else:
            return 0

    def feature6(self,time_anchor):
        time = ''.join(self.word_list[time_anchor[0]:time_anchor[1]])
        if features.earliestTime(time, times)
            return 1
        else:
            return 0

    def feature7(self,time_anchor):
        time = ''.join(self.word_list[time_anchor[0]:time_anchor[1]])
        if features.latestTime(time, times):
            return 1
        else:
            return 0

    def feature8(self, time_anchor):
        lasttime_anchor = self.time_anchors[-1]
        if time_anchor==lasttime_anchor:
            return 0
        ind = self.time_anchors.index(time_anchor)
        time2_anchor = self.time_anchors[ind+1]
        if features.isStartOfTimePeriod(time1_anchor, time2_anchor, self.sentences_anchor, self.word_list)
            return 1
        else:
            return 0
#######################################


class MyTrainer(object):
    """docstring for MyTrainer"""
    def __init__(self, arg):
        super(MyTrainer, self).__init__()
        self.arg = arg
        self.n_features_disc = 7
        self.n_features_crime = 7
        self.mylr_crime = linear_model.LogisticRegression()
        self.mylr_disc = linear_model.LogisticRegression()
        self.feature_vector_crime = []
        self.feature_vector_disc = []

    def gen_feature_disc(self, time_anchor):
        feature_vector = npy.zeros(self.n_features_disc)

        for ii, feature in enumerate(myrecognizer.disc_features):
            feature_vector[ii]=feature(time_anchor)

    def gen_feature_crime(self, time_anchor):
        feature_vector = npy.zeros(self.n_features_crime)

        for ii, feature in enumerate(myrecognizer.crime_features):
            feature_vector[ii]=feature(time_anchor)

    def train(self, filedir):
        for tmpfile in filedir:
            with open(path + filename, 'r') as f:
                paragraph = f.read()
                paragraph = unicode(paragraph, 'utf-8')
                # for paragraph in paragraphs:
                word_list, sentences, sentences_anchor = sentence_index(paragraph)
# get the time_anchors:
                for ii, sentence in enumerate(sentences):
                    # print ii, len(sentences)
                    # print 'sentence=', sentence
                    # print 'encoded:', [sentence]
                    anchor = sentence_anchor[ii]

                    # tag = labelSentence(sentence)
                    tagScoreDict, tagged_items = labelTime(sentence)
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
                                time_anchors.append(tag_anchor)
                                old_pos = tag_anchor[1]
                        # print "I FINISHED!!"
# time_anchors got

                for ii, time_anchor in enumerate(time_anchors):
                    tmp_feature_vector_crime = self.gen_feature_crime(time_anchor)
                    tmp_feature_vector_disc = self.gen_feature_disc(time_anchor)
                    self.feature_vector_disc.append(tmp_feature_vector_disc)
                    self.feature_vector_crime.append(tmp_feature_vector_crime)
                    curr_tag = tags[ii]
                    if curr_tag=="Year_Disc":
                        self.all_tags_disc.append(curr_tag)
                        self.all_tags_crime.append('None')
                    elif curr_tag=="Year_Crime":
                        self.all_tags_disc.append('None')
                        self.all_tags_crime.append(curr_tag)
                    else:
                        self.all_tags_disc.append('None')
                        self.all_tags_crime.append('None')
        self.mylr_crime.fit(self.feature_vector_crime, self.all_tags_crime)
        self.mylr_disc.fit(self.feature_vector_disc, self.all_tags_disc)


    def train_dev(self):
        self.train(self.dev_file)

    def train_train(self):
        self.train(self.train_file)


        return feature_vector

    def greedy2(self,word1, word2, tag):
        features = self.gen_feature2(1, 2, [word1, word2],[tag])
        return self.mylr.predict(features)

    def test2(self):
        pass

    def run2(self):
        identest, list_tokenstest = self.read_tagfile(self.test_file)
        for ii, sentence in enumerate(list_tokenstest):
            splitted_tokens = self.split_tokens(sentence)
            l = len(splitted_tokens)
            # f.write(identest[ii])
            print identest[ii][:-1]
            tagged_sentence = ''
            for kk, pair in enumerate(splitted_tokens):
                splitted_pair = self.split_pair(pair)
                word=splitted_pair[0]
                # tags[kk]=splitted_pair[1]
                if kk==0:
                    # f1 = self.feature1(word)
                    # f2 = self.feature2(word)
                    # f3 = self.feature3(word)
                    # feature_vector = [f1, f2, f3, 0, 0]
                    feature_vector = [0, 0, 0]
                    new_tag = self.mylr.predict(feature_vector)[0]
                else:
                    new_tag = self.greedy2(word1, word, tag1)[1]
                    # print "new_tag=", new_tag
                word1 = word
                tag1 = new_tag
                if new_tag=="GENE":
                    new_tag = "GENE1"
                tagged_sentence += word + "_" + new_tag+" "
            print tagged_sentence
            # if ii>4:
            #     break


def main():
    n=0 # the length of my memory
    myrecognizer = MyRecognizer()

    training_file = sys.argv[1]
    test_file = sys.argv[2]
    mode = sys.argv[3]

    myrecognizer.mode = mode
    myrecognizer.test_file = test_file
    if mode!="1":
        myrecognizer.n_mem = 1
        myrecognizer.n_features = 3
    else:
        myrecognizer.n_mem = 0
        myrecognizer.n_features = 3
    myrecognizer.train(training_file)
    # print myrecognizer.mylr.coef_
    myrecognizer.train_dev()
    myrecognizer.train_train()
    if mode=="1":
        myrecognizer.run1()
    if mode=="2":
        myrecognizer.run2()
        # myrecognizer.test2()
    if mode=="3":
        myrecognizer.run2()

if __name__ == '__main__':
    main()
