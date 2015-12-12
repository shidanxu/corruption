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
        self.all_tags_crime = []
        self.all_tags_disc = []
        self.myrecognizer = MyRecognizer()

    def gen_feature_disc(self, time_anchor):
        feature_vector = npy.zeros(self.n_features_disc)

        feature_vector[0]=self.myrecognizer.feature1(time_anchor)
        feature_vector[1]=self.myrecognizer.feature2(time_anchor)
        feature_vector[2]=self.myrecognizer.feature3(time_anchor)
        feature_vector[3]=self.myrecognizer.feature4(time_anchor)
        feature_vector[4]=self.myrecognizer.feature5(time_anchor)
        feature_vector[5]=self.myrecognizer.feature6(time_anchor)
        feature_vector[6]=self.myrecognizer.feature7(time_anchor)

        return feature_vector

    def gen_feature_crime(self, time_anchor):
        feature_vector = npy.zeros(self.n_features_crime)

        feature_vector[0]=self.myrecognizer.feature1(time_anchor)
        feature_vector[1]=self.myrecognizer.feature2(time_anchor)
        feature_vector[2]=self.myrecognizer.feature3(time_anchor)
        feature_vector[3]=self.myrecognizer.feature4(time_anchor)
        feature_vector[4]=self.myrecognizer.feature5(time_anchor)
        feature_vector[5]=self.myrecognizer.feature6(time_anchor)
        feature_vector[6]=self.myrecognizer.feature7(time_anchor)

        return feature_vector

    def train(self, filedir):
        path = './corruption annotated data/'
        for ftxt, fann in findAllFiles():
            with open(path + ftxt, 'r') as f:
                paragraph = f.read()
                paragraph = unicode(paragraph, 'utf-8')
                # for paragraph in paragraphs:
                word_list, sentences, sentences_anchor = sentence_index(paragraph)
                self.myrecognizer.word_list = word_list
                self.myrecognizer.sentences_anchor = sentences_anchor

# get the time_anchors:
                time_anchors, all_tags = self.get_time_anchors_train(word_list, sentences, sentences_anchor)
                self.myrecognizer.time_anchors = time_anchors
# append the feature vectors and tags to self.**
                for ii, time_anchor in enumerate(time_anchors):
                    tmp_feature_vector_crime = self.gen_feature_crime(time_anchor)
                    tmp_feature_vector_disc = self.gen_feature_disc(time_anchor)
                    self.feature_vector_disc.append(tmp_feature_vector_disc)
                    self.feature_vector_crime.append(tmp_feature_vector_crime)
                    curr_tag = all_tags[ii]
                    if curr_tag=="Year_Disc":
                        self.all_tags_disc.append(curr_tag)
                        self.all_tags_crime.append('None')
                    elif curr_tag=="Year_Crime":
                        self.all_tags_disc.append('None')
                        self.all_tags_crime.append(curr_tag)
                    else:
                        self.all_tags_disc.append('None')
                        self.all_tags_crime.append('None')

# now fit
        self.mylr_crime.fit(self.feature_vector_crime, self.all_tags_crime)
        self.mylr_disc.fit(self.feature_vector_disc, self.all_tags_disc)

    def get_time_anchors_train(self, word_list, sentences, sentences_anchor):
        time_anchors = []
        all_tags = []
        for ii, sentence in enumerate(sentences):
            anchor = sentence_anchor[ii]
            tagScoreDict, tagged_items = labelTime(sentence)
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
                    year = re.match('.*年', entity_word)
                    tmptag = tagTime(year, tag_anchor, path+fann)
                    all_tags.append(tmptag)

        return time_anchors, all_tags

    def get_time_anchors_test(self, word_list, sentences, sentences_anchor):

        time_anchors = []
        for ii, sentence in enumerate(sentences):
            anchor = sentence_anchor[ii]
            tagScoreDict, tagged_items = labelTime(sentence)
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

        return time_anchors

    def predict_tag(self, time_anchor):
        features_disc = self.gen_feature_disc(time_anchor)
        features_crime = self.gen_feature_crime(time_anchor)

        return self.mylr_disc.predict(features_disc), self.mylr_crime.predict(features_crime)


    def analyse_time(self, word_list, sentences, sentences_anchor):
        self.myrecognizer.word_list = word_list
        self.myrecognizer.sentences_anchor = sentences_anchor
        time_anchors = self.get_time_anchors_test(word_list, sentences, sentences_anchor)
        self.myrecognizer.time_anchors = time_anchors
        tags = []
        for time_anchor in time_anchors:
            tag1, tag2 = self.predict_tag(time_anchor)
            if tag1=="None":
                tags.append((time_anchor,tag2))
            else:
                tags.append((time_anchor,tag1))
        return tags

