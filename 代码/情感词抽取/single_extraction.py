import sys
sys.path.append("..")
from nlp_model import *
import pandas as pd
import re
import jieba
import os

path = input("总情感词典路径"+'\n')
# jieba.load_userdict("/Users/huwentao/Desktop/sentiment-analysis/代码/all_dic.txt")
jieba.load_userdict(path)



def search2(file, acp,root_dir,keys):
    temp = pd.read_csv(file)
    f_name = file.split(r"/")[-1]
    title = temp["title"][0]
    content = temp['content'][0]
    st = cut_sentence(content)
    St_Sts = set()
    for t, ss in enumerate(st):
        list_word  = []
        ss = "".join(ss.split())
        if re.search("责任编辑：", ss):
            break
        tp = str(t)
        ss = tp + '.' + ss
        d = acp.runkmp(ss)
        for i in d.keys():
            list_word.append(keys[i-1])
        # if sign == True :
        if d:
            list_words = ",".join(list_word)
            ss = ss + "  " + "sentiment_words=[" + list_words + "]"
            St_Sts.add(ss)
    if St_Sts:
        file_name = root_dir + r"/result3/" + f_name
        f_result = open(file_name, "w", encoding='utf-8')
        f_result.write(title + '\n')
        f_result.close()
        f_result = open(file_name, "a", encoding='utf-8')
        seq = '\n'
        f_result.write(seq.join(St_Sts))
        f_result.close()
        print("end")




if __name__ == '__main__' :
     root_dir = input("输入当前路径:")
     #root_dir = r"/Users/huwentao/Desktop/sentiment-analysis/test/result"
     Dic_path = input("输入情感词典路径:")
     #Dic_path = r"/Users/huwentao/Desktop/sentiment-analysis/dictionary"
     isExists = os.path.exists(root_dir + r"/result")
     if not isExists:
         os.mkdir(root_dir + r"/result")
     List = os.listdir(root_dir)
     List_dic = os.listdir(Dic_path)
     words = []
     for temp_dic in List_dic:
         DIC_PATH = os.path.join(Dic_path, temp_dic)
         if os.path.isfile(DIC_PATH) and temp_dic != ".DS_Store":
             temp_words = extraction_words(DIC_PATH)
             words = words + temp_words
     words = list_to_set(words)
     acp = acmation()
     for key in words:
         acp.insert(key)
     acp.ac_automation()
     for i in range(0, len(List)):
         path = os.path.join(root_dir, List[i])
         if os.path.isfile(path) and List[i] != ".DS_Store" and List[i] != "changeitem.py":
             search2(path,acp, root_dir,words)
             print(i)
     print("-----end------")