"""
@author Jacob
@time 2019/05/21
"""

import sys
from os.path import isfile, realpath, dirname, join
from os import makedirs
from typing import Union, List
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorboard import program
from pprint import pprint


def crash_proof():
    """
    in case of GPU CUDA crashing
    """
    config = tf.ConfigProto(
        gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.8)
        # device_count = {'GPU': 1}
    )
    config.gpu_options.allow_growth = True
    session = tf.Session(config=config)
    tf.keras.backend.set_session(session)


def get_file_dir(file_path: str):
    return dirname(realpath(file_path))


def create_file_dir(filename: str):
    makedirs(get_file_dir(filename), exist_ok=True)


def create_model_dir(root_path: str, consistent_model: bool = True):
    if consistent_model:
        model_dir = root_path
    else:
        model_dir = join(root_path, pd.datetime.now().strftime('%Y%m%d-%H%M%S'))

    makedirs(model_dir, exist_ok=True)
    return model_dir


def generate_tf_records_path(tf_records_name: str, tf_records_dir: str = r'.\tmp'):
    train_path = fr"{tf_records_dir}\{tf_records_name}_train.tfrecords"
    test_path = fr"{tf_records_dir}\{tf_records_name}_test.tfrecords"
    return train_path, test_path


def launch_tb(dir_path: str):
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', dir_path])
    url = tb.launch()
    sys.stdout.write('TensorBoard at %s \n' % url)
    input('press enter to quit TensorBoard')


def files_exist(file_path: Union[str, List[str]]) -> bool:
    if isinstance(file_path, str):
        if isfile(file_path):
            return True
        else:
            return False
    elif isinstance(file_path, list):
        if all([isfile(i) for i in file_path]):
            return True
        else:
            return False
    else:
        raise ValueError('file_path should either be str or List[str]')


def print_features_labels_name(data: pd.DataFrame,
                               feature_cols: Union[List[int], List[List[int]]],
                               label_col: int):
    name_cols = np.array(data.columns)

    if all(isinstance(i, List) for i in feature_cols):
        fc = [name_cols[i].tolist() for i in feature_cols]
    elif all(isinstance(i, int) for i in feature_cols):
        fc = name_cols[feature_cols].tolist()
    else:
        raise ValueError("feature_cols type error")

    lc = name_cols[[label_col]].tolist()

    print('features name: ')
    pprint(fc)
    print('label name: ')
    pprint(lc)
