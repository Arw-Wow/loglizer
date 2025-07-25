#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
from loglizer import dataloader
from loglizer.models import DeepLog
from loglizer.preprocessing import Vectorizer, Iterator


batch_size = 32
hidden_size = 32
num_directions = 2
topk = 5
train_ratio = 0.2
window_size = 10
epoches = 2
num_workers = 2
device = 0 
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

if __name__ == '__main__':
    (x_train, window_y_train, y_train), (x_test, window_y_test, y_test) = dataloader.load_HDFS(struct_log, label_file=label_file, window='session', window_size=window_size, train_ratio=train_ratio, split_type='uniform')
    
    feature_extractor = Vectorizer()
    train_dataset = feature_extractor.fit_transform(x_train, window_y_train, y_train)
    test_dataset = feature_extractor.transform(x_test, window_y_test, y_test)

    train_loader = Iterator(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers).iter
    test_loader = Iterator(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers).iter

    model = DeepLog(num_labels=feature_extractor.num_labels, hidden_size=hidden_size, num_directions=num_directions, topk=topk, device=device)
    model.fit(train_loader, epoches)

    print('Train validation:')
    metrics = model.evaluate(train_loader)

    print('Test validation:')
    metrics = model.evaluate(test_loader)
