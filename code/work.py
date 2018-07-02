import pandas as pd
from AcMachine import *
import jieba
#path = input("输入obejct路径" + '\n')
jieba.load_userdict("../entity/object")
#jieba.load_userdict(path)
import os
import re
from nlp_model import *
import pairs_extraction.nlp as nlp
from pairs_extraction.pairs_extraction import *
from pairs_extraction.Objection_extraction import no_company
def words_extraction(sentence,acp,words):
    list_words = []
    words_list = jieba.lcut(sentence)
    for Word in words_list:
        d = acp.runkmp(Word)
        for i in d.keys():
            if words[i-1] != Word :
                continue
            list_words.append(words[i-1])
    return list_words

def build_acMachine(dir1='../dictionary'):
    List_dic = os.listdir(dir1)
    words = []
    for temp_dic in List_dic:
        DIC_PATH = os.path.join(dir1, temp_dic)
        if os.path.isfile(DIC_PATH) and temp_dic != ".DS_Store":
            temp_words = extraction_words(DIC_PATH)
            words = words + temp_words
    words = list_to_set(words)
    acp = acmation()
    for key in words:
        acp.insert(key)
    acp.ac_automation()
    return words,acp

def build_pos(dir1='../dictionary/pos_dict.txt'):
    temp_words = extraction_words(dir1)
    acp = acmation()
    for key in temp_words:
        acp.insert(key)
    acp.ac_automation()
    return temp_words,acp


def build_neg(dir1='../dictionary/neg_dict.txt'):
    temp_words = extraction_words(dir1)
    acp = acmation()
    for key in temp_words:
        acp.insert(key)
    acp.ac_automation()
    return temp_words,acp


if __name__ == '__main__':
    # name_temp = ['pairs']
    # dic = dict.fromkeys(name_temp,[0]*534)
    # temp_data = pd.DataFrame.from_dict(dic)
    read_csv = pd.read_csv('../singleEntity/test_data.csv')
    # read_csv = pd.concat([read_csv,temp_data],axis=1)
    # read_csv.columns = ['index', 'sentence', 'entity', 'Score', 'Score2', 'pair']
    words,acp = build_acMachine()
    pos_words, pos_acp = build_pos()
    neg_words, neg_acp = build_neg()
    fc_temp = nlp.pt()
    for i, sentence in enumerate(read_csv.iloc[:,1]):
        entity = read_csv.iloc[:,2][i]
        sign_temp = 0
        sentence = re.sub(r'\D{2}证券:', '证券:', sentence)
        for temp in no_company:
            if temp in sentence:
                sign_temp = 1
                read_csv.iloc[i, -2] = 0
                break
        if sign_temp ==1:
            continue
        list_words = words_extraction(sentence,acp,words)
        P = Object_Extraction(sentence, list_words, fc_temp)
        for temp_tuple in P:
            if entity in temp_tuple:
                read_csv.iloc[i, -1] = temp_tuple
                temp = temp_tuple.strip('()')
                temp = temp.split(',')
                word = temp[1]
                d_pos = pos_acp.runkmp(word)
                d_neg = neg_acp.runkmp(word)
                if d_pos :
                    read_csv.iloc[i,-2] = 1
                    break
                elif d_neg:
                    read_csv.iloc[i,-2] = -1
                    break
        if i !=0 and not i%10:
            read_csv.to_csv('../singleEntity/test_data_change')













