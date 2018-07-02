from nlp import *
import re
from EmotionWord import *



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
     for role in roles:
        if words[role.index] == o:
            arg_name_list = [arg.name for arg in role.arguments]
            if a in arg_name_list:
                t = Extraction(a, role, words)
            elif b in arg_name_list:
                t = Extraction(b, role, words)
            else:
                t = Extraction(c, role, words)
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
def isCOO_Object(s,o,t,words,arcs):
    temp = ""
    for i, arc in enumerate(arcs):
        if words[arc.head - 1] == t and arc.relation == "COO":
            temp = words[i]
            temp = postRull(s,o,temp,words,arcs) + temp
            return temp
    return temp


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
        if postags[number] == 'n':
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
        if o in neg_envalute or o in pos_envalute:
            t = Firest_Extraction("A0", "A1", "A2", o, roles, words)
        elif o in neg_emotion or o in pos_emotion:
            t = Firest_Extraction("A1", "A2", "A0", o, roles, words)
        else:
            t = Xs_Extraction(s, o, words, arcs)
            t = postRull(s, o ,t, words, arcs) + t
    elif isSBV_Core(s, o, words, arcs):
        t = Xs_Extraction(s, o, words, arcs)
        t = postRull(s, o, t, words, arcs) + t
    elif isATT_Xs(s, o, words, arcs):
        t = isATT_Xs(s, o, words, arcs)
        t= postRull(s, o, t,words,arcs) + t
    else:
        t = find_nearst_n(s, o,words,fc_temp)
        t = postRull(s, o, t, words, arcs)
    return t



def Object_Extraction(s,Os,fc_temp):
    P = []
    words = fc_temp.Cws(s)
    postags = fc_temp.Pos(s,words)
    arcs = fc_temp.Parser1(s,words,postags)
    for o in Os:
        t = ruleBaseExtraction(s,o, words, arcs,fc_temp)
        if not t:
            continue
        result = "({0},{1})".format(t, o)
        if isCOO_Object(s, o, t, words, arcs):
            temp = isCOO_Object(s, o, t, words,arcs)
            result2 = "({0},{1})".format(temp, o)
            P.append(result2)
        print(result)
        P.append(result)
    return P



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
    DOC_DIR = "/home/huwentao/sentiment-analysis/FinicialNews/result/result"
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


