import sys
sys.path.append("..")
from AcMachine import *
#path = input("输入obejct路径" + '\n')
#jieba.load_userdict("../entity/object")
#jieba.load_userdict(path)
import os
from nlp_model import *
def search3(file,root_dir,acp, words):
    f_name = file.split(r"/")[-1]
    with open(file,'r') as f:
        temp = f.readlines()
        temp = temp[1:]
        tumple_temp = set()
        for tt in temp:
            tt = tt.strip("\n")
            t = tt.strip("()")
            tumple_num = t.split(",")
            t = tumple_num[1]
            list_words = []
            words_list = jieba.lcut(t)
            for Word in words_list:
                d = acp.runkmp(Word)
                for i in d.keys():
                    if words[i-1] != Word :
                        continue
                    list_words.append(words[i-1])
            if list_words:
                list_words = ",".join(list_words)
                list_words = "sentiment_words: " + "[" + list_words + "]"
                add_tuple = "({0},sentence:{1},{2})".format(tumple_num[0],tumple_num[1],list_words)
                tumple_temp.add(add_tuple)
        if tumple_temp:
            file_name = root_dir + r"/result/" + f_name
            f_result = open(file_name, "a", encoding='utf-8')
            seq = '\n'
            f_result.write(seq.join(tumple_temp))
            f_result.close()

def main2():
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
        if os.path.isfile(path)  and List[i] != ".DS_Store" and List[i] != "changeitem.py":
            search3(path, root_dir,acp, words)
            print(i)
    print("-----end------")

#输入为 [句子，实体]表，情感词表，acp,输出目录
def sentiment_word_Extraction(entity_dic, SenWords, SenAcp, file_path, fc_temp):
    for sentence in entity_dic:
        sentence_temp = sentence[0]
        list_words = []
        words_list = fc_temp.Cws(sentence_temp)
        for Word in words_list:
            d = SenAcp.runkmp(Word)
            for i in d.keys():
                if SenWords[i - 1] != Word:
                    continue
                list_words.append(SenWords[i - 1])
        if list_words:
            sentence[2] = list_words
        else:
            sentence[-1] = 0
        if len(sentence_temp) > 300:
            sentence[-1] = 0
    file_name = os.path.join(file_path, 'senWords_extraction')
    temp = pd.DataFrame(entity_dic, columns=['sentence', 'entity', 'SenWords', 'pairs', 'polarity'])
    temp.to_csv(file_name)
    print("{0} save senWords ".format(file_name))
    return entity_dic


if __name__ == '__main__':
    main2()
