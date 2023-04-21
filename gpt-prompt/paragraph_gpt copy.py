import json
import openai
import Levenshtein
import itertools
openai.organization = "org-2wXrLf4fLEfdyawavmkAqi8z"
openai.api_key = "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"

template = {
            "p1" : {
                "Jour-mariage": "",
                "Mois-mariage": "",
                "Année-mariage": "",
                "Heure-mariage": "",
                "Minute-mariage": ""
            },
            "p2" : {
                "Prenom-mari": "",
                "Nom-mari": "",
                "Profession-mari": "",
                "ville-naissance-mari": "",
                "Departement-naissance-mari": "",
                "Pays-naissance-mari": "",
                "Jour-naissance-mari": "",
                "Mois-naissance-mari": "",
                "Année-naissance-mari": "",
                "Age-mari": "",
                "ville-residence-mari": "",
                "Departement-residence-mari": "",
                "Pays-residence-mari": "",
                "Numero-rue-residence-mari": "",
                "Type-rue-residence-mari": "",
                "Nom-rue-residence-mari": "",
                "Prenom-pere-mari": "",
                "Nom-pere-mari": "",
                "Profession-pere-mari": "",
                "ville-residence-pere-mari": "",
                "Departement-residence-pere-mari": "",
                "Numero-residence-pere-mari": "",
                "Type-rue-residence-pere-mari": "",
                "Nom-rue-residence-pere-mari": "",
                "Prenom-mere-mari": "",
                "Nom-mere-mari": "",
                "Profession-mere-mari": "",
                "ville-residence-mere-mari": "",
                "Departement-residence-mere-mari": "",
                "Pays-residence-mere-mari": "",
                "Numero-rue-residence-mere-mari": "",
                "Type-rue-residence-mere-mari": "",
                "Nom-rue-residence-mere-mari": "",
                "Prenom-ex-epouse": "",
                "Nom-ex-epouse": ""
                },
            "p3" : {
                "Prenom-mariee": "",
                "Nom-mariee": "",
                "Profession-mariee": "",
                "ville-naissance-mariee": "",
                "Departement-naissance-mariee": "",
                "Pays-naissance-mariee": "",
                "Jour-naissance-mariee": "",
                "Mois-naissance-mariee": "",
                "Année-naissance-mariee": "",
                "Age-mariee": "",
                "ville-residence-mariee": "",
                "Departement-residence-mariee": "",
                "Pays-residence-mariee": "",
                "Numero-rue-residence-mariee": "",
                "Type-rue-residence-mariee": "",
                "Nom-rue-residence-mariee": "",
                "Prenom-pere-mariee": "",
                "Nom-pere-mariee": "",
                "Profession-pere-mariee": "",
                "ville-residence-pere-mariee": "",
                "Departement-residence-pere-mariee": "",
                "Numero-residence-pere-mariee": "",
                "Type-rue-residence-pere-mariee": "",
                "Nom-rue-residence-pere-mariee": "",
                "Prenom-mere-mariee": "",
                "Nom-mere-mariee": "",
                "Profession-mere-mariee": "",
                "ville-residence-mere-mariee": "",
                "Departement-residence-mere-mariee": "",
                "Pays-residence-mere-mariee": "",
                "Numero-rue-residence-mere-mariee": "",
                "Type-rue-residence-mere-mariee": "",
                "Nom-rue-residence-mere-mariee": "",
                "Prenom-ex-epoux": "",
                "Nom-ex-epoux": ""
            },
            "p4" : {
            },
            "p5" : {
                "Prenom-temoin-0": "",
                "Nom-temoin-0": "",
                "Profession-temoin-0": "",
                "Age-temoin-0": "",
                "Numero-rue-residence-temoin-0": "",
                "Type-rue-residence-temoin-0": "",
                "Nom-rue-residence-temoin-0": "",
                "ville-residence-temoin-0": "",
                "Departement-residence-temoin-0": "",
                "Prenom-temoin-1": "Marcelle",
                "Nom-temoin-1": "MOUROT",
                "Profession-temoin-1": "vendeuse",
                "Age-temoin-1": "",
                "Numero-rue-residence-temoin-1": "",
                "Type-rue-residence-temoin-1": "",
                "Nom-rue-residence-temoin-1": "",
                "ville-residence-temoin-1": "",
                "Departement-residence-temoin-1": "",
                "Prenom-adjoint-maire": "",
                "Nom-adjoint-maire": "",
                "ville-mariage": ""
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
        prompt += "Répondre. Utilise exact même labels même si personne non mentionnée\n"
        prompt += f"Example {i+1}:\n"
        prompt += f"{examples[example]['text'][paragraph_index]}\n"
        prompt += f"Labels {i+1}:\n"
        prompt += f"{examples[example]['labels'][paragraph_index]}\n\n"

    return prompt

def make_prompt(example_prompt, paragraph, paragraph_index):
    #make the prompt
    prompt = example_prompt
    prompt += f"Question:\n {paragraph}\n"
    #print(f"{paragraph}\nLabels:")
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
    answer = answer.replace('-\\n', '')
    answer = answer.replace('\\n', ' ')
    #replace Prenom-du-maire with Prenom-adjoint-maire
    answer = answer.replace('Prenom-maire', 'Prenom-adjoint-maire')
    #replace Nom-du-maire with Nom-adjoint-maire
    answer = answer.replace('Nom-maire', 'Nom-adjoint-maire')
    #remplacer les apostrophes par des guillemets
    answer = answer.replace("\\'", "\'")
    #print(answer)
    answer = answer[answer.index('{'):]
    #print(f'answer : {answer}')
    answer = json.loads(answer)

    #print(answer)

    return answer

if __name__ == "__main__":
    examples = read_json("paragraphes_train copy.json")
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


        







