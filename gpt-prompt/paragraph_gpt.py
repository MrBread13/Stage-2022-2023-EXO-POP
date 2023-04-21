import json
import openai
import Levenshtein
import itertools
openai.organization = "org-2wXrLf4fLEfdyawavmkAqi8z"
openai.api_key = "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"

template = {
            "p1" : {
                "Jour-du-mariage": "",
                "Mois-du-mariage": "",
                "Année-du-mariage": "",
                "Heure-du-mariage": "",
                "Minute-du-mariage": ""
            },
            "p2" : {
                "Prénom-du-mari": "",
                "Nom-du-mari": "",
                "Métier-du-mari": "",
                "Ville-de-naissance-du-mari": "",
                "Département-de-naissance-du-mari": "",
                "Pays-de-naissance-du-mari": "",
                "Jour-de-naissance-du-mari": "",
                "Mois-de-naissance-du-mari": "",
                "Année-de-naissance-du-mari": "",
                "Age-du-mari": "",
                "Ville-de-résidence-du-mari": "",
                "Département-de-résidence-du-mari": "",
                "Pays-de-résidence-du-mari": "",
                "Numéro-de-rue-de-résidence-du-mari": "",
                "Type-de-rue-de-résidence-du-mari": "",
                "Nom-de-rue-de-résidence-du-mari": "",
                "Prénom-du-père-du-mari": "",
                "Nom-du-père-du-mari": "",
                "Métier-du-père-du-mari": "",
                "Ville-de-résidence-du-père-du-mari": "",
                "Département-de-résidence-du-père-du-mari": "",
                "Numéro-de-résidence-du-père-du-mari": "",
                "Type-de-rue-de-résidence-du-père-du-mari": "",
                "Nom-de-rue-de-résidence-du-père-du-mari": "",
                "Prénom-de-la-mère-du-mari": "",
                "Nom-de-la-mère-du-mari": "",
                "Profession-de-la-mère-du-mari": "",
                "Ville-de-résidence-de-la-mère-du-mari": "",
                "Département-de-résidence-de-la-mère-du-mari": "",
                "Pays-de-résidence-de-la-mère-du-mari": "",
                "Numéro-de-rue-de-résidence-de-la-mère-du-mari": "",
                "Type-de-rue-de-résidence-de-la-mère-du-mari": "",
                "Nom-de-rue-de-résidence-de-la-mère-du-mari": "",
                "Prénom-de-l'ex-épouse": "",
                "Nom-de-l'ex-épouse": ""
                },
            "p3" : {
                "Prénom-de-la-mariée": "",
                "Nom-de-la-mariée": "",
                "Métier-de-la-mariée": "",
                "Ville-de-naissance-de-la-mariée": "",
                "Département-de-naissance-de-la-mariée": "",
                "Pays-de-naissance-de-la-mariée": "",
                "Jour-de-naissance-de-la-mariée": "",
                "Mois-de-naissance-de-la-mariée": "",
                "Année-de-naissance-de-la-mariée": "",
                "Age-de-la-mariée": "",
                "Ville-de-résidence-de-la-mariée": "",
                "Département-de-résidence-de-la-mariée": "",
                "Pays-de-résidence-de-la-mariée": "",
                "Numéro-de-rue-de-résidence-de-la-mariée": "",
                "Type-de-rue-de-résidence-de-la-mariée": "",
                "Nom-de-rue-de-résidence-de-la-mariée": "",
                "Prénom-du-père-de-la-mariée": "",
                "Nom-du-père-de-la-mariée": "",
                "Métier-du-père-de-la-mariée": "",
                "Ville-de-résidence-du-père-de-la-mariée": "",
                "Département-de-résidence-du-père-de-la-mariée": "",
                "Numéro-de-résidence-du-père-de-la-mariée": "",
                "Type-de-rue-de-résidence-du-père-de-la-mariée": "",
                "Nom-de-rue-de-résidence-du-père-de-la-mariée": "",
                "Prénom-de-la-mère-de-la-mariée": "",
                "Nom-de-la-mère-de-la-mariée": "",
                "Profession-de-la-mère-de-la-mariée": "",
                "Ville-de-résidence-de-la-mère-de-la-mariée": "",
                "Département-de-résidence-de-la-mère-de-la-mariée": "",
                "Pays-de-résidence-de-la-mère-de-la-mariée": "",
                "Numéro-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
                "Type-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
                "Nom-de-rue-de-résidence-de-la-mère-de-la-mariée": "",
                "Prénom-de-l'ex-époux": "",
                "Nom-de-l'ex-époux": ""
            },
            "p4" : {
            },
            "p5" : {
                "Prénom-du-témoin-0": "",
                "Nom-du-témoin-0": "",
                "Métier-du-témoin-0": "",
                "Age-du-témoin-0": "",
                "Numéro-de-rue-de-résidence-du-témoin-0": "",
                "Type-de-rue-de-résidence-du-témoin-0": "",
                "Nom-de-rue-de-résidence-du-témoin-0": "",
                "Ville-de-résidence-du-témoin-0": "",
                "Département-de-résidence-du-témoin-0": "",
                "Prénom-du-témoin-1": "Marcelle",
                "Nom-du-témoin-1": "MOUROT",
                "Métier-du-témoin-1": "vendeuse",
                "Age-du-témoin-1": "",
                "Numéro-de-rue-de-résidence-du-témoin-1": "",
                "Type-de-rue-de-résidence-du-témoin-1": "",
                "Nom-de-rue-de-résidence-du-témoin-1": "",
                "Ville-de-résidence-du-témoin-1": "",
                "Département-de-résidence-du-témoin-1": "",
                "Prenom-de-l'adjoint-au-maire": "",
                "Nom-de-l'adjoint-au-maire": "",
                "Ville-du-mariage": ""
            }
        }

def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)
    
def split_examples(examples : dict, index : int):
    #return the example corresponding to index, and the others examples. Beware if index is the last example. use itertools slices.

    return examples[str(index)], {k: v for k, v in examples.items() if k != str(index)}

def get_example_prompt(examples, paragraph_index):
    #get the prompt
    prompt = ""
    for i, example in enumerate(examples):
        #print(examples[example]['text'][paragraph_index])
        prompt += "Réponds. Utilise exactement les mêmes labels, même si personne non mentionnée ou décédée.\n"
        prompt += f"Example {i+1}:\n"
        prompt += f"{examples[example]['text'][paragraph_index]}\n"
        prompt += f"Labels {i+1}:\n"
        prompt += f"{examples[example]['labels'][paragraph_index]}\n\n"

    return prompt

def make_prompt(example_prompt, paragraph, paragraph_index):
    #make the prompt
    prompt = example_prompt
    prompt += f"Question:\n {paragraph}\n"
    print(f"{paragraph}\nLabels:")
    #prompt += "template:\n"
    #prompt += f"{template[paragraph_index]}\n"
    prompt += ("Labels:\n")

    #print(prompt)
    return prompt

def get_answer(prompt):
    #get the answer
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt,},
    ]
    )
    answer = completion.choices[0].message['content']
    answer = answer.replace('\n', '').replace('.','')

    #remove quote around comma
    answer = answer.replace('\',', '",')
    answer = answer.replace(',\'', ',"')
    #remove quote around space
    answer = answer.replace(' \'', ' "')
    answer = answer.replace('\' ', '" ')
    #remove quote around colon
    answer = answer.replace('\':', '":')
    answer = answer.replace(':\'', ':"')
    #remove quote around {}
    answer = answer.replace('{\'', '{"')
    answer = answer.replace('\'}', '"}')

    #remove \n and -\n
    answer = answer.replace('-\n', '')
    answer = answer.replace('\\n', ' ')

    #replace Prenom-du-maire with Prenom-de-l'adjoint-au-maire
    answer = answer.replace('Prenom-du-maire', 'Prenom-de-l\'adjoint-au-maire')
    #replace Nom-du-maire with Nom-de-l'adjoint-au-maire
    answer = answer.replace('Nom-du-maire', 'Nom-de-l\'adjoint-au-maire')
    
    #remplacer les apostrophes par des guillemets
    answer = answer.replace("\\'", "\'")
    #print(answer)
    answer = answer[answer.index('{'):]
    print(f'answer : {answer}')
    answer = json.loads(answer)
    #print(answer)

    return answer

if __name__ == "__main__":
    examples = read_json("paragraphes_train.json")
    for i, _ in enumerate(examples):
        example, examples = split_examples(examples, i)
        distances = 0
        print('===================================================')
        print('Test: ', i)
        for j,paragraph_index in enumerate(example["text"]):
            print(paragraph_index)
            if paragraph_index == 'p4':
                continue

            example_prompt = get_example_prompt(examples, paragraph_index)
            prompt = make_prompt(example_prompt, example["text"][paragraph_index], paragraph_index)
            labels = get_answer(prompt)
            
            ref = example["labels"][paragraph_index]
            #replace all -\n by '' and \n by ' ' in the ref values
            for key in ref.keys():
                ref[key] = ref[key].replace('-\n', '').replace('\n', ' ')
            for key in ref.keys():
                if key not in labels.keys():
                    labels[key] = ''
                distance = Levenshtein.distance(labels[key], ref[key])
                if distance > 0:
                    print(key, distance, labels[key] if labels[key] != '' else 'VIDE', ref[key] if ref[key] != '' else 'VIDE')
                distances += distance
        print('============================ Distance :' , distances)


            # if Levenshtein.distance(answer, example["labels"][paragraph_index]) > 5:
            #     print("Example: ", i)
            #     print("Paragraph: ", j)
            #     print("Answer: ", answer)
            #     print("Label: ", example["labels"][paragraph_index])
            #     print("Distance: ", Levenshtein.distance(answer, example["labels"][paragraph_index]))
            #     print()


        







