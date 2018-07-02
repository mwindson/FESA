import os
import random
import shutil
import pandas as pd
import re
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
class senAnalysis:
    def __init__(self):
        pass
    #随机挑选文章，参数是输入路径，输出路径，文章个数
    def random_files(self,input, output, numbers):
        list_files = os.listdir(input)
        for i in range(int(numbers)):
            file_name = list_files[int((len(list_files)-1)*random.random())]
            raw_file = os.path.join(input, file_name)
            if not os.path.exists(output):
                os.makedirs(output)
            new_file = os.path.join(output, file_name)
            shutil.copyfile(raw_file, new_file)

    #利用AC自动机查找元素
        #在一个字符串里查找是否由元素在某个列表里
    def AcMachine(self,sentence, list_words):
        class node:
            def __init__(self, ch):
                self.ch = ch  # 结点值
                self.fail = None  # Fail指针
                self.tail = 0  # 尾标志：标志为 i 表示第 i 个模式串串尾
                self.child = []  # 子结点
                self.childvalue = []  # 子结点的值

        # AC自动机类
        class acmation:
            def __init__(self):
                self.root = node("")  # 初始化根结点
                self.count = 0  # 模式串个数

            # 第一步：模式串建树
            def insert(self, strkey):
                self.count += 1  # 插入模式串，模式串数量加一
                p = self.root
                for i in strkey:
                    if i not in p.childvalue:  # 若字符不存在，添加子结点
                        child = node(i)
                        p.child.append(child)
                        p.childvalue.append(i)
                        p = child
                    else:  # 否则，转到子结点
                        p = p.child[p.childvalue.index(i)]
                p.tail = self.count  # 修改尾标志

            # 第二步：修改Fail指针
            def ac_automation(self):
                queuelist = [self.root]  # 用列表代替队列
                while len(queuelist):  # BFS遍历字典树
                    temp = queuelist[0]
                    queuelist.remove(temp)  # 取出队首元素
                    for i in temp.child:
                        if temp == self.root:  # 根的子结点Fail指向根自己
                            i.fail = self.root
                        else:
                            p = temp.fail  # 转到Fail指针
                            while p:
                                if i.ch in p.childvalue:  # 若结点值在该结点的子结点中，则将Fail指向该结点的对应子结点
                                    i.fail = p.child[p.childvalue.index(i.ch)]
                                    break
                                p = p.fail  # 否则，转到Fail指针继续回溯
                            if not p:  # 若p==None，表示当前结点值在之前都没出现过，则其Fail指向根结点
                                i.fail = self.root
                        queuelist.append(i)  # 将当前结点的所有子结点加到队列中

            # 第三步：模式匹配
            def runkmp(self, strmode):
                p = self.root
                cnt = {}  # 使用字典记录成功匹配的状态
                for i in strmode:  # 遍历目标串
                    while i not in p.childvalue and p is not self.root:
                        p = p.fail
                    if i in p.childvalue:  # 若找到匹配成功的字符结点，则指向那个结点，否则指向根结点
                        p = p.child[p.childvalue.index(i)]
                    else:
                        p = self.root
                    temp = p
                    while temp is not self.root:
                        if temp.tail:  # 尾标志为0不处理
                            if temp.tail not in cnt:
                                cnt.setdefault(temp.tail)
                                cnt[temp.tail] = 1
                            else:
                                cnt[temp.tail] += 1
                        temp = temp.fail
                return cnt
        acp = acmation()
        for key in list_words:
            acp.insert(key)
        acp.ac_automation()
        d = acp.runkmp(sentence)
        find_words = []
        for i in d.keys():
            find_words.append(list_words[i-1])
        return find_words

    #读取csv格式字典，并将其变成set集合,csv文件列表，列名为【'公司代码'，'公司简称'，''】
    def add_dic(self,Path):
        f = pd.read_csv(Path,index_col='公司代码')
        Dic = set()
        f_company = f.columns[0]
        cp_name = f[f_company]
        for name in cp_name:
            Dic.add(name)
        print("The number of dictionary: {0}".format(len(cp_name)))
        return Dic

    #将集合转换成列表
    def set_to_list(self, Set_temp):
        b = set(Set_temp)
        c = [i for i in b]
        return c

    #分句,输入是一篇文章，输出是句子列表
    def cut_sentence(self, content):
        cut = u'[。？！\n]'
        temp = re.split(cut, content)
        return temp

    # 搜索实体 输入是一篇文章内容，输出为dataframe【句子，实体】
    def search_entity(self,content,list_entity):
        f = senAnalysis()
        list_sentence = f.cut_sentence(content)
        output_list = []
        for sentence in list_sentence:
            find_entity = f.AcMachine(sentence,list_entity)
            if find_entity:
                for entity in find_entity:
                    output_list.append([sentence, entity])
        temp = pd.DataFrame(output_list,columns=['sentence', 'entity'])
        return temp

    # 搜索情感词 输入是一篇文章内容，输出为dataframe[句子，情感词列表]
    def search_senWords(self):
        pass

    #归一化,将分数小于0的归为-1，大于0的归为1
    def normalize(self,test, Column):
        q = test[Column].apply(lambda x: 1 if x > 0 else x)
        test[Column] = q
        q = test[Column].apply(lambda x: -1 if x < 0 else x)
        test[Column] = q
        return test

    # 计算准确率等四项指标
    def get_exp(self,y_pre, y_true, target_name):
        print(classification_report(y_true, y_pre, target_names=target_name))
        print('accuracy = {0}'.format(accuracy_score(y_true, y_pre)))

    #打分，计算一句话中情感词的分数，使用默认的情感词典
    def get_score(self,sentence):
        pass






