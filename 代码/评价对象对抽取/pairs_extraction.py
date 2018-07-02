from nlp import *
import re
import pandas as pd

target_words = ['保荐', '建议', '关注', '发布', '推荐', '提醒', '看好', '表示', '认为', '迎接']
# def ruleBaseExtraction1(s,o):
#     words = Cws(s)
#     arcs = Parser1(s)
#     roles = Srl1(s)
#     ob_list = []
#     if not bool(roles):
#         return ob_list
#     for role in roles:
#         if words[role.index] == o:
#             for arg in role.arguments:
#                  if re.search("A0", arg.name):
#                      start = arg.range.start
#                      end = arg.range.end + 1
#                      ob_list.append("({0},{1})".format("".join(words[start:end]), words[role.index]))
#     return ob_list
list_NotWords = ['不','非','无','未','不曾','没','毋''莫','否','弗']
def Extraction(pattern,role, words):
    # ob_list = []
    for arg in role.arguments:
        if re.search(pattern, arg.name):
            start = arg.range.start
            end = arg.range.end + 1
            t = "".join(words[start:end])
            return t
    #         ob_list.append("({0},{1})".format("".join(words[start:end]), words[role.index]))
    # return ob_list

def Firest_Extraction(a,b,c,o,roles, words):
     global sign
     for role in roles:
        if words[role.index] == o and sign.iloc[role.index,0] == 0:
            arg_name_list = [arg.name for arg in role.arguments]
            if a in arg_name_list:
                t = Extraction(a, role, words)
            elif b in arg_name_list:
                t = Extraction(b, role, words)
            else:
                t = Extraction(c, role, words)
            sign.iloc[role.index,0] = 1
            return t

def isSBV_Core(s,o,words,arcs):
    for arc in arcs:
        if words[arc.head - 1] == o and arc.relation == "SBV":
            return True
    return False
def isATT_Xs(s,o,words,arcs):
    for i, arc in enumerate(arcs):
        if words[i] == o and arc.relation == "ATT":
            t = words[arc.head - 1]
            return t
    return False
def isCOO_Object(s,o,t,words,arcs,coo_dic):
    temp = ""
    for i, arc in enumerate(arcs):
        if (words[i] in coo_dic or words[arc.head - 1] in coo_dic) and arc.relation == "COO":
            if words[i] in t:
                temp = words[arc.head - 1]
            else:
                temp = words[i]
            if temp in coo_dic:
                continue
            temp = postRull(s,o,temp,words,arcs) + temp
            return temp
    return 0


def find_nearst_n(s, o, words,fc_temp):
    postags = fc_temp.Pos(s,words)
    postags = [pos for pos in postags]
    number = 0
    if o not in words:
        return None
    for i , word in enumerate(words):
        if word == o:
            number = i
            break
    while(number):
        number = number -1
        if postags[number] == 'n' or postags[number] == 'nz':
            t = words[number]
            return t

def Xs_Extraction(s,o,words,arcs):
    for i, arc in enumerate(arcs):
        if words[arc.head - 1] == o and arc.relation == "SBV":
            t = words[i]
            return t

def search_words_tree(s,w, words, arcs):
    temp = None
    for i, arc in enumerate(arcs):
        if words[arc.head - 1] == w:
            temp = words[i]
            return temp
    return  temp


def postRull(s,o,t, words,arcs):
    temp = ""
    for i , arc in enumerate(arcs):
        if words[arc.head - 1] == t and arc.relation == "ATT" and words[i] != o:
            if search_words_tree(s,words[i],words,arcs):
                temp = ""
                temp = temp + search_words_tree(s, words[i], words, arcs)
            temp = temp + words[i]
    return temp



def ruleBaseExtraction(s,o, words, arcs,fc_temp):
    postags = fc_temp.Pos(s,words)
    roles =fc_temp.Srl1(s,words,postags,arcs)
    WC_list = [words[i.index] for i in roles]
    if o in WC_list:
            t = Firest_Extraction("A0", "A1", "A2", o, roles, words)
    elif isSBV_Core(s, o, words, arcs):
        t = Xs_Extraction(s, o, words, arcs)
        t = postRull(s, o, t, words, arcs) + t
    elif isATT_Xs(s, o, words, arcs):
        t = isATT_Xs(s, o, words, arcs)
        t= postRull(s, o, t,words,arcs) + t
    else:
        t = find_nearst_n(s, o,words,fc_temp)
        if not t:
            return t
        t = postRull(s, o, t, words, arcs) + t
    return t



def Object_Extraction(s,Os,fc_temp, appear_entity):
    P = []
    words = fc_temp.Cws(s)
    count = len(words)
    global sign
    dic = dict.fromkeys('f',[0]*count)
    sign = pd.DataFrame.from_dict(dic)
    postags = fc_temp.Pos(s,words)
    arcs = fc_temp.Parser1(s,words,postags)
    for o in Os:
        t = ruleBaseExtraction(s,o, words, arcs,fc_temp)
        if not t:
            continue
        o = NotMeans(s,words,arcs,o)
        result = [t, o]
        coo_dic = {}
        Sign = False
        for entity in appear_entity:
            if entity in t:
                coo_dic[entity] = 1
                Sign = True
        if not Sign:
            coo_dic[t] = 1
        count = 0
        while (isCOO_Object(s, o, t, words, arcs,coo_dic) and count <10):
            t = isCOO_Object(s, o[1], t, words, arcs,coo_dic)
            result2 = [t,o]
            coo_dic[t] = 1
            P.append(result2)
            count += 1
        P.append(result)
    return P

not_No_words = ['是否', '不止']
def NotMeans(sentence,words,arcs,o):
    for word in list_NotWords:
        for temp in words:
            if word in temp:
                if temp in not_No_words:
                    continue
                index_words = words.index(temp)
                o_word_index = (arcs[index_words].head - 1)
                o_words = words[o_word_index]
                if o_words == o:
                    o = [temp,o]
                    return o
    return ['', o]

def Extraction_sentence_words(s):
    s = s.strip("\n")
    s_list = s.split("sentiment_words:")
    entity = s_list[0].split(",sentence:")[0][1:]
    sentence = s_list[0].split(",sentence:")[1]
    words = s_list[1].strip("[]").split(",")
    return entity, sentence, words

def Extraction_sentence_words2(s):
    s = s.strip("\n")
    s_list = s.split("sentiment_words=")
    sentence = s_list[0][2:]
    words = s_list[1].strip("[]").split(",")
    words = [word[0] for word in words]
    return sentence, words

def analysiszq(sentence, fc_temp,sign):
    words = fc_temp.Cws(sentence)
    postages = fc_temp.Pos(sentence,words)
    arcs = fc_temp.Parser1(sentence,words,postages)
    roles = fc_temp.Srl1(sentence,words,postages,arcs)
    for role in roles:
        if words[role.index] in target_words:
            for arg in role.arguments:
                if arg.name =='A0' and ('证券' in words[arg.range.start] or '证券' in words[arg.range.end] ):
                    sign = True
                    return sign
#输入是[sentence,entity,senWords]列表、输出为输入列表上添加评价对象对列表
def pairs_extraction(senwords_dic,fc_temp, entity_list, acp):
    for temp in senwords_dic:
        if temp[-1] == 0:
            continue
        sentence = temp[0]
        appear_entity = []
        d = acp.runkmp(sentence)
        for i in d.keys():
            appear_entity.append(entity_list[i-1])
        entity = temp[1]
        list_words = temp[2]
        if len(appear_entity) > 2:
            temp[3] = [[entity, ['', list_words[-1]]]]
            continue
        temp_P = Object_Extraction(sentence, list_words, fc_temp, appear_entity)
        if '证券' in entity:
            sign = False
            sign = analysiszq(sentence, fc_temp, sign)
            if sign:
                temp[-1] = 0
                continue
        P = []
        for T_P in temp_P:
            target_obejct = T_P[0]
            if entity in target_obejct:
                P.append(T_P)
        if P:
            temp[3] = P
        elif len(list_words) == 1:
            temp[3] = [[entity, ['', list_words[-1]]]]
        else:
            temp[-1] = 0
    pairs_dic = senwords_dic
    return pairs_dic

if __name__ == '__main__':

    # DOC_DIR = "/Users/huwentao/Desktop/sentiment-analysis/FinicialNews/result3"
    # isExists = os.path.exists(DOC_DIR + r"/result")
    # if not isExists:
    #     os.mkdir(DOC_DIR + r"/result")
    # list = os.listdir(DOC_DIR)
    # fc_temp = pt()
    # for i in range(0, len(list)):
    #     path = os.path.join(DOC_DIR, list[i])
    #     if os.path.isfile(path) and list[i] != ".DS_Store":
    #         with open(path) as f:
    #             f.readline()
    #             temp = f.readlines()
    #         P = []
    #         for i, sentence in enumerate(temp):
    #             s, words = Extraction_sentence_words(sentence)
    #             P = P + Object_Extraction(s,words,fc_temp)
    #             print(i)
    #         if P:
    #             file_name = DOC_DIR + r"/result/" + list[i]
    #             f_result = open(file_name, "a", encoding='utf-8')
    #             seq = '\n'
    #             f_result.write(seq.join(P))
    #             f_result.close()
    #             print("end")
    #         print(i)
    # print("-----end------")
   # DOC_DIR = "/Users/huwentao/Desktop/sentiment-analysis/FinicialNews/result/result"
    DOC_DIR = input("请输入目标地址:"+ '\n')
    #DOC_DIR = "/Users/huwentao/Desktop/sentiment-analysis/test/result/result"
    isExists = os.path.exists(DOC_DIR + r"/tuple")
    if not isExists:
        os.mkdir(DOC_DIR + r"/tuple")
    list = os.listdir(DOC_DIR)
    fc_temp = pt()
    list_tuple = os.listdir(DOC_DIR + r"/tuple")
    for i in range(0, len(list)):
        path = os.path.join(DOC_DIR, list[i])
        if os.path.isfile(path) and list[i] != ".DS_Store" and list[i] not in list_tuple:
            with open(path) as f:
                temp = f.readlines()
            all_temp = []
            for m, sentence in enumerate(temp):
                entity, s, words = Extraction_sentence_words(sentence)
                P = Object_Extraction(s,words,fc_temp)
                tuples = "(entity: {0},sentence: {1},sentiment_words: {2},pairs: {3})".format(entity, s, words, P)
                all_temp.append(tuples)
                print("第"+str(m)+"句")
            if all_temp:
                file_name = DOC_DIR + r"/tuple/" + list[i]
                f_result = open(file_name, "a", encoding='utf-8')
                seq = '\n'
                f_result.write(seq.join(all_temp))
                f_result.close()
                print("end")
        print("第"+str(i)+"篇")
    print("-----end------")
    # s = "1.公司的重要优势是廉价的电和劳动力 sentiment_words=[廉价]"
    # s, words = Extraction_sentence_words(s)
    # p= []
    # p = p + Object_Extraction(s, words)
    # print("{0}  sentiment_words = {1}   二元组 = {2}".format(s, words, p))


