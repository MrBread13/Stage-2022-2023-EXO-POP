import json
import openai
import Levenshtein
import itertools
from time import sleep
import get_paragraph_labels_16k as pgc
import split_paragraph_16k as sp
import get_complete_act_labels as gett
from fix_labels import sanitize_labels

file = open("donnees-test.json", "r")
data = json.load(file)
file.close()

# first we need to split the text in paragraphs


def split_text(text_to_split):
    splitted = sp.split_text(text_to_split)
    return splitted


def get_labels(text):
    labels = pgc.get_labels(text)
    return labels



one_shot_levenshtein_history = []
few_shot_levenshtein_history = []
one_shot_errors_history = {}
few_shot_errors_history = {}
one_shot_error_count = []
few_shot_error_count = []

iter = 0

already_done = []
labels_history = {}
with open('donnees-test-labels-gpt35-paragraph-16k.json', 'r') as f:
    labels_history = json.load(f)
for i in labels_history.keys():
    already_done.append(i)
print('total already done : ', len(already_done))


for i, name in enumerate(data):
    if name in already_done:
        continue
    iter += 1
    print('==================================')
    print('Now testing : ', name)
    print('==================================')

    text = data[name]['texte']
    if 'divorce' in text:
        continue
    reference = data[name]['questions']

    # one_shot_tags = gett.labels_from_act(text)
    # #print('one_shot_tags : ', one_shot_tags)
    # distances = 0
    # errors = 0
    # # for key in reference.keys():
    # #     reference[key] = reference[key].replace('-\n', '').replace('\n', ' ')
    # for key in reference.keys():
    #     ####Patch for Boolean, temporary
    #     if isinstance(reference[key], bool):
    #         continue
    #     ################################
    #     if key not in one_shot_tags.keys():
    #         one_shot_tags[key] = ''
    # key_to_remove = []
    # for key in one_shot_tags.keys():
    #     if key not in reference.keys():
    #         key_to_remove.append(key)
    # for key in key_to_remove:
    #     one_shot_tags.pop(key, None)

    # labels = one_shot_tags

    #     distance = Levenshtein.distance(one_shot_tags[key], reference[key])
    #     if distance > 5 or (one_shot_tags[key] == '' and reference[key] != ''):
    #         #print(key, distance, one_shot_tags[key] if one_shot_tags[key] != '' else 'VIDE', reference[key] if reference[key] != '' else 'VIDE')
    #         errors += 1
    #         #one_shot_errors_history[name] = {}
    #         if name not in one_shot_errors_history.keys():
    #             one_shot_errors_history[name] = {}
    #         one_shot_errors_history[name][errors] = {}
    #         err = one_shot_errors_history[name][errors]
    #         err['question'] = key
    #         err['distance'] = distance
    #         err['one_shot_tags'] = one_shot_tags[key]
    #         err['reference'] = reference[key]
    #     distances += distance
    # one_shot_error_count.append(errors)
    # print('============================ Distance one-shot :' , distances)
    # print('============================ Errors one-shot :' , errors)
    # one_shot_levenshtein_history.append(distances)

    splitted = split_text(text)
    # print('splitted : ', splitted)
    labels = get_labels(splitted)
    print('labels : ', labels)
    # extract labels into a list
    dic = {}
    for key in labels.keys():
        # print('key : ', key)
        if key == 'p4':
            if ('Nom-mari' in dic.keys()) and ('Prenom-mari' in dic.keys()) and ('Nom-mariee' in dic.keys()) and ('Prenom-mariee' in dic.keys()):
                continue
        for bkey in labels[key].keys():
            # print('bkey : ', bkey)
            dic[bkey] = labels[key][bkey]
    labels = dic
    if 'Pays-residence-pere-mari' not in labels.keys():
        labels['Pays-residence-pere-mari'] = ''
    if 'Pays-residence-pere-mariee' not in labels.keys():
        labels['Pays-residence-pere-mariee'] = ''
    for key in reference.keys():

        # Patch for Boolean, temporary
        if isinstance(reference[key], bool):
            continue
        ################################

        if key not in labels.keys():
            labels[key] = ''

    labels = sanitize_labels(labels)
    #print(labels)
    #print('labels : ', labels['Jour-mariage'])

    labels_history[name] = labels
    # store labels_history in json file
    with open('donnees-test-labels-gpt35-paragraph-16k.json', 'w') as outfile:
        json.dump(labels_history, outfile, indent=4)

    # distances = 0
    # errors = 0
    # for key in reference.keys():

    #     ####Patch for Boolean, temporary
    #     if isinstance(reference[key], bool):
    #         continue
    #     ################################

    #     reference[key] = reference[key].replace('-\n', '').replace('\n', ' ')
    # for key in reference.keys():

    #     ####Patch for Boolean, temporary
    #     if isinstance(reference[key], bool):
    #         continue
    #     ################################

    #     distance = Levenshtein.distance(labels[key], reference[key])
    #     if (distance >= min(5, len(labels[key]) // 2) and distance != 0) or (labels[key] == '' and reference[key] != '') or (reference[key] == '' and labels[key] != ''):
    #         errors += 1
    #         #creer un dic pour name si existe pas
    #         if name not in few_shot_errors_history.keys():
    #             few_shot_errors_history[name] = {}
    #         few_shot_errors_history[name][errors] = {}
    #         err = few_shot_errors_history[name][errors]
    #         err['question'] = key
    #         err['distance'] = distance
    #         err['one_shot_tags'] = labels[key]
    #         err['reference'] = reference[key]
    #         #print(key, distance, labels[key] if labels[key] != '' else 'VIDE', reference[key] if reference[key] != '' else 'VIDE')
    #     distances += distance
    # few_shot_error_count.append(errors)
    # print('============================ Distance few shot:' , distances)
    # print('============================ Errors few shot:' , errors)
    # few_shot_levenshtein_history.append(distances)

    # #print current mean levenshtein distance
    # if iter % 5 == 0:
    #     # print('============================ Mean distance one-shot :' , sum(one_shot_levenshtein_history)/len(one_shot_levenshtein_history))
    #     print('============================ Mean distance few shot :' , sum(few_shot_levenshtein_history)/len(few_shot_levenshtein_history))
    #     # print('============================ Mean errors one-shot :' , sum(one_shot_error_count)/len(one_shot_error_count))
    #     print('============================ Mean errors few shot :' , sum(few_shot_error_count)/len(few_shot_error_count))

    # #write error history in a file
    # # with open('one_shot_errors_history_fixed.json', 'w') as outfile:
    #     # json.dump(one_shot_errors_history, outfile, indent=4)
    # with open('few_shot_errors_history_fixed.json', 'w') as outfile:
    #     json.dump(few_shot_errors_history, outfile, indent=4)
