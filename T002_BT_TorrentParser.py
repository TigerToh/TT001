# -*- coding: utf-8 -*-

import csv

import pandas as pd
# import zone
from bencode import bdecode

'''
难点在于不同的key采用了不同的格式，需要逐个区别对待.先取值，再格式化
# torrent文件本身为字典，可以直接读取键值。对于固定键值的，直接读取。如果无该键值，取空
# 固定键值的包括哪些？

# 多文件
# b'announce' <class 'bytes'> <class 'bytes'> [yes]
# b'announce-list' <class 'bytes'> <class 'list'> [Yes]
# b'comment' <class 'bytes'> <class 'bytes'> [yes]
# b'comment.utf-8' <class 'bytes'> <class 'bytes'>
# b'created by' <class 'bytes'> <class 'bytes'> [yes]
# b'creation date' <class 'bytes'> <class 'int'> [yes]
# b'encoding' <class 'bytes'> <class 'bytes'> [yes]
# b'info' <class 'bytes'> <class 'dict'> [yes]
# b'nodes' <class 'bytes'> <class 'list'>

# info键值非固定
# b'files' <class 'list'>, [多文件，非固定] [yes]
# b'name' <class 'bytes'> [固定]
# b'name.utf-8' <class 'bytes'>
# b'piece length' <class 'int'>,[固定】
# b'pieces' <class 'bytes'>,[固定]
# b'publisher' <class 'bytes'>
# b'b'publisher-url' <class 'bytes'>
# b'publisher-url.utf-8' <class 'bytes'>
# b'publisher.utf-8' <class 'bytes'>

# 多文件
# b'ed2k', [yes]
# b'filehash',
# b'length', [yes]
# b'path', [yes]
# b'path.utf-8'

'''


# 函数区


def torrentparser(filepath):
    print(type(filepath))
    try:
        # 确定输入源，并用bdecode打开torrent文件
        with open(filepath, 'rb') as fObj:
            content = bdecode(fObj.read())
            # print(content)
            # print(content.keys())
            # print(str(content[bytes('comment.utf-8', encoding='utf8')],'utf-8')) #可以转换成字符
        # tor_info['announce'] = (content[bytes('announce', 'utf-8')]
    except:
        pass

    for key in content.keys():
        # print(key, type(key),type(content[key]))
        tor_info[str(key, 'utf-8')] = content[key]
        # print('@@@',tor_info.keys())

        # print('###torrent###', key, type(content[key]))  # )
        # try:
        #     print('###torrent###', content[key].decode('utf-8'))
        # except:
        #     pass

    # 提取info下面的信息
    info = content[bytes('info', 'utf-8')]
    # print('typeinfo', type(info), info.keys())
    # for key in info.keys():
    #     print('+++info+++', key, type(info[key]))
    #     try:
    #         print('+++info+++', key, info[key].decode('utf-8'))
    #     except:
    #         pass

    # 判断单一文件还是多文件
    if bytes('files', 'utf-8') in info.keys():
        m_files = info[bytes('files', 'utf-8')]
        tor_info_all = multifile(filepath, m_files)
        # print('info.keys', info.keys())
    else:
        # print(tor_info)
        # tor_info['name'].setdefault(info[bytes('name', 'utf-8')], '')
        # tor_info['length'].setdefault(info[bytes('length', 'utf-8')], '')
        s_file = info
        tor_info_all = singfile(filepath, s_file)
        # print('wrong',singfile(s_file))
    return tor_info_all


'''
待解决的问题：其他变量的传入
要传入filepath, 基础的信息和info信息
'''


def multifile(filepath, m_files):
    t_info_m = []

    # 提取多文件信息，分解文件结构
    for i in range(len(m_files)):  # 遍历所有的文件
        # print(m_files[i][bytes('path','utf-8')])
        # print(info[bytes('files', 'utf-8')][i].keys()) # 不同文件对应不同的key
        if bytes('ed2k', 'utf-8') in m_files[i].keys():  # 判断是不是直接文件
            # print('//', m_files[i].keys())  # 是，就打印出文件的keys
            # for key in m_files[i].keys():  # 遍历文件下所有的key
            if len(m_files[i][bytes('path', 'utf-8')]) == 2:  # 判断是不是多层文件
                t_info_m_temp = [filepath.split('~'), str(m_files[i][bytes('path', 'utf-8')][1], 'utf-8'),
                                 m_files[i][bytes('length', 'utf-8')]]
                t_info_m.append(t_info_m_temp)
                # print(t_info_m)
                # print('t_info_m', t_info_m)
                # for m in range(len(m_files[i][bytes('path', 'utf-8')])):  # 多层文件则取打印文件夹和文件路径
                #     print(m_files[i][bytes('path', 'utf-8')][m].decode('utf-8'))
            else:
                t_info_m_temp = [filepath.split('~'), str(m_files[i][bytes('path', 'utf-8')][0], 'utf-8'),
                                 m_files[i][bytes('length', 'utf-8')]]
                t_info_m.append(t_info_m_temp)
                # print('t_info_m', t_info_m)
                # print(type(m_files[i][bytes('path', 'utf-8')]))
                # m_files[i][bytes('path', 'utf-8')])  # 直接打印文件路径
        else:
            print('wrrr')
    return t_info_m


def singfile(filepath, s_file):
    t_info_s = []
    t_info_s_temp = [filepath.split('~'), str(s_file[bytes('name', 'utf-8')], 'utf-8'),
                     s_file[bytes('length', 'utf-8')]]
    t_info_s.append(t_info_s_temp)
    # print('t_info_s',t_info_s)
    # tor_info['file-']
    # for key in s_file.keys():
    # print('===', key, type(s_file[key]))
    # print(s_file[bytes('name'), 'utf-8']).decode('utf-8')
    return t_info_s


def m_info_dafault():
    tor_info.setdefault('announce', '')
    tor_info.setdefault('announce-list', '')
    tor_info.setdefault('created by', '')
    tor_info.setdefault('comment', '')
    tor_info.setdefault('creation date', '')
    tor_info.setdefault('encoding', '')
    tor_info.setdefault('info', '')
    tor_info.setdefault('files', '')
    tor_info.setdefault('length', '')
    tor_info.setdefault('path', '')
    tor_info.setdefault('path.utf-8', '')
    tor_info.setdefault('name', '')
    tor_info.setdefault('name.utf-8', '')
    tor_info.setdefault('piece length', '')
    tor_info.setdefault('pieces', '')
    tor_info.setdefault('publisher', '')
    tor_info.setdefault('publisher-url', '')
    tor_info.setdefault('publisher-url.utf-8', '')
    tor_info.setdefault('publisher.utf-8', '')
    tor_info.setdefault('nodes', '')


def s_info_default():
    tor_info.setdefault('announce', '')
    tor_info.setdefault('announce - list', '')
    tor_info.setdefault('created by', '')
    tor_info.setdefault('comment', '')
    tor_info.setdefault('comment.utf - 8', '')
    tor_info.setdefault('creation date', '')
    tor_info.setdefault('encoding', '')
    tor_info.setdefault('info', '')
    tor_info.setdefault('length', '')
    tor_info.setdefault('name', '')
    tor_info.setdefault('name.utf - 8', '')
    tor_info.setdefault('piece length', '')
    tor_info.setdefault('pieces', '')
    tor_info.setdefault('publisher', '')
    tor_info.setdefault('publisher - url', '')
    tor_info.setdefault('publisher - url.utf - 8', '')
    tor_info.setdefault('publisher.utf - 8', '')
    tor_info.setdefault('nodes', '')


'''
文件信息的输出结果是个列表，按指定顺序，分别取值。然后用result.append


def t_info():

'''


# 输出到文件,不包含MD5信息
def out_csv(_result, csv_name):
    data_row: pd.DataFrame = pd.DataFrame(_result, columns=['path', 'name', 'size'])
    # 读取结果，定义表头
    data_row.to_csv(csv_name, encoding='utf-8-sig', index=False)  # 输出到文件


if __name__ == '__main__':
    # 基础申明，例如输入输出的位置和格式
    tor_info = {}
    file_input = r'C:\Users\TAO\Desktop\T2019002\input\allseed.csv'
    path_out = './output'  # 指定输出目录
    # path_out: str = r'C:\Users\TAO\Desktop\T2019002\output'  # 指定输出目录
    # filetype: list = ['.xls', '.xlsx', 'xlt']
    result = []
    fail = []
    # result_move = []
    n = 1
    # 读取csv文件

    # 主功能区
    filelist = csv.reader(open(file_input, 'r', encoding='utf-8'))
    for row in filelist:
        n = n + 1
        print(n)
        # print(type(str(row)))
        # print(row[0])
        try:
            result_t = torrentparser(row[0])
            result.extend(result_t)

        except:
            fail.append(row)  # 待处理， fail文件的记录

    # print(result)

    # 输出区

    '''
    注意新的输出，如果输出文件不存在，会报错
    '''

    out_csv(result, path_out + '\\seed_t.csv')
