# /usr/bin/env python3
# coding: utf-8
# File: event_relation_extractor.py
# Author: hchX009
# python 3.5


import re
from ltp_parser import LtpParser


class EventRelationExtractor:
    def __init__(self):
        self.but_patterns = self.create_pattern(self.pattern_but())
        self.seq_patterns = self.create_pattern(self.pattern_seq())
        self.and_patterns = self.create_pattern(self.pattern_and())
        self.condition_patterns = self.create_pattern(self.pattern_condition())
        self.causality_patterns = self.create_pattern(self.pattern_causality_1())
        self.anti_causality_patterns = self.create_pattern((self.pattern_causality_2()))

    # 转折事件
    def pattern_but(self):
        keywords = [[['与其'], ['不如'], 'but'],
                    [['虽然', '尽管', '虽'], ['但也', '但还', '但却', '但'], 'but'],
                    [['虽然', '尽管', '虽'], ['但', '但是也', '但是还', '但是却', ], 'but'],
                    [['不是'], ['而是'], 'but'],
                    [['即使', '就算是'], ['也', '还'], 'but'],
                    [['即便'], ['也', '还'], 'but'],
                    [['虽然', '即使'], ['但是', '可是', '然而', '仍然', '还是', '也', '但'], 'but'],
                    [['虽然', '尽管', '固然'], ['也', '还', '却'], 'but'],
                    [['与其', '宁可'], ['决不', '也不', '也要'], 'but'],
                    [['与其', '宁肯'], ['决不', '也要', '也不'], 'but'],
                    [['与其', '宁愿'], ['也不', '决不', '也要'], 'but'],
                    [['虽然', '尽管', '固然'], ['也', '还', '却'], 'but'],
                    [['不管', '不论', '无论', '即使'], ['都', '也', '总', '始终', '一直'], 'but'],
                    [['虽'], ['可是', '倒', '但', '可', '却', '还是', '但是'], 'but'],
                    [['虽然', '纵然', '即使'], ['倒', '还是', '但是', '但', '可是', '可', '却'], 'but'],
                    [['虽说'], ['还是', '但', '但是', '可是', '可', '却'], 'but'],
                    [['无论'], ['都', '也', '还', '仍然', '总', '始终', '一直'], 'but'],
                    [['与其'], ['宁可', '不如', '宁肯', '宁愿'], 'but']]
        return keywords

    # 顺承事件
    def pattern_seq(self):
        keywords = [[['又', '再', '才', '并'], ['进而'], 'sequence'],
                    [['首先', '第一'], ['其次', '然后'], 'sequence'],
                    [['首先', '先是'], ['再', '又', '还', '才'], 'sequence'],
                    [['一方面'], ['另一方面', '又', '也', '还'], 'sequence'],
                    [[], ['之后', '然后', '后来', '接着', '随后', '其次', '接下来'], 'sequence']]
        return keywords

    # 并列事件
    def pattern_and(self):
        keywords = [[['不但', '不仅'], ['并且'], 'and'],
                    [['不单'], ['而且', '并且', '也', '还'], 'and'],
                    [['不但'], ['而且', '并且', '也', '还'], 'and'],
                    [['不管'], ['都', '也', '总', '始终', '一直'], 'and'],
                    [['不光'], ['而且', '并且', '也', '还'], 'and'],
                    [['虽然', '尽管'], ['不过'], 'and'],
                    [['不仅'], ['还', '而且', '并且', '也'], 'and'],
                    [['不论'], ['还是', '也', '总', '都', '始终', '一直'], 'and'],
                    [['不只'], ['而且', '也', '并且', '还'], 'and'],
                    [['不但', '不仅', '不光', '不只'], ['而且'], 'and'],
                    [['尚且', '都', '也', '又', '更'], ['还', '又'], 'and'],
                    [['既然', '既', ], ['就', '便', '那', '那么', '也', '还'], 'and'],
                    [['无论', '不管', '不论', '或'], ['或'], 'and'],
                    [['或是'], ['或是'], 'and'],
                    [['或者', '无论', '不管', '不论'], ['或者'], 'and'],
                    [['不是'], ['也'], 'and'],
                    [['要么', '或者'], ['要么', '或者'], 'and']]
        return keywords

    # 条件事件
    def pattern_condition(self):
        keywords = [[['除非'], ['否则', '才', '不然', '要不'], 'condition'],
                    [['除非'], ['否则的话'], 'condition'],
                    [['还是', '无论', '不管'], ['还是', '都', '总'], 'condition'],
                    [['既然'], ['又', '且', '也', '亦'], 'condition'],
                    [['假如'], ['那么', '就', '也', '还'], 'condition'],
                    [['假若', '如果'], ['那么', '就', '那', '则', '便'], 'condition'],
                    [['假使', '如果'], ['那么', '就', '那', '则', '便'], 'condition'],
                    [['尽管', '如果'], ['那么', '就', '那', '则', '便'], 'condition'],
                    [['即使', '就是'], ['也', '还是'], 'condition'],
                    [['如果', '既然'], ['那么'], 'condition'],
                    [['如', '假设'], ['则', '那么', '就', '那'], 'condition'],
                    [['如果', '假设'], ['那么', '则', '就', '那'], 'condition'],
                    [['万一'], ['那么', '就'], 'condition'],
                    [['要是', '如果'], ['就', '那'], 'condition'],
                    [['要是', '如果', '假如'], ['那么', '就', '那', '的话'], 'condition'],
                    [['一旦'], ['就'], 'condition'],
                    [['既然', '假如', '既', '如果'], ['则', '就'], 'condition'],
                    [['只要'], ['就', '便', '都', '总'], 'condition'],
                    [['只有'], ['才', '还'], 'condition'],
                    [['如果'], ['，'], 'condition'],
                    [['即使'], ['，'], 'condition']]
        return keywords

    # 因果事件，因到果
    def pattern_causality_1(self):
        keywords = [[['因为'], ['从而', '为此', '因而', '致使', '以致于?', '以至于?', '所以', '于是', '故', '故而', '因此'],
                     'causality'],
                    [['由于'], ['从而', '为此', '因而', '致使', '以致于?', '以至于?', '所以', '于是', '故', '为此', '因此'], 'causality'],
                    [['既然'], ['所以', '却', '因此'], 'causality'],
                    [[], ['从而', '为此', '因而', '致使', '以致于?', '以至于?', '所以', '于是', '故', '故而', '因此'], 'causality'],
                    [[], ['致使', '结果', '牵动', '导向', '导致', '勾起', '引入', '指引', '予以', '产生', '促成', '造成', '引导', '造就', '促使', '酿成',
                          '引发', '渗透', '促进', '引起', '诱导', '引来', '促发', '引致', '诱发', '推进', '诱致', '推动', '招致', '影响下?', '致使',
                          '滋生', '归于', '作用', '使得', '决定', '攸关', '令人', '引出', '浸染', '带来', '挟带', '触发', '关系到', '渗入', '诱惑',
                          '波及', '诱使'], 'causality'],
                    [['为了', '依据', '按照', '因为', '因', '按', '依赖', '凭借', '由于', '既然'], ['，'], 'causality'],
                    [[], ['以免', '以便', '为此', '才'], 'causality']]
        return keywords

    # 因果事件，果到因
    def pattern_causality_2(self):
        keywords = [
            [[], ['根源于', '取决', '来源于', '出于', '取决于', '缘于', '在于', '出自', '起源于', '来自', '发源于', '发自', '源于', '立足于', '立足'],
             'anti_causality'],
            [['之所以'], ['是因为', '是由于', '是缘于'], 'anti_causality'],
            [[], ['是因为', '是由于'], 'anti_causality']]
        return keywords

    # 将事件关系用正则编译为模式
    def create_pattern(self, keywords):
        pattern = dict()
        patterns_list = list()
        for keyword in keywords:
            pre = keyword[0]
            post = keyword[1]
            # 生成模式匹配 XX... XX... 并且后半句不匹配结束句子的标点符号
            p = re.compile(r'({0})(.*)({1})([^?？!！。;；:：\n\r]*)'.format('|'.join(pre), '|'.join(post)))
            patterns_list.append(p)
        # 为了方便识别，将模式种类放入字典keyword中
        pattern['keyword'] = keyword[2]
        pattern['list'] = patterns_list
        return pattern

    # 模式匹配，输出句子的事件关系三元组和具体关系所组成的字典
    def pattern_match(self, pattern, sentence):
        pattern_res = dict()
        # 记录输出匹配出最多的字符的组的标记
        max_len = 0
        patterns_list = pattern['list']
        for p in patterns_list:
            # 使用模式匹配将关系和除了关系以外的事件子句提取出来
            event_subsents = p.findall(sentence)
            if not event_subsents:
                continue
            for event_subsent in event_subsents:
                # 找到匹配出逻辑关系字符串最多的组
                if len(event_subsent[0] + event_subsent[2]) > max_len:
                    # <事件子句1， 逻辑关系， 事件子句2>
                    triple_data = [event_subsent[1], pattern['keyword'], event_subsent[3]]
                    relation_data = event_subsent[0] + '-' + event_subsent[2]
                    pattern_res['triple_data'] = triple_data
                    pattern_res['relation_data'] = relation_data
                    max_len = len(relation_data) - 1
        return pattern_res

    # 模式匹配集成，句子在此函数中对现有所有模式进行匹配，输出最先匹配到的结果字典
    def all_pattern_match(self, sentence):
        pattern_res = dict()
        pattern_res = self.pattern_match(self.condition_patterns, sentence)
        if pattern_res:
            return pattern_res
        pattern_res = self.pattern_match(self.anti_causality_patterns, sentence)
        if pattern_res:
            return pattern_res
        pattern_res = self.pattern_match(self.causality_patterns, sentence)
        if pattern_res:
            return pattern_res
        pattern_res = self.pattern_match(self.but_patterns, sentence)
        if pattern_res:
            return pattern_res
        pattern_res = self.pattern_match(self.seq_patterns, sentence)
        if pattern_res:
            return pattern_res
        pattern_res = self.pattern_match(self.and_patterns, sentence)
        if pattern_res:
            return pattern_res
        pattern_res['triple_data'] = []
        pattern_res['relation_data'] = "NULL"
        return pattern_res

    # 主控函数
    def event_relation_extrator_main(self, content):
        ltp_extractor = LtpParser()
        sentences = ltp_extractor.get_sentences(content)
        event_relation_triples_list = \
            [self.all_pattern_match(sentence)['triple_data'] for sentence in sentences if sentence]
        return event_relation_triples_list


if __name__ == '__main__':
    content1 = "我将在一个月后于电子科技大学毕业，之后我工作在银行。"
    content2 = "由于李克强总理今天来我家了，因此我感到非常荣幸。"
    content3 = "因为钢铁雄心玩家抵达了君士坦丁堡，所以赤旗将插满整个世界。"
    content4 = "北极熊的栖息地越来越少，是因为海平面不断上升导致的。"
    content5 = "在极端天气的影响下，天气变得越来越热"
    event_relation_extractor = EventRelationExtractor()
    event_relation_triples = event_relation_extractor.event_relation_extrator_main(content5)
    print(event_relation_triples)
