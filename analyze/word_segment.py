# encoding=utf-8

import re
import json
import codecs
import jieba
import traceback

from analyze_settings import STOPWORDS_FILE, DICT
from utils.threadpool import Handler, ThreadPool
from utils.file_operator import FileMultiReadWrite
from utils import util_func

# 待去除的标点符号
PUNCT = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

# 设置分句的标志符号；可以根据实际需要进行修改
SENTENCE_CUT_LIST = u'。|！|？|；|!|;|\?'
# 设置词典
jieba.set_dictionary(DICT)
STOP_WORDS = None


def sentence_split(str_doc):
    ''' 进行分句的函数 '''
    sentences = re.split(SENTENCE_CUT_LIST, str_doc)
    ss = [s.strip() for s in sentences]
    return ss


def word_segment(line, stop=False, remain_number=True):
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
                if word in STOP_WORDS:
                    word = None
            if word is not None and not remain_number:
                if util_func.atof(word) is not None:
                    word = None
            if word is not None:
                sl.append(word)
    return sl


def chinese_letter_segment(
        line, stop=False, remain_digit=True, remain_char=True):
    ''' 进行分字的函数
    stop 是否去掉停用字
    '''
    letter_list = []
    if STOP_WORDS is None:
        load_stopwords()
    for letter in line:
        letter = letter.strip()
        if len(letter) == 0 or letter in PUNCT:
            continue
        if stop and letter in STOP_WORDS:
            continue
        if not remain_digit and letter.isdigit():
            continue
        '''
        if not remain_char and letter.isalpha():
            continue
        '''
        letter_list.append(letter)
    return letter_list


def doc_word_segment(unicode_doc, stop=False, remain_number=True):
    '''
    文档级分词，返回列表的列表
    一级列表是sentences，二级列表是words
    stop：是否去停用词
    '''
    sentences = sentence_split(unicode_doc)
    doc_seg = [word_segment(s, stop, remain_number) for s in sentences]
    return doc_seg


def doc_letter_segment(
        unicode_doc, stop=False, remain_digit=True, remain_char=True):
    '''
    文档级分字，返回列表的列表
    一级列表是sentences，二级列表是letters
    这里的字是中文字
    stop：是否去停用词
    '''
    sentences = sentence_split(unicode_doc)
    doc_seg = [chinese_letter_segment(
        s, stop, remain_digit, remain_char) for s in sentences]
    return doc_seg


def load_stopwords():
    ''' 加载停用词 '''
    global STOP_WORDS
    STOP_WORDS = set([line.strip()
                      for line in codecs.open(STOPWORDS_FILE, 'r', 'utf-8')])
    pass


def text_word_segment_multithread(
        filename, ouput_filename, thread_num=20, level='word'):
    ''' 多线程文档分词 '''
    output_file = FileMultiReadWrite(ouput_filename, "wb")
    pool = ThreadPool(thread_num)
    # 使用线程池
    for i in range(thread_num):
        handler = WordSegmentHandler(output_file=output_file, level=level)
        pool.add_handler(handler)
    pool.startAll()
    # 打开新闻爬虫文件
    f = codecs.open(filename, 'r', 'utf-8', errors='ignore')
    if f is None:
        return
    for line in f:
        try:
            line = line.strip().replace(u'\xa0', u' ')
            data_item = json.loads(line)
            if data_item is not None:
                pool.add_process_data(data_item)
        except:
            traceback.print_exc()
            continue
    pool.wait_completion()
    output_file.close()
    pass


class WordSegmentHandler(Handler):

    def __init__(self, output_file=None, level='word'):
        '''
        level: 分词粒度：
            word（分词）, letter（分字）, sentence（分句）
        '''
        self.output_file = output_file
        self.level = level
        pass

    def before_thread_start(self):
        ''' 回调函数: 线程启动前调用 '''
        load_stopwords()
        pass

    def init_handler(self):
        ''' 回调函数: 线程启动后立马调用该方法 '''
        pass

    def process_function(self, data_item):
        ''' 回调函数: 从任务队列中取出一个数据进行处理 '''
        url = data_item['url']
        # print url
        content = data_item['content']
        doc_words = None
        if self.level == 'word':
            doc_words = doc_word_segment(
                content, stop=True, remain_number=False)
        elif self.level == 'letter':
            doc_words = doc_letter_segment(
                content, stop=True, remain_digit=False, remain_char=False)
        if doc_words is None:
            return
        line = "# " + url + "\n"
        for sentences in doc_words:
            line += " ".join(sentences) + "\n"
        self.output_file.write(line)
        pass

    def clear_handler(self):
        ''' 回调函数: 线程结束前调用 '''
        pass
