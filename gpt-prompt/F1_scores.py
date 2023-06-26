import json
import Levenshtein
from typing import List, Dict, Tuple
PER = ['Nom-','Prenom-','Age-']
LOC = ['Ville-','Pays-','-rue-','Departement-']
DATE = ['Jour-','Mois-','Annee-','Minute-','Heure-']
JOB = ['Profession-']

MERE_MARIEE = ['mere-mariee']
PERE_MARIEE = ['pere-mariee']
EX_EPOUX = ['ex-epoux','ex-epouse']
PERE_MARI = ['pere-mari']
MERE_MARI = ['mere-mari']
ADMIN = ['mariage','maire']
MARIEE = ['mariee']
MARI = ['mari']
TEMOIN = ['temoin']



def f1_score (labels : dict, golden : dict, levenshtein_treshold : float) -> dict:
    """
    Compute the F1 score for each entity type
    :param labels: dict of labels
    :param golden: dict of golden labels
    :param levenshtein_treshold: treshold of the max ratio between the levenshtein distance and the length of the golden label to consider the label as correct
    :return: dict of F1 scores
    """
    f1_scores = {
    'PER': {
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0,
        'TN' : 0
    },
    'LOC': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0
    },
    'DATE': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0
    },
    'JOB': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0

    },
    'MERE_MARIEE': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0
    },
    'PERE_MARIEE': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0
    },
    'EX_EPOUX': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0
    },
    'PERE_MARI': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0
    },
    'MERE_MARI': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0
    },
    'ADMIN': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS' : 0
    },
    'MARIEE': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS': 0
    },
    'MARI': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS': 0
    },
    'TEMOIN': {
        'TN' : 0,
        'TOTAL': 0,
        'FN': 0,
        'FP': 0,
        'PARTIAL': 0,
        'TP': 0,
        'MISS': 0
    },
    'TOTAL': 0,
    'FN': 0,
    'FP': 0,
    'PARTIAL': 0,
    'TP': 0,
    'MISS': 0,
    'TN' : 0
}
    for key in golden.keys():

        if isinstance(golden[key], bool):
            continue
         
        f1_scores['TOTAL'] += 1
        #print(key)

        emplacements = []
        for i in PER :
            if emplacements:
                break
            if i in key :
                emplacements.append('PER')
                break
        for i in LOC :
            if emplacements:
                break
            if i in key :
                emplacements.append('LOC')
                break
        for i in DATE :
            if emplacements:
                break
            if i in key :
                emplacements.append('DATE')
                break
        for i in JOB :
            if emplacements:
                break
            if i in key :
                emplacements.append('JOB')
                break

        for i in MERE_MARIEE :
            if len(emplacements) == 2 :
                break
            if i in key :
                emplacements.append('MERE_MARIEE')
                break
        for i in PERE_MARIEE :
            if len(emplacements) == 2 :
                break
            if i in key :
                emplacements.append('PERE_MARIEE')
                break
        for i in EX_EPOUX :
            if len(emplacements) == 2 :
                break
            if i in key :
                emplacements.append('EX_EPOUX')
                break
        for i in PERE_MARI :
            if len(emplacements) == 2 :
                break
            if i in key :
                emplacements.append('PERE_MARI')
                break
        for i in MERE_MARI :
            if len(emplacements) == 2 :
                break
            if i in key :
                emplacements.append('MERE_MARI')
                break
        for i in ADMIN :
            if len(emplacements) == 2 :
                break
            if i in key :
                emplacements.append('ADMIN')
                break
        for i in MARIEE :
            if len(emplacements) == 2 :
                break
            if i in key :
                emplacements.append('MARIEE')
                break
        for i in MARI :
            if len(emplacements) == 2 :
                break
            if i in key :
                emplacements.append('MARI')
                break
        
        for i in TEMOIN:
            if len(emplacements) == 2:
                break
            if i in key :
                emplacements.append('TEMOIN')
                break
        


        #print(emplacements)

        f1_scores[emplacements[0]]['TOTAL'] += 1
        f1_scores[emplacements[1]]['TOTAL'] += 1
        if key in labels.keys():

            if not labels[key] and not golden[key]:
                f1_scores[emplacements[0]]['TN'] += 1
                f1_scores[emplacements[1]]['TN'] += 1
                f1_scores['TN'] += 1
            
            elif labels[key] == golden[key]:
                f1_scores[emplacements[0]]['TP'] += 1
                f1_scores[emplacements[1]]['TP'] += 1
                f1_scores['TP'] += 1

            elif labels[key] and not golden[key]:
                f1_scores[emplacements[0]]['FP'] += 1
                f1_scores[emplacements[1]]['FP'] += 1
                f1_scores['FP'] += 1

            elif not labels[key] and golden[key]:
                f1_scores[emplacements[0]]['FN'] += 1
                f1_scores[emplacements[1]]['FN'] += 1
                f1_scores['FN'] += 1
            elif labels[key] != golden[key]:
                if (Levenshtein.distance(labels[key], golden[key]) // len(golden[key])) < levenshtein_treshold:
                    f1_scores[emplacements[0]]['PARTIAL'] += 1
                    f1_scores[emplacements[1]]['PARTIAL'] += 1
                    f1_scores['PARTIAL'] += 1
                else:
                    f1_scores[emplacements[0]]['MISS'] += 1
                    f1_scores[emplacements[1]]['MISS'] += 1
                    f1_scores['MISS'] += 1
        else:
            f1_scores[emplacements[0]]['FN'] += 1
            f1_scores[emplacements[1]]['FN'] += 1
            f1_scores['FN'] += 1

    return f1_scores


def test():
    golden_set = {}
    labels_set = {}

    with open('donnees-test.json', 'r') as file:
        golden_set = json.load(file)

    with open('donnees-test-labels-gpt35-paragraph-16k.json', 'r') as file:
        labels_set = json.load(file)

    results = {}
    for archive in golden_set.keys():
        if archive not in labels_set.keys():
            #print('Archive ' + archive + ' not found in labels_set')
            continue

        f1_scores = f1_score(labels_set[archive], golden_set[archive]['questions'], 0.5)
        results[archive] = f1_scores
    #print(results)

    #dump json file
    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)
    #print('--------------------------------------------')


def precision_recall(labels : dict, weight : float, count_tn : bool) -> dict:
    scores = {}
    for archive in labels.keys():
        scores[archive] = { name :{'F1_strict' : 0, 'F1_weighted' : 0, 'F1_ok' : 0} for name in ['PER', 'LOC', 'DATE', 'JOB', 'MERE_MARIEE', 'PERE_MARIEE', 'EX_EPOUX', 'PERE_MARI', 'MERE_MARI', 'ADMIN', 'MARIEE', 'MARI', 'TEMOIN']}

        if not count_tn:
            for tag in scores[archive].keys():

                
                #strict mode
                precision_strict = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ) == 0 else (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ))
                recall_strict = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ) == 0 else (labels[archive][tag]['TP'] + labels[archive][tag]['TN']  / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ))
                f1_strict = 0 if (precision_strict + recall_strict) == 0 else 2 * (precision_strict * recall_strict) / (precision_strict + recall_strict)

                #weighted mode
                precision_weighted = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + weight * labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + weight * labels[archive][tag]['PARTIAL'] )/ (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + weight * labels[archive][tag]['PARTIAL'] ))
                recall_weighted = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + weight * labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + weight * labels[archive][tag]['PARTIAL'])  / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + weight * labels[archive][tag]['PARTIAL'] ))
                f1_weighted = 0 if (precision_weighted + recall_weighted) == 0 else 2 * (precision_weighted * recall_weighted) / (precision_weighted + recall_weighted)

                #ok mode
                precision_ok = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['PARTIAL']) / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ))
                recall_ok = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['PARTIAL'])  / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ))
                f1_ok = 0 if (precision_ok + recall_ok) == 0 else 2 * (precision_ok * recall_ok) / (precision_ok + recall_ok)

                scores[archive][tag]['F1_strict'] = f1_strict
                scores[archive][tag]['F1_weighted'] = f1_weighted
                scores[archive][tag]['F1_ok'] = f1_ok

            precision_strict = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ) == 0 else (labels[archive]['TP'] + labels[archive]['TN'] / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ))
            recall_strict = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ) == 0 else (labels[archive]['TP'] + labels[archive]['TN']  / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ))
            f1_strict = 0 if (precision_strict + recall_strict) == 0 else 2 * (precision_strict * recall_strict) / (precision_strict + recall_strict)

            #weighted mode
            precision_weighted = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + weight * labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'] + weight * labels[archive]['PARTIAL']) / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + weight * labels[archive]['PARTIAL'] ))
            recall_weighted = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + weight * labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'] + weight * labels[archive]['PARTIAL'])  / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + weight * labels[archive]['PARTIAL'] ))
            f1_weighted = 0 if (precision_weighted + recall_weighted) == 0 else 2 * (precision_weighted * recall_weighted) / (precision_weighted + recall_weighted)

            #ok mode
            precision_ok = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['PARTIAL']) / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + labels[archive]['PARTIAL']))
            recall_ok = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['PARTIAL'])  / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ))
            f1_ok = 0 if (precision_ok + recall_ok) == 0 else 2 * (precision_ok * recall_ok) / (precision_ok + recall_ok)

            scores[archive]['F1_strict'] = f1_strict
            scores[archive]['F1_weighted'] = f1_weighted
            scores[archive]['F1_ok'] = f1_ok
            print(scores[archive]['F1_strict'], scores[archive]['F1_weighted'], scores[archive]['F1_ok'])

        else:
            for tag in scores[archive].keys():

                    
                #strict mode
                precision_strict = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN']) / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ))
                recall_strict = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'])  / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ))
                f1_strict = 0 if (precision_strict + recall_strict) == 0 else 2 * (precision_strict * recall_strict) / (precision_strict + recall_strict)

                #weighted mode
                precision_weighted = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + weight * labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + weight * labels[archive][tag]['PARTIAL'] )/ (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + weight * labels[archive][tag]['PARTIAL'] ))
                recall_weighted = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + weight * labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + weight * labels[archive][tag]['PARTIAL'])  / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + weight * labels[archive][tag]['PARTIAL'] ))
                f1_weighted = 0 if (precision_weighted + recall_weighted) == 0 else 2 * (precision_weighted * recall_weighted) / (precision_weighted + recall_weighted)

                #ok mode
                precision_ok = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['PARTIAL']) / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FP'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ))
                recall_ok = 0 if (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ) == 0 else ((labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['PARTIAL'])  / (labels[archive][tag]['TP'] + labels[archive][tag]['TN'] + labels[archive][tag]['FN'] + labels[archive][tag]['MISS'] + labels[archive][tag]['PARTIAL'] ))
                f1_ok = 0 if (precision_ok + recall_ok) == 0 else 2 * (precision_ok * recall_ok) / (precision_ok + recall_ok)

                scores[archive][tag]['F1_strict'] = f1_strict
                scores[archive][tag]['F1_weighted'] = f1_weighted
                scores[archive][tag]['F1_ok'] = f1_ok

            precision_strict = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN']) / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ))
            recall_strict = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'])  / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ))
            f1_strict = 0 if (precision_strict + recall_strict) == 0 else 2 * (precision_strict * recall_strict) / (precision_strict + recall_strict)

            #weighted mode
            precision_weighted = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + weight * labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'] + weight * labels[archive]['PARTIAL']) / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + weight * labels[archive]['PARTIAL'] ))
            recall_weighted = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + weight * labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'] + weight * labels[archive]['PARTIAL'])  / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + weight * labels[archive]['PARTIAL'] ))
            f1_weighted = 0 if (precision_weighted + recall_weighted) == 0 else 2 * (precision_weighted * recall_weighted) / (precision_weighted + recall_weighted)

            #ok mode
            precision_ok = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['PARTIAL']) / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FP'] + labels[archive]['MISS'] + labels[archive]['PARTIAL']))
            recall_ok = 0 if (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ) == 0 else ((labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['PARTIAL'])  / (labels[archive]['TP'] + labels[archive]['TN'] + labels[archive]['FN'] + labels[archive]['MISS'] + labels[archive]['PARTIAL'] ))
            f1_ok = 0 if (precision_ok + recall_ok) == 0 else 2 * (precision_ok * recall_ok) / (precision_ok + recall_ok)

            scores[archive]['F1_strict'] = f1_strict
            scores[archive]['F1_weighted'] = f1_weighted
            scores[archive]['F1_ok'] = f1_ok
            print(scores[archive]['F1_strict'], scores[archive]['F1_weighted'], scores[archive]['F1_ok'])

    return scores


import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot(scores : dict):
    #create a DataFrame
    #Each line is an archive
    #Index is the archive name
    #Columnns are : F1_strict, F1_weighted, F1_ok
    df = pd.DataFrame(columns=['F1_strict', 'F1_weighted', 'F1_ok'])
    for archive in scores.keys():
        #append is deprecated, use loc instead
        df.loc[archive] = [scores[archive]['F1_strict'], scores[archive]['F1_weighted'], scores[archive]['F1_ok']]

    print(df)

    #Now append multi_index columns : 
    # 1st layer is : ['PER', 'LOC', 'DATE', 'JOB', 'MERE_MARIEE', 'PERE_MARIEE', 'EX_EPOUX', 'PERE_MARI', 'MERE_MARI', 'ADMIN', 'MARIEE', 'MARI', 'TEMOIN']
    # 2nd layer is : ['F1_strict', 'F1_weighted', 'F1_ok']
    #So we have 39 columns
    #We need to create a MultiIndex
    #Then we can append it to the DataFrame

    #Create the MultiIndex
    #First layer
    first_layer = []
    for tag in scores['archives_AD075EC_11M549_0094-right.png-0'].keys():
        if tag == 'F1_strict' or tag == 'F1_weighted' or tag == 'F1_ok':
            continue
        first_layer.append(tag)

    #Second layer
    second_layer = ['F1_strict', 'F1_weighted', 'F1_ok']

    #Create the MultiIndex
    multi_index = pd.MultiIndex.from_product([first_layer, second_layer], names=['tag', 'F1'])

    #Create the DataFrame
    df2 = pd.DataFrame(columns=multi_index)

    #Fill the DataFrame
    for archive in scores.keys():
        for tag in scores[archive].keys():
            if tag == 'F1_strict' or tag == 'F1_weighted' or tag == 'F1_ok':
                continue
            for f1 in scores[archive][tag].keys():
                df2.loc[archive, (tag, f1)] = scores[archive][tag][f1]

    #Concatenate the two DataFrames
    df = pd.concat([df, df2], axis=1)

    #Print the DataFrame

    print(df)






def test2():
    golden_set = {}
    labels_set = {}

    with open('donnees-test.json', 'r') as file:
        golden_set = json.load(file)

    with open('donnees-test-labels-gpt35-paragraph-16k.json', 'r') as file:
        labels_set = json.load(file)

    results = {}
    for archive in golden_set.keys():
        if archive not in labels_set.keys():
            print('Archive ' + archive + ' not found in labels_set')
            continue

        f1_scores = f1_score(labels_set[archive], golden_set[archive]['questions'], 0.5)
        results[archive] = f1_scores
        
    scores = precision_recall(results, 0.5, True)
    plot(scores)
    #print('--------------------------------------------')

test2()


        

    



