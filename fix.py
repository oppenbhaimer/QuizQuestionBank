import os, sys
import json
from json_repair import repair_json

# Define the raw and text directories
clean_dir = 'clean'
fixed_dir = 'fixed'

for root, dirs, files in os.walk(clean_dir):

    fixed_root = root.replace(clean_dir, fixed_dir)
    if not os.path.exists(fixed_root):
        os.makedirs(fixed_root)
    # Iterate through all PDF files in the current directory
    for file in files:
        if file.endswith('.json'):
            src_file = os.path.join(root, file)
            tgt_file = os.path.join(fixed_root, file)
            if os.path.exists(tgt_file):
                continue

            lines = open(src_file, 'r', encoding='utf-8').readlines()
            try:
                good_json = repair_json(''.join(lines), return_objects=True)
                json.dump(good_json, open(tgt_file, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
            except Exception:
                print(src_file)


