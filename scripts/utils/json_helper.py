import json
import os
import logging

# Returns None if filename doesn't exist (silent fail)
def read_json(json_file_path): 
    repo_data_obj = None
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            repo_data_obj = json.load(json_file)
    logging.info(f"read_json() completed! Data read from {json_file_path}.")
    return repo_data_obj

def save_json(json_file_path, data_obj):
    with open(json_file_path, 'w') as json_file:
        json.dump(data_obj, json_file, indent=4)
    logging.info(f"save_json() completed! {data_obj} saved to {json_file_path}.")