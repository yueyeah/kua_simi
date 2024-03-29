from github import Github
from argparse import ArgumentParser
from datetime import datetime

from utils import json_helper

import json
import os
import logging


REPOS_INFO_PATH = "../repos_info/metadata/"
GITHUB_METADATA_JSON_PREFIX = "github_metadata___"

def get_repo_string_from_url(repo_url):
    repo_url_token_list = repo_url.split("/")
    repo_string = repo_url_token_list[-2] + '/' + repo_url_token_list[-1]
    return repo_string

def obtain_collected_metadata_filename(repo_string):
    repo_string_token_list = repo_string.split("/")
    metadata_filename = repo_string_token_list[0] + "___" + repo_string_token_list[1]
    return metadata_filename

# returns empty dict if file doesn't exist
# TODO: abstract this out into utilities
def read_from_json(repo_string): 
    filename_repo_suffix = obtain_collected_metadata_filename(repo_string)
    json_file_path = os.path.join(REPOS_INFO_PATH, f"{GITHUB_METADATA_JSON_PREFIX}{filename_repo_suffix}.json")
    repo_data_obj = {}
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            repo_data_obj = json.load(json_file)
    else:
        print(f"{json_file_path} doesn't exist.")
    return repo_data_obj

# TODO: abstract this out into utilities
def save_to_json(repo_string, data_obj): 
    filename_repo_suffix = obtain_collected_metadata_filename(repo_string)
    json_file_path = os.path.join(REPOS_INFO_PATH, f"{GITHUB_METADATA_JSON_PREFIX}{filename_repo_suffix}.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(data_obj, json_file, indent=4)
    logging.info(f"Processing completed! File hashes saved to {json_file_path}.")

def main():
    # starList = repo.get_stargazers_with_dates()
    # print("starList; ")
    # for starPage in starList:
    #     print(starPage)

    # forkList = repo.get_forks()
    # print("forkList: ")
    # for forkPage in forkList:
    #     print(forkPage)

    argparser = ArgumentParser(description="Pull GitHub metadata of a given repo")
    argparser.add_argument("repo_config_file", help="Config file containing list of target repo URLs")
    args = argparser.parse_args()
    g = Github()

    repo_list = json_helper.read_json(args.repo_config_file)
    print("Taking in list of target repos from config file ", args.repo_config_file)

    for target_repo_url in repo_list:
        # parse through target repo url and GET the repo object 
        print(f"Start pulling metadata for {target_repo_url}")
        target_repo_string = get_repo_string_from_url(target_repo_url)
        target_repo = g.get_repo(target_repo_string)

        # Collect metadata of the target repo at specified timestamp
        # then append it to the current json file for that target repo
        metadata_dict = read_from_json(target_repo_string)
        timestamp = int(datetime.now().timestamp() * 1000)
        metadata_at_timestamp_dict = {
            "forks_count": target_repo.forks_count,
            "stars_count": target_repo.stargazers_count
        }
        metadata_dict[timestamp] = metadata_at_timestamp_dict

        save_to_json(target_repo_string, metadata_dict)
        print(f"Finish pulling metadata for {target_repo_url}")

    
if __name__ == "__main__":
    main()