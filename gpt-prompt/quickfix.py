from fix_labels import sanitize_labels
import json


labels_history = {}
with open('donnees-test-labels-gpt35-paragraph-16k.json', 'r') as f:
    labels_history = json.load(f)

for name in labels_history.keys():
    labels = labels_history[name]
    labels = sanitize_labels(labels)
    #print(labels)
    #print('labels : ', labels['Jour-mariage'])

    labels_history[name] = labels
# store labels_history in json file
with open('donnees-test-labels-gpt35-paragraph-16k.json', 'w') as outfile:
    json.dump(labels_history, outfile, indent=4)