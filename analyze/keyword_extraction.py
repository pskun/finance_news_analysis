# encoding=utf-8

import codecs
import jieba
import jieba.analyse
import esm

from analyze_settings import IDF_FILE


class KeywordExtractor(object):
    def __init__(self):
        self.given_words_indexs = {}
        self.words_idf = None
        pass

    def initGivenKeywords(
            self, keyword_type, filename=r'', given_words_list=None):
        given_words_index = esm.Index()
        words_list = None
        if len(filename) > 0:
            words_list = [word.strip()
                          for word in codecs.open(filename, 'r', 'utf-8')]
        if words_list is None and given_words_list is not None:
            words_list = given_words_list
        for word in words_list:
            # word = word.encode('utf-8')
            given_words_index.enter(word)
        given_words_index.fix()
        self.given_words_indexs[keyword_type] = given_words_index
        pass

    def extractGivenKeywords(self, doc_str):
        all_type_keywords = {}
        for keyword_type in self.given_words_indexs:
            keywords = {}
            given_words_index = self.given_words_indexs[keyword_type]
            for word in given_words_index.query(doc_str):
                word = word[1]
                if word not in keywords:
                    keywords[word] = 1
                else:
                    keywords[word] = keywords[word] + 1
            all_type_keywords[keyword_type] = keywords
        return all_type_keywords
        pass

    def extarctTextRankKeywords(self, doc_str, window=5):
        keywords = jieba.analyse.textrank(doc_str, withWeight=True)
        return keywords
        pass

    def initTfidfKeywords(self, idf_file=None):
        self.words_idf = {}
        if idf_file is not None:
            jieba.analyse.set_idf_path(idf_file)
            '''
            for line in codecs.open(idf_file, 'r', 'utf-8'):
                word, idf_value = line.strip().split()
                self.words_idf[word] = float(idf_value)
            pass
            '''
        pass

    def extractTfidfKeywords(self, doc_str):
        keywords = jieba.analyse.extract_tags(doc_str, withWeight=True)
        return keywords
        pass


def main():
    extractor = KeywordExtractor()
    extractor.initTfidfKeywords(idf_file=IDF_FILE)
    for line in 
    pass


if __name__ == '__main__':
    main()
