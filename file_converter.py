import csv
import json

def get_file_format(file):
    if file.endswith('.csv'):
        csv_to_jsonl(file, "output.jsonl")
    elif file.endswith('.json'):
        json_to_jsonl(file, file.replace('.json', "file_convertered/output.jsonl"))
    else:
        return "Invalid file format"

def csv_to_jsonl(csv_file, jsonl_file):
    with open(csv_file, 'r') as csvfile, open(jsonl_file, 'w') as jsonlfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            json.dump(row, jsonlfile)
            jsonlfile.write('\n')

def json_to_jsonl(json_file, jsonl_file):
    with open(json_file, 'r') as jsonfile, open(jsonl_file, 'w') as jsonlfile:
        data = json.load(jsonfile)
        for item in data:
            json.dump(item, jsonlfile)
            jsonlfile.write('\n')

# Example usage
# get_file_format('input.csv')
