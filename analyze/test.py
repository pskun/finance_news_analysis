# -*- coding: utf-8 -*-

import os
import sys
import json
import codecs

from universe_settings import *
from analyze_settings import *
import word_segment
from keyword_extraction import KeywordExtractor
import word2vec

reload(sys)
sys.setdefaultencoding('utf8')


def doc_segment():
    field_name = 'content'
    filename = CRAWL_FILE_NAMES[TYPE_NEWS][WEBSITE_EASTMONEY]
    f = codecs.open(filename, 'r', 'utf-8', errors='ignore')
    out = codecs.open(os.path.join(ANA_DATA_DIR, 'words.txt'), 'wb', 'utf-8')
    for line in f:
        try:
            data = json.loads(line.strip())
            content = data.get(field_name)
            if content is not None:
                doc_words = word_segment.doc_word_segment(content, stop=True)
                for sentences in doc_words:
                    line = " ".join(sentences)
                    out.write(line + '\n')
        except:
            continue
    pass


def processIDF():
    doc_file = CRAWL_FILE_NAMES[TYPE_NEWS][WEBSITE_EASTMONEY]
    idf_file = IDF_FILE
    file = codecs.open(doc_file, 'r', 'utf-8', errors='ignore')
    tfidf = TFIDFTransformer()
    i = 0
    for line in file:
        i = i + 1
        print i
        try:
            data = json.loads(line.strip())
            content = data.get('content')
            if content is not None:
                tfidf.addDocument(content)
        except:
            continue
    tfidf.calculateIDF()
    tfidf.dumpIDFDict(idf_file)
    tfidf.clear()
    pass


def extract_keyword():
    doc_file = CRAWL_FILE_NAMES[TYPE_NEWS][WEBSITE_EASTMONEY]
    idf_file = IDF_FILE
    extractor = KeywordExtractor()
    extractor.initTfidfKeywords(idf_file)
    file = codecs.open(doc_file, 'r', 'utf-8', errors='ignore')
    for line in file:
        try:
            data = json.loads(line.strip())
            content = data.get('content')
            url = data['url']
            if content is not None:
                print "\n# " + url
                print "TF-IDF"
                keywords = extractor.extractTfidfKeywords(content)
                for item in keywords:
                    print "%s\t%f" % (item[0], item[1])
                print "# Textrank"
                keywords = extractor.extarctTextRankKeywords(content)
                for item in keywords:
                    print "%s\t%f" % (item[0], item[1])
        except:
            continue
    pass


def word2vec_train():
    # Gensim的word2vec的输入是句子的序列. 每个句子是一个单词列表
    sentences = word2vec.Word2vecSentence(
        os.path.join(ANA_DATA_DIR, 'words.txt'))
    word2vec.train(sentences)
    '''
    if not os.path.exists(output_file):
        train_sentences = LineSentence('data/whispers.default_hmm.random.cut')
        train(model, sentences, output_file, train_sentences)
    else:
        # test_model_random(sentences, output_file)
        test_model('data/exam_words.txt', output_file)
    '''
    pass


def word2vec_test():
    word2vec.test_model(os.path.join(ANA_DATA_DIR, 'word2vec_test_word.txt'))

if __name__ == '__main__':
    word2vec_test()
