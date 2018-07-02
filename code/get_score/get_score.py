import os
import pandas as pd
very_degree = ['非常','重大','不过', '不少', '不胜', '惨', '沉', '沉沉', '出奇', '大为', '多', '多多', '多加', '多么', '分外', '格外', '够瞧的', '够戗', '好', '好不', '何等', '很', '很是', '坏', '可', '老', '老大', '良', '颇', '颇为', '甚', '实在', '太', '太甚', '特', '特别', '尤', '尤其', '尤为', '尤以', '远', '着实', '曷', '碜']
no_words = ['缺少','不','甭','勿','别','未','反','没','否','木有','非','无','请勿','无须','并非','毫无','决不','休想','永不','不要','未尝','未曾','毋','莫','从未','从未有过','尚未','一无','并未','尚无','从没','绝非','远非','切莫','绝不','毫不','禁止','忌','拒绝','杜绝','弗']
#输入为评价对象对列表
def rull_score0(word,list_words,neg_acp):
    score = 0
    word_index = list_words.index(word)
    pre_word = list_words[word_index-1]
    if list_words[word_index] == word:
        after_word = ''
    if pre_word in very_degree:
        score = 2
    elif pre_word in no_words or  neg_acp.runkmp(pre_word) or neg_acp.runkmp(after_word):
        score = -1
    else:
        score = 1
    return score

def rull_score1(word,list_words,pos_acp):
    score = 0
    word_index = list_words.index(word)
    pre_word = list_words[word_index - 1]
    if list_words[word_index] == word:
        after_word = ''
    if pre_word in very_degree:
        score = -2
    elif pre_word in no_words or pos_acp.runkmp(pre_word) or pos_acp.runkmp(after_word):
        score = +1
    else:
        score = -1
    return score


def get_score(pairs_dic, pos_acp, neg_acp, file_path,fc_temp):
    # file_temp = pd.read_csv(file_path + '/senWords_extraction', index_col='Unnamed: 0')
    for i,temp in enumerate(pairs_dic):
        if temp[-1] == 0:
            # file_temp.iloc[i, -1] = 0
            continue
        pairs = temp[-2]
        score_temp = 0
        for pair in pairs:
            senword = pair[-1]
            word = senword[-1]
            if word in no_words:
                score_temp -= 0.5
                continue
            d_pos = pos_acp.runkmp(word)
            d_neg = neg_acp.runkmp(word)
            list_words = fc_temp.Cws(temp[0])
            if d_pos:
                score_temp += rull_score0(word, list_words, neg_acp)
            elif d_neg:
                score_temp += rull_score1(word, list_words, pos_acp)
        if score_temp > 0 :
            score_temp = 1
        elif score_temp < 0 :
            score_temp = -1
        temp[-1] = score_temp
        # file_temp.iloc[i,-1] = score_temp
    result = pairs_dic
    entity_score = {}
    for result_temp in result:
        entity = result_temp[1]
        score = result_temp[-1]
        if entity not in entity_score:
            entity_score[entity] = score
        else:
            entity_score[entity] += score
    tt =[]
    for t in entity_score.keys():
        v =entity_score[t]
        m =[t,v]
        tt.append(m)

    temp = pd.DataFrame(tt, columns=['entity', 'score'])
    file_name = os.path.join(file_path, 'SentimentClassification')
    temp.to_csv(file_name)
    # file_temp.to_csv(file_path + '/senWords_extraction')
    print("{0} save score ".format(file_name))
    return result




