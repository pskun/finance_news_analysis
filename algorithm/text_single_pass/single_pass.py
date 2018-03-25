#encoding=utf8
import numpy as np
import time
import codecs
import sys
import heapq
import argparse

################################################
# Custom Class
################################################
class ClusterIndex(object):
    def __init__(self, true_index, cluster_info_list):
        self.true_index = 0
        self.cluster_info_list = cluster_info_list

    def __cmp__(self, other):
        if self.cluster_info_list[self.true_index] < self.cluster_info_list[other.true_index]:
            return -1
        elif self.cluster_info_list[self.true_index] > self.cluster_info_list[other.true_index]:
            return 1
        else:
            return 0

class ClusterInfo(object):
    def __init__(self, cluster_centroid_vector, original_data_id, cluster_final_idx):
        self.cluster_centroid_vector = cluster_centroid_vector
        self.cluster_size = 1
        self.original_data_id = original_data_id
        self.cluster_final_idx = cluster_final_idx

    def __cmp__(self, other):
        # self < other, return -1
        # self == other, return 0
        # self > other, return 1
        if self.cluster_size < other.cluster_size:
            return -1
        elif self.cluster_size > other.cluster_size:
            return 1
        elif self.original_data_id < other.original_data_id:
            return -1
        elif self.original_data_id > other.original_data_id:
            return 1
        else:
            return 0

class SimpleInvertedIndex(object):
    def __init__(self):
        self.word2index = {}
        self.next_word_index = 0
        self.index2doc = []
        self.doc_words = {}

    def insert(self, words, doc_id):
        # 映射word到一个索引的下标
        for word in words:
            index = self.word2index.get(word, -1)
            if index < 0:
                self.word2index[word] = self.next_word_index
                self.index2doc.append(set())
                self.next_word_index += 1
            # 建立索引和文档的关系
            doc_set = self.index2doc[index].add(doc_id)
            self.doc_words[doc_id] = set(words)
        pass

    def delete(self, doc_id):
        # 找到doc对应的words
        cur_doc_words = self.doc_words.get(doc_id, None)
        if cur_doc_words is None:
            return
        # 对每个word删除在索引表中的项
        for word in cur_doc_words:
            index = self.word2index.get(word, -1)
            if index >= 0:
                try:
                    self.index2doc[index].remove(doc_id)
                except:
                    continue
        pass

    def find_most_common_doc(self, words):
        # 找不到返回-1
        doc_occurrence_count = {}
        for word in words:
            index = self.word2index.get(word, -1)
            if index >= 0:
                doc_set = self.index2doc[index]
                for doc_id in doc_set:
                    doc_count = doc_occurrence_count.get(doc_id, -1)
                    if doc_count < 0: doc_occurrence_count[doc_id] = 0
                    doc_occurrence_count[doc_id] += 1
        if len(doc_occurrence_count) == 0:
            return -1
        else:
            # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
            return max(doc_occurrence_count, key=doc_occurrence_count.get)

################################################
# Custom Function
################################################
def read_data(path):
    ''' 读入以空格分割的doc list，一行表示一个doc，doc以utf8形式编码 '''
    texts = []
    f = codecs.open(path, encoding='utf8', errors='ignore')
    for line in f:
        line = line.rstrip()
        values = line.split()
        texts.append(values)
    return texts

def hard_jaccard_from_two_sets(set1, set2):
    return float(len(set1 & set2)) / max(len(set1), len(set2)) 
    
def do_single_pass(texts, capacity, threshold):
    processed = [(0, 0)]
    available_cluster_list = []
    available_cluster_heap = []
    next_cluster_id = 1

    total_line_num = len(texts)
    print "total samples:", total_line_num
    print "cluster capacity:", capacity
    print "similarity threshold: ", threshold
    if total_line_num <= 0:
        return []

    initial_text_set = set(texts[0])
    cluster_info = ClusterInfo(initial_text_set, 0, 0)
    available_cluster_list.append(cluster_info)
    available_cluster_heap.append(ClusterIndex(0, available_cluster_list))
    inverted_index = SimpleInvertedIndex()
    inverted_index.insert(initial_text_set, 0)

    t1 = time.time()
    for i in range(1, len(texts)):
        if i % 100 == 0:
            print "Process %.2f%%, cluster count: %d\r" % (float(i) / total_line_num * 100, next_cluster_id),
            sys.stdout.flush()
            pass
        cur_text_set = set(texts[i])
        # 查找倒排索引，找到最相似的类
        most_similar_cluster_id = inverted_index.find_most_common_doc(cur_text_set)
        max_similarity_score = 0
        if most_similar_cluster_id >= 0:
            most_similar_centroid_vector = available_cluster_list[most_similar_cluster_id].cluster_centroid_vector
            max_similarity_score = hard_jaccard_from_two_sets(cur_text_set, most_similar_centroid_vector)
        # 如果最相似的分数大于阈值，加入该类
        if max_similarity_score >= threshold:
            processed.append((i, available_cluster_list[most_similar_cluster_id].cluster_final_idx))
            # 如果当前的代表向量的word个数大于中心代表向量，则替换中心向量为当前向量
            if len(cur_text_set) > len(most_similar_centroid_vector):
                available_cluster_list[most_similar_cluster_id].original_data_id = i
                available_cluster_list[most_similar_cluster_id].cluster_centroid_vector = cur_text_set
            available_cluster_list[most_similar_cluster_id].cluster_size += 1
        # 不然的话，自成一类
        else:
            processed.append((i, next_cluster_id))
            # 如果聚类数大于最大聚类容量，则丢弃类别个数最少的且最久未用的类
            true_cluster_index = len(available_cluster_list)
            if true_cluster_index >= capacity:
                cluster_index = heapq.heappop(available_cluster_heap)
                true_cluster_index = cluster_index.true_index
                inverted_index.delete(true_cluster_index)
            # 插入到堆中
            cluster_info = ClusterInfo(cur_text_set, i, next_cluster_id)
            if true_cluster_index == len(available_cluster_list):
                available_cluster_list.append(cluster_info)
            else:
                available_cluster_list[true_cluster_index] = cluster_info
            cluster_index = ClusterIndex(true_cluster_index, available_cluster_list)
            heapq.heappush(available_cluster_heap, cluster_index)
            inverted_index.insert(cur_text_set, true_cluster_index)
            next_cluster_id += 1
    t2 = time.time()
    print "\ntotal cluster:", (next_cluster_id - 1)
    print "total time: %.2fs" % (t2 - t1)

    return processed

def output_to_file(output_path, processed):
    processed = [item[1] for item in processed]
    np.savetxt(fname=output_path, X=processed, delimiter="", fmt="%d")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rapid text clustering using single-pass algorithm.')
    parser.add_argument("-i", "--input", dest="input_path", required=True, help="input text path")
    parser.add_argument("-o", "--output", dest="output_path", required=True, help="output class infomation corresponding to input texts")
    parser.add_argument("-c", "--capacity", dest="cluster_capacity", type=int, default=5000, help="max retaining cluster size")
    parser.add_argument("-t", "--threshold", dest="similar_threshold", type=float, default=0.7, help="similarity threshold while regarding two texts as the same class")
    args = parser.parse_args()

    texts = read_data(args.input_path)
    processed = do_single_pass(texts, args.cluster_capacity, args.similar_threshold)
    output_to_file(args.output_path, processed)
    pass