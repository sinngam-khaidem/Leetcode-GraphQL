import requests
import json
import re
from bs4 import BeautifulSoup
import os
import pandas as pd
from utils import update_tracker, read_tracker, append_error
import os

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
json_file_path = "coding-questions-sql.json"


def load_questions_from_json(json_file_path):
    try: 
        with open(json_file_path, 'r') as file:
            sql_question = json.load(file)
            sql_question_list = sql_question["data"]["problemsetQuestionList"]["questions"]
            return sql_question_list
            
    except Exception as e:
        print(f"Error: {e}")



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

def create_test_cases(q_data):
    testcases = []
    # html_snippet = q_data["content"].replace("\n", "").replace("\t", "")
    exampleTestcaseList = q_data["exampleTestcaseList"]
    # soup = BeautifulSoup(html_snippet, 'html.parser')
    # results = []
    # pre_tags = soup.find_all('pre')
    # for pre_tag in pre_tags:
    #     output = []
    #     if "<strong>Explanation:</strong>" in str(pre_tag):
    #         output = re.findall(r'<strong>Output:</strong>(.*?)<strong>Explanation:</strong>', str(pre_tag), re.DOTALL)
    #     elif "<strong>Explanation: </strong>" in str(pre_tag): 
    #         output = re.findall(r'<strong>Output:</strong>(.*?)<strong>Explanation: </strong>', str(pre_tag), re.DOTALL)
    #     elif "<strong> Explanation: </strong>" in str(pre_tag):
    #         output = re.findall(r'<strong>Output:</strong>(.*?)<strong> Explanation: </strong>', str(pre_tag), re.DOTALL)
    #     else:
    #         output = re.findall(r'<strong>Output:</strong>(.*?)</pre>', str(pre_tag), re.DOTALL)
    #     if len(output) > 0 :
    #         results.append(output[0])

    # results = [result.strip() for result in results]

    for i in range(len(exampleTestcaseList)):
        testcases.append({
            "input": exampleTestcaseList[i],
        })
    return testcases

        
def create_cq_json(q_data:str, problem_num:int):
    try: 
        if q_data["content"] != None:
            result = {
                'title': q_data["title"],
                'titleSlug': q_data["titleSlug"],
                'questionFrontendId': q_data["frontendQuestionId"],
                'question': q_data["content"],
                'difficulty': q_data["difficulty"],
                'testcases': create_test_cases(q_data),
                'tags': [item["slug"] for item in q_data["topicTags"]],
            }
            print(result)
            append_to_json_file(result)
            update_tracker("track.conf", problem_num)
    except Exception as e:
        print(f"Error: {e}")
        append_error("error.txt", q_data["frontendQuestionId"])
    
    
if __name__== "__main__":
    # print(json.dumps(create_cq_json(titleSlug="combine-two-tables")))
    sql_question_list = load_questions_from_json("sql-question-list.json")
    completed_upto = read_tracker("track.conf")
    for i in range(completed_upto+1, len(sql_question_list)):
        create_cq_json(sql_question_list[i], i)