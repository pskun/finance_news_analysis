import numpy as np

class CoForest(object):
    
    def __init__(self, base_estimator, num_classifiers, num_features, num_kvalue, threshold, random_seed=None):
        self.base_estimator = base_estimator
        self.num_classifiers = num_classifiers
        self.num_features = num_features
        self.num_kvalue = num_kvalue
        self.threshold = threshold
        self.random_seed = random_seed
        self.classifiers = []
        pass
    
    def resample_with_weights(self, data_weights, is_sampled):
        new_data_indices = []
        
        num_samples = data_weights.shape[0]
        new_weights = np.copy(data_weights)
        probabilities = np.random.rand(num_samples)
        sum_probs = np.sum(probabilities)
        probabilities = np.cumsum(probabilities)
        sum_weights = np.sum(data_weights)
        probabilities = probabilities / (sum_probs / sum_weights)
        probabilities[-1] = sum_weights
        
        k = 0, l = 0
        sum_probs = 0
        while k < num_samples and l < num_samples:
            if new_weights[i] < 0:
                raise Exception("Weights have to be positive.")
            sum_probs += new_weights[i]
            while k < num_samples and probabilities[k] <= sum_probs:
                new_data_indices.append(l)
                is_sampled[l] = True
                k = k + 1
            l = l + 1
        
        return new_data_indices
    
    def distribution_for_instance(instance, num_classes):
        res = np.zeros(num_classes)
        for classifier in self.classifiers:
            distr = classifier.predict_proba(instance)
            res = res + distr
        sum_res = np.sum(res)
        res = res / sum_res
        return res
    
    def classify_instance(instance):
        distr = self.distribution_for_instance(instance)
        return np.argmax(distr)
    
    def build_classifier(labeled, unlabeled):
        err = np.zeros(self.num_classifiers)
        err_prime = np.zeros(self.num_classifiers)
        s_prime = np.zeros(self.num_classifiers)
        
        inbags = [None] * self.num_classifiers
        
        np.random.seed(self.m_seed)
        
        num_original_labeled_insts = labeled.shape[0]
        
        # set up the random tree options
        self.num_kvalue = self.num_features
        if self.num_kvalue < 1:
            self.num_kvalue = int(np.log2(labeled.shape[1])) + 1
        self.estimator = self.estimator.set_params(**{"max_features": self.m_kvalue})
        
        pass