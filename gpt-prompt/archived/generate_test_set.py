import json
import openai
import Levenshtein
import itertools
from time import sleep
import get_paragraphs_labels as pgc
import split_paragraph as sp
import get_complete_act_labels as gett

file = open("donnees-train.json", "r")
data = json.load(file)
file.close()

file = open("testset.json", "r")
testset = json.load(file)
already_tested = list(testset.keys())
file.close()

file = open("template.json", "r")
template = json.load(file)
file.close()

#first we need to split the text in paragraphs

def split_text(text_to_split):
    splitted = sp.split_text(text_to_split)
    return splitted

def get_labels(text):
    labels = pgc.get_labels(text)
    return labels

i = 0
for i, name in enumerate(data):
    
    if name in already_tested:
        continue

    print('==================================')
    print('Now testing : ', name)
    print('==================================')

    text = data[name]['texte']

    splitted = split_text(text)
    print('splitted : ', splitted)

    labels = get_labels(splitted)


    dic = {}
    for key in labels.keys():
        for bkey in labels[key].keys():
            dic[bkey] = labels[key][bkey]
    labels = dic

    for key in template.keys():
        if key not in labels.keys():
            labels[key] = ''

    print('labels : ', labels)

    act_dict = {}
    act_dict['texte'] = text
    act_dict['questions'] = labels
    testset[name] = act_dict
    i+=1
    if i % 2 == 0:
        file = open("testset.json", "w")
        json.dump(testset, file, indent=4)
        file.close()
        print('saved')
        sleep(5)
        print("Just labelled 10 acts !")
        
