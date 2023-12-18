import json

with open('text.txt', 'r', encoding='utf-8') as file:
    dane_json = json.load(file)

print(dane_json)