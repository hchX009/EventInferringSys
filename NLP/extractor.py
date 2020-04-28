# python 3.5
# pyltp 0.2.3
#   git clone http://github.com/HIT-SCIR/pyltp
#   cd pyltp
#   git submodule init
#   git submodule update
#   python setup.py install
# ltp model 3.4.0


import os
import re
import jieba
import jieba.posseg
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser


# 长句切分。将段落分句，将一段话或一篇文章中的文字按句子分开，按句子形成独立的单元。返回切分好的句子列表
def get_sentences(content):
    # 消去句子中的空格以及换行
    content = content.replace(' ', '').replace('\n', '')
    sents = SentenceSplitter.split(content)
    sents_list = list(sents)
    return sents_list


# 短句切分。将长句按逗号和顿号切分为短句。返回切分好的短句列表
def get_subsents(sentence):
    subsents_list = list()
    subsents = re.split(r'[，：,:]', sentence)
    # 消去长度为0的子句，并将子句加入列表中
    for subsent in subsents:
        if subsent:
            subsents_list.append(subsent)
    return subsents_list


# pyltp分词。
# 公安部 / 将 / 1712 / 名 / 涉黑 / 涉恶 / 逃犯 / 列为 / “ / 清零 / ” / 行动 / 目标 / 逃犯
def get_words_by_pyltp(sent):
    words_list = list()
    # 分词模型路径，模型名称为`cws.model`
    cws_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/cws.model')
    # dictionary是自定义词典的文件路径
    dictonary_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/dictionary.txt')
    segmentor = Segmentor()
    segmentor.load_with_lexicon(cws_model_path, dictonary_path)
    # 分词
    words = segmentor.segment(sent)
    segmentor.release()
    words_list = list(words)
    return words_list


# pyltp标注词性
def get_postags_by_pyltp(words_list):
    postags_list = list()
    # 词性标注模型路径，模型名称为‘pos.model’
    pos_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/pos.model')
    postagger = Postagger()
    postagger.load(pos_model_path)
    postags = postagger.postag(words_list)
    postagger.release()
    postags_list = list(postags)
    return postags_list


# pyltp命名实体识别
def get_entity_by_pyltp(words_list, postags_list):
    entitys_list = list()
    # 实体命名识别模型路径，模型名称为‘ner.model’
    ner_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/ner.model')
    recongnizer = NamedEntityRecognizer()
    recongnizer.load(ner_model_path)
    netags = recongnizer.recognize(words_list, postags_list)
    recongnizer.release()
    entitys_list = list(netags)
    return entitys_list


# pyltp依存句法分析
def get_parser_by_pyltp(words_list, postags_list):
    arcs_list = list()
    # 依存句法分析模型路径，模型名称为‘ner.model’
    par_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/parser.model')
    parser = Parser()
    parser.load(par_model_path)
    arcs = parser.parse(words_list, postags_list)
    parser.release()
    arcs_list = list(arcs)
    return arcs_list


# jieba分词
# 公安部 / 将 / 1712 / 名涉 / 黑涉 / 恶 / 逃犯 / 列为 / “ / 清零 / ” / 行动 / 目标 / 逃犯
def get_words_by_jieba(sent):
    words_list = list()
    words = jieba.cut(sent)
    words_list = list(words)
    return words_list


# jieba分词并标注词性
def get_postags_by_jieba(words_list):
    postags_list = list()
    sent = ''
    for word in words_list:
        sent += word
    words = jieba.posseg.cut(sent, use_paddle=True)
    for word, flag in words:
        postags_list.append(flag)
    return postags_list


# 处理段落content
def process_content(content):
    sentences = get_sentences(content)
    print('\n'.join(sentences))
    print('\n')
    subsents = list()
    for sentence in sentences:
        subsents = get_subsents(sentence)
        print(' / '.join(subsents))
    print('\n')
    print('pyltp:')
    pyltp_words_list = get_words_by_pyltp(sentences[0])
    print(' / '.join(pyltp_words_list))
    # print('jieba:')
    # jieba_words_list = get_words_by_jieba(subsents[0])
    # print(' / '.join(jieba_words_list))
    # print('\n')
    # print(get_wordpos_by_jieba(pyltp_words_list))
    pyltp_postags_list = get_postags_by_pyltp(pyltp_words_list)
    print(pyltp_postags_list)
    print(get_entity_by_pyltp(pyltp_words_list, pyltp_postags_list))
    print(' / '.join(i.relation for i in get_parser_by_pyltp(pyltp_words_list, pyltp_postags_list)))
    return


def main():
    test_content = '''
    据韩联社12月28日反映，美国
        防部发言人杰夫·莫莱尔27日表示：美国防部长盖 茨将
    于2011年1月14日访问韩国。盖茨原计划从   
    
    明年1月9日至14日陆续访问中国和日本，目前，他决定在行程     
    中增加对韩国的访问;莫莱尔表示，盖茨在访韩期间将会晤韩国国
    防部长官金宽镇，就朝鲜近日的行动交换意见，同时商讨加强韩美两军同盟关系等问题，
    拟定共同应对朝鲜挑衅和核计划的方案。
    '''
    test_content2 = '''
    甲吃了饭。
    乙没吃饭。
    吃了饭可以玩。
    没吃饭不能玩。
    '''
    test_content3 = '''
    公安部近日组织全国公安机关开展扫黑除恶
    追逃“清零”行动。公安部将1712名涉黑涉恶
    逃犯列为“清零”行动目标逃犯，逐一明确追
    逃责任人，实行挂账督捕，并对13名重点在
    逃人员发布A级通缉令↓见到这些人请报警，
    转发扩散！
    '''
    process_content(test_content3)
    return


if __name__ == '__main__':
    main()
