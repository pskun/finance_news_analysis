#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import codecs
import random
import multiprocessing
import logging

from gensim.models import Word2Vec

reload(sys)
sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

CPU_COUNT = multiprocessing.cpu_count()


class Word2vecSentence(object):

    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        f = codecs.open(self.filename, 'r', 'utf-8', errors='ignore')
        for line in f:
            yield line.strip().split()
        pass


def train(sentences, output_file='test.word2vec'):
    model = Word2Vec(sentences, size=300, window=10, workers=CPU_COUNT)
    # model.save_word2vec_format(output_file)
    model.save(output_file)
    return model


def test_model_random(sentences, output_file):
    # model = Word2Vec.load_word2vec_format(output_file, binary=False)
    model = Word2Vec.load(output_file)
    list_sentences = list(sentences)
    for i in range(10):
        sentence = random.choice(list_sentences)
        while len(sentence) < 3:
            sentence = random.choice(list_sentences)

        word = random.choice(sentence)
        print ">>> %s: %s" % (word, "".join(sentence))
        try:
            for w, s in model.most_similar(word):
                print "%.6f %s" % (s, w)
        except:
            print "[WARN] low-frequency word"


def test_model(word_file, model_file='test.word2vec'):
    model = Word2Vec.load(model_file)
    for line in codecs.open(word_file, 'r', 'utf-8'):
        word = line.strip()
        print ">>> %s" % (word)
        try:
            for w, s in model.most_similar("10"):
                print "%.6f %s" % (s, w)
        except:
            print "[WARN] low-frequency word"
