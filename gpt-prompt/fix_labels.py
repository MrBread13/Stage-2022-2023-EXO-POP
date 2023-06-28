import re

#list of all european countries
countries = ['Albanie', 'Allemagne', 'Andorre', 'Autriche', 'Belgique', 'Biélorussie', 'Bosnie-Herzégovine', 'Bulgarie', 'Croatie', 'Danemark', 'Espagne', 'Estonie', 'Finlande', 'France', 'Grèce', 'Hongrie','Hollande','Irlande', 'Islande', 'Italie', 'Lettonie', 'Liechtenstein', 'Lituanie', 'Luxembourg', 'Macédoine', 'Malte', 'Moldavie', 'Monaco', 'Monténégro', 'Norvège', 'Pays-Bas', 'Pologne', 'Portugal', 'Roumanie', 'Royaume-Uni', 'Russie', 'Saint-Marin', 'Serbie', 'Slovaquie', 'Slovénie', 'Suède', 'Suisse', 'République tchèque', 'Turquie', 'Ukraine', 'Vatican']

def check_dep_country(labels : dict) -> dict :
    for event in ['naissance', 'residence']:
        for per in ['mari','mariee']:
            dep = labels[''.join(['Departement','-',event,'-',per])]
            country = labels[''.join(['Pays','-',event,'-',per])]
            city = labels[''.join(['Ville','-',event,'-',per])]

            if dep != '' and (dep in countries) :
                labels[''.join(['Pays','-',event,'-',per])] = dep
                labels[''.join(['Departement','-',event,'-',per])] = ''

            if country != '' and (country not in countries) : 
                labels[''.join(['Departement','-',event,'-',per])] = country
                labels[''.join(['Pays','-',event,'-',per])] = ''

            #use a regex to check if city contains a country between () or **
            if city != '' :
                regex = re.compile(r'\((.*?)\)')
                match = regex.search(city)
                if match :
                    potential_country = match.group(1)
                    if potential_country in countries :
                        labels[''.join(['Pays','-',event,'-',per])] = potential_country
                        labels[''.join(['Ville','-',event,'-',per])] = city.replace(match.group(0),'')
                        labels[''.join(['Departement','-',event,'-',per])] = ''

                    else :
                        labels[''.join(['Pays','-',event,'-',per])] = ''
                        labels[''.join(['Ville','-',event,'-',per])] = city.replace(match.group(0),'')
                        labels[''.join(['Departement','-',event,'-',per])] = potential_country

                regex = re.compile(r'\*\*(.*?)\*\*')
                match = regex.search(city)
                if match :
                    potential_country = match.group(1)
                    if potential_country in countries :
                        labels[''.join(['Pays','-',event,'-',per])] = potential_country
                        labels[''.join(['Ville','-',event,'-',per])] = city.replace(match.group(0),'')
                        labels[''.join(['Departement','-',event,'-',per])] = ''

                    else :
                        labels[''.join(['Pays','-',event,'-',per])] = ''
                        labels[''.join(['Ville','-',event,'-',per])] = city.replace(match.group(0),'')
                        labels[''.join(['Departement','-',event,'-',per])] = potential_country


            

    for event in ['residence']:
        for per in ['pere-mari', 'mere-mari', 'pere-mariee', 'mere-mariee']:
            dep = labels[''.join(['Departement','-',event,'-',per])]
            country = labels[''.join(['Pays','-',event,'-',per])]

            if dep != '' and (dep in countries) :
                labels[''.join(['Pays','-',event,'-',per])] = dep
                labels[''.join(['Departement','-',event,'-',per])] = ''

            if country != '' and (country not in countries) : 
                labels[''.join(['Departement','-',event,'-',per])] = country
                labels[''.join(['Pays','-',event,'-',per])] = ''

    return labels

def check_job(labels : dict) -> dict :
    to_check = ['décédé','décédée','décédés','disparu','disparue','disparus']
    for field in ['Profession-pere-mari', 'Profession-mere-mari', 'Profession-pere-mariee', 'Profession-mere-mariee']:
        for word in to_check :
            if word in labels[field] :
                labels[field] = ''

        if 'sans profession' in labels[field] :
            labels[field] = 'sans profession'

        #if 'son épouse' in string, string = string - son épouse
        if 'son épouse' in labels[field] :
            labels[field] = labels[field].replace('son épouse','')

    return labels

def check_minutes(labels : dict) -> dict :
    to_check = ['none', 'None', 'non précisé', 'non spécifié', 'non mentionné', 'inconnues','non référencé']
    if labels['Minute-mariage'] in to_check :
        labels['Minute-mariage'] = ''

    return labels


def sanitize_labels(labels : dict) -> dict :
    labels = check_dep_country(labels)
    labels = check_job(labels)
    labels = check_minutes(labels)

    return labels


