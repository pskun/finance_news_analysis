#!/usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
import corpora


class LdaAnalysis(object):


    def __init__():
        self.words = []
        self.word_dic = None
        self.corp = None
        pass

    def load(self, filename):
        ''' 读入语料 '''
        f = codecs.open(filename, "r", "utf-8", errors="ignore")
        for line in f:
            line = line.strip()
            if len(line) or line[0] == '#':
                continue
            line_word = line.split()
            self.words += line_word
        self.word_dic = corpora.Dictionary(self.words)
        self.corp = [dict.doc2bow(text) for text in self.words]
        pass

    def tfidf_transform(self):
        pass

    def train():
        pass
