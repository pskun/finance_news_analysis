#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import random
import multiprocessing
import logging

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

reload(sys)
sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

WORD2VEC_INDEX = 2
CPU_COUNT = multiprocessing.cpu_count()
WORD2VEC_LIST = [
    (0, 'word2vec/whispers_SG_s400_w5_m5.word2vec',
     Word2Vec(size=400, window=5, min_count=5, workers=CPU_COUNT)),
    (1, 'word2vec/whispers_SG_s800_w6_m5_n3_s1e5.word2vec', Word2Vec(sg=1, size=800,
                                                                     window=6, min_count=5, negative=3, sample=0.001, hs=1, workers=CPU_COUNT)),
    (2, 'word2vec/whispers_CBOW_s800_w3_m5_n3_s1e3.word2vec', Word2Vec(sg=0, size=800,
                                                                       window=3, min_count=5, negative=3, sample=0.001, hs=1, workers=CPU_COUNT)),
]


def train(model, sentences, output_file='test.word2vec', train_sentences=None):
    model.build_vocab(sentences)
    if train_sentences:
        model.train(train_sentences)
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


def test_model(word_file, output_file):
    model = Word2Vec.load(output_file)
    print "# %s %s" % (model, output_file)
    for line in file(word_file):
        word = line.strip().decode('utf8')
        print ">>> %s" % (word)
        try:
            for w, s in model.most_similar(word):
                print "%.6f %s" % (s, w)
        except:
            print "[WARN] low-frequency word"


def main():
    (index, output_file, model) = WORD2VEC_LIST[WORD2VEC_INDEX]
    sentences = LineSentence('data/whispers.default_hmm.cut')

    if not os.path.exists(output_file):
        train_sentences = LineSentence('data/whispers.default_hmm.random.cut')
        train(model, sentences, output_file, train_sentences)
    else:
        # test_model_random(sentences, output_file)
        test_model('data/exam_words.txt', output_file)

if __name__ == '__main__':
    main()
