import  jieba
import os
jieba.load_userdict("userDict.txt")
from EmotionWord import *
import re

def get_partial_score(news, weight=1):
    word_list = list(jieba.cut(news))

    pos_dict = {'times': 0, 'score': 0}
    neg_dict = {'times': 0, 'score': 0}

    for (index, word) in enumerate(word_list):
        word_score = 0
        # 判断极性
        if (word in pos_emotion) or (word in pos_envalute):
            word_score += weight
            '''
            两种情况：
            1. 非常 不 好吃
            2. 不是 很 好吃
            需要极性反转
            '''
            if (index - 1 >= 0 and word_list[index - 1] in neg_degree) or (
                    index - 2 >= 0 and word_list[index - 2] in neg_degree):
                word_score = word_score * (-1)

        elif (word in neg_emotion) or (word in neg_envalute):
            word_score -= 1
            '''
            1. 不是 不好
            2. 不是 很 不好
            极性反转
            '''
            if (index - 1 >= 0 and word_list[index - 1] in neg_degree) or (
                    index - 2 >= 0 and word_list[index - 2] in neg_degree):
                word_score = word_score * (-1)
        # 判断程度词
        if index - 1 >= 0:
            # 赫夫曼二叉树，加权路径最小
            if word_list[index - 1] in more_degree or (index - 2 >= 0 and word_list[index - 2] in more_degree):
                word_score = word_score * 2
            elif word_list[index - 1] in ish_degree or (index - 2 >= 0 and word_list[index - 2] in more_degree):
                word_score = word_score * 1.5
            elif word_list[index - 1] in very_degree or (index - 2 >= 0 and word_list[index - 2] in more_degree):
                word_score = word_score * 2.5
            elif word_list[index - 1] in least_degree or (index - 2 >= 0 and word_list[index - 2] in more_degree):
                word_score = word_score * 1.1
            elif word_list[index - 1] in most_degree or (index - 2 >= 0 and word_list[index - 2] in more_degree):
                word_score = word_score * 3

        if word_score > 0:
            # print(word,index)
            pos_dict['times'] += 1
            pos_dict['score'] += word_score
        elif word_score < 0:
            neg_dict['times'] += 1
            neg_dict['score'] += word_score

    return (pos_dict, neg_dict)
def get_score(news):
    score = 0
    middle_dict = get_partial_score(news)
    score += (middle_dict[0]['score']+middle_dict[1]['score'])
    return score

def findst(str):
    st = 0
    if re.search("积极",str):
        st = 1
    elif re.search("消极",str):
        st = -1
    return  st
def acc():
    error = 0
    num = 0
    err=[]
    fileList = os.listdir('标注')
    for file in fileList:
        filename = '标注/%s'%(file)
        print(filename)
        if filename ==  "标注/.DS_Store":
            continue
        with open(filename,'r',encoding='utf-8') as f:
            temp = f.read().split('\n')
            for i , tt in enumerate(temp):
                m = i + 1
                if i % 2 == 0:
                    if i == 0:
                        sentence = tt
                        score = get_score(sentence)
                    else:
                        sentence = tt.split(',')[1]
                        score = get_score(sentence)
                    st = findst(temp[m])
                    if st == -1 and score>0:
                        error+=1
                        mp="({0},{1},{2})".format(sentence, score, st)
                        err.append(mp)
                    elif st == 1and score<0:
                        error+=1
                        mp="({0},{1},{2})".format(sentence, score, st)
                        err.append(mp)
                    elif st == 0 and score!=0:
                        error+=1
                        mp="({0},{1},{2})".format(sentence, score, st)
                        err.append(mp)
                    num+=1
                    print("{0} {1}".format(filename, i))
    print("  rate =",1-error/num)
    print(err)
    return 1-error/num, err

