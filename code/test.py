from nlp_model import *
from object_extraction.entity_search import *
from senWords_extraction.Sentiment_words_Extraction import *
from pairs_extraction.pairs_extraction import *
from get_score.get_score import *
import jieba
no_words = ['缺少','不','甭','勿','别','未','反','没','否','木有','非','无','请勿','无须','并非','毫无','决不','休想','永不','不要','未尝','未曾','毋','莫','从未','从未有过','尚未','一无','并未','尚无','从没','绝非','远非','切莫','绝不','毫不','禁止','忌','拒绝','杜绝','弗']
jieba.load_userdict("../code/userDict.txt")
def init():
    # input_path = input("输入文件夹地址\n")
    input_path = '../demo/test/'
    # output_path = input("输出文件夹地址\n")
    output_path = '../demo/test/output'
    #加载情感词典,并构建ac自动机
    #情感词典路径
    sen_dic_path = '../dictionary'
    words, acp = build_senDic(sen_dic_path)
    fc_temp  = pt()
    return input_path, output_path, words, acp, fc_temp

def bulid_dir(file,output_path):
    file_output = os.path.join(output_path, file)

    if not os.path.exists(file_output):
        os.makedirs(file_output)

    return file_output

def get_scoring(senwords_dic,fc_temp,pos_acp):
    for sentence in senwords_dic:
        sentence_temp = sentence[0]
        words_list = fc_temp.Cws(sentence_temp)
        list_words = sentence[2]
        entity = sentence[1]
        if sentence[-1]:
            continue
        try:
            entity_index = words_list.index(entity)
        except:
            entity_index = -1
        score = 0
        for words in list_words:
            try:
                words_index = words_list.index(words)
            except:
                words_index = len(list_words)+1
            if entity_index ==words_index:
                entity_index = 1 + words_index
            if pos_acp.runkmp(words):
                if words_list[words_index-1] in no_words:
                    # score += -1/(abs(entity_index-words_index))
                    score += -1
                else:
                    # score += 1 / (abs(entity_index - words_index))
                    score += 1
            elif words_list[words_index-1] in no_words:
                # score += 1 / (abs(entity_index - words_index))
                score +=1
            else:
                # score += -1 / (abs(entity_index - words_index))
                score +=-1
        if score >0:
            sentence[-1] = 1
        elif score <0:
            sentence[-1] = -1
        else:
            sentence[-1] = 0
    return senwords_dic









if __name__ == '__main__':
    input_path, output_path, SenWords, SenAcp, fc_temp = init()
    pos_words, pos_acp = build_pos()
    neg_words, neg_acp = build_neg()
    file_list = os.listdir(input_path)
#    File_list = os.listdir(output_path)
    file_number = 0
    for file in file_list:
        file_number += 1
        if file == '.DS_Store' or file !='test.csv':
            continue
        print('*************start**************')
        print(file)
        file_output = bulid_dir('test',output_path)
        file_path = os.path.join(input_path,file)
        f = pd.read_csv(file_path,index_col=0)
        f['pres'] = None
        entity_list, acp = entity_build()
        for i in f.index:
            content = f.content[i]
            if len(str(content)) < 10 :
                f.loc[i,'pres'] = [0]
                continue
            content_list = cut_sentence(content)
        #实体抽取，利用AC自动机 输出格式为 [[sentence1,entity1],[sentence2,entity2]]
            entity_dic = entity_search(content_list, entity_list, acp, file_output)
            if not entity_dic:
                continue
        # 情感词抽取,输出格式为[[sentence,entity,SenWords]],无情感词句子极性为0
            senwords_dic = sentiment_word_Extraction(entity_dic,SenWords,SenAcp,file_output,fc_temp)
        #
        #
            result = get_scoring(senwords_dic,fc_temp,pos_acp)

        # #评价对象对抽取，输出格式为[[sentence,entity,SenWords,pairs]],无pairs对句子极性为0
        #     pairs_dic = pairs_extraction(senwords_dic, fc_temp, entity_list, acp, pos_acp)
        # #打分计算
        #     result = get_score(pairs_dic, pos_acp, neg_acp, file_output, fc_temp)
        #     number = len(result[0][2])
            pres = []
            for t in range(len(result)):
                pres.append(result[t][4])
            f.loc[i, 'pres'] = pres
            print(i)
            f.to_csv('../demo/test1.csv')
        print('*************end***************')