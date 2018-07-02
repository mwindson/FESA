import os
import pandas as pd
def read_csv():
    input_path = '../single'
    list_dir = os.listdir(input_path)
    tt = []
    for file_name in list_dir:
        if file_name == '.DS_Store':
            continue
        file_path = os.path.join(input_path,file_name)
        doc_dir = os.listdir(file_path)
        if not doc_dir:
            continue
        path1 = os.path.join(file_path, 'SentimentClassification')
        temp1 = pd.read_csv(path1, index_col='Unnamed: 0')
        print('start')
        print(file_name)
        entity_score = {}
        for i in range(len(temp1)):
            entity = temp1.iloc[i, :].entity
            score = temp1.score[i]
            if entity not in entity_score:
                entity_score[entity] = int(score)
            else:
                entity_score[entity] += int(score)

        for t in entity_score.keys():
            v = entity_score[t]
            m = [t, v]
            tt.append(m)
        print(file_name)
    temp = pd.DataFrame(tt, columns=['entity', 'pre_score'])
    file_name = os.path.join(input_path, 'result')
    temp.to_csv(file_name + '.csv')
    print('end')


def change():
    input_path = '../single'
    input2_path = '../2single'
    list_dir = os.listdir(input_path)
    list_dir2 = os.listdir(input2_path)
    for file_name in list_dir:
        if file_name == '.DS_Store' or file_name not in list_dir2:
            continue
        file_path = os.path.join(input_path,file_name)
        doc_dir = os.listdir(file_path)
        if not doc_dir:
            continue
        path1 = os.path.join(file_path, 'entity_extraction')
        path2 = os.path.join(file_path, 'senWords_extraction')
        temp1 = pd.read_csv(path2, index_col='Unnamed: 0')
        temp2 = pd.read_csv(path1, index_col='Unnamed: 0')
        temp2.index = temp1.index
        temp2.to_csv(path1)
        print(file_name)

if __name__ == '__main__':
    read_csv()


