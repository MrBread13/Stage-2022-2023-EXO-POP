import json
import openai
import Levenshtein

openai.organization = "org-2wXrLf4fLEfdyawavmkAqi8z"
openai.api_key = "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"

#intro sequence:
intro = "Nous allons te fournir un certificat de mariage, un document ayant toujours la même mise en forme.Tu vas devoir procéder à l’extraction de certaines données sur plusieurs certificats ensuite. Voici le premier certificat, je précise qu’il est extrait d’un document au format Json et que tu auras toutes les réponses fournies à la fin, cela te permettra de mieux reconnaître ce qu’il te faut obtenir dans les contrats suivants. "
# Un exemple d'acte:
act_example = """Le huit avril mil neuf cent quarante, onze heures cinq minutes ****\ndevant Nous ont comparu publiquement en la maison commune: Camille Marcel MOUROT, barman, né à Dijon\nCôte d'Or * le dix-huit février mil neuf cent onze * vingt-neuf ans, domicilié à Paris, 17, rue\nPierre Lescot, actuellement aux armées; fils de Emile MOUROT et de Pauline MONIOT, époux décédés,\nd'une part ,/- ET Jeanne BLONDEAU, sans profession, née à Jars * Cher * le seize mars mil neuf cent\nneuf, trente et un ans, domiciliée à Paris, 17, rue Pierre Lescot; fille de Emile Joseph BLONDEAU\net de Marie Louise MELOT, son épouse, marchands de bestiaux, domiciliés à Vailly sur Saône * Cher *\nDivorcée de William Louis Paul BERNON, d'autre part ;- Les futurs époux déclarent quil n'a pas été\nfait de contrat de mariage .- Camille Marcel MOUROT et Jeanne BLONDEAU ont déclaré l'un après l'autre\nvouloir se prendre pour époux et Nous avons prononcé au nom de la loi qu'ils sont unis par le mariage.\nEn présence de: Emile SOLIGNAC, commerçant, Médaillé militaire, Croix de Guerre, 16 bis, rue\nLauriston, et de Marcelle MOUROT, vendeuse, 22, rue de l'Echiquier, témoins majeurs, qui, lecture\nfaite ont signé avec les époux et Nous, Pierre Louis Adolphe BERTRAND, Maire du Premier arrondisse-\nment de Paris, Chevalier de la Légion d'Honneur ./ \n  
            "Jour-du-mariage": "huit",
            "Mois-du-mariage": "avril",
            "Année-du-mariage": "mil neuf cent quarante",
            "Heure-du-mariage": "onze heures",
            "Minute-du-mariage": "cinq minutes",
            "Prenom-de-l'adjoint-au-maire": "Pierre Louis Adolphe",
            "Nom-de-l'adjoint-au-maire": "BERTRAND",
            "Ville-du-mariage": "",
            "Prénom-du-mari": "Camille Marcel",
            "Nom-du-mari": "MOUROT",
            "Métier-du-mari": "barman",
            "Ville-de-naissance-du-mari": "Dijon\nCôte d'Or",
            "Département-de-naissance-du-mari": "",
            "Pays-de-naissance-du-mari": "",
            "Jour-de-naissance-du-mari": "dix-huit",
            "Mois-de-naissance-du-mari": "février",
            "Année-de-naissance-du-mari": "mil neuf cent onze",
            "Age-du-mari": "vingt-neuf ans",
            "Ville-de-résidence-du-mari": "Paris",
            "Département-de-résidence-du-mari": "",
            "Pays-de-résidence-du-mari": "",
            "Numéro-de-rue-de-résidence-du-mari": "17",
            "Type-de-rue-de-résidence-du-mari": "rue",
            "Nom-de-rue-de-résidence-du-mari": "Pierre Lescot",
            "Prénom-du-père-du-mari": "Emile",
            "Nom-du-père-du-mari": "MOUROT",
            "Métier-du-père-du-mari": "",
            "Ville-de-résidence-du-père-du-mari": "",
            "Département-du-résidence-du-père-du-mari": "",
            "Numéro-de-résidence-du-père-du-mari": "",
            "Type-de-rue-de-résidence-du-père-du-mari": "",
            "Nom-de-rue-de-résidence-du-père-du-mari": "",
            "Prénom-de-la-mère-du-mari": "Pauline",
            "Nom-de-la-mère-du-mari": "MONIOT",
            "Profession-de-la-mère-du-mari": "",
            "Ville-de-résidence-de-la-mère-du-mari": "",
            "Département-de-résidence-de-la-mère-du-mari": "",
            "Pays-de-résidence-de-la-mère-du-mari": "",
            "Numéro-de-rue-de-résidence-de-la-mère-du-mari": "",
            "Type-de-rue-de-résidence-de-la-mère-du-mari": "",
            "Nom-de-rue-de-résidence-de-la-mère-du-mari": "",
            "Prénom-de-la-mariée": "Jeanne",
            "Nom-de-la-mariée": "BLONDEAU",
            "Métier-de-la-mariée": "sans profession",
            "Ville-de-naissance-de-la-mariée": "Jars",
            "Département-de-naissance-de-la-mariée": "Cher",
            "Pays-de-naissance-de-la-mariée": "",
            "Jour-de-naissance-de-la-mariée": "seize",
            "Mois-de-naissance-de-la-mariée": "mars",
            "Année-de-naissance-de-la-mariée": "mil neuf cent\nneuf",
            "Age-de-la-mariée": "trente et un ans",
            "Ville-de-résidence-de-la-mariée": "Paris",
            "Département-de-résidence-de-la-mariée": "Cher",
            "Pays-de-résidence-de-la-mariée": "",
            "Numéro-de-rue-de-résidence-de-la-mariée": "17",
            "Type-de-rue-de-résidence-de-la-mariée": "rue",
            "Nom-de-rue-de-résidence-de-la-mariée": "Pierre Lescot",
            "Prénom-du-père-de-la-mariée": "Emile Joseph",
            "Nom-du-père-de-la-mariée": "BLONDEAU",
            "Métier-du-père-de-la-mariée": "",
            "Ville-de-résidence-du-père-de-la-mariée": "",
            "Département-du-résidence-du-père-de-la-mariée": "",
            "Numéro-de-résidence-du-père-de-la-mariée": "",
            "Type-de-rue-de-résidence-du-père-de-la-mariée": "",
            "Nom-de-rue-de-résidence-du-père-de-la-mariée": "",
            "Prénom-de-la-mère-de-la-mariée": "Marie Louise",
            "Nom-de-la-mère-de-la-mariée": "MELOT",
            "Profession-de-la-mère-de-la-mariée": "marchands de bestiaux",
            "Ville-de-résidence-de-la-mère-de-la-mariée": "",
            "Département-de-résidence-de-la-mère-de-la-mariée": "",
            "Pays-de-résidence-de-la-mère-de-la-mariée": "",
            "Numéro-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
            "Type-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
            "Nom-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
            "Prénom-de-l'ex-époux": "William Louis Paul",
            "Nom-de-l'ex-époux": "BERNON",
            "Prénom-du-témoin-0": "Emile",
            "Nom-du-témoin-0": "SOLIGNAC",
            "Métier-du-témoin-0": "commerçant",
            "Age-du-témoin": "",
            "Numéro-de-rue-de-résidence-du-témoin-0": "16 bis",
            "Type-de-rue-de-résidence-du-témoin-0": "rue",
            "Nom-de-rue-de-résidence-du-témoin-0": "Lauriston",
            "Ville-de-résidence-du-témoin": "",
            "Département-du-résidence-du-témoin": "",
            "Prénom-du-témoin-1": "Marcelle",
            "Nom-du-témoin-1": "MOUROT",
            "Métier-du-témoin-1": "vendeuse",
            "Numéro-de-rue-de-résidence-du-témoin-1": "22",
            "Type-de-rue-de-résidence-du-témoin-1": "rue",
            "Nom-de-rue-de-résidence-du-témoin-1": "de l'Echiquier"""

question=""" Maintenant, voici un autre certificat de mariage : je veux que tu m'extrais des données sous la meme forme que les réponses que je t'ai fourni. Précision : compte les arrondissement comme une ville."""

def labels_from_act(act_text : str) -> dict :
    """
    Extrait les labels d'un acte de mariage.
    input: act_text: texte de l'acte de mariage
    output: dictionnaire des label
    """
    prompt= intro + act_example + question + act_text

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt,},
    ]
    )
    answer = completion.choices[0].message['content']
    answer = answer.replace('\n', '').replace('.','')
    print(answer)
    answer = json.loads('{'+','.join(answer.split(',')[:-1])+'}')
    return answer

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    act_text = """ neuf avril mil neuf cent quarante * onze heures vingt minutes ****\ndevant Nous ont comparu publiquement en la maison commune: Antoine POCARD, porteur aux halles, né à\nParis, dixième arrondissement, le cinq février mil neuf cent un, trente-neuf ans, domicilié à Paris\n56, rue Saint Honoré; actuellement mobilisé- fils de Jeanne Marie POCARD- Veuf de Juliette **\nAlbertine GAYRARD, d'une part ,/- ET Adrienne Jeanne ALBRIEUX, journalière, née à Paris, onzième\narrondissement, le onze septembre mil neuf cent deux, trente-sept ans; domiciliée à Paris, 56, rue\nSaint Honoré; fille de Marie Charles ALBRIEUX, sans profession, domicilié à Aulnay sous Bois * Sein\net Oise * et de Marguerite TERLES, décédée, d'autre part ;- Les futurs époux déclarent qu'il n'a\npas été fait de contrat de mariage .- Antoine POCARD et Adrienne Jeanne ALBRIEUX ont déclaré l'un\naprès l'autre vouloir se prendre pour époux et Nous avons prononcé au nom de la loi qu'ils sont\nunis par le mariage .- En présence de: Fernande PASTEAU, concierge, 13, rue Dussoubs, et de\nAmélie MASSONIE, ménagère, 10 rue Volta, témoins majeurs, qui, lecture farte ont signé avec\nles époux et Nous, Charles Louis TOURY, Officier de l'état-civil du premier arrondissement de\nParis, Chevalier de la Légion d'Honneur ./"""

    labels = labels_from_act(act_text)
    #print(labels)

    # On vérifie que les labels extraits sont bien les mêmes que ceux de l'acte de mariage:

    ref = {
            "Jour-du-mariage": "neuf",
            "Mois-du-mariage": "avril",
            "Année-du-mariage": "mil neuf cent quarante",
            "Heure-du-mariage": "onze heures",
            "Minute-du-mariage": "vingt minutes",
            "Prenom-de-l'adjoint-au-maire": "Charles Louis",
            "Nom-de-l'adjoint-au-maire": "TOURY",
            "Ville-du-mariage": "premier arrondissement de\nParis",
            "Prénom-du-mari": "Antoine",
            "Nom-du-mari": "POCARD",
            "Métier-du-mari": "porteur aux halles",
            "Ville-de-naissance-du-mari": "Paris, dixième arrondissement",
            "Département-de-naissance-du-mari": "",
            "Pays-de-naissance-du-mari": "",
            "Jour-de-naissance-du-mari": "cinq",
            "Mois-de-naissance-du-mari": "février",
            "Année-de-naissance-du-mari": "mil neuf cent un",
            "Age-du-mari": "trente-neuf ans",
            "Ville-de-résidence-du-mari": "Paris",
            "Département-de-résidence-du-mari": "",
            "Pays-de-résidence-du-mari": "",
            "Numéro-de-rue-de-résidence-du-mari": "56",
            "Type-de-rue-de-résidence-du-mari": "rue",
            "Nom-de-rue-de-résidence-du-mari": "Saint Honoré",
            "Prénom-du-père-du-mari": "",
            "Nom-du-père-du-mari": "",
            "Métier-du-père-du-mari": "",
            "Ville-de-résidence-du-père-du-mari": "",
            "Département-du-résidence-du-père-du-mari": "",
            "Numéro-de-résidence-du-père-du-mari": "",
            "Type-de-rue-de-résidence-du-père-du-mari": "",
            "Nom-de-rue-de-résidence-du-père-du-mari": "",
            "Prénom-de-la-mère-du-mari": "Jeanne Marie",
            "Nom-de-la-mère-du-mari": "POCARD-",
            "Profession-de-la-mère-du-mari": "",
            "Ville-de-résidence-de-la-mère-du-mari": "",
            "Département-de-résidence-de-la-mère-du-mari": "",
            "Pays-de-résidence-de-la-mère-du-mari": "",
            "Numéro-de-rue-de-résidence-de-la-mère-du-mari": "",
            "Type-de-rue-de-résidence-de-la-mère-du-mari": "",
            "Nom-de-rue-de-résidence-de-la-mère-du-mari": "",
            "Prénom-de-la-mariée": "Adrienne Jeanne",
            "Nom-de-la-mariée": "ALBRIEUX",
            "Métier-de-la-mariée": "journalière",
            "Ville-de-naissance-de-la-mariée": "Paris, onzième\narrondissement",
            "Département-de-naissance-de-la-mariée": "",
            "Pays-de-naissance-de-la-mariée": "",
            "Jour-de-naissance-de-la-mariée": "onze",
            "Mois-de-naissance-de-la-mariée": "septembre",
            "Année-de-naissance-de-la-mariée": "mil neuf cent deux",
            "Age-de-la-mariée": "trente-sept ans",
            "Ville-de-résidence-de-la-mariée": "Paris",
            "Département-de-résidence-de-la-mariée": "",
            "Pays-de-résidence-de-la-mariée": "",
            "Numéro-de-rue-de-résidence-de-la-mariée": "56",
            "Type-de-rue-de-résidence-de-la-mariée": "rue",
            "Nom-de-rue-de-résidence-de-la-mariée": "Saint Honoré",
            "Prénom-du-père-de-la-mariée": "Marie Charles",
            "Nom-du-père-de-la-mariée": "ALBRIEUX",
            "Métier-du-père-de-la-mariée": "sans profession",
            "Ville-de-résidence-du-père-de-la-mariée": "Aulnay sous Bois",
            "Département-du-résidence-du-père-de-la-mariée": "Sein \net Oise",
            "Numéro-de-résidence-du-père-de-la-mariée": "",
            "Type-de-rue-de-résidence-du-père-de-la-mariée": "",
            "Nom-de-rue-de-résidence-du-père-de-la-mariée": "",
            "Prénom-de-la-mère-de-la-mariée": "Marguerite",
            "Nom-de-la-mère-de-la-mariée": "TERLES",
            "Profession-de-la-mère-de-la-mariée": "",
            "Ville-de-résidence-de-la-mère-de-la-mariée": "",
            "Département-de-résidence-de-la-mère-de-la-mariée": "",
            "Pays-de-résidence-de-la-mère-de-la-mariée": "",
            "Numéro-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
            "Type-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
            "Nom-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
            "Prénom-de-l'ex-époux": "",
            "Nom-de-l'ex-époux": "",
            "Prénom-du-témoin-0": "Fernande",
            "Nom-du-témoin-0": "PASTEAU",
            "Métier-du-témoin-0": "concierge",
            "Age-du-témoin": "",
            "Numéro-de-rue-de-résidence-du-témoin-0": "13",
            "Type-de-rue-de-résidence-du-témoin-0": "rue",
            "Nom-de-rue-de-résidence-du-témoin-0": "Dussoubs",
            "Ville-de-résidence-du-témoin": "",
            "Département-du-résidence-du-témoin": "",
            "Prénom-du-témoin-1": "Amélie",
            "Nom-du-témoin-1": "MASSONIE",
            "Métier-du-témoin-1": "ménagère",
            "Numéro-de-rue-de-résidence-du-témoin-1": "10",
            "Type-de-rue-de-résidence-du-témoin-1": "rue",
            "Nom-de-rue-de-résidence-du-témoin-1": "Volta"
        }
    
    distances = 0
    for key in ref.keys():
        distance = Levenshtein.distance(labels[key], ref[key])
        if distance > 0:
            print(key, distance, labels[key] if labels[key] != '' else 'VIDE', ref[key] if ref[key] != '' else 'VIDE')
        distances += distance

    print(distances)







