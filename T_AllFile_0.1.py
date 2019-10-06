"""
1.查找指定目录下所有的文件夹及文件，并提取文件夹名称或文件名、路径、大小、创建时间、修改时间，md5
2.输出到指定目录下的AllFile.csv，AllFile_md5.csv或者AllFolder.csv文件
"""
import csv
import hashlib
import os
import time
from os.path import getsize, join
from time import localtime

import pandas as pd

"""以下为函数区"""


# 遍历目录，建立所有文件名和文件路径
def file_info(folder):
    _file_list = []
    for paths, folders, filenames in os.walk(folder):  # 遍历所有目录
        for f in filenames:  # 遍历所有文件名
            f_name, f_ext = os.path.splitext(f)
            file_attr = {'name': f,
                         'name_s': f_name,
                         'type': f_ext,
                         'path': os.path.join(paths, f),
                         'size': getsize(os.path.join(paths, f)),
                         'ctime': os.path.getctime(os.path.join(paths, f)),
                         'mtime': os.path.getmtime(os.path.join(paths, f))}
            # 获得文件属性
            # print(type(file_attr))
            if file_attr not in _file_list:
                _file_list.append(file_attr)
    print('find file count', len(_file_list))
    # print(_file_list)
    _file_list = sorted(_file_list, key=lambda i: (i['type'], i['name'], i['size']), reverse=True)
    # print('file_list_ext',(file_list)
    return _file_list


# 遍历目录，建立所有文件名和文件路径,提取MD5属性
def file_info_md5(folder):
    _file_list = []
    for paths, folders, filenames in os.walk(folder):  # 遍历所有目录
        for f in filenames:  # 遍历所有文件名
            f_path = os.path.join(paths, f)
            f_name, f_ext = os.path.splitext(f)
            file_attr = {'name': f,
                         'name_s': f_name,
                         'type': f_ext,
                         'path': f_path,
                         'size': getsize(f_path),
                         'ctime': os.path.getctime(f_path),
                         'mtime': os.path.getmtime(f_path),
                         'md5': get_md5(f_path)}
            # 获得文件属性
            # print(file_attr)
            if file_attr not in _file_list:
                _file_list.append(file_attr)
    print('find file count', len(_file_list))
    _file_list = sorted(_file_list, key=lambda i: (i['type'], i['name'], i['size']), reverse=True)
    # print('file_list_ext',(file_list)
    return _file_list


# 采集文件的MD5值， 时间较长，尽量减少调用
def get_md5(_file_path):
    f = open(_file_path, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    print(md5)
    return md5


# 输出到文件，包含MD5信息
def out_csv_md5(_result, csv_name):
    data_row: pd.DataFrame = pd.DataFrame(_result, columns=['name', 'type', 'size', 'path', 'mtime', 'ctime', 'md5'])
    # 读取结果，定义表头
    data_row.to_csv(csv_name, encoding='utf-8-sig', index=False)  # 输出到文件


# 输出到文件,不包含MD5信息
def out_csv(_result, csv_name):
    data_row: pd.DataFrame = pd.DataFrame(_result, columns=['name', 'type', 'size', 'path', 'mtime', 'ctime'])
    # 读取结果，定义表头
    data_row.to_csv(csv_name, encoding='utf-8-sig', index=False)  # 输出到文件


def list_all():
    for p in path_in:  # 遍历多重目录
        print('now open', p)
        file_path_in.extend(file_info(p))
        print('find file total:', len(file_path_in))

    for i in range(0, len(file_path_in)):
        f0 = [file_path_in[i]['name_s'],
              file_path_in[i]['type'],
              file_path_in[i]['size'],
              file_path_in[i]['path'],
              time.strftime("%Y-%m-%d %H:%M:%S", localtime(file_path_in[i]['mtime'])),
              time.strftime("%Y-%m-%d %H:%M:%S", localtime(file_path_in[i]['ctime']))]
        result.append(f0)
    out_csv(result, path_out + '\\allfile_001.csv')


def list_all_md5():
    for p in path_in:  # 遍历多重目录
        print('now open', p)
        file_path_in.extend(file_info_md5(p))
        print('find file total:', len(file_path_in))

    for i in range(0, len(file_path_in)):
        f0 = [file_path_in[i]['name_s'],
              file_path_in[i]['type'],
              file_path_in[i]['size'],
              file_path_in[i]['path'],
              time.strftime("%Y-%m-%d %H:%M:%S", localtime(file_path_in[i]['mtime'])),
              time.strftime("%Y-%m-%d %H:%M:%S", localtime(file_path_in[i]['ctime'])),
              file_path_in[i]['md5']]
        result.append(f0)
    out_csv_md5(result, path_out + '\\allfile_md5_001.csv')


if __name__ == '__main__':
    file_path_in = []
    result = []
    path_in = ['C:\\Users\\TAO\\FangCloudV2', 'C:\\Users\\TAO\\downloads\\data']  # 设定多重目录
    path_out = './output'  # 指定输出目录

    input0 = input("1.No MD5 or 2.MD5")

    if input0 == '1':
        list_all()
    elif input0 == '2':
        list_all_md5()

    else:
        print('input wrong')
