import os
import json
import pandas as pd
import numpy as np
import re

LABEL_EQUIVALENCES = {
    'C' : 'CADINZAL',
    'L' : 'LOCATION',
    'G' : 'ORGANIZATION',
    'P' : 'PERSON',
    'O' : 'O',
    'N' : 'NORP',
    'T' : 'TIME'
}

def split_line(line):
    line = line[0].split(' ')
    return line[:1] + [' '.join(line[8:])]

def format_to_BIO(words_path : str, label_path : str, output_path : str , subsets : list, label_count : int):
    """
    Converts the IAM dataset to BIO format
    """
    labels = pd.DataFrame()
    for sub in subsets:
        tmp = pd.read_csv(f'{label_path}/iam_{sub}_rwth_{label_count}_all.txt', sep=' ', header=None, names=['index', 'label'])
        tmp['set'] = sub
        labels = pd.concat([labels,tmp])
        
    labels = labels.reset_index(drop=True)

    #create a mask for labels O
    mask = labels['label'] == 'O'
    #for each label replace it with 'B-' + label or 'I-' + label if it is the same as the previous label. use np.where and shift
    labels = labels.replace({'label': LABEL_EQUIVALENCES})
    labels['label'] = np.where(labels['label'] == labels['label'].shift(1), 'I-' + labels['label'], 'B-' + labels['label'])
    #replace all labels O with 'O'
    labels['label'] = np.where(mask, 'O', labels['label'])

    #read the words file
    words_tmp = pd.read_csv(words_path, comment='#', sep='_', header=None)
    words_tmp = words_tmp.apply(lambda x : split_line(x), axis=1)
    words = pd.DataFrame(words_tmp.values.tolist(), columns=['index', 'word'])

    #merge the labels and words on index
    words = pd.merge(words, labels, on='index').drop(columns=['index'])

    #for each subset create a new file called iam_{subset}_rwth_{label_count}_all_MIO.txt in the output_path folder
    for sub in subsets:
        words[words.set == sub].drop('set').to_csv(f'{output_path}/iam_{sub}_rwth_{label_count}_all_MIO.txt', sep=' ', index=False, header=False)










    print(words[words.set == 'train'].head(10))


