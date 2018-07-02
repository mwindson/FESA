import pandas as pd
import re
import os
import sys
sys.path.append("..")
from AcMachine import *
from nlp_model import *
global dic1,dict2
dic1 = set()
dic2 = set()
no_company = ['东方财富网','中国新能源','我国新能源','全国新能源','宝石','中国银行业','老百姓','机器人','太平洋','中国高科技','长白山','祁连山','太阳能','跨太平洋','爱茉莉太平洋']

def cut_sentence(content):
    cut = u"[。？！]"
    temp = re.split(cut, content)
    return temp


def add_dict2(dictfile):
    f_dict = open(dictfile, 'r', encoding='utf-8')
    temp = f_dict.read().split("\n")
    count = 0
    for i in temp:
        name1 = i.split(',')[2]
        if name1 =="公司简称":
            continue
        name1 = ''.join(name1.split())
        name1 = name1.replace("*", "")
        name2 = i.split(',')[3]
        count += 1
        global dic1
        dic1.add(name1)
        dic1.add(name2)
    print("The number of dictionary: {0}".format(count))
    f_dict.close()
    return dic1

def add_dict(dictfile):
    f_dict = open(dictfile, 'r', encoding='utf-8')
    temp = f_dict.readlines()
    count = 0
    for i in temp:
        name = i.split('\t')[2]
        name = ''.join(name.split())
        name = name.replace("*", "")
        count += 1
        global dic2
        if name == "name" :
            continue
        dic2.add(name)
    print("The number of dictionary: {0}".format(count))
    f_dict.close()
    return dic2

def search(file, root_dir, acp, keys):
    temp = pd.read_csv(file)
    f_name = file.split(r"/")[-1]
    title = temp['title'][0]
    news_dic = []
    content = temp['content'][0]
    cutting_sentence = cut_sentence(content)
    count = 0
    for i,  sentence in enumerate(cutting_sentence):
        if '责任编辑' in sentence:
             break
        sentence = re.sub(r'\D{2}证券:', '证券:', sentence)
        sign = False
        for No_company in no_company:
            if No_company in sentence:
                sign = True
                break
        if sign:
            break
        d = acp.runkmp(sentence)
        for i in d.keys():
            sign = False
            for No_company in no_company:
                if keys[i-1] in No_company:
                    sign = True
                    break
            if sign:
                continue
            temp_tuple = "({0},{1},{2})".format(keys[i-1], sentence, count)
            news_dic.append(temp_tuple)
        count += 1

    if news_dic:
        file_name = root_dir + r"/result/" + f_name
        f_result = open(file_name, "w", encoding='utf-8')
        f_result.write(title+'\n')
        f_result.close()
        f_result = open(file_name, "a", encoding='utf-8')
        seq = '\n'
        f_result.write(seq.join(news_dic))
        f_result.close()
        print("end")

#实体数量抽取
def object_number():
    root_dir = '../../alldata'
    out_path = '../../result'
    List = os.listdir(root_dir)
    keys, acp = entity_build()
    single = 0
    many = 0
    for file in List:
        if file =='.DS_Store':
            continue
        file_path = os.path.join(root_dir, file)
        f = pd.read_csv(file_path)
        content = f.iloc[0, 5]
        d = acp.runkmp(content)
        count = 0
        for i in d.keys():
            sign = False
            for No_company in no_company:
                if keys[i-1] in No_company:
                    sign = True
                    break
            if not sign:
                count += 1
        if count == 0 :
            continue

        elif count == 1:
            Path = os.path.join(out_path, 'single')
            single += 1
        else:
            Path = os.path.join(out_path, 'many')
            many += 1

        if not os.path.exists(Path):
            os.makedirs(Path)
        Path = os.path.join(Path, file)
        if single <=100 or many <= 100:
            f.to_csv(Path)
        else:
            break










def main1():
    root_dir = input("输入当前路径:")
    dictionary_file = input("输入字典company路径：")
    dictionary_file1 = input("输入字典tushare_data路径：")
    isExists = os.path.exists(root_dir + r"/result")
    if not isExists:
        os.mkdir(root_dir+ r"/result")
    List = os.listdir(root_dir)
    global dic1, dic2
    dic1 = add_dict2(dictionary_file)
    dic2 = add_dict(dictionary_file1)
    dictionary = dic1.union(dic2)
    keys = list(dictionary)
    acp = acmation()
    for key in keys:
        acp.insert(key)
    acp.ac_automation()
    for i in range(0, len(List)):
        path = os.path.join(root_dir, List[i])
        if os.path.isfile(path) and List[i] != '.DS_Store':
            search(path, root_dir, acp,keys)
            print(List[i])
    print("........end..........")

if __name__ == "__main__":
    object_number()
