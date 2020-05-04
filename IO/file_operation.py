# /usr/bin/env python3
# coding: utf-8
# File: file_operation.py
# Author: hchX009
# python 3.5


class FileOperation():
    # 定义事件关系文件名称
    EVENT_RELATIONS_LIST_FILE_NAME = "/home/hchx009/Downloads/event_relations_list.txt"

    def __init__(self):
        pass

    # 从文件中得到一定数量的一行一行的文本
    def get_file_rows_list(self, filename, start, end):
        fd = open(filename, 'r')
        file_rows_list = list()
        if start >= end:
            return file_rows_list
        # 防止内存太小而只读一定的文本行
        # file_rows_list = fd.readlines()
        for index in range(0, end):
            if index < start:
                fd.readline()
            else:
                # 去除文中空格与末尾换行（只限中文文本）
                file_rows_list.append(fd.readline().replace(' ', '').rstrip('\n'))
        fd.close()
        return file_rows_list

    # 将输出的关系对转化为txt文本
    def get_event_relations_list_file(self, event_sets_list):
        fd = open(self.EVENT_RELATIONS_LIST_FILE_NAME, 'a')
        for event_set in event_sets_list:
            events_list_pre = event_set[0]
            events_list_post = event_set[2]
            '''
            pre = post = ""
            for event_pre in events_list_pre:
                pre = pre + ''.join(event_pre)
            for event_post in events_list_post:
                post = post + ''.join(event_post)
            if pre and post:
                output_line = pre + '--' + event_set[1] + '->' + post + '\n'
                fd.write(output_line)
            '''
            for event_pre in events_list_pre:
                for event_post in events_list_post:
                    if event_pre and event_post:
                        output_line = ''.join(event_pre) + '--' + event_set[1] + '->' + ''.join(event_post) + '\n'
                        fd.write(output_line)
        return


if __name__ == '__main__':
    file_operation = FileOperation()
    text_list = file_operation.get_file_rows_list("/home/hchx009/Downloads/text.txt", 30)
    print('\n'.join(text_list))