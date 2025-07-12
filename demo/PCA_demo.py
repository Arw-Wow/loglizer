#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
label_file = '../data/HDFS/anomaly_label.csv' # The anomaly label file

pkl_path = "../../proceeded_data/BGL"



if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(struct_log,
                                                                label_file=label_file,
                                                                window='session', 
                                                                train_ratio=0.5,
                                                                split_type='uniform')
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train, term_weighting='tf-idf', 
                                              normalization='zero-mean')
    x_test = feature_extractor.transform(x_test)

    model = PCA()
    model.fit(x_train)

    print('Train validation:')
    precision, recall, f1 = model.evaluate(x_train, y_train)
    
    print('Test validation:')
    precision, recall, f1 = model.evaluate(x_test, y_test)
