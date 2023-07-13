import pandas as pd
import json

def json_to_csv(file_to_open, csv_file):
    #the JSON has the following structure:
    #{
    # "archivename1" :
    #  {
    #  "key1" : "value1",
    # "key2" : "value2",
    # "key3" : "value3",
    # "key4" : "value4",
    # ....}
    # "archivename2" :
    #  {
    #  "key1" : "value1",
    # "key2" : "value2",
    # "key3" : "value3",
    # "key4" : "value4",
    # ....}
    #...}
    # We want to create a csv file with the following structure:
    # archivename1, key1, key2, key3, key4, ...
    # archivename2, key1, key2, key3, key4, ...
    # ...

    print('Converting JSON to CSV...')
    print('Opening JSON file: ' + file_to_open)
    with open(file_to_open) as f:
        data = json.load(f)

    #test the json structure, else exit
    if not isinstance(data, dict):
        print('JSON file is not a dictionary')
        exit()
    if not all(isinstance(value, dict) for value in data.values()):
        print('JSON file values are not dictionaries')
        exit()

    print('JSON loaded successfully')
    df = pd.DataFrame.from_dict(data, orient='index')
    print(f'Converting to CSV : {df.shape[1]} features, from {df.shape[0]} mariage acts')
    print('Saving CSV file: ' + csv_file)
    df.to_csv(csv_file, index=True, header=True)
    print('Done !')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert JSON to CSV')
    parser.add_argument('file_to_open', help='JSON file to open')
    parser.add_argument('csv_file', help='CSV file to create')
    args = parser.parse_args()
    json_to_csv(args.file_to_open, args.csv_file)




