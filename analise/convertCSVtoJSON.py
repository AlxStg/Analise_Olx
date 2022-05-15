import csv
import json

csvFilePath = 'veiculos.csv'
jsonFilePath = 'veiculos.json'

dados = []

# Abre e lê o arquivo csv
with open(csvFilePath, 'r') as csvFile:
    csvReader = csv.DictReader(csvFile)
    print(csvReader)
    for rows in csvReader:
        dados.append(rows)
    print('CONVERSÃO BEM SUCEDIDA!')
# Cria o arquivo json
with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(dados, indent=4))