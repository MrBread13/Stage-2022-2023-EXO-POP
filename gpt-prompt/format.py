import json
#donnees-test is a json without indent. Open it then resave it with proper indentation
with open('donnees-test.json', 'r+') as file:
    data = file.read()
    data = json.loads(data)
    file.seek(0)
    json.dump(data, file, indent=4)