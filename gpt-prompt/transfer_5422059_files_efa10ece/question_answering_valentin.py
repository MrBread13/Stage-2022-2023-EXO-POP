from copy import copy
import re
import json
from pathlib import Path

named_entities = [
    "⌚",
    "⌛",
    "⏰",
    "⏳",
    "Ⓑ",
    "Ⓘ",
    "Ⓜ",
    "Ⓝ",
    "Ⓟ",
    "ⓑ",
    "ⓘ",
    "ⓜ",
    "ⓝ",
    "ⓟ",
    "⚰",
    "🌇",
    "🌉",
    "🌍",
    "🌝",
    "🌞",
    "🎉",
    "🎩",
    "🏠",
    "🏡",
    "🏥",
    "🏳",
    "👒",
    "👦",
    "👧",
    "👨",
    "👰",
    "👴",
    "👵",
    "👶",
    "👹",
    "💬",
    "💭",
    "📅",
    "📆",
    "📌",
    "📕",
    "📖",
    "🔍",
    "🔎",
    "🔟",
    "🔠",
    "🔡",
    "🔢",
    "🔧",
    "🕑",
    "🕘",
    "🗓",
    "🗨",
    "🗯",
    "🗺",
    "😡",
    "😢",
    "😭",
    "🛣",
    "🛤",
    "🥸",
    "🧐",
    "🪛",
    "🪦"
]

questions_dict = {
    "Jour-du-mariage": {"begin": "📖🌞", "end": "📕🌝"},
    "Mois-du-mariage": {"begin": "📖📅", "end": "📕📆"},
    "Année-du-mariage": {"begin": "📖🗓", "end": "📕🎉"},
    "Heure-du-mariage": {"begin": "📖⏰", "end": "📕⌚"},
    "Minute-du-mariage": {"begin": "📖🕑", "end": "📕🕘"},
    "Prenom-de-l'adjoint-au-maire": {"begin": "📖💬", "end": "📕🗯"},
    "Nom-de-l'adjoint-au-maire": {"begin": "📖🗨", "end": "📕💭"},
    "Ville-du-mariage": {"begin": "📖🌇", "end": "📕🌉"},
    "Prénom-du-mari": {"begin": "👨💬", "end": "👦🗯"},
    "Nom-du-mari": {"begin": "👨🗨", "end": "👦💭"},
    "Métier-du-mari": {"begin": "👨🔧", "end": "👦🪛"},
    "Ville-de-naissance-du-mari": {"begin": "👨🏥🌇", "end": "👦👶🌉"},
    "Département-de-naissance-du-mari": {"begin": "👨🏥🗺", "end": "👦👶📌"},
    "Pays-de-naissance-du-mari": {"begin": "👨🏥🏳", "end": "👦👶🌍"},
    "Jour-de-naissance-du-mari": {"begin": "👨🏥🌞", "end": "👦👶🌝"},
    "Mois-de-naissance-du-mari": {"begin": "👨🏥📅", "end": "👦👶📆"},
    "Année-de-naissance-du-mari": {"begin": "👨🏥🗓", "end": "👦👶🎉"},
    "Age-du-mari": {"begin": "👨⌛", "end": "👦⏳"},
    "Ville-de-résidence-du-mari": {"begin": "👨🏠🌇", "end": "👦🏡🌉"},
    "Département-de-résidence-du-mari": {"begin": "👨🏠🗺", "end": "👦🏡📌"},
    "Pays-de-résidence-du-mari": {"begin": "👨👴🏠🏳", "end": "👦🎩🏡🌍"},
    "Numéro-de-rue-de-résidence-du-mari": {"begin": "👨🏠🔟", "end": "👦🏡🔢"},
    "Type-de-rue-de-résidence-du-mari": {"begin": "👨🏠🛣", "end": "👦🏡🛤"},
    "Nom-de-rue-de-résidence-du-mari": {"begin": "👨🏠🔠", "end": "👦🏡🔡"},
    "Prénom-du-père-du-mari": {"begin": "👨👴💬", "end": "👦🎩🗯"},
    "Nom-du-père-du-mari": {"begin": "👨👴🗨", "end": "👦🎩💭"},
    "Métier-du-père-du-mari": {"begin": "👨👴🔧", "end": "👦🎩🪛"},
    "Ville-de-résidence-du-père-du-mari": {"begin": "👨👴🏠🌇", "end": "👦🎩🏡🌉"},
    "Département-du-résidence-du-père-du-mari": {"begin": "👨👴🏠🗺", "end": "👦🎩🏡📌"},
    "Numéro-de-résidence-du-père-du-mari": {"begin": "👨👴🏠🔟", "end": "👦🎩🏡🔢"},
    "Type-de-rue-de-résidence-du-père-du-mari": {"begin": "👨👴🏠🛣", "end": "👦🎩🏡🛤"},
    "Nom-de-rue-de-résidence-du-père-du-mari": {"begin": "👨👴🏠🔠", "end": "👦🎩🏡🔡"},
    "Prénom-de-la-mère-du-mari": {"begin": "👨👵💬", "end": "👦👒🗯"},
    "Nom-de-la-mère-du-mari": {"begin": "👨👵🗨", "end": "👦👒💭"},
    "Profession-de-la-mère-du-mari": {"begin": "👨👵🔧", "end": "👦👒🪛"},
    "Ville-de-résidence-de-la-mère-du-mari": {"begin": "👨👵🏠🌇", "end": "👦👒🏡🌉"},
    "Département-de-résidence-de-la-mère-du-mari": {"begin": "👨👵🏠🗺", "end": "👦👒🏡📌"},
    "Pays-de-résidence-de-la-mère-du-mari": {"begin": "👨👵🏠🏳", "end": "👦👒🏡🌍"},
    "Numéro-de-rue-de-résidence-de-la-mère-du-mari": {"begin": "👨👵🏠🔟", "end": "👦👒🏡🔢"},
    "Type-de-rue-de-résidence-de-la-mère-du-mari": {"begin": "👨👵🏠🛣", "end": "👦👒🏡🛤"},
    "Nom-de-rue-de-résidence-de-la-mère-du-mari": {"begin": "👨👵🏠🔠", "end": "👦👒🏡🔡"},
    "Prénom-de-la-mariée": {"begin": "👰💬", "end": "👧🗯"},
    "Nom-de-la-mariée": {"begin": "👰🗨", "end": "👧💭"},
    "Métier-de-la-mariée": {"begin": "👰🔧", "end": "👧🪛"},
    "Ville-de-naissance-de-la-mariée": {"begin": "👰🏥🌇", "end": "👧👶🌉"},
    "Département-de-naissance-de-la-mariée": {"begin": "👰🏥🗺", "end": "👧👶📌"},
    "Pays-de-naissance-de-la-mariée": {"begin": "👰🏥🏳", "end": "👧👶🌍"},
    "Jour-de-naissance-de-la-mariée": {"begin": "👰🏥🌞", "end": "👧👶🌝"},
    "Mois-de-naissance-de-la-mariée": {"begin": "👰🏥📅", "end": "👧👶📆"},
    "Année-de-naissance-de-la-mariée": {"begin": "👰🏥🗓", "end": "👧👶🎉"},
    "Age-de-la-mariée": {"begin": "👰⌛", "end": "👧⏳"},
    "Ville-de-résidence-de-la-mariée": {"begin": "👰🏠🌇", "end": "👧🏡🌉"},
    "Département-de-résidence-de-la-mariée": {"begin": "👰🏠🗺", "end": "👧🏡📌"},
    "Pays-de-résidence-de-la-mariée": {"begin": "👰👴🏠🏳", "end": "👧🎩🏡🌍"},
    "Numéro-de-rue-de-résidence-de-la-mariée": {"begin": "👰🏠🔟", "end": "👧🏡🔢"},
    "Type-de-rue-de-résidence-de-la-mariée": {"begin": "👰🏠🛣", "end": "👧🏡🛤"},
    "Nom-de-rue-de-résidence-de-la-mariée": {"begin": "👰🏠🔠", "end": "👧🏡🔡"},
    "Prénom-du-père-de-la-mariée": {"begin": "👰👴💬", "end": "👧🎩🗯"},
    "Nom-du-père-de-la-mariée": {"begin": "👰👴🗨", "end": "👧🎩💭"},
    "Métier-du-père-de-la-mariée": {"begin": "👰👴🔧", "end": "👧🎩🪛"},
    "Ville-de-résidence-du-père-de-la-mariée": {"begin": "👰👴🏠🌇", "end": "👧🎩🏡🌉"},
    "Département-du-résidence-du-père-de-la-mariée": {"begin": "👰👴🏠🗺", "end": "👧🎩🏡📌"},
    "Numéro-de-résidence-du-père-de-la-mariée": {"begin": "👰👴🏠🔟", "end": "👧🎩🏡🔢"},
    "Type-de-rue-de-résidence-du-père-de-la-mariée": {"begin": "👰👴🏠🛣", "end": "👧🎩🏡🛤"},
    "Nom-de-rue-de-résidence-du-père-de-la-mariée": {"begin": "👰👴🏠🔠", "end": "👧🎩🏡🔡"},
    "Prénom-de-la-mère-de-la-mariée": {"begin": "👰👵💬", "end": "👧👒🗯"},
    "Nom-de-la-mère-de-la-mariée": {"begin": "👰👵🗨", "end": "👧👒💭"},
    "Profession-de-la-mère-de-la-mariée": {"begin": "👰👵🔧", "end": "👧👒🪛"},
    "Ville-de-résidence-de-la-mère-de-la-mariée": {"begin": "👰👵🏠🌇", "end": "👧👒🏡🌉"},
    "Département-de-résidence-de-la-mère-de-la-mariée": {"begin": "👰👵🏠🗺", "end": "👧👒🏡📌"},
    "Pays-de-résidence-de-la-mère-de-la-mariée": {"begin": "👰👵🏠🏳", "end": "👧👒🏡🌍"},
    "Numéro-de-rue-de-résidence-de-la-mère-de-la-mariée": {"begin": "👰👵🏠🔟", "end": "👧👒🏡🔢"},
    "Type-de-rue-de-résidence-de-la-mère-de-la-mariée": {"begin": "👰👵🏠🛣", "end": "👧👒🏡🛤"},
    "Nom-de-rue-de-résidence-de-la-mère-de-la-mariée": {"begin": "👰👵🏠🔠", "end": "👧👒🏡🔡"},
    "Prénom-de-l'ex-époux": {"begin": "👰👹💬", "end": "👧😡🗯"},
    "Nom-de-l'ex-époux": {"begin": "👰👹🗨", "end": "👧😡💭"},

    'Métier-des-parents-de-la-mariée':{'begin': '👰👴👵🔧', 'end': '👧🎩👒🪛'},
    'Ville-de-résidence-des-parents-de-la-mariée':{'begin': '👰👴👵🏠🌇', 'end': '👧🎩👒🏡🌉'},
    'Département-du-résidence-des-parents-de-la-mariée':{'begin': '👰👴👵🏠🗺', 'end': '👧🎩👒🏡📌'},
    'Pays-de-résidence-de-la-mariée':{'begin': '👰👴👵🏠🏳', 'end': '👧🎩👒🏡🌍'},
    'Numéro-de-résidence-des-parents-de-la-mariée':{'begin': '👰👴👵🏠🔟', 'end': '👧🎩👒🏡🔢'},
    'Type-de-rue-de-résidence-des-parents-de-la-mariée':{'begin': '👰👴👵🏠🛣', 'end': '👧🎩👒🏡🛤'},
    'Nom-de-rue-de-résidence-des-parents-de-la-mariée':{'begin': '👰👴👵🏠🔠', 'end': '👧🎩👒🏡🔡'},
    'Métier-des-parents-du-mari':{'begin': '👨👴👵🔧', 'end': '👦🎩👒🪛'},
    'Ville-de-résidence-des-parents-du-mari':{'begin': '👨👴👵🏠🌇', 'end': '👦🎩👒🏡🌉'},
    'Département-du-résidence-des-parents-du-mari':{'begin': '👨👴👵🏠🗺', 'end': '👦🎩👒🏡📌'},
}

questions_bool = {
    "Mère-du-mari-décédée": {"begin": "👨👵💬🪦", "end": "👦👒🗯⚰"},
    "Mère-du-mari-disparue": {"begin": "👨👵💬🔎", "end": "👦👒🗯🔍"},
    "Mère-de-la-mariée-décédée": {"begin": "👰👵💬🪦", "end": "👧👒🗯⚰"},
    "Mère-de-la-mariée-disparue": {"begin": "👰👵💬🔎", "end": "👧👒🗯🔍"},
    "Père-du-mari-décédée": {"begin": "👨👴💬🪦", "end": "👦🎩🗯⚰"},
    "Père-du-mari-disparue": {"begin": "👨👴💬🔎", "end": "👦🎩🗯🔍"},
    "Père-de-la-mariée-décédée": {"begin": "👰👴💬🪦", "end": "👧🎩🗯⚰"},
    "Père-de-la-mariée-disparue": {"begin": "👰👴💬🔎", "end": "👧🎩🗯🔍"},
    "Mari-veuf": {"begin": "👨💬😢", "end": "👦🗯😭"},
    "Mariée-veuve": {"begin": "👰💬😢", "end": "👧🗯😭"},
    "Mariée-a-un-ex-époux": {"begin": "👰👹", "end": "👧😡"},
    "Mère-de-la-mariée-a-un-ex-époux": {"begin": "👰👵👹🗨", "end": "👧👒😡💭"},
    "Père-de-la-mariée-a-un-ex-épouse": {"begin": "👰👴👹🗨", "end": "👧🎩😡💭"},
    "Mari-a-une-ex-épouse": {"begin": "👨👹", "end": "👦😡"},
    "Mère-du-mari-a-un-ex-époux": {"begin": "👨👵👹🗨", "end": "👦👒😡💭"},
    "Père-du-mari-a-un-ex-épouse": {"begin": "👨👴👹🗨", "end": "👦🎩😡💭"},
}

questions_temoins = {
    "Prénom-du-témoin": {"begin": "🥸💬", "end": "🧐🗯"},
    "Nom-du-témoin": {"begin": "🥸🗨", "end": "🧐💭"},
    "Métier-du-témoin": {"begin": "🥸🔧", "end": "🧐🪛"},
    "Age-du-témoin": {"begin": "🥸⌛", "end": "🧐⏳"},
    "Numéro-de-rue-de-résidence-du-témoin": {"begin": "🥸🏠🔟", "end": "🧐🏡🔢"},
    "Type-de-rue-de-résidence-du-témoin": {"begin": "🥸🏠🛣", "end": "🧐🏡🛤"},
    "Nom-de-rue-de-résidence-du-témoin": {"begin": "🥸🏠🔠", "end": "🧐🏡🔡"},
    "Ville-de-résidence-du-témoin": {"begin": "🥸🏠🌇", "end": "🧐🏡🌉"},
    "Département-du-résidence-du-témoin": {"begin": "🥸🏠🗺", "end": "🧐🏡📌"},
}

def extract_begin_end(ne_dict):
    beg = ne_dict['begin']
    end = ne_dict['end']
    num_begin = len(begin)

    begin_tags = ''.join([beg[i] for i in range(1,num_begin)])
    begin_tags_old_people = ''.join([beg[i] for i in range(2,num_begin)])

    if num_begin == 2:
        act_regex_str = f"{beg0}[^{end0}{begin_tags}]*{beg1}(?P<str>[^{end1}]*){end1}"
    elif num_begin == 3:
        act_regex_str = f"{beg0}[^{end0}{begin_tags}]*{beg1}[^{end0}{begin_tags}]*{beg2}(?P<str>[^{end2}]*){end2}"
    elif num_begin == 4:
        act_regex_str = f"{beg0}[^{end0}{begin_tags}]*{beg1}[^{end0}{begin_tags}]*{beg2}[^{end0}{begin_tags}]*{beg3}(?P<str>[^{end3}]*){end3}"
        if '👴' in begin and '👵' in begin:
            act_regex_str = f"({act_regex_str})|({beg0}[^{end0}{begin_tags_old_people}]*{beg2}[^{end0}{begin_tags_old_people}]*{beg1}[^{end0}{begin_tags_old_people}]*{beg3}(?P<str2>[^{end3}]*){end3})"
    elif num_begin == 5:
        act_regex_str = f"{beg0}[^{end0}{begin_tags}]*{beg1}[^{end0}{begin_tags}]*{beg2}[^{end0}{begin_tags}]*{beg3}[^{end0}{begin_tags}]*{beg4}(?P<str>[^{end4}]*){end4}"
        if '👴' in begin and '👵' in begin:
            act_regex_str = f"({act_regex_str})|({beg0}[^{end0}{begin_tags_old_people}]*{beg2}[^{end0}{begin_tags_old_people}]*{beg1}[^{end0}{begin_tags_old_people}]*{beg3}[^{end0}{begin_tags_old_people}]*{beg4}(?P<str2>[^{end4}]*){end4})"

    return act_regex_str


def extract_answers(act_label):
    answers_dict = {}
    ## infos classiques
    for description, ne_dict in questions_dict.items():
        if 'parent' in description:
            print('aled')
        act_regex_str = extract_begin_end(ne_dict)
        matches = list(re.finditer(act_regex_str, act_label))
        if matches:

            named_entity = matches[0]['str'] if matches[0]['str'] else matches[0]['str2']
            for char in named_entities:
                named_entity = named_entity.replace(char,'')
            answers_dict[description] = named_entity
        else:
            answers_dict[description] = ''

    question_names = answer_dicts = list(questions_dict.keys())
    for question_name in question_names:
        if 'parent' in question_name:
            answers_dict[question_name.replace('des parents', 'du père')] = answers_dict[question_name]
            answers_dict[question_name.replace('des parents', 'de la mère')] = answers_dict[question_name]
            del answers_dict[question_name]

    ## infos correspondant à des booléens
    for description, ne_dict in questions_bool.items():
        answers_dict[description] = ne_dict['begin'] in act_label

    ## infos concernant les témoins
    for i in range(2):
        for description, ne_dict in questions_temoins.items():
            act_regex_str = extract_begin_end(ne_dict)
            matches = list(re.finditer(act_regex_str, act_label))
            if matches and len(matches) > i:
                named_entity = matches[i]['str']
                for char in named_entities:
                    named_entity = named_entity.replace(char,'')
                answers_dict[description+'-'+str(i)] = named_entity
            else:
                answers_dict[description] = ''

    return answers_dict

if __name__ == "__main__":
    labels_path = "transfer_5422059_files_efa10ece/formatted-splitted-labels-tapuscrit-v10-begin-end.json"

    with open(labels_path, "r") as f:
        labels_dict = json.load(f)["ground_truth"]

    act_regex_str = "(?P<str>{}([^{}])*){}".format("ⓜⓑ", "ⒷⓂ", "ⒷⓂ")

    subsets = {'train': ['train','valid'], 'test': ['test']}

    for mode in ['train', 'test']:
        answer_dicts = {}
        for subset_name in subsets[mode]:
            for img_name, img_dict in labels_dict[subset_name].items():
                for i, match in enumerate(re.finditer(act_regex_str, img_dict['text'])):
                    regular_text = match["str"]
                    for char in named_entities:
                        regular_text = regular_text.replace(char,'')
                    answer_dicts[Path(img_name).name+'-'+str(i)] = {
                        'questions' : extract_answers(match["str"]),
                        'texte': regular_text
                    }

        with open(f'donnees-{mode}.json', "w") as f:
            json.dump(answer_dicts, f, ensure_ascii=False)
