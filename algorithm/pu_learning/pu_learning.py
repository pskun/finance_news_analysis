#encoding=utf8

import sys
import time
import codecs
import numpy as np
from scipy.sparse import coo_matrix, vstack
from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
from scipy.stats import entropy
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from pu_learning_adapter import PUAdapter

################# 全局训练参数设置 #######################
##########################################################
''' PU Learning的分类器 '''
''' Logistic Regression '''
from sklearn.linear_model import LogisticRegression
base_estimator = LogisticRegression(
    penalty='l2',
    C=0.5,
    fit_intercept=True,
    class_weight='balanced',
    max_iter=20,
    solver='sag',
    tol=0.005,
    verbose=1,
    n_jobs=8
)

''' adaboost '''
from sklearn.tree import DecisionTreeClassifier
dt_stump = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=1,
    min_samples_leaf=1,
    class_weight='balanced',
)
from sklearn.ensemble import AdaBoostClassifier
base_estimator = AdaBoostClassifier(
    base_estimator=dt_stump,
    n_estimators=200,
    learning_rate=0.5,
    algorithm='SAMME'
)

''' PU Learning的迭代次数 '''
n_pu_iter = 10
n_selected = 1000

''' PU learning模型的hold_out比例 '''
hold_out_ratio = 0.1
''' 初始的判断为正例的概率阈值 '''
start_positive_threshold = 0.9

''' 模型存储文件名 '''
vectors_save_name = "all_data.vectors.20170526"
##########################################################

# load word2vec model and construct word vectors for each sentence
import word2vec
print "start loading word2vec model..."
t1 = time.time()
w2v_model = word2vec.load("../biz_title_word.bin")
t2 = time.time()
sys.stderr.write("Model loading time: %.4fs\n" % (t2 - t1))
t1 = time.time()
f = codecs.open('all_data.output', encoding='utf-8', errors='ignore')
X = []
y = []
titles = []
print "start construct vectors of each title"
for line in f:
    try:
        label, title, segment = line.strip().split("\t")
    except:
        continue
    v = np.zeros(200)
    cnt = 0
    for w in segment:
        try:
            wv = w2v_model.get_vector(w)
            v = v + wv
            cnt += 1
        except:
            continue
    if cnt == 0:
        continue
    v = v / cnt
    y.append(int(label))
    titles.append(title)
    X.append(v)
del w2v_model
t2 = time.time()
sys.stderr.write("Vector Constructing time: %.4fs\n" % (t2 - t1))

# transform data to fit model
# 转换数据的类型以适合训练
y_with_pu = np.copy(y)
y_with_pu[np.where(y_with_pu == 0)] = -1
X = np.asarray(X)


print "start pu learning...\n"
adapter = PUAdapter(base_estimator, hold_out_ratio=hold_out_ratio, precomputed_kernel=False)
for epoch in range(1, n_pu_iter+1):
    print "epoch %d:" % epoch
    n_samples = len(y_with_pu) * 1.0
    n_positives = len(np.where(y_with_pu == 1)[0])
    n_negatives = n_samples - n_positives
    print "Training set contains %d examples." % n_samples
    print "positive num: %d" % n_positives
    print "negative num: %d" % n_negatives
    priori_prob = [n_negatives / n_samples, n_positives / n_samples]
    print "start training estimator..."
    adapter.fit(X, y_with_pu)
    c = adapter.c
    recall = adapter.hold_out_recall
    print "hold_out mean probility: %.4f" % c
    print "hold_out recall: %.4f" % recall
    y_pred_prob = adapter.predict_proba(X)
    y_pred = adapter.predict(X)
    sys.stdout.write(classification_report(y_with_pu, y_pred, digits=4))
    print "start changing labels...\n\n"
    change_pos_indices = []
    change_neg_indices = []
    threshold = min(start_positive_threshold, priori_prob)
    for i in range(len(y_with_pu)):
        if y_with_pu[i] != 1 and y_pred_prob[i] > threshold:
            change_pos_indices.append(i)
        if y_with_pu[i] != -1 and y_pred_prob[i] < (1 - threshold) / 2:
            change_neg_indices.append(i)
    y_with_pu[change_pos_indices] = 1
    y_with_pu[change_neg_indices] = -1

t1 = time.time()
# dump_svmlight_file(X, y_with_pu, vectors_save_name)
# title_file = codecs.open('vectors_titles', mode='w', encoding='utf8', errors='ignore')
# title_file.writelines(["%s\n" % item  for item in titles])
X_train, X_test, y_train, y_test, title_train, title_test = train_test_split(X, y_with_pu, titles, test_size=0.2)
dump_svmlight_file(X_train, y_train, "vectors_train_data")
dump_svmlight_file(X_test, y_test, "vectors_test_data")
title_train_file = codecs.open('vectors_title_train', mode='w', encoding='utf8', errors='ignore')
title_test_file = codecs.open('vectors_title_test', mode='w', encoding='utf8', errors='ignore')
title_train_file.writelines(["%s\n" % item  for item in title_train])
title_test_file.writelines(["%s\n" % item  for item in title_test])
t2 = time.time()
sys.stderr.write("Vector dumping time: %.4fs\n" % (t2 - t1))