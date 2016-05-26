# encoding=utf-8

import codecs
import jieba
import jieba.analyse
import esm


class KeywordExtractor(object):
    ''' 关键词抽取类
        支持给定关键词、TFIDF关键词和Textrank关键字的抽取
    '''
    def __init__(self):
        self.given_words_indexs = {}
        self.words_idf = None
        pass

    def initGivenKeywords(
            self, keyword_type, filename=r'', given_words_list=None):
        ''' 初始给定的关键词
            可以初始多个文件
        '''
        given_words_index = esm.Index()
        words_list = None
        if len(filename) > 0:
            words_list = [word.strip()
                          for word in codecs.open(filename, 'r', 'utf-8')]
        if words_list is None and given_words_list is not None:
            words_list = given_words_list
        for word in words_list:
            word = word.encode('utf-8')
            given_words_index.enter(word)
        given_words_index.fix()
        self.given_words_indexs[keyword_type] = given_words_index
        pass

    def extractGivenKeywords(self, doc_str):
        ''' 从一个字符串中抽取给定的关键词
            给定关键词需要预先初始化
            抽取给定关键词使用的是AC自动机算法
            参考: http://www.cppblog.com/mythit/archive/2009/04/21/80633.html
        '''
        doc_str = doc_str.encode('utf-8')
        all_type_keywords = {}
        for keyword_type in self.given_words_indexs:
            keywords = {}
            given_words_index = self.given_words_indexs[keyword_type]
            for word in given_words_index.query(doc_str):
                word = word[1].decode('utf-8')
                if word not in keywords:
                    keywords[word] = 1
                else:
                    keywords[word] = keywords[word] + 1
            all_type_keywords[keyword_type] = keywords
        return all_type_keywords
        pass

    def extarctTextRankKeywords(self, doc_str, window=5):
        ''' 使用TextRank算法提取关键词
            参考: http://www.letiantian.me/2014-12-01-text-rank/
        '''
        keywords = jieba.analyse.textrank(doc_str, withWeight=True)
        return keywords
        pass

    def initTfidfKeywords(self, idf_file=None):
        ''' 使用TFIDF关键词抽取算法时，需要先初始化IDF文件 '''
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
    pass


if __name__ == '__main__':
    main()
