# -*- coding: utf-8 -*-

from universe_settings import *

# 分词词典
DICT = "dict.txt.big"
# 停用词词典
STOPWORDS_FILE = "stopwords.txt"
# 逆向文档词典
IDF_FILE = "idf.txt"
# 新闻分词后生成的文件
NEWS_WORDS_FILE = 'news_words.txt'
# 新闻分字后生成的文件
NEWS_LETTER_FILE = 'news_letter.txt'

''' 分析模型文件 '''
# word2vec文件
WORD2VEC_MODEL = "word2vec.model"
# LDA文件
LDA_MODEL = "lda.model"

''' 基本不需要修改的部分 '''
# 预处理数据文件目录
ANA_DATA_DIR = os.path.join(ANALYZE_DIR, 'ana_data')

DICT = os.path.join(ANA_DATA_DIR, DICT)
STOPWORDS_FILE = os.path.join(ANA_DATA_DIR, STOPWORDS_FILE)
IDF_FILE = os.path.join(ANA_DATA_DIR, IDF_FILE)
NEWS_WORDS_FILE = os.path.join(ANA_DATA_DIR, NEWS_WORDS_FILE)
NEWS_LETTER_FILE = os.path.join(ANA_DATA_DIR, NEWS_LETTER_FILE)
WORD2VEC_MODEL = os.path.join(ANA_DATA_DIR, WORD2VEC_MODEL)
LDA_MODEL = os.path.join(ANA_DATA_DIR, LDA_MODEL)
