import os
import json

fixed_dir = 'fixed'

questions = []

no_q = 0
no_a = 0

for root, dirs, files in os.walk(fixed_dir):
    for file in files:
        if file.endswith('.json'):
            json_file = os.path.join(root, file)
            file_qs = json.load(open(json_file, 'r', encoding='utf-8'))
            questions += file_qs

            for qa in file_qs:
                if 'Q' not in qa or qa['Q'] == "":
                    no_q += 1
                if 'A' not in qa or qa['A'] == "":
                    no_a += 1

print(f"Got {len(questions)} questions, {no_q} of which don't have a question and {no_a} of which don't have an answer")
json.dump(questions, open('final.json', 'w'), indent=4, ensure_ascii=False)
