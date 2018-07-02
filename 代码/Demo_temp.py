from nlp_model import *
from 实体抽取.entity_search import *
from 情感词抽取.Sentiment_words_Extraction import *
from 评价对象对抽取.pairs_extraction import *
from 打分.get_score import *
def init():
    input_path = input("输入文件夹地址\n")
    # input_path = '../100/single'
    output_path = input("输出文件夹地址\n")
    # output_path = '../demo/result/single'
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


if __name__ == '__main__':
    input_path, output_path, SenWords, SenAcp, fc_temp = init()
    pos_words, pos_acp = build_pos()
    neg_words, neg_acp = build_neg()
    file_list = os.listdir(input_path)
#    File_list = os.listdir(output_path)
    file_number = 0
    for file in file_list:
        if file == '.DS_Store':
            continue
        print('*************start**************')
        print(file)
        file_output = bulid_dir(file,output_path)
        file_path = os.path.join(input_path,file)
        f = pd.read_csv(file_path)
        content = f['content'][0]
        if len(str(content)) < 10 :
            continue
        content_list = cut_sentence(content)
        #实体抽取，利用AC自动机 输出格式为 [[sentence1,entity1],[sentence2,entity2]]
        entity_list, acp = entity_build()
        entity_dic = entity_search(content_list, entity_list, acp, file_output)
        if not entity_dic:
            continue
        #情感词抽取,输出格式为[[sentence,entity,SenWords]],无情感词句子极性为0
        senwords_dic = sentiment_word_Extraction(entity_dic,SenWords,SenAcp,file_output,fc_temp)
        #评价对象对抽取，输出格式为[[sentence,entity,SenWords,pairs]],无pairs对句子极性为0
        pairs_dic = pairs_extraction(senwords_dic, fc_temp, entity_list, acp)
        #打分计算
        result = get_score(pairs_dic, pos_acp, neg_acp, file_output, fc_temp)
        file_number += 1
        print(file_number)
        print('*************end***************')





        











