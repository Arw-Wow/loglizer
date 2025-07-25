#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' This is a demo file for the PCA model.
    API usage:
        dataloader.load_HDFS(): load HDFS dataset
        feature_extractor.fit_transform(): fit and transform features
        feature_extractor.transform(): feature transform after fitting
        model.fit(): fit the model
        model.predict(): predict anomalies on given data
        model.evaluate(): evaluate model accuracy with labeled data
'''

import sys
sys.path.append('../')
from loglizer.models import PCA
from loglizer import dataloader, preprocessing
import argparse
import os

valid_datasets = {
    'Android', 'Apache', 'BGL', 'HDFS', 'HPC', 'Hadoop',
    'HealthApp', 'Linux', 'Mac', 'OpenSSH', 'OpenStack',
    'Proxifier', 'Spark', 'Thunderbird', 'Windows', 'Zookeeper'
}

def parse_args():
    parser = argparse.ArgumentParser(description='Choose a dataset for structured log file.')
    parser.add_argument('--dataset', type=str, required=True,
                        help='Name of the dataset, e.g., HDFS, Apache, or HDFS100k for the special full log')
    return parser.parse_args()


args = parse_args()
dataset = args.dataset

if dataset == 'HDFS100k':
    struct_log = '../data/HDFS/HDFS_100k.log_structured.csv'
elif dataset in valid_datasets:
    struct_log = os.path.join('../data/loghub_2k', dataset, f'{dataset}_2k.log_structured.csv')
else:
    raise ValueError(f"Invalid dataset name '{dataset}'. Valid options are: HDFS100k, or one of {', '.join(valid_datasets)}")
# struct_log = '../data/HDFS/HDFS_100k.log_structured.csv' # The structured log file

if __name__ == '__main__':
    ## 1. Load strutured log file and extract feature vectors
    # Save the raw event sequence file by setting save_csv=True
    (x_train, _), (_, _) = dataloader.load_HDFS(struct_log, window='session', 
                                                split_type='sequential', save_csv=True)
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train, term_weighting='tf-idf', 
                                              normalization='zero-mean')
    
    ## 2. Train an unsupervised model
    print('Train phase:')
    # Initialize PCA, or other unsupervised models, LogClustering, InvariantsMiner
    model = PCA() 
    # Model hyper-parameters may be sensitive to log data, here we use the default for demo
    model.fit(x_train)
    # Make predictions and manually check for correctness. Details may need to go into the raw logs
    y_train = model.predict(x_train) 

    ## 3. Use the trained model for online anomaly detection
    print('Test phase:')
    # Load another new log file. Here we use struct_log for demo only
    (x_test, _), (_, _) = dataloader.load_HDFS(struct_log, window='session', split_type='sequential')
    # Go through the same feature extraction process with training, using transform() instead
    x_test = feature_extractor.transform(x_test) 
    # Finally make predictions and alter on anomaly cases
    y_test = model.predict(x_test)
    


