from pyltp import SentenceSplitter
import os
import jieba
LTP_DATA_DIR = '../ltp_data_v3.4.0'
#LTP_DATA_DIR = input("请输入LTP_DATA_DIR:" + '\n')
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')
from pyltp import *
global segmentor
# import jieba
# jieba.load_userdict('userDict.txt')
labeller =SementicRoleLabeller()
parser = Parser()
segmentor = Segmentor()
# segmentor.load_with_lexicon(cws_model_path, "/Users/huwentao/Desktop/sentiment-analysis/情感分类/algorithm/userDict.txt")
postagger = Postagger()
class pt:
    def __init__(self):
        segmentor.load_with_lexicon(cws_model_path,
                                "userDict.txt")
        #segmentor.load(cws_model_path)
        postagger.load(pos_model_path)
        parser.load(par_model_path)
        labeller.load(srl_model_path)

    def Cws(self,sentence):
        words = list(segmentor.segment(sentence))
        # words = jieba.lcut(sentence)
        return words


    def Pos(self,sentence,words):
    # postagger.load(pos_model_path)
        postags = postagger.postag(words)
    # postagger.release()
        return postags
    def Parser1(self,sentence,words,postags):
    # parser.load(par_model_path)
        arcs = parser.parse(words, postags)
    # parser.release()
        return arcs

    def Srl1(self,sentence,words,postags,arcs):

    # labeller.load(srl_model_path)
        roles = labeller.label(words, postags, arcs)
    # labeller.release()
        return roles


# words = list(segmentor.segment("欧股上周普涨，英、法、德股市周涨幅分别为0.47%、2.98%、3.11"))
# postags = postagger.postag(words)
# arcs = parser.parse(words, postags)
# roles = labeller.label(words, postags, arcs)
#
#
# print('\t'.join(words))
#
# print("\t".join("{0}:{1}".format(arc.head, arc.relation )for arc in arcs ))
#
# for role in roles:
#     print(role.index, "".join(
#         ["{0}:({1},{2})".format(arg.name, arg.range.start, arg.range.end) for arg in role.arguments]
#     ))
# postagger.release()
# segmentor.release()
# parser.release()
# labeller.release()


