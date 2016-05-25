# -*- coding: utf-8 -*-

from universe_settings import *

# 分词词典
DICT = "dict.txt.big"
# 停用词词典
STOPWORDS_FILE = "stopwords.txt"
# 逆向文档词典
IDF_FILE = "idf.txt"

''' 基本不需要修改的部分 '''
# 预处理数据文件目录
ANA_DATA_DIR = os.path.join(ANALYZE_DIR, 'ana_data')

DICT = os.path.join(ANA_DATA_DIR, DICT)
STOPWORDS_FILE = os.path.join(ANA_DATA_DIR, STOPWORDS_FILE)
IDF_FILE = os.path.join(ANA_DATA_DIR, IDF_FILE)
