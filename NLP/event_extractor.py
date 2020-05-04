# /usr/bin/env python3
# coding: utf-8
# File: event_extractor.py
# Author: hchX009
# python 3.5


from ltp_parser import LtpParser


class EventExtrator:
    def __init__(self):
        self.parser = LtpParser()

    # 通过语义角色标注进行三元组提取，获得主谓宾三元组
    def get_triple_from_roles(self, words_list, postags_list, roles_dict, index):
        triple = list()
        v = words_list[index]
        role = roles_dict[index]
        if 'A0' in role.keys() and 'A1' in role.keys():
            s = ''.join(words_list[word_index] for word_index in range(role['A0'][1], role['A0'][2] + 1) if
                        postags_list[word_index][0] not in ['w', 'u', 'x'] and words_list[word_index])
            o = ''.join(words_list[word_index] for word_index in range(role['A1'][1], role['A1'][2] + 1) if
                        postags_list[word_index][0] not in ['w', 'u', 'x'] and words_list[word_index])
            if s and o:
                triple = [s, v, o]
        elif 'A0' in role.keys():
            s = ''.join(words_list[word_index] for word_index in range(role['A0'][1], role['A0'][2] + 1) if
                        postags_list[word_index][0] not in ['w', 'u', 'x'] and words_list[word_index])
            o = ''
            if s:
                triple = [s, v, o]
        elif 'A1' in role.keys():
            s = ''
            o = ''.join(words_list[word_index] for word_index in range(role['A1'][1], role['A1'][2] + 1) if
                        postags_list[word_index][0] not in ['w', 'u', 'x'] and words_list[word_index])
            if o:
                triple = [s, v, o]
        return triple

    # 通过依存句法进行以谓语为中心的三元组提取，前置宾语的句子暂时没考虑
    def get_triple_from_arcs(self, words_list, postags_list, child_nodes_dict_list, format_arcs_list, index):
        triple = list()
        child_nodes_dict = child_nodes_dict_list[index]
        # 谓宾，主谓，主谓宾
        if 'SBV' in child_nodes_dict and 'VOB' in child_nodes_dict:
            v = words_list[index]
            s = self.complete_subject_or_object(
                words_list, postags_list, child_nodes_dict_list, child_nodes_dict['SBV'][0])
            o = self.complete_subject_or_object(
                words_list, postags_list, child_nodes_dict_list, child_nodes_dict['VOB'][0])
            triple = [s, v, o]
        elif 'VOB' in child_nodes_dict:
            v = words_list[index]
            s = ''
            o = self.complete_subject_or_object(
                words_list, postags_list, child_nodes_dict_list, child_nodes_dict['VOB'][0])
            triple = [s, v, o]
        elif 'SBV' in child_nodes_dict:
            v = words_list[index]
            s = self.complete_subject_or_object(
                words_list, postags_list, child_nodes_dict_list, child_nodes_dict['SBV'][0])
            o = ''
            triple = [s, v, o]
        # 含有介宾关系的主谓动补关系
        if 'SBV' in child_nodes_dict and 'CMP' in child_nodes_dict:
            cmp_index = child_nodes_dict['CMP'][0]
            s = self.complete_subject_or_object(
                words_list, postags_list, child_nodes_dict_list, child_nodes_dict['SBV'][0])
            v = words_list[index] + words_list[cmp_index]
            if 'POB' in child_nodes_dict_list[cmp_index]:
                o = self.complete_subject_or_object(
                    words_list, postags_list, child_nodes_dict_list, child_nodes_dict_list[cmp_index]['POB'][0])
                triple = [s, v, o]
        # 定语后置，动宾关系
        arc_relation = format_arcs_list[index][0]
        arc_head = format_arcs_list[index][2]
        if arc_relation == 'ATT':
            if 'VOB' in child_nodes_dict:
                v = words_list[index]
                s = self.complete_subject_or_object(
                    words_list, postags_list, child_nodes_dict_list, arc_head - 1)
                o = self.complete_subject_or_object(
                    words_list, postags_list, child_nodes_dict_list, child_nodes_dict['VOB'][0])
                verb_object_string = v + o
                # 去除重合字段
                if verb_object_string == s[:len(verb_object_string)]:
                    s = s[len(verb_object_string):]
                if verb_object_string not in s:
                    triple = [s, v, o]
        return triple

    # 对找出的主语或者宾语进行扩展
    def complete_subject_or_object(self, words_list, postags_list, child_nodes_dict_list, word_index):
        child_nodes_dict = child_nodes_dict_list[word_index]
        prefix = ""
        # 如果有定中关系，红苹果 => 红<-苹果，则将该词定语加上
        if 'ATT' in child_nodes_dict:
            for index in range(len(child_nodes_dict['ATT'])):
                prefix += self.complete_subject_or_object(
                    words_list, postags_list, child_nodes_dict_list, child_nodes_dict['ATT'][index])
        # 提取状中关系，主要是解决否定词问题
        if 'ADV' in child_nodes_dict:
            for index in range(len(child_nodes_dict['ADV'])):
                prefix += self.complete_subject_or_object(
                    words_list, postags_list, child_nodes_dict_list, child_nodes_dict['ADV'][index])
        postfix = ""
        if postags_list[word_index] == 'v':
            # 如果输入的是动词，存在动宾关系，添加其宾语
            if 'CMP' in child_nodes_dict:
                postfix += self.complete_subject_or_object(
                    words_list, postags_list, child_nodes_dict_list, child_nodes_dict['CMP'][0])
            if 'VOB' in child_nodes_dict:
                postfix += self.complete_subject_or_object(
                    words_list, postags_list, child_nodes_dict_list, child_nodes_dict['VOB'][0])
            # 如果存在主谓关系，添加其主语
            if 'SBV' in child_nodes_dict:
                prefix = self.complete_subject_or_object(
                    words_list, postags_list, child_nodes_dict_list, child_nodes_dict['SBV'][0]) + prefix
        return prefix + words_list[word_index] + postfix

    # 得到事件三元组，主要识别主谓宾和谓宾事件
    def get_event_triples(self, data):
        event_triples_list = list()
        words_list = data['words_list']
        postags_list = data['postags_list']
        roles_dict = data['roles_dict']
        child_nodes_dict_list = data['child_nodes_dict_list']
        format_arcs_list = data['format_arcs_list']
        for index in range(len(postags_list)):
            event_triple = list()
            # 先借助语义角色标注结果进行三元组提取
            if index in roles_dict:
                event_triple = self.get_triple_from_roles(words_list, postags_list, roles_dict, index)
                if event_triple:
                    event_triples_list.append(event_triple)
                    # 得到三元组又进行下一轮循环
                    continue
            # 如果语义角色标记为空，则使用依存句法进行抽取，抽取以谓语为中心的事件三元组
            if postags_list[index] == 'v' and not event_triple:
                event_triple = self.get_triple_from_arcs(words_list, postags_list,
                                                         child_nodes_dict_list, format_arcs_list, index)
                if event_triple:
                    event_triples_list.append(event_triple)
        return event_triples_list

    # 过滤掉属于从句或者多余的event_triple
    def drop_unnecssary_event_triples(self, event_triples):
        event_last_triple = event_triples[0]
        for event_triple in event_triples:
            event_str = event_last_str = ""
            for i in event_triple:
                event_str += i
            for j in event_last_triple:
                event_last_str += j
            if len(event_str) >= len(event_last_str) and \
                    event_triple[0] not in event_last_triple[0] or \
                    event_triple[2] not in event_last_triple[2]:
                event_last_triple = event_triple
        return event_last_triple

    # 主控制函数
    def event_extrator_main(self, content):
        datas_list = self.parser.ltp_parser_main(content)
        events_list = list()
        for data in datas_list:
            event_triples = self.get_event_triples(data)
            if event_triples:
                #event = event_triples
                event = self.drop_unnecssary_event_triples(event_triples)
                events_list.append(event)
        return events_list


if __name__ == '__main__':
    content1 = "我将在一个月后于电子科技大学毕业，之后我工作在银行。"
    content2 = "李克强总理今天来我家了，我感到非常荣幸。"
    content3 = "因为钢铁雄心玩家抵达了君士坦丁堡，所以赤旗将插满整个世界。"
    content4 = '''
            公安部近日组织全国公安机关开展扫黑除恶
            追逃“清零”行动。公安部将1712名涉黑涉恶
            逃犯列为“清零”行动目标逃犯，逐一明确追
            逃责任人，实行挂账督捕，并对13名重点在
            逃人员发布A级通缉令。
            '''
    event_extrator = EventExtrator()
    events_list = event_extrator.event_extrator_main(content3)
    print(events_list)