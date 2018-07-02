from Main import get_score

with open('111') as f:
    count = 0
    for temp in f.readlines():
        temp = temp.split(",")
        sentence = temp[1]
        score = get_score(sentence)
        if score >0:
            score = 1
        elif score < 0:
            score = -1
        else:
            score = 0
        print(score)

