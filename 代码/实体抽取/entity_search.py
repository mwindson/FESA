import re
import os
import pandas as pd
from AcMachine import *
no_company = ['东方财富网','国新能源','宝石','中国银行业','老百姓','机器人','太平洋','中国高科技','长白山','祁连山','太阳能','跨太平洋','爱茉莉太平洋']

def entity_search(content_list,keys,acp,output_path):

    entity_dic = []
    for i,  sentence in enumerate(content_list):
        if '责任编辑' in sentence:
             break
        sentence = re.sub(r'\D{2}证券：', '证券：', sentence)
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
            temp_tuple = [sentence, keys[i-1], '', '', '']
            entity_dic.append(temp_tuple)

    if entity_dic:
        output_path = os.path.join(output_path, )
        file_name = os.path.join(output_path, 'entity_extraction')
        temp = pd.DataFrame(entity_dic,columns=['sentence', 'entity', 'SenWords', 'pairs', 'polarity'])
        temp.to_csv(file_name)
        print("{0} save entity ".format(file_name))
    else:
        print("No entity")
    return entity_dic