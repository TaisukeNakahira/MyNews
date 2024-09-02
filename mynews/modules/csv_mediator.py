import csv

def write(file_path, texts):
    with open(file_path, 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(texts)