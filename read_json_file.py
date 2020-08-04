import json

with open('grammars.json', 'rb') as data_file:
    json_data = data_file.read().decode('utf8')
    json_load = json.loads(json_data)

    print(json_load)