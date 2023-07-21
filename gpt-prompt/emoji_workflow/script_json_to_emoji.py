import Levenshtein
import re

#This is the charset used to ignore emojis and ponctuation 
charset = [
    " ",
    "!",
    "#",
    ")",
    "("
    "\\n",
    ",",
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

emoji_charset = [
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

#THis is the dict associating every field in the 'json version' to emojis at the beginning and at the end of the word in the text
questions_dict = {
    "Jour-mariage": {"begin": "📖🌞", "end": "📕🌝"},
    "Mois-mariage": {"begin": "📖📅", "end": "📕📆"},
    "Annee-mariage": {"begin": "📖🗓", "end": "📕🎉"},
    "Heure-mariage": {"begin": "📖⏰", "end": "📕⌚"},
    "Minute-mariage": {"begin": "📖🕑", "end": "📕🕘"},
    "Prenom-adjoint-maire": {"begin": "📖💬", "end": "📕🗯"},
    "Nom-adjoint-maire": {"begin": "📖🗨", "end": "📕💭"},
    "Ville-mariage": {"begin": "📖🌇", "end": "📕🌉"},
    "Prenom-mari": {"begin": "👨💬", "end": "👦🗯"},
    "Nom-mari": {"begin": "👨🗨", "end": "👦💭"},
    "Prenom-mari-p4": {"begin": "👨💬", "end": "👦🗯"},
    "Nom-mari-p4": {"begin": "👨🗨", "end": "👦💭"},
    "Profession-mari": {"begin": "👨🔧", "end": "👦🪛"},
    "Ville-naissance-mari": {"begin": "👨🏥🌇", "end": "👦👶🌉"},
    "Departement-naissance-mari": {"begin": "👨🏥🗺", "end": "👦👶📌"},
    "Pays-naissance-mari": {"begin": "👨🏥🏳", "end": "👦👶🌍"},
    "Jour-naissance-mari": {"begin": "👨🏥🌞", "end": "👦👶🌝"},
    "Mois-naissance-mari": {"begin": "👨🏥📅", "end": "👦👶📆"},
    "Annee-naissance-mari": {"begin": "👨🏥🗓", "end": "👦👶🎉"},
    "Age-mari": {"begin": "👨⌛", "end": "👦⏳"},
    "Ville-residence-mari": {"begin": "👨🏠🌇", "end": "👦🏡🌉"},
    "Departement-residence-mari": {"begin": "👨🏠🗺", "end": "👦🏡📌"},
    "Pays-residence-mari": {"begin": "👨🏠🏳", "end": "👦🏡🌍"},
    "Numero-rue-residence-mari": {"begin": "👨🏠🔟", "end": "👦🏡🔢"},
    "Type-rue-residence-mari": {"begin": "👨🏠🛣", "end": "👦🏡🛤"},
    "Nom-rue-residence-mari": {"begin": "👨🏠🔠", "end": "👦🏡🔡"},
    "Prenom-pere-mari": {"begin": "👨👴💬", "end": "👦🎩🗯"},
    "Nom-pere-mari": {"begin": "👨👴🗨", "end": "👦🎩💭"},
    "Profession-pere-mari": {"begin": "👨👴🔧", "end": "👦🎩🪛"},
    "Ville-residence-pere-mari": {"begin": "👨👴🏠🌇", "end": "👦🎩🏡🌉"},
    "Departement-residence-pere-mari": {"begin": "👨👴🏠🗺", "end": "👦🎩🏡📌"},
    "Pays-residence-pere-mari": {"begin": "👨👴🏠🏳", "end": "👦🎩🏡🌍"},
    "Numero-rue-residence-pere-mari": {"begin": "👨👴🏠🔟", "end": "👦🎩🏡🔢"},
    "Type-rue-residence-pere-mari": {"begin": "👨👴🏠🛣", "end": "👦🎩🏡🛤"},
    "Nom-rue-residence-pere-mari": {"begin": "👨👴🏠🔠", "end": "👦🎩🏡🔡"},
    "Prenom-mere-mari": {"begin": "👨👵💬", "end": "👦👒🗯"},
    "Nom-mere-mari": {"begin": "👨👵🗨", "end": "👦👒💭"},
    "Profession-mere-mari": {"begin": "👨👵🔧", "end": "👦👒🪛"},
    "Ville-residence-mere-mari": {"begin": "👨👵🏠🌇", "end": "👦👒🏡🌉"},
    "Departement-residence-mere-mari": {"begin": "👨👵🏠🗺", "end": "👦👒🏡📌"},
    "Pays-residence-mere-mari": {"begin": "👨👵🏠🏳", "end": "👦👒🏡🌍"},
    "Numero-rue-residence-mere-mari": {"begin": "👨👵🏠🔟", "end": "👦👒🏡🔢"},
    "Type-rue-residence-mere-mari": {"begin": "👨👵🏠🛣", "end": "👦👒🏡🛤"},
    "Nom-rue-residence-mere-mari": {"begin": "👨👵🏠🔠", "end": "👦👒🏡🔡"},
    "Prenom-ex-epouse": {"begin": "👨👹💬", "end": "👧😡🗯"},
    "Prenom-ex-epouse-mari" : {"begin": "👨👹💬", "end": "👧😡🗯"},
    "Nom-ex-epouse": {"begin": "👨👹🗨", "end": "👦😡💭"},
    "Nom-ex-epouse-mari": {"begin": "👨👹🗨", "end": "👦😡💭"},
    "Prenom-mariee": {"begin": "👰💬", "end": "👦🗯"},
    "Nom-mariee": {"begin": "👰🗨", "end": "👧💭"},
    "Prenom-mariee-p4": {"begin": "👰💬", "end": "👦🗯"},
    "Nom-mariee-p4": {"begin": "👰🗨", "end": "👧💭"},
    "Profession-mariee": {"begin": "👰🔧", "end": "👧🪛"},
    "Ville-naissance-mariee": {"begin": "👰🏥🌇", "end": "👧👶🌉"},
    "Departement-naissance-mariee": {"begin": "👰🏥🗺", "end": "👧👶📌"},
    "Pays-naissance-mariee": {"begin": "👰🏥🏳", "end": "👧👶🌍"},
    "Jour-naissance-mariee": {"begin": "👰🏥🌞", "end": "👧👶🌝"},
    "Mois-naissance-mariee": {"begin": "👰🏥📅", "end": "👧👶📆"},
    "Annee-naissance-mariee": {"begin": "👰🏥🗓", "end": "👧👶🎉"},
    "Age-mariee": {"begin": "👰⌛", "end": "👧⏳"},
    "Ville-residence-mariee": {"begin": "👰🏠🌇", "end": "👧🏡🌉"},
    "Departement-residence-mariee": {"begin": "👰🏠🗺", "end": "👧🏡📌"},
    "Pays-residence-mariee": {"begin": "👰🏠🏳", "end": "👧🏡🌍"},
    "Numero-rue-residence-mariee": {"begin": "👰🏠🔟", "end": "👧🏡🔢"},
    "Type-rue-residence-mariee": {"begin": "👰🏠🛣", "end": "👧🏡🛤"},
    "Nom-rue-residence-mariee": {"begin": "👰🏠🔠", "end": "👧🏡🔡"},
    "Prenom-pere-mariee": {"begin": "👰👴💬", "end": "👧🎩🗯"},
    "Nom-pere-mariee": {"begin": "👰👴🗨", "end": "👧🎩💭"},
    "Profession-pere-mariee": {"begin": "👰👴🔧", "end": "👧🎩🪛"},
    "Ville-residence-pere-mariee": {"begin": "👰👴🏠🌇", "end": "👧🎩🏡🌉"},
    "Departement-residence-pere-mariee": {"begin": "👰👴🏠🗺", "end": "👧🎩🏡📌"},
    "Pays-residence-pere-mariee": {"begin": "👰👴🏠🏳", "end": "👧🎩🏡🌍"},
    "Numero-rue-residence-pere-mariee": {"begin": "👰👴🏠🔟", "end": "👧🎩🏡🔢"},
    "Type-rue-residence-pere-mariee": {"begin": "👰👴🏠🛣", "end": "👧🎩🏡🛤"},
    "Nom-rue-residence-pere-mariee": {"begin": "👰👴🏠🔠", "end": "👧🎩🏡🔡"},
    "Prenom-mere-mariee": {"begin": "👰👵💬", "end": "👧👒🗯"},
    "Nom-mere-mariee": {"begin": "👰👵🗨", "end": "👧👒💭"},
    "Profession-mere-mariee": {"begin": "👰👵🔧", "end": "👧👒🪛"},
    "Ville-residence-mere-mariee": {"begin": "👰👵🏠🌇", "end": "👧👒🏡🌉"},
    "Departement-residence-mere-mariee": {"begin": "👰👵🏠🗺", "end": "👧👒🏡📌"},
    "Pays-residence-mere-mariee": {"begin": "👰👵🏠🏳", "end": "👧👒🏡🌍"},
    "Numero-rue-residence-mere-mariee": {"begin": "👰👵🏠🔟", "end": "👧👒🏡🔢"},
    "Type-rue-residence-mere-mariee": {"begin": "👰👵🏠🛣", "end": "👧👒🏡🛤"},
    "Nom-rue-residence-mere-mariee": {"begin": "👰👵🏠🔠", "end": "👧👒🏡🔡"},
    "Prenom-ex-epoux": {"begin": "👰👹💬", "end": "👧😡🗯"},
    "Nom-ex-epoux": {"begin": "👰👹🗨", "end": "👧😡💭"},
    
    "Prenom-temoin-1": {"begin": "🥸💬", "end": "🧐🗯"},
    "Nom-temoin-1": {"begin": "🥸🗨", "end": "🧐💭"},
    "Profession-temoin-1": {"begin": "🥸🔧", "end": "🧐🪛"},
    "Numero-rue-residence-temoin-1": {"begin": "🥸🏠🔟", "end": "🧐🏡🔢"},
    "Type-rue-residence-temoin-1": {"begin": "🥸🏠🛣", "end": "🧐🏡🛤"},
    "Nom-rue-residence-temoin-1": {"begin": "🥸🏠🔠", "end": "🧐🏡🔡"},
    "Ville-residence-temoin-1": {"begin": "🥸🏠🌇", "end": "🧐🏡🌉"},
    "Departement-residence-temoin-1": {"begin": "🥸🏠🗺", "end": "🧐🏡📌"},

    "Prenom-temoin-2": {"begin": "🥸💬", "end": "🧐🗯"},
    "Nom-temoin-2": {"begin": "🥸🗨", "end": "🧐💭"},
    "Profession-temoin-2": {"begin": "🥸🔧", "end": "🧐🪛"},
    "Numero-rue-residence-temoin-2": {"begin": "🥸🏠🔟", "end": "🧐🏡🔢"},
    "Type-rue-residence-temoin-2": {"begin": "🥸🏠🛣", "end": "🧐🏡🛤"},
    "Nom-rue-residence-temoin-2": {"begin": "🥸🏠🔠", "end": "🧐🏡🔡"},
    "Ville-residence-temoin-2": {"begin": "🥸🏠🌇", "end": "🧐🏡🌉"},
    "Departement-residence-temoin-2": {"begin": "🥸🏠🗺", "end": "🧐🏡📌"},

    "Prenom-temoin-3": {"begin": "🥸💬", "end": "🧐🗯"},
    "Nom-temoin-3": {"begin": "🥸🗨", "end": "🧐💭"},
    "Profession-temoin-3": {"begin": "🥸🔧", "end": "🧐🪛"},
    "Numero-rue-residence-temoin-3": {"begin": "🥸🏠🔟", "end": "🧐🏡🔢"},
    "Type-rue-residence-temoin-3": {"begin": "🥸🏠🛣", "end": "🧐🏡🛤"},
    "Nom-rue-residence-temoin-3": {"begin": "🥸🏠🔠", "end": "🧐🏡🔡"},
    "Ville-residence-temoin-3": {"begin": "🥸🏠🌇", "end": "🧐🏡🌉"},
    "Departement-residence-temoin-3": {"begin": "🥸🏠🗺", "end": "🧐🏡📌"},

    "Prenom-temoin-4": {"begin": "🥸💬", "end": "🧐🗯"},
    "Nom-temoin-4": {"begin": "🥸🗨", "end": "🧐💭"},
    "Profession-temoin-4": {"begin": "🥸🔧", "end": "🧐🪛"},
    "Numero-rue-residence-temoin-4": {"begin": "🥸🏠🔟", "end": "🧐🏡🔢"},
    "Type-rue-residence-temoin-4": {"begin": "🥸🏠🛣", "end": "🧐🏡🛤"},
    "Nom-rue-residence-temoin-4": {"begin": "🥸🏠🔠", "end": "🧐🏡🔡"},
    "Ville-residence-temoin-4": {"begin": "🥸🏠🌇", "end": "🧐🏡🌉"},
    "Departement-residence-temoin-4": {"begin": "🥸🏠🗺", "end": "🧐🏡📌"},

    'Profession-parents-mariee': {'begin': '👰👴👵🔧', 'end': '👧🎩👒🪛'},
    'Ville-residence-parents-mariee': {'begin': '👰👴👵🏠🌇', 'end': '👧🎩👒🏡🌉'},
    'Departement-residence-parents-mariee': {'begin': '👰👴👵🏠🗺', 'end': '👧🎩👒🏡📌'},
    'Pays-residence-parents-mariee': {'begin': '👰👴👵🏠🏳', 'end': '👧🎩👒🏡🌍'},
    'Numero-rue-residence-parents-mariee': {'begin': '👰👴👵🏠🔟', 'end': '👧🎩👒🏡🔢'},
    'Type-rue-residence-parents-mariee': {'begin': '👰👴👵🏠🛣', 'end': '👧🎩👒🏡🛤'},
    'Nom-rue-residence-parents-mariee': {'begin': '👰👴👵🏠🔠', 'end': '👧🎩👒🏡🔡'},
    'Profession-parents-mariee': {'begin': '👰👴👵🔧', 'end': '👧🎩👒🪛'},

    'Ville-residence-parents-mari': {'begin': '👨👴👵🏠🌇', 'end': '👦🎩👒🏡🌉'},
    'Departement-residence-parents-mari': {'begin': '👨👴👵🏠🗺', 'end': '👦🎩👒🏡📌'},
    'Pays-residence-parents-mari': {'begin': '👨👴👵🏠🏳', 'end': '👦🎩👒🏡🌍'},
    'Numero-rue-residence-parents-mari': {'begin': '👨👴👵🏠🔟', 'end': '👦🎩👒🏡🔢'},
    'Type-rue-residence-parents-mari': {'begin': '👨👴👵🏠🛣', 'end': '👦🎩👒🏡🛤'},
    'Nom-rue-residence-parents-mari': {'begin': '👨👴👵🏠🔠', 'end': '👦🎩👒🏡🔡'},
    'Profession-parents-mari': {'begin': '👨👴👵🔧', 'end': '👦🎩👒🪛'},
}

#same but for boolean fields, processed separately (WIP)
questions_bool = {
    "Mère-mari-décédée": {"begin": "👨👵💬🪦", "end": "👦👒🗯⚰"},
    "Mère-mariee-décédée": {"begin": "👰👵💬🪦", "end": "👧👒🗯⚰"},
    "Père-mari-décédée": {"begin": "👨👴💬🪦", "end": "👦🎩🗯⚰"},
    "Père-mariee-décédée": {"begin": "👰👴💬🪦", "end": "👧🎩🗯⚰"},
    "Mari-veuf": {"begin": "👨💬😢", "end": "👦🗯😭"},
    "Mariée-veuve": {"begin": "👰💬😢", "end": "👧🗯😭"},
    "Mariée-a-un-ex-époux": {"begin": "👰👹", "end": "👧😡"},
    "Mari-a-une-ex-épouse": {"begin": "👨👹", "end": "👦😡"},
}


def emojize(json_acts_dictionnary, raw_text):
    '''
    @param json_acts_dictionnary: a dictionnary of acts in json format. format to follow : 

    {"act_name": {
        "labels": 
            {"p1" : {"label1" : "value1", "label2" : "value2", ...}, 
            "p2" : {"label1" : "value1", "label2" : "value2", ...}}, 
        "text": { "p1" : "text", "p2" : "text"} 
    ...}
    
    @output emogised_acts: a dictionnary of acts in text format with emojis around entities. Format : 
    
    {"act_name": {
        "p1" : "text", 
        "p2" : "text"} 
    ...}

    @description: this function takes a dictionnary of acts in json format and returns a dictionnary of acts in text format with emojis around entities. A few tricks are used :
    - a levenshtein distance of 1/3 of the length off a string to find is considered as a potential matching occurence
    - entities are processed by paragraph to avoid too many false positives in non-relevant paragraphs.
    - Complete entites (persons) are processed sequentially : husband, husband's parents, wife, wife's parents, witnesses, officier
    - The first name of a person is used as a 'reference' for its upcoming informations if multiple occurences are found, the first one after its firstname is prioritized. If there isn't any after, the closest before is used.
    - To avoid partial words to match (ex : Jean in Jeanne), if an occurence is found, then it is expanded until a character from the above charset is found. Then another LEvenshtein test is performed to see which occurences are still relevant.
    - To avoid firstname to match where they shouldnt (ex : Jean in 'rue Jean Jaurès') a firstname match MUST be 'virgin' of any other label. An history of positions and span length of precedent occurences is kept to avoid this.
    '''
    emogised_acts = {}

    for act_name, acts in json_acts_dictionnary.items():
        labels_act = acts["labels"]
        text = acts["text"]

        positions = {}
        label_length = {}

        def check_for_occurence(occ, text):
            #check for occurences of occ in text
            #return a list of tuples (occurence, position) from the first to the last occurence in the text.
            #allow a levenshtein distance of 1/4 of the length of occ and 0 if occ is shorter than 4 characters

            if len(occ) < 4:
                lev = 0
            else:
                lev = len(occ)//3

            print("check_for_occurence -> occ : ", occ, "lev : ", lev)
            occurences = []

            #print("text : ", text)

            for i in range(len(text) - len(occ)):

                if Levenshtein.distance(occ, text[i:i+len(occ)]) <= lev:
                    match = text[i:i+len(occ)]
                    print("match : ", match)
                    #if a match is found "expand" it until something from charset (dic above) is found
                    add = 0
                    if text[i+len(occ)+add-1] not in charset:
                        while (i+len(occ)+add < len(text)) and (text[i+len(occ)+add]) not in charset:
                            match += text[i+len(occ)+add]
                            add += 1
                    #print("match : ", match)
                        

                    #check if there is already an occurence in the list in the len(occ) characters before (overlapping occurences)
                    #if there is, replace it with the new one only if it is a better match
                    if len(occurences) > 0 and occurences[-1][1] > i - len(occ):
                        if Levenshtein.distance(occ, occurences[-1][0]) > Levenshtein.distance(occ, match):
                            print("Comparison -> ", occurences[-1][0], " : ", Levenshtein.distance(occ, occurences[-1][0]), " vs ", match, " : ", Levenshtein.distance(occ, match))
                            occurences[-1] = (match, i)
                    else:
                        occurences.append((match, i))
            print("Occurences :", occurences)
            return occurences

        def insert_emojis_around_label(label, paragraph, text=text):
            # insert emojis around occ in text
            # return the text with emojis around occ
            # if occ is not found, return None
            if label not in questions_dict.keys():
                print("Label not in questions_dict.keys() : ", label)
                return text
            emojis = questions_dict[label]
            occ = labels_act[paragraph][label]
            print("Occurence :", occ)
            print("Text->insert_emojis_around_label :", text)
            occurences = check_for_occurence(occ, text)
            #print("Key :", label, "Ref :", occ, "Occurences :", occurences)
            print("Final occurences list before best_position :", occurences)
            if len(occurences) == 0:
                print("No occurence found for ", label)
                return text
            else:
                # the position of the occurence in the text is occurences[0][1]

                def search_best_position(occurences, positions=positions, label=label, oc=occ):

                    

                    if 'Prenom' in label:
                        #print("I was here !")
                        # check the list and remove the worst matching occurence if there are 2 or more
                        if len(occurences) > 1:
                            lev = []
                            for occurence in occurences:
                                lev.append(Levenshtein.distance(oc, occurence[0]))
                            #print("lev : ", lev)
                            # if all elements are equal, continue
                            if lev.count(lev[0]) != len(lev):
                                worst = lev.index(max(lev))
                                if worst != -1:
                                    print("Worst :", occurences[worst])
                                    occurences.pop(worst)

                        for occurence in occurences:
                            for key in positions.keys():
                                if key in labels_act[paragraph].keys():
                                    begin = positions[key]
                                    end = positions[key] + label_length[key]
                                    if occurence[1] >= begin and occurence[1] <= end:
                                        print('Key :', key, 'Begin :', begin, 'End :', end)
                                        #print('I was here too !')
                                        #print("Occurence :", occurence[0], "Position :", occurence[1], "Key :", key, "Begin :", begin, "End :", end)
                                        occurences.remove(occurence)

                    if 'Ville-naissance-mari' in label :
                        for occurence in occurences:
                            if 'Ville-naissance-mari' in positions.keys():
                                begin = positions['Ville-naissance-mari']
                                end = positions['Ville-naissance-mari'] + label_length['Ville-naissance-mari']
                                if occurence[1] >= begin and occurence[1] <= end:
                                    occurences.remove(occurence)

                    if 'Ville-naissance-mariee' in label :
                        for occurence in occurences:
                            if 'Ville-naissance-mariee' in positions.keys():
                                begin = positions['Ville-naissance-mariee']
                                end = positions['Ville-naissance-mariee'] + label_length['Ville-naissance-mariee']
                                if occurence[1] >= begin and occurence[1] <= end:
                                    occurences.remove(occurence)

                    if 'Pays-naissance-mari' in label :
                        for occurence in occurences:
                            if 'Pays-naissance-mari' in positions.keys():
                                begin = positions['Pays-naissance-mari']
                                end = positions['Pays-naissance-mari'] + label_length['Pays-naissance-mari']
                                if occurence[1] >= begin and occurence[1] <= end:
                                    occurences.remove(occurence)

                    if 'Pays-naissance-mariee' in label :
                        for occurence in occurences:
                            if 'Pays-naissance-mariee' in positions.keys():
                                begin = positions['Pays-naissance-mariee']
                                end = positions['Pays-naissance-mariee'] + label_length['Pays-naissance-mariee']
                                if occurence[1] >= begin and occurence[1] <= end:
                                    occurences.remove(occurence)



                    if 'mere-mariee' in label:
                        if label == 'Prenom-mere-mariee':
                            positions['Prenom-mere-mariee'] = occurences[0][1]
                            return occurences[0]
                        # elif label == 'Nom-mere-mariee':
                        #     positions['Nom-mere-mariee'] = occurences[0][1]
                        #     return occurences[0]

                        p = positions['Prenom-mere-mariee'] if (
                            'Prenom-mere-mariee' in positions.keys()) else 0

                        # choisir la première occurence après p
                        for occ in occurences:
                            if occ[1] > p:
                                positions[label] = occ[1]
                                return occ

                        # si aucune occurence après p, choisir la dernière occurence
                        positions[label] = occurences[-1][1]
                        return occurences[-1]

                    if 'pere-mariee' in label:
                        if label == 'Prenom-pere-mariee':
                            positions['Prenom-pere-mariee'] = occurences[0][1]
                            return occurences[0]
                        # elif label == 'Nom-pere-mariee':
                        #     positions['Nom-pere-mariee'] = occurences[0][1]
                        #     return occurences[0]

                        p = positions['Prenom-pere-mariee'] if (
                            'Prenom-pere-mariee' in positions.keys()) else 0

                        # choisir la première occurence après p
                        for occ in occurences:
                            if occ[1] > p:
                                positions[label] = occ[1]
                                return occ

                        # si aucune occurence après p, choisir la dernière occurence
                        positions[label] = occurences[-1][1]
                        return occurences[-1]

                    if 'mere-mari' in label:
                        if label == 'Prenom-mere-mari':
                            positions['Prenom-mere-mari'] = occurences[0][1]
                            return occurences[0]
                        # elif label == 'Nom-mere-mari':
                        #     positions['Nom-mere-mari'] = occurences[0][1]
                        #     return occurences[0]

                        p = positions['Prenom-mere-mari'] if (
                            'Prenom-mere-mari' in positions.keys()) else 0

                        # choisir la première occurence après p
                        for occ in occurences:
                            if occ[1] > p:
                                positions[label] = occ[1]
                                return occ

                        # si aucune occurence après p, choisir la dernière occurence
                        positions[label] = occurences[-1][1]
                        return occurences[-1]

                    if 'pere-mari' in label:
                        if label == 'Prenom-pere-mari':
                            positions['Prenom-pere-mari'] = occurences[0][1]
                            return occurences[0]
                        # elif label == 'Nom-pere-mari':
                        #     positions['Nom-pere-mari'] = occurences[0][1]
                        #     return occurences[0]

                        p = positions['Prenom-pere-mari'] if (
                            'Prenom-pere-mari' in positions.keys()) else 0

                        # choisir la première occurence après p
                        for occ in occurences:
                            if occ[1] > p:
                                positions[label] = occ[1]
                                return occ

                        # si aucune occurence après p, choisir la dernière occurence
                        positions[label] = occurences[-1][1]
                        return occurences[-1]

                    if 'temoin-2' in label:
                        if label == 'Prenom-temoin-2':
                            positions['Prenom-temoin-2'] = occurences[0][1]
                            return occurences[0]
                        # elif label == 'Nom-temoin-2':
                        #     positions['Nom-temoin-2'] = occurences[0][1]
                        #     return occurences[0]

                        p = positions['Prenom-temoin-2'] if (
                            'Prenom-temoin-2' in positions.keys()) else 0

                        # choisir la première occurence après p
                        for occ in occurences:
                            if occ[1] > p:
                                positions[label] = occ[1]
                                return occ

                        # si aucune occurence après p, choisir la dernière occurence
                        positions[label] = occurences[-1][1]
                        return occurences[-1]

                    if len(occurences) == 0:
                        return None, None
                    
                    positions[label] = occurences[0][1]
                    return occurences[0]

                good_occ, pos = search_best_position(occurences)
                if good_occ is None:
                    return text
                #print(positions)
                def update_positions(pos, len_after, len_before, positions = positions):
                    for label, position in positions.items():
                        for paragraph in labels_act.keys():
                            if label in labels_act[paragraph].keys():
                                if position > pos:
                                    positions[label] += len_after + len_before

                # I want to insert emojis around the occurence, I want this to be done only for good_occ
                text = text[:pos] + emojis['begin'] + good_occ + \
                    emojis['end'][::-1] + text[pos+len(good_occ):]
                
                # update positions
                label_length[label] = len(good_occ) + len(emojis['begin']) + len(emojis['end'])
                update_positions(pos, len(emojis['begin']), len(emojis['end']))

                #print("Text :", text)
                return text

        def fix_pluriels(text, pluriels = questions_dict):
            for paragraph, txt in text.items():

                #Mariee + 2 parents
                # txt = txt.replace('👰🏠🌇👰👴🏠🌇👰👵🏠🌇', pluriels['Ville-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🌉👧🎩🏡🌉👧🏡🌉', pluriels['Ville-residence-parents-mariee']['end'])
                # txt = txt.replace('👰🏠🗺👰👴🏠🗺👰👵🏠🗺', pluriels['Departement-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡📌👧🎩🏡📌👧🏡📌', pluriels['Departement-residence-parents-mariee']['end'])
                # txt = txt.replace('👰🏠🏳👰👴🏠🏳👰👵🏠🏳', pluriels['Pays-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🌍👧🎩🏡🌍👧🏡🌍', pluriels['Pays-residence-parents-mariee']['end'])
                # txt = txt.replace('👰🏠🔟👰👴🏠🔟👰👵🏠🔟', pluriels['Numero-rue-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🔢👧🎩🏡🔢👧🏡🔢', pluriels['Numero-rue-residence-parents-mariee']['end'])
                # txt = txt.replace('👰🏠🛣👰👴🏠🛣👰👵🏠🛣', pluriels['Type-rue-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🛤👧🎩🏡🛤👧🏡🛤', pluriels['Type-rue-residence-parents-mariee']['end'])
                # txt = txt.replace('👰🏠🔠👰👴🏠🔠👰👵🏠🔠', pluriels['Nom-rue-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🔡👧🎩🏡🔡👧🏡🔡', pluriels['Nom-rue-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Ville-residence-mariee']['begin']+questions_dict['Ville-residence-pere-mariee']['begin']+questions_dict['Ville-residence-mere-mariee']['begin'], pluriels['Ville-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Ville-residence-mere-mariee']['end'][::-1]+questions_dict['Ville-residence-pere-mariee']['end'][::-1]+questions_dict['Ville-residence-mariee']['end'][::-1], pluriels['Ville-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Departement-residence-mariee']['begin']+questions_dict['Departement-residence-pere-mariee']['begin']+questions_dict['Departement-residence-mere-mariee']['begin'], pluriels['Departement-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Departement-residence-mere-mariee']['end'][::-1]+questions_dict['Departement-residence-pere-mariee']['end'][::-1]+questions_dict['Departement-residence-mariee']['end'][::-1], pluriels['Departement-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Pays-residence-mariee']['begin']+questions_dict['Pays-residence-pere-mariee']['begin']+questions_dict['Pays-residence-mere-mariee']['begin'], pluriels['Pays-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Pays-residence-mere-mariee']['end'][::-1]+questions_dict['Pays-residence-pere-mariee']['end'][::-1]+questions_dict['Pays-residence-mariee']['end'][::-1], pluriels['Pays-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Numero-rue-residence-mariee']['begin']+questions_dict['Numero-rue-residence-pere-mariee']['begin']+questions_dict['Numero-rue-residence-mere-mariee']['begin'], pluriels['Numero-rue-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Numero-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Numero-rue-residence-pere-mariee']['end'][::-1]+questions_dict['Numero-rue-residence-mariee']['end'][::-1], pluriels['Numero-rue-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Type-rue-residence-mariee']['begin']+questions_dict['Type-rue-residence-pere-mariee']['begin']+questions_dict['Type-rue-residence-mere-mariee']['begin'], pluriels['Type-rue-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Type-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Type-rue-residence-pere-mariee']['end'][::-1]+questions_dict['Type-rue-residence-mariee']['end'][::-1], pluriels['Type-rue-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Nom-rue-residence-mariee']['begin']+questions_dict['Nom-rue-residence-pere-mariee']['begin']+questions_dict['Nom-rue-residence-mere-mariee']['begin'], pluriels['Nom-rue-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Nom-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Nom-rue-residence-pere-mariee']['end'][::-1]+questions_dict['Nom-rue-residence-mariee']['end'][::-1], pluriels['Nom-rue-residence-parents-mariee']['end'])



                #Mariee + mere
                # txt = txt.replace('👰🏠🌇👰👵🏠🌇', pluriels['Ville-residence-mere-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🌉👧🏡🌉', pluriels['Ville-residence-mere-mariee']['end'])
                # txt = txt.replace('👰🏠🗺👰👵🏠🗺', pluriels['Departement-residence-mere-mariee']['begin'])
                # txt = txt.replace('👧👒🏡📌👧🏡📌', pluriels['Departement-residence-mere-mariee']['end'])
                # txt = txt.replace('👰🏠🏳👰👵🏠🏳', pluriels['Pays-residence-mere-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🌍👧🏡🌍', pluriels['Pays-residence-mere-mariee']['end'])
                # txt = txt.replace('👰🏠🔟👰👵🏠🔟', pluriels['Numero-rue-residence-mere-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🔢👧🏡🔢', pluriels['Numero-rue-residence-mere-mariee']['end'])
                # txt = txt.replace('👰🏠🛣👰👵🏠🛣', pluriels['Type-rue-residence-mere-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🛤👧🏡🛤', pluriels['Type-rue-residence-mere-mariee']['end'])
                # txt = txt.replace('👰🏠🔠👰👵🏠🔠', pluriels['Nom-rue-residence-mere-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🔡👧🏡🔡', pluriels['Nom-rue-residence-mere-mariee']['end'])

                txt = txt.replace(questions_dict['Ville-residence-mariee']['begin']+questions_dict['Ville-residence-mere-mariee']['begin'], pluriels['Ville-residence-mere-mariee']['begin'])
                txt = txt.replace(questions_dict['Ville-residence-mere-mariee']['end'][::-1]+questions_dict['Ville-residence-mariee']['end'][::-1], pluriels['Ville-residence-mere-mariee']['end'])

                txt = txt.replace(questions_dict['Departement-residence-mariee']['begin']+questions_dict['Departement-residence-mere-mariee']['begin'], pluriels['Departement-residence-mere-mariee']['begin'])
                txt = txt.replace(questions_dict['Departement-residence-mere-mariee']['end'][::-1]+questions_dict['Departement-residence-mariee']['end'][::-1], pluriels['Departement-residence-mere-mariee']['end'])

                txt = txt.replace(questions_dict['Pays-residence-mariee']['begin']+questions_dict['Pays-residence-mere-mariee']['begin'], pluriels['Pays-residence-mere-mariee']['begin'])
                txt = txt.replace(questions_dict['Pays-residence-mere-mariee']['end'][::-1]+questions_dict['Pays-residence-mariee']['end'][::-1], pluriels['Pays-residence-mere-mariee']['end'])

                txt = txt.replace(questions_dict['Numero-rue-residence-mariee']['begin']+questions_dict['Numero-rue-residence-mere-mariee']['begin'], pluriels['Numero-rue-residence-mere-mariee']['begin'])
                txt = txt.replace(questions_dict['Numero-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Numero-rue-residence-mariee']['end'][::-1], pluriels['Numero-rue-residence-mere-mariee']['end'])

                txt = txt.replace(questions_dict['Type-rue-residence-mariee']['begin']+questions_dict['Type-rue-residence-mere-mariee']['begin'], pluriels['Type-rue-residence-mere-mariee']['begin'])
                txt = txt.replace(questions_dict['Type-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Type-rue-residence-mariee']['end'][::-1], pluriels['Type-rue-residence-mere-mariee']['end'])

                txt = txt.replace(questions_dict['Nom-rue-residence-mariee']['begin']+questions_dict['Nom-rue-residence-mere-mariee']['begin'], pluriels['Nom-rue-residence-mere-mariee']['begin'])
                txt = txt.replace(questions_dict['Nom-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Nom-rue-residence-mariee']['end'][::-1], pluriels['Nom-rue-residence-mere-mariee']['end'])



                #Mariee + pere
                # txt = txt.replace('👰🏠🌇👰👴🏠🌇', pluriels['Ville-residence-pere-mariee']['begin'])
                # txt = txt.replace('👧🎩🏡🌉👧🏡🌉', pluriels['Ville-residence-pere-mariee']['end'])
                # txt = txt.replace('👰🏠🗺👰👴🏠🗺', pluriels['Departement-residence-pere-mariee']['begin'])
                # txt = txt.replace('👧🎩🏡📌👧🏡📌', pluriels['Departement-residence-pere-mariee']['end'])
                # txt = txt.replace('👰🏠🏳👰👴🏠🏳', pluriels['Pays-residence-pere-mariee']['begin'])
                # txt = txt.replace('👧🎩🏡🌍👧🏡🌍', pluriels['Pays-residence-pere-mariee']['end'])
                # txt = txt.replace('👰🏠🔟👰👴🏠🔟', pluriels['Numero-rue-residence-pere-mariee']['begin'])
                # txt = txt.replace('👧🎩🏡🔢👧🏡🔢', pluriels['Numero-rue-residence-pere-mariee']['end'])
                # txt = txt.replace('👰🏠🛣👰👴🏠🛣', pluriels['Type-rue-residence-pere-mariee']['begin'])
                # txt = txt.replace('👧🎩🏡🛤👧🏡🛤', pluriels['Type-rue-residence-pere-mariee']['end'])
                # txt = txt.replace('👰🏠🔠👰👴🏠🔠', pluriels['Nom-rue-residence-pere-mariee']['begin'])
                # txt = txt.replace('👧🎩🏡🔡👧🏡🔡', pluriels['Nom-rue-residence-pere-mariee']['end'])

                txt = txt.replace(questions_dict['Ville-residence-mariee']['begin']+questions_dict['Ville-residence-pere-mariee']['begin'], pluriels['Ville-residence-pere-mariee']['begin'])
                txt = txt.replace(questions_dict['Ville-residence-pere-mariee']['end'][::-1]+questions_dict['Ville-residence-mariee']['end'][::-1], pluriels['Ville-residence-pere-mariee']['end'])

                txt = txt.replace(questions_dict['Departement-residence-mariee']['begin']+questions_dict['Departement-residence-pere-mariee']['begin'], pluriels['Departement-residence-pere-mariee']['begin'])
                txt = txt.replace(questions_dict['Departement-residence-pere-mariee']['end'][::-1]+questions_dict['Departement-residence-mariee']['end'][::-1], pluriels['Departement-residence-pere-mariee']['end'])

                txt = txt.replace(questions_dict['Pays-residence-mariee']['begin']+questions_dict['Pays-residence-pere-mariee']['begin'], pluriels['Pays-residence-pere-mariee']['begin'])
                txt = txt.replace(questions_dict['Pays-residence-pere-mariee']['end'][::-1]+questions_dict['Pays-residence-mariee']['end'][::-1], pluriels['Pays-residence-pere-mariee']['end'])

                txt = txt.replace(questions_dict['Numero-rue-residence-mariee']['begin']+questions_dict['Numero-rue-residence-pere-mariee']['begin'], pluriels['Numero-rue-residence-pere-mariee']['begin'])
                txt = txt.replace(questions_dict['Numero-rue-residence-pere-mariee']['end'][::-1]+questions_dict['Numero-rue-residence-mariee']['end'][::-1], pluriels['Numero-rue-residence-pere-mariee']['end'])

                txt = txt.replace(questions_dict['Type-rue-residence-mariee']['begin']+questions_dict['Type-rue-residence-pere-mariee']['begin'], pluriels['Type-rue-residence-pere-mariee']['begin'])
                txt = txt.replace(questions_dict['Type-rue-residence-pere-mariee']['end'][::-1]+questions_dict['Type-rue-residence-mariee']['end'][::-1], pluriels['Type-rue-residence-pere-mariee']['end'])

                txt = txt.replace(questions_dict['Nom-rue-residence-mariee']['begin']+questions_dict['Nom-rue-residence-pere-mariee']['begin'], pluriels['Nom-rue-residence-pere-mariee']['begin'])
                txt = txt.replace(questions_dict['Nom-rue-residence-pere-mariee']['end'][::-1]+questions_dict['Nom-rue-residence-mariee']['end'][::-1], pluriels['Nom-rue-residence-pere-mariee']['end'])



                #Parents mariee seuls
                # txt = txt.replace('👰👴🏠🌇👰👵🏠🌇', pluriels['Ville-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🌉👧🎩🏡🌉', pluriels['Ville-residence-parents-mariee']['end'])
                # txt = txt.replace('👰👴🏠🗺👰👵🏠🗺', pluriels['Departement-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡📌👧🎩🏡📌', pluriels['Departement-residence-parents-mariee']['end'])
                # txt = txt.replace('👰👴🏠🏳👰👵🏠🏳', pluriels['Pays-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🌍👧🎩🏡🌍', pluriels['Pays-residence-parents-mariee']['end'])
                # txt = txt.replace('👰👴🏠🔟👰👵🏠🔟', pluriels['Numero-rue-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🔢👧🎩🏡🔢', pluriels['Numero-rue-residence-parents-mariee']['end'])
                # txt = txt.replace('👰👴🏠🛣👰👵🏠🛣', pluriels['Type-rue-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🛤👧🎩🏡🛤', pluriels['Type-rue-residence-parents-mariee']['end'])
                # txt = txt.replace('👰👴🏠🔠👰👵🏠🔠', pluriels['Nom-rue-residence-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🏡🔡👧🎩🏡🔡', pluriels['Nom-rue-residence-parents-mariee']['end'])
                # txt = txt.replace('👰👴🔧👰👵🔧', pluriels['Profession-parents-mariee']['begin'])
                # txt = txt.replace('👧👒🪛👧🎩🪛', pluriels['Profession-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Ville-residence-pere-mariee']['begin']+questions_dict['Ville-residence-mere-mariee']['begin'], pluriels['Ville-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Ville-residence-mere-mariee']['end'][::-1]+questions_dict['Ville-residence-pere-mariee']['end'][::-1], pluriels['Ville-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Departement-residence-pere-mariee']['begin']+questions_dict['Departement-residence-mere-mariee']['begin'], pluriels['Departement-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Departement-residence-mere-mariee']['end'][::-1]+questions_dict['Departement-residence-pere-mariee']['end'][::-1], pluriels['Departement-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Pays-residence-pere-mariee']['begin']+questions_dict['Pays-residence-mere-mariee']['begin'], pluriels['Pays-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Pays-residence-mere-mariee']['end'][::-1]+questions_dict['Pays-residence-pere-mariee']['end'][::-1], pluriels['Pays-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Numero-rue-residence-pere-mariee']['begin']+questions_dict['Numero-rue-residence-mere-mariee']['begin'], pluriels['Numero-rue-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Numero-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Numero-rue-residence-pere-mariee']['end'][::-1], pluriels['Numero-rue-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Type-rue-residence-pere-mariee']['begin']+questions_dict['Type-rue-residence-mere-mariee']['begin'], pluriels['Type-rue-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Type-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Type-rue-residence-pere-mariee']['end'][::-1], pluriels['Type-rue-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Nom-rue-residence-pere-mariee']['begin']+questions_dict['Nom-rue-residence-mere-mariee']['begin'], pluriels['Nom-rue-residence-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Nom-rue-residence-mere-mariee']['end'][::-1]+questions_dict['Nom-rue-residence-pere-mariee']['end'][::-1], pluriels['Nom-rue-residence-parents-mariee']['end'])

                txt = txt.replace(questions_dict['Profession-pere-mariee']['begin']+questions_dict['Profession-mere-mariee']['begin'], pluriels['Profession-parents-mariee']['begin'])
                txt = txt.replace(questions_dict['Profession-mere-mariee']['end'][::-1]+questions_dict['Profession-pere-mariee']['end'][::-1], pluriels['Profession-parents-mariee']['end'])


                #mari + 2 parents
                # txt = txt.replace('👨🏠🌇👨👴🏠🌇👨👵🏠🌇', pluriels['Ville-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🌉👦🎩🏡🌉👦🏡🌉', pluriels['Ville-residence-parents-mari']['end'])
                # txt = txt.replace('👨🏠🗺👨👴🏠🗺👨👵🏠🗺', pluriels['Departement-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡📌👦🎩🏡📌👦🏡📌', pluriels['Departement-residence-parents-mari']['end'])
                # txt = txt.replace('👨🏠🏳👨👴🏠🏳👨👵🏠🏳', pluriels['Pays-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🌍👦🎩🏡🌍👦🏡🌍', pluriels['Pays-residence-parents-mari']['end'])
                # txt = txt.replace('👨🏠🔟👨👴🏠🔟👨👵🏠🔟', pluriels['Numero-rue-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🔢👦🎩🏡🔢👦🏡🔢', pluriels['Numero-rue-residence-parents-mari']['end'])
                # txt = txt.replace('👨🏠🛣👨👴🏠🛣👨👵🏠🛣', pluriels['Type-rue-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🛤👦🎩🏡🛤👦🏡🛤', pluriels['Type-rue-residence-parents-mari']['end'])
                # txt = txt.replace('👨🏠🔠👨👴🏠🔠👨👵🏠🔠', pluriels['Nom-rue-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🔡👦🎩🏡🔡👦🏡🔡', pluriels['Nom-rue-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Ville-residence-mari']['begin']+questions_dict['Ville-residence-pere-mari']['begin']+questions_dict['Ville-residence-mere-mari']['begin'], pluriels['Ville-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Ville-residence-mere-mari']['end'][::-1]+questions_dict['Ville-residence-pere-mari']['end'][::-1]+questions_dict['Ville-residence-mari']['end'][::-1], pluriels['Ville-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Departement-residence-mari']['begin']+questions_dict['Departement-residence-pere-mari']['begin']+questions_dict['Departement-residence-mere-mari']['begin'], pluriels['Departement-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Departement-residence-mere-mari']['end'][::-1]+questions_dict['Departement-residence-pere-mari']['end'][::-1]+questions_dict['Departement-residence-mari']['end'][::-1], pluriels['Departement-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Pays-residence-mari']['begin']+questions_dict['Pays-residence-pere-mari']['begin']+questions_dict['Pays-residence-mere-mari']['begin'], pluriels['Pays-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Pays-residence-mere-mari']['end'][::-1]+questions_dict['Pays-residence-pere-mari']['end'][::-1]+questions_dict['Pays-residence-mari']['end'][::-1], pluriels['Pays-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Numero-rue-residence-mari']['begin']+questions_dict['Numero-rue-residence-pere-mari']['begin']+questions_dict['Numero-rue-residence-mere-mari']['begin'], pluriels['Numero-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Numero-rue-residence-mere-mari']['end'][::-1]+questions_dict['Numero-rue-residence-pere-mari']['end'][::-1]+questions_dict['Numero-rue-residence-mari']['end'][::-1], pluriels['Numero-rue-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Type-rue-residence-mari']['begin']+questions_dict['Type-rue-residence-pere-mari']['begin']+questions_dict['Type-rue-residence-mere-mari']['begin'], pluriels['Type-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Type-rue-residence-mere-mari']['end'][::-1]+questions_dict['Type-rue-residence-pere-mari']['end'][::-1]+questions_dict['Type-rue-residence-mari']['end'][::-1], pluriels['Type-rue-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Nom-rue-residence-mari']['begin']+questions_dict['Nom-rue-residence-pere-mari']['begin']+questions_dict['Nom-rue-residence-mere-mari']['begin'], pluriels['Nom-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Nom-rue-residence-mere-mari']['end'][::-1]+questions_dict['Nom-rue-residence-pere-mari']['end'][::-1]+questions_dict['Nom-rue-residence-mari']['end'][::-1], pluriels['Nom-rue-residence-parents-mari']['end'])

                #mari + mere
                # txt = txt.replace('👨🏠🌇👨👵🏠🌇', pluriels['Ville-residence-mere-mari']['begin'])
                # txt = txt.replace('👦👒🏡🌉👦🏡🌉', pluriels['Ville-residence-mere-mari']['end'])
                # txt = txt.replace('👨🏠🗺👨👵🏠🗺', pluriels['Departement-residence-mere-mari']['begin'])
                # txt = txt.replace('👦👒🏡📌👦🏡📌', pluriels['Departement-residence-mere-mari']['end'])
                # txt = txt.replace('👨🏠🏳👨👵🏠🏳', pluriels['Pays-residence-mere-mari']['begin'])
                # txt = txt.replace('👦👒🏡🌍👦🏡🌍', pluriels['Pays-residence-mere-mari']['end'])
                # txt = txt.replace('👨🏠🔟👨👵🏠🔟', pluriels['Numero-rue-residence-mere-mari']['begin'])
                # txt = txt.replace('👦👒🏡🔢👦🏡🔢', pluriels['Numero-rue-residence-mere-mari']['end'])
                # txt = txt.replace('👨🏠🛣👨👵🏠🛣', pluriels['Type-rue-residence-mere-mari']['begin'])
                # txt = txt.replace('👦👒🏡🛤👦🏡🛤', pluriels['Type-rue-residence-mere-mari']['end'])
                # txt = txt.replace('👨🏠🔠👨👵🏠🔠', pluriels['Nom-rue-residence-mere-mari']['begin'])
                # txt = txt.replace('👦👒🏡🔡👦🏡🔡', pluriels['Nom-rue-residence-mere-mari']['end'])

                txt = txt.replace(questions_dict['Ville-residence-mari']['begin']+questions_dict['Ville-residence-mere-mari']['begin'], pluriels['Ville-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Ville-residence-mere-mari']['end'][::-1]+questions_dict['Ville-residence-mari']['end'][::-1], pluriels['Ville-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Departement-residence-mari']['begin']+questions_dict['Departement-residence-mere-mari']['begin'], pluriels['Departement-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Departement-residence-mere-mari']['end'][::-1]+questions_dict['Departement-residence-mari']['end'][::-1], pluriels['Departement-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Pays-residence-mari']['begin']+questions_dict['Pays-residence-mere-mari']['begin'], pluriels['Pays-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Pays-residence-mere-mari']['end'][::-1]+questions_dict['Pays-residence-mari']['end'][::-1], pluriels['Pays-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Numero-rue-residence-mari']['begin']+questions_dict['Numero-rue-residence-mere-mari']['begin'], pluriels['Numero-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Numero-rue-residence-mere-mari']['end'][::-1]+questions_dict['Numero-rue-residence-mari']['end'][::-1], pluriels['Numero-rue-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Type-rue-residence-mari']['begin']+questions_dict['Type-rue-residence-mere-mari']['begin'], pluriels['Type-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Type-rue-residence-mere-mari']['end'][::-1]+questions_dict['Type-rue-residence-mari']['end'][::-1], pluriels['Type-rue-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Nom-rue-residence-mari']['begin']+questions_dict['Nom-rue-residence-mere-mari']['begin'], pluriels['Nom-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Nom-rue-residence-mere-mari']['end'][::-1]+questions_dict['Nom-rue-residence-mari']['end'][::-1], pluriels['Nom-rue-residence-parents-mari']['end'])


                #mari + pere
                # txt = txt.replace('👨🏠🌇👨👴🏠🌇', pluriels['Ville-residence-pere-mari']['begin'])
                # txt = txt.replace('👦🎩🏡🌉👦🏡🌉', pluriels['Ville-residence-pere-mari']['end'])
                # txt = txt.replace('👨🏠🗺👨👴🏠🗺', pluriels['Departement-residence-pere-mari']['begin'])
                # txt = txt.replace('👦🎩🏡📌👦🏡📌', pluriels['Departement-residence-pere-mari']['end'])
                # txt = txt.replace('👨🏠🏳👨👴🏠🏳', pluriels['Pays-residence-pere-mari']['begin'])
                # txt = txt.replace('👦🎩🏡🌍👦🏡🌍', pluriels['Pays-residence-pere-mari']['end'])
                # txt = txt.replace('👨🏠🔟👨👴🏠🔟', pluriels['Numero-rue-residence-pere-mari']['begin'])
                # txt = txt.replace('👦🎩🏡🔢👦🏡🔢', pluriels['Numero-rue-residence-pere-mari']['end'])
                # txt = txt.replace('👨🏠🛣👨👴🏠🛣', pluriels['Type-rue-residence-pere-mari']['begin'])
                # txt = txt.replace('👦🎩🏡🛤👦🏡🛤', pluriels['Type-rue-residence-pere-mari']['end'])
                # txt = txt.replace('👨🏠🔠👨👴🏠🔠', pluriels['Nom-rue-residence-pere-mari']['begin'])
                # txt = txt.replace('👦🎩🏡🔡👦🏡🔡', pluriels['Nom-rue-residence-pere-mari']['end'])

                txt = txt.replace(questions_dict['Ville-residence-mari']['begin']+questions_dict['Ville-residence-pere-mari']['begin'], pluriels['Ville-residence-pere-mari']['begin'])
                txt = txt.replace(questions_dict['Ville-residence-pere-mari']['end'][::-1]+questions_dict['Ville-residence-mari']['end'][::-1], pluriels['Ville-residence-pere-mari']['end'])

                txt = txt.replace(questions_dict['Departement-residence-mari']['begin']+questions_dict['Departement-residence-pere-mari']['begin'], pluriels['Departement-residence-pere-mari']['begin'])
                txt = txt.replace(questions_dict['Departement-residence-pere-mari']['end'][::-1]+questions_dict['Departement-residence-mari']['end'][::-1], pluriels['Departement-residence-pere-mari']['end'])

                txt = txt.replace(questions_dict['Pays-residence-mari']['begin']+questions_dict['Pays-residence-pere-mari']['begin'], pluriels['Pays-residence-pere-mari']['begin'])
                txt = txt.replace(questions_dict['Pays-residence-pere-mari']['end'][::-1]+questions_dict['Pays-residence-mari']['end'][::-1], pluriels['Pays-residence-pere-mari']['end'])

                txt = txt.replace(questions_dict['Numero-rue-residence-mari']['begin']+questions_dict['Numero-rue-residence-pere-mari']['begin'], pluriels['Numero-rue-residence-pere-mari']['begin'])
                txt = txt.replace(questions_dict['Numero-rue-residence-pere-mari']['end'][::-1]+questions_dict['Numero-rue-residence-mari']['end'][::-1], pluriels['Numero-rue-residence-pere-mari']['end'])

                txt = txt.replace(questions_dict['Type-rue-residence-mari']['begin']+questions_dict['Type-rue-residence-pere-mari']['begin'], pluriels['Type-rue-residence-pere-mari']['begin'])
                txt = txt.replace(questions_dict['Type-rue-residence-pere-mari']['end'][::-1]+questions_dict['Type-rue-residence-mari']['end'][::-1], pluriels['Type-rue-residence-pere-mari']['end'])

                txt = txt.replace(questions_dict['Nom-rue-residence-mari']['begin']+questions_dict['Nom-rue-residence-pere-mari']['begin'], pluriels['Nom-rue-residence-pere-mari']['begin'])
                txt = txt.replace(questions_dict['Nom-rue-residence-pere-mari']['end'][::-1]+questions_dict['Nom-rue-residence-mari']['end'][::-1], pluriels['Nom-rue-residence-pere-mari']['end'])


                #Parents mari seuls
                # txt = txt.replace('👨👴🏠🌇👨👵🏠🌇', pluriels['Ville-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🌉👦🎩🏡🌉', pluriels['Ville-residence-parents-mari']['end'])
                # txt = txt.replace('👨👴🏠🗺👨👵🏠🗺', pluriels['Departement-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡📌👦🎩🏡📌', pluriels['Departement-residence-parents-mari']['end'])
                # txt = txt.replace('👨👴🏠🏳👨👵🏠🏳', pluriels['Pays-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🌍👦🎩🏡🌍', pluriels['Pays-residence-parents-mari']['end'])
                # txt = txt.replace('👨👴🏠🔟👨👵🏠🔟', pluriels['Numero-rue-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🔢👦🎩🏡🔢', pluriels['Numero-rue-residence-parents-mari']['end'])
                # txt = txt.replace('👨👴🏠🛣👨👵🏠🛣', pluriels['Type-rue-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🛤👦🎩🏡🛤', pluriels['Type-rue-residence-parents-mari']['end'])
                # txt = txt.replace('👨👴🏠🔠👨👵🏠🔠', pluriels['Nom-rue-residence-parents-mari']['begin'])
                # txt = txt.replace('👦👒🏡🔡👦🎩🏡🔡', pluriels['Nom-rue-residence-parents-mari']['end'])

                # txt = txt.replace('👨👴🔧👨👵🔧', pluriels['Profession-parents-mari']['begin'])
                # txt = txt.replace('👦👒🪛👦🎩🪛', pluriels['Profession-parents-mari']['end'])


                txt = txt.replace(questions_dict['Ville-residence-pere-mari']['begin']+questions_dict['Ville-residence-mere-mari']['begin'], pluriels['Ville-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Ville-residence-mere-mari']['end'][::-1]+questions_dict['Ville-residence-pere-mari']['end'][::-1], pluriels['Ville-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Departement-residence-pere-mari']['begin']+questions_dict['Departement-residence-mere-mari']['begin'], pluriels['Departement-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Departement-residence-mere-mari']['end'][::-1]+questions_dict['Departement-residence-pere-mari']['end'][::-1], pluriels['Departement-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Pays-residence-pere-mari']['begin']+questions_dict['Pays-residence-mere-mari']['begin'], pluriels['Pays-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Pays-residence-mere-mari']['end'][::-1]+questions_dict['Pays-residence-pere-mari']['end'][::-1], pluriels['Pays-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Numero-rue-residence-pere-mari']['begin']+questions_dict['Numero-rue-residence-mere-mari']['begin'], pluriels['Numero-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Numero-rue-residence-mere-mari']['end'][::-1]+questions_dict['Numero-rue-residence-pere-mari']['end'][::-1], pluriels['Numero-rue-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Type-rue-residence-pere-mari']['begin']+questions_dict['Type-rue-residence-mere-mari']['begin'], pluriels['Type-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Type-rue-residence-mere-mari']['end'][::-1]+questions_dict['Type-rue-residence-pere-mari']['end'][::-1], pluriels['Type-rue-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Nom-rue-residence-pere-mari']['begin']+questions_dict['Nom-rue-residence-mere-mari']['begin'], pluriels['Nom-rue-residence-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Nom-rue-residence-mere-mari']['end'][::-1]+questions_dict['Nom-rue-residence-pere-mari']['end'][::-1], pluriels['Nom-rue-residence-parents-mari']['end'])

                txt = txt.replace(questions_dict['Profession-pere-mari']['begin']+questions_dict['Profession-mere-mari']['begin'], pluriels['Profession-parents-mari']['begin'])
                txt = txt.replace(questions_dict['Profession-mere-mari']['end'][::-1]+questions_dict['Profession-pere-mari']['end'][::-1], pluriels['Profession-parents-mari']['end'])

                
            
                text[paragraph] = txt

            return text
        # full_text = ""
        # for paragraph, labels in labels_act.items():
        #     full_text += text[paragraph]

        full_text = raw_text[act_name]
        print("full_text : ", full_text)
        for paragraph, labels  in labels_act.items():
            text[paragraph] = text[paragraph].replace("-\n", "").replace("\n", " ")
            print('aled')
            print("Paragraph : ", paragraph)
            print("text : ", text[paragraph])
            if text[paragraph] == "":
                print("empty paragraph")
                continue
            for key, label in labels.items():
                if label != "":
                    if label == "true" or label == "false":
                        continue
                    #print("\n\n")
                    print('key : ', key, " label : ", label)
                    text[paragraph] = insert_emojis_around_label(key, paragraph, text[paragraph])
                    print("done")
                    #print(text[paragraph])
                    #print("\n\n")
        final = fix_pluriels(text)
        full_text_with_emojis = ""
        for paragraph, txt in final.items():
            full_text_with_emojis += txt

        #Merge full_text and full_text_with_emojis. The goal is to keep emojis, and to add \n, -\n and missing words from full_text_with_emojis to full_text
        #We assume that full_text_with_emojis is a superset of full_text
        #We also assume that full_text_with_emojis is a subset of full_text


        
        emogised_acts[act_name] = {'paragraphs' : final, 'full_text' : full_text_with_emojis}

    return emogised_acts


#main : take 2 args : input file and output name.
#- load the input json
#- emojize the acts
#- save the output json

if __name__ == "__main__":
    import json
    import argparse

    parser = argparse.ArgumentParser(description='Emojize the acts')
    parser.add_argument('input', metavar='input', type=str,
                        help='the input json file')
    parser.add_argument('output', metavar='output', type=str,
                        help='the output json file')
    parser.add_argument('raw_text', metavar='raw_text', type=str,
                        help='the raw text with special characters')
    args = parser.parse_args()
    with open(args.input) as json_file:
        data = json.load(json_file)

    with open(args.raw_text) as json_file:
        raw_text = json.load(json_file)
    
    for name in data.keys():
        tmp = {
            "prenom-mari-p4" :"",
            "nom-mari-p4" :"",
            "prenom-mariee-p4" :"",
            "nom-mariee-p4" :"",
        }
        for key in tmp.keys():
            if key in data[name]:
                tmp[key] = data[name]['labels']['p4'][key]
            
        data[name]['labels']['p4'] = tmp

        
    emojized = emojize(data, raw_text)


    with open(args.output, 'w') as outfile:
        #dump json, keep special characters
        json.dump(emojized, outfile, ensure_ascii=False, indent=4)

