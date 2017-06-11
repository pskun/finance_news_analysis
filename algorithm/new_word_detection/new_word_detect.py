
# coding: utf-8

import os
import codecs
import math

####################################
'''
Usage:
'''
####################################

data_dir = ""


single_count_filename = os.path.join(data_dir, 'maybe_clickbait_word.count')
single_count_file = codecs.open(single_count_filename, encoding='utf8', errors='ignore')


single_word_count = dict()


for line in single_count_file:
    line = line.strip()
    res = line.split("\t")
    if len(res) < 2: continue
    word, count = res[0], int(res[1])
    if(count < 3): continue
    single_word_count[word] = count

double_count_filename = os.path.join(data_dir, 'maybe_clickbait_word_double.count')
double_count_file = codecs.open(double_count_filename, encoding='utf8', errors='ignore')


double_word_count = dict()


for line in double_count_file:
    line = line.strip()
    res = line.split("\t")
    if len(res) < 2: continue
    word, count = res[0], int(res[1])
    # if(count < 5): continue
    double_word_count[word] = count

all_word_count = 10261112.0


new_word_candidates = dict()


kw_candidates = codecs.open(os.path.join(data_dir, 'maybe_clickbait_word_double.candidate'), mode='w', encoding="utf-8")


avg_pmi = 0
for double_word, freq_w1w2 in double_word_count.iteritems():
    res = double_word.split()
    if len(res) != 2: continue
    w1, w2 = res[0], res[1]
    freq_w1 = single_word_count.get(w1, 0)
    freq_w2 = single_word_count.get(w2, 0)
    if freq_w1 * freq_w2 == 0: continue
    pmi = math.log(float(freq_w1w2) / (freq_w1 * freq_w2) * all_word_count)
    if pmi >= 0.5 and freq_w1w2 >= 10:
        kw_candidates.write("%s%s\n" % (w1, w2))
        print "%s%s" % (w1, w2)
        #new_word_candidates[double_word] = pmi
        pass
    avg_pmi += pmi

right_entropy_dict = dict()
left_entropy_dict = dict()

def calculate_left_right_entropy(union_occur_filename, single_word_count):
    ent_dict = dict()
    ent_filename = os.path.join(data_dir, union_occur_filename)
    ent_file = codecs.open(ent_filename, encoding='utf8', errors='ignore')
    last_word = None
    last_word_freq = 0
    ent_val = 0.0
    for line in ent_file:
        if last_word != None and (0 - ent_val > 1e-5):
            ent_dict[last_word] = -1 * ent_val
            ent_val = 0.0
            last_word_freq = 0
            last_word = None
        line = line.strip()
        res = line.split("\t")
        if len(res) != 3: continue
        word, next_word, count = res[0], res[1], float(res[2])
        if last_word is None and word not in single_word_count: continue
        if last_word is None:
            last_word = word
            last_word_freq = single_word_count[last_word]
        prob = count / last_word_freq
        ent_val += prob * math.log(prob)
    return ent_dict


right_ent = calculate_left_right_entropy('right_occur_count', single_word_count)
left_ent = calculate_left_right_entropy('left_occur_count', single_word_count)

# 词的左右熵
output = codecs.open(os.path.join(data_dir, "kw_candidates_score"), encoding='utf-8', mode='w', errors='ignore')
for word in kw_candidates:
    if word not in single_word_count:
        output.write("%s\t0\t0\t0\n" % word)
    else:
        le = left_ent.get(word, 0)
        re = right_ent.get(word, 0)
        output.write("%s\t%d\t%f\t%f\n" % (word, single_word_count[word], le, re))

# 词段的左右熵
# cat nickname_cut | awk '{if(NF>=3) for(i=3; i<=NF; i++) print $(i-2)" "$(i-1)" "$i}' > nickname_triple_word
# cat nickname_triple_word | sort | uniq -c | awk '{print $2" "$3" "$4"\t"$1}' > nickname_triple_word_count
# cat nickname_triple_word_count | sort -t $'\t' -k 1,1 | awk '{print $1" "$2"\t"$3"\t"$4}' > double_right_occur_count &
# cat nickname_triple_word_count | awk '{$2" "$3"\t"$1"\t"$4}' | sort -t $'\t' -k 1,1 | > double_left_occur_count &
segment_right_entropy_dict = dict()
segment_left_entropy_dict = dict()


segment_right_entropy_dict = calculate_left_right_entropy('double_right_occur_count', double_word_count)


segment_left_entropy_dict = calculate_left_right_entropy('double_left_occur_count', double_word_count)

# 给出最终的新词
# score = pmi - min(h_r_l, h_l_r) + min(h_l, h_r)
# pmi: 点间互信息越高，内部聚合程度越高

# min(h_r_l, h_l_r): 两个单词片段信息熵 h_r_l 和 h_l_r 的最小值，这个数值越大，则意味着两个单词一起出现的可能性越小
# min(h_l, h_r): 单词左右信息熵的最小值，这个数值越大就表示着候选词出现的语境越多，越有可能成词
new_word_output = codecs.open(os.path.join(data_dir, "public_service_new_word_score"), encoding='utf-8', mode='w', errors='ignore')
for word_candidate, pmi in new_word_candidates.iteritems():
    segment_lr_ent = min(segment_left_entropy_dict.get(word_candidate, 0), segment_right_entropy_dict.get(word_candidate, 0))
    w1, w2 = word_candidate.split()
    word_lr_ent = min(right_ent.get(w1, 0), left_ent.get(w2, 0))
    score = pmi - word_lr_ent + segment_lr_ent
    new_word_output.write("%s %s\t%f\n" % (w1, w2, score))
new_word_output.close()
