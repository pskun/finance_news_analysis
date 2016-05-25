# -*- coding: utf-8 -*-

import sys
import json

from keyword_extraction import KeywordExtractor
from universe_settings import *
from data.data_settings import *
from analyze_settings import *


reload(sys)
sys.setdefaultencoding('utf8')


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

if __name__ == '__main__':
    extract_keyword()
