import pandas as pd
import re
import os
from AcMachine import *

def extraction_words(path):
    with open(path) as f:
        temp = f.readlines()
    dic = []
    for word in temp:
        word = word.strip('\n')
        dic.append(word)
    return dic

def cut_sentence(content):
    cut = u"[。？！\n]"
    temp = re.split(cut, content)
    return temp

def list_to_set(dic):
    b = set(dic)
    c = [i for i in b]
    return c

def build_senDic(path):
    List_dic = os.listdir(path)
    words = []
    for temp_dic in List_dic:
        DIC_PATH = os.path.join(path, temp_dic)
        if os.path.isfile(DIC_PATH) and temp_dic != ".DS_Store":
            temp_words = extraction_words(DIC_PATH)
            words = words + temp_words
    words = list_to_set(words)
    acp = acmation()
    for key in words:
        acp.insert(key)
    acp.ac_automation()
    return words, acp

def entity_build():
    #实体表地址
    entity_path = '../entity/object'
    with open(entity_path) as f:
        temp = f.readlines()
        temp = ''.join(temp).strip('\n')
        temp = temp.split('\n')
        acp = acmation()
        for entity in temp:
            acp.insert(entity)
        acp.ac_automation()
    return temp, acp


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
