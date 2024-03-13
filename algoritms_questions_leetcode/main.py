import requests
import json
import re
from bs4 import BeautifulSoup
import os
import pandas as pd
from utils import update_tracker, read_tracker, append_error

# Leetcode's graphql api endpoint
BASE_URL = "https://leetcode.com/graphql"

endpoint_url = "https://leetcode.com/api/problems/{endpoint}/"

 # endpoints = [
        #     "algorithms",
        #     "database",
        #     "shell",
        #     "concurrency",
        #     "javascript",
        # ]
endpoints = ["all"]  # returns all questions
# Path of the output json file
json_file_path = "coding-questions-most-accepted.json"

def load_questions_from_csv(csv_file_path):
    dataframe = pd.read_csv(csv_file_path)
    result = list(dataframe["Url"].values)
    all_title_slugs = []
    for item in result:
        titleSlug = item.split('/')[-1]
        all_title_slugs.append(titleSlug)
    return all_title_slugs


def append_to_json_file(new_items,file_path = json_file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []
        
        existing_data.append(new_items)
        with open(file_path, 'w') as file:
            json.dump(existing_data, file)
        print("JSON items appended successfully")
    except Exception as e:
        print(f"Error: {e}")

# Function used for extracting and formulating test cases from the question body HTML
def create_test_cases(q_data):
    testcases = []
    html_snippet = q_data["data"]["question"]["content"].replace("\n", "").replace("\t", "")
    exampleTestcaseList = q_data["data"]["question"]["exampleTestcaseList"]
    soup = BeautifulSoup(html_snippet, 'html.parser')
    results = []
    pre_tags = soup.find_all('pre')
    for pre_tag in pre_tags:
        output = []
        if "<strong>Explanation:</strong>" in str(pre_tag):
            output = re.findall(r'<strong>Output:</strong>(.*?)<strong>Explanation:</strong>', str(pre_tag), re.DOTALL)
        elif "<strong>Explanation: </strong>" in str(pre_tag): 
            output = re.findall(r'<strong>Output:</strong>(.*?)<strong>Explanation: </strong>', str(pre_tag), re.DOTALL)
        elif "<strong> Explanation: </strong>" in str(pre_tag):
            output = re.findall(r'<strong>Output:</strong>(.*?)<strong> Explanation: </strong>', str(pre_tag), re.DOTALL)
        else:
            output = re.findall(r'<strong>Output:</strong>(.*?)</pre>', str(pre_tag), re.DOTALL)
        if len(output) > 0 :
            results.append(output[0])
        else:
            results.append("-")

    results = [result.strip() for result in results]

    for i in range(len(exampleTestcaseList)):
        testcases.append({
            "input": exampleTestcaseList[i],
            "output": results[i]
        })
    return testcases

# Function used for extracting question informations from the Leetcode GraphQL, and write it down to a json file.         
def create_cq_json(titleSlug:str, problem_num:int):
    print(f"Appending problem at index {problem_num}:")
    # This the query used to extract necessary informations about the question
    data = {
        "query": """query questionHints($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                title
                titleSlug
                questionFrontendId
                difficulty
                content
                exampleTestcaseList
                hints
                topicTags {
                    name
                    id
                    slug
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }

                isPaidOnly
            }
        }
        """,
        "variables": {"titleSlug": titleSlug},
        }
    
    req = requests.post(BASE_URL, json=data)
    q_data = req.json()
    try: 
        # Extract the necessary informations about the question
        result = {
            'title': q_data["data"]["question"]["title"],
            'titleSlug': q_data["data"]["question"]["titleSlug"],
            'questionFrontendId': q_data["data"]["question"]["questionFrontendId"],
            'question': q_data["data"]["question"]["content"],
            'difficulty': q_data["data"]["question"]["difficulty"],
            # The test cases itself was not the graphql api result, so I am extracting and formulating test cases from the question body html
            'testcases': create_test_cases(q_data),
            'tags': [item["slug"] for item in q_data["data"]["question"]["topicTags"]],
        }
        print(result)
        append_to_json_file(result)
        # Update the track.conf file
        update_tracker("track.conf", problem_num)
    except Exception as e:
        print(f"Error: {e}")
        append_error("error.txt", problem_num)

    
if __name__== "__main__":
    # Get a list of title slugs from the CSV file.
    all_title_slugs = load_questions_from_csv("most-acceptance.csv")
    # I am iterating through the list of title slugs and the index of the most recently used titleSlug is written down in track.conf
    # Here, I am reading the index from track.conf
    completed_upto = read_tracker("track.conf")
    # Iterating through the list of titleSlugs, extract all  the necessary informations from the leetcode graphql api, and write it down to a json file.
    for i in range(completed_upto+1, len(all_title_slugs)):
        create_cq_json(all_title_slugs[i], i)

