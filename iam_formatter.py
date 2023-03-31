import json
import os
import pickle as pkl
import re
from tkinter import E
import xml.etree.ElementTree as ET
from pathlib import Path
import sys
from glob import glob

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(os.path.dirname(DOSSIER_PARENT))
sys.path.append(os.path.dirname(os.path.dirname(DOSSIER_PARENT)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(DOSSIER_PARENT))))
import numpy as np
from Datasets.dataset_formatters.generic_dataset_formatter import OCRDatasetFormatter

# from generic_dataset_formatter import OCRDatasetFormatter  # main_line_ctc
from PIL import Image

SEM_MATCHING_TOKENS = {
    "ⓟ": "Ⓟ",  # page
    '':''
}

def get_charset_espo(labels_dict):
    charset = set()
    for split_name, split_dict in labels_dict.items():
        for page_name, page_dict in split_dict.items():
            charset = charset.union(set(page_dict["text"]))

    return charset

emojis_to_name ={
    "🔟": "<CARDINAL>",
    "📅": "<TIME>",
    "🗺": "<LOCATION>",
    "📖": "<ORGANISATION>",
    '🏳': "<NORP>",
    '👨': "<PER>",
    "🔢" : "</CARDINAL>",
    "📆" : "</TIME>",
    "📌" : "</LOCATION>",
    "📕" : "</ORGANISATION>",
    '🏴' : "</NORP>",
    "👦" : "</PER>",
    }

ne_name_to_token = {
    "CARDINAL": '🔟',
    'TIME': '📅',
    'LOCATION': "🗺",
    'ORGANISATION': '📖',
    'PER': '👨',
    'NORP': '🏳', # pays d'origine?
    "C": '🔟',
    'L': "🗺",
    'T': '📅',
    'N': '🏳', # NORP
    'G': '📖', # ORGANISATION
    'P': '👨',
    'O':'',
    '':''
}
# Location (FAC, GPE, Location), Time (Date,Time), Cardinal (Cardinal, Ordinal, Percent, Quantity, Money), NORP, Person and Organization
MATCHING_NAMED_ENTITY_TOKENS = {
    "🔟": "🔢",  # cardinal
    "📅": "📆",  # date
    "🗺":"📌",
    "📖":"📕",
    '🏳':'🏴',
    '👨':"👦",
    '':''
}

def format_iam_images(imgs_path, bb_path, output_path):
    img_coords_dict = {}
    with open(bb_path, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                line = line.strip()
                columns = line.split(' ')
                line_id = columns[0]
                sentence = columns[-1]
                min_x, min_y, w, h = columns[4:8]
                # min_x = int(min_x)
                min_y = int(min_y)
                # max_x = min_x + int(w)
                # max_y = min_y + int(h)

                img_name = '-'.join(line_id.split('-')[0:2])+'.png'
                if img_name not in img_coords_dict:
                    # img_coords_dict[img_name] = {'min_x': min_x, 'min_y': min_y, 'max_x': max_x, 'max_y': max_y}
                    img_coords_dict[img_name] = {'min_y': min_y}
                else:
                    # img_coords_dict[img_name]['min_x'] = min(img_coords_dict[img_name]['min_x'], min_x)
                    img_coords_dict[img_name]['min_y'] = min(img_coords_dict[img_name]['min_y'], min_y)
                    # img_coords_dict[img_name]['max_x'] = max(img_coords_dict[img_name]['max_x'], max_x)
                    # img_coords_dict[img_name]['max_y'] = max(img_coords_dict[img_name]['max_y'], max_y)

    for img_name, coords in img_coords_dict.items():
        img = Image.open(f'{imgs_path}/{img_name}')
        # img = img.crop((coords['min_x'], coords['min_y'], coords['max_x'], coords['max_y']))
        img = img.crop((0, coords['min_y']-50, img.width, img.height))
        img.save(output_path + '/' + img_name)

def format_sentence_ne(sentence_id, sentences, named_entities_dict, ne_mode, previous_entity):
    words_list = []
    sentence = sentences[sentence_id]
    if int(sentence_id.split('-')[-1]):
        previous_sentence_id = '-'.join(sentence_id.split('-')[:2]) + '-' + str(int(sentence_id.split('-')[-1])-1).zfill(2)

    for i, word in enumerate(sentence.split('|')):
        word_id = f'{sentence_id}-{i:0>2d}'
        entity = named_entities_dict[word_id]
        if ne_mode == 'after':
            word = word + ne_name_to_token[entity]
        elif ne_mode == 'before':
            word = ne_name_to_token[entity] + word
        if ne_mode == 'both':
            if entity != previous_entity:
                if ne_name_to_token[previous_entity]:
                    if i:
                        words_list[i-1] += MATCHING_NAMED_ENTITY_TOKENS[ne_name_to_token[previous_entity]]
                    else:
                        sentences[previous_sentence_id] += MATCHING_NAMED_ENTITY_TOKENS[ne_name_to_token[previous_entity]]

                if ne_name_to_token[entity]:
                    word = ne_name_to_token[entity] + word
        words_list.append(word)

        previous_entity=entity
    sentence = ' '.join(words_list)
    sentences[sentence_id] = sentence
    return sentences, previous_entity

def format_labels_single_page_iam(
    labels_path, real_text_path, use_sem=True, use_nes=False, ne_mode='after', set_len=0
):
    page_format = "page"
    page_sides = ["left", "right"]
    nb_cols = 1
    formatted_labels_dict = {"charset": [], "ground_truth": {}}
    old_page_name = ''

    real_words = []
    word_split_dict = {subset : [] for subset in ['train', 'valid','test']}

    page_text_dict = {}
    with open(real_text_path, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                line = line.strip()
                columns = line.split(' ')
                line_id = columns[0]
                sentence = ' '.join(columns[8:])
                page_id = '-'.join(line_id.split('-')[0:2])
                if page_id in page_text_dict:
                    page_text_dict[page_id]['sentences'][line_id] = sentence
                else:
                    page_text_dict[page_id] = {'sentences':{line_id: sentence}}

    i = 0
    for subset in ['train', 'valid','test']:
        formatted_split_dict = {}
        page_label = ''
        named_entities_dict = {}

        with open(f'{labels_path}/iam_{subset}_rwth_{set_len}_all.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                word_id = line.split(' ')[0]
                word_split_dict[subset].append(word_id)

                if use_nes:
                    named_entity = line.split(' ')[1]
                    named_entities_dict[word_id] = named_entity

        # ne_set = set(named_entities_dict.values())

        for page_id, page_dict in page_text_dict.items():
            page_name = page_id + '.png'
            if not list(page_dict['sentences'].keys())[0]+'-00' in word_split_dict[subset]:
                continue
            formatted_split_dict[page_name] = {
                    "nb_cols": nb_cols,
                    "pages": [{"text": "", "nb_cols": nb_cols, "paragraphs": []}],
                }

            page_label = 'ⓟ' if use_sem else ''
            previous_entity = ''

            for line_id, sentence in page_dict['sentences'].items():
                if use_nes:
                    page_dict['sentences'], previous_entity = format_sentence_ne(line_id, page_dict['sentences'], named_entities_dict, ne_mode, previous_entity)

                page_dict['sentences'][line_id] = page_dict['sentences'][line_id].replace('|', ' ').replace(' ,', ',').replace(' .', '.').replace(' ;', ';').replace(' :', ':')

            page_label += '\n'.join(list(page_dict['sentences'].values()))
            page_label += 'Ⓟ' if use_sem else ''

            formatted_split_dict[page_name]["text"] = page_label
            formatted_split_dict[page_name]["pages"][0]["text"] = page_label

        formatted_labels_dict["ground_truth"][subset] = formatted_split_dict

    formatted_labels_dict["charset"] = get_charset_espo(formatted_labels_dict['ground_truth'])

    if use_sem:
        formatted_labels_dict["charset"] = formatted_labels_dict["charset"].union(
            ["ⓟ", "Ⓟ"]
        )
    if use_nes:
        formatted_labels_dict["charset"] = formatted_labels_dict["charset"].union(
            set([token for token in MATCHING_NAMED_ENTITY_TOKENS.values() if token]+[token for token in MATCHING_NAMED_ENTITY_TOKENS.keys() if token])
        )
    formatted_labels_dict["charset"] = sorted(list(formatted_labels_dict["charset"]))

    if use_sem:
        page_format = "page_sem"
    else:
        page_format = "page"

    with open(Path(labels_path).joinpath("formatted-" + Path(labels_path).stem  + ".json"), "w") as f:
        json.dump(formatted_labels_dict, f, ensure_ascii=False)

    with open(
        Path(labels_path).joinpath("formatted-" + Path(labels_path).stem + ".pkl"), "wb"
    ) as f:
        pkl.dump(formatted_labels_dict, f)



if __name__ == "__main__":
    real_text_path = "/mnt/3abb9a61-a9cb-4642-92bb-0fe043b422d8/Datasets divers/IAM/lines.txt"
    imgs_path = "/mnt/3abb9a61-a9cb-4642-92bb-0fe043b422d8/Datasets divers/IAM/images"
    output_path = "/home/thomasconstum/Documents/Repos/OCR/DAN/Datasets/formatted/IAM_page_sem/flat"

    # format_iam_images(imgs_path, real_text_path, output_path)

    xml_folder_path = '/home/thomasconstum/Documents/Repos/OCR/DAN/Datasets/raw/IAM-DB/6 entités'
    # use_sem = False
    use_sem = True
    use_nes = True
    set_len = 6
    # use_nes = False
    only_body = True
    # ne_mode = 'after'
    # ne_mode = 'after_no_hierarchy'
    ne_mode = 'both'
    format_labels_single_page_iam(
    xml_folder_path, real_text_path, use_sem=use_sem, use_nes=use_nes, ne_mode=ne_mode, set_len=set_len)