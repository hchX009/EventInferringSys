# /usr/bin/env python3
# coding: utf-8
# File: file_operation.py
# Author: hchX009
# python 3.5

class FileOperation():
    def __init__(self):
        pass

    # 从文件中得到一定数量的一行一行的文本
    def get_file_rows_list(self, filename, row_num):
        fd = open(filename, 'r')
        file_rows_list = list()
        # 防止内存太小而只读一定的文本行
        # file_rows_list = fd.readlines()
        for index in range(0, row_num):
            # 去除文中空格与末尾换行（只限中文文本）
            file_rows_list.append(fd.readline().replace(' ', '').rstrip('\n'))
        fd.close()
        return file_rows_list


if __name__ == '__main__':
    file_operation = FileOperation()
    text_list = file_operation.get_file_rows_list("/home/hchx009/Downloads/source_BIO_2014_cropus.txt", 30)
    print('\n'.join(text_list))