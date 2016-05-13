# encoding=utf-8

import re
import codecs
import jieba

from analyze_settings import STOPWORDS_FILE


# 待去除的标点符号
PUNCT = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

# 设置分句的标志符号；可以根据实际需要进行修改
SENTENCE_CUT_LIST = u'。|！|？|；|!|;|\?'

STOP_WORDS = None


def sentence_split(str_doc):
    ''' 进行分句的函数 '''
    sentences = re.split(SENTENCE_CUT_LIST, str_doc)
    ss = [s.strip() for s in sentences]
    return ss


def word_segment(line, stop=False):
    '''
    进行分词的函数
    stop 是否去停用词
    '''
    if STOP_WORDS is None:
        load_stopwords()
    seg_list = jieba.cut(line, HMM=True)
    sl = []
    for word in seg_list:
        word = word.strip()
        if len(word) > 0 and word not in PUNCT:
            if stop:
                if word not in STOP_WORDS:
                    sl.append(word)
            else:
                sl.append(word)
    return sl


def doc_word_segment(unicode_doc, stop=False):
    '''
    文档级分词，返回列表的列表
    一级列表是sentences，二级列表是words
    stop：是否去停用词
    '''
    sentences = sentence_split(unicode_doc)
    doc_seg = [word_segment(s, stop) for s in sentences]
    return doc_seg


def load_stopwords():
    ''' 加载停用词 '''
    global STOP_WORDS
    STOP_WORDS = set([line.strip()
                      for line in codecs.open(STOPWORDS_FILE, 'r', 'utf-8')])
    pass
