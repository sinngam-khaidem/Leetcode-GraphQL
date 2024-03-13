import requests
import json
import re
from bs4 import BeautifulSoup
import os
import pandas as pd
from utils import update_tracker, read_tracker, append_error
import os
from sql_compiler import get_output
from generate_ouptut_llm import generate_output

json_file_path = "coding-questions-sql-with-output.json"


def load_questions_from_json(json_file_path):
    try: 
        with open(json_file_path, 'r') as file:
            sql_question = json.load(file)
            return sql_question
            
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

def append_output(json_item, problem_num):
    try:
        problem_description = json_item["question"]
        input_testcases = json_item["testcases"]
        for tcase in input_testcases:
            tcase_input = json.loads(tcase["input"])
            print(json.dumps(tcase_input, indent=2))
            response = generate_output(problem_description=problem_description, input_testcase=tcase_input)
            print(json.dumps(response, indent=2))
            print(type(response["sql_solution"]))
            tcase_output = get_output(SQL_solution=response["sql_solution"], input_testcase=tcase_input)
            tcase["output"] = tcase_output
            tcase["input"] = tcase_input
            if "solutionCode" not in json_item.keys():
                json_item["solutionCode"] = {"SQL": response["sql_solution"]}
        append_to_json_file(json_item)
        #update_tracker("track.conf",problem_num)
            
    except Exception as e:
        print(f"Error: {e}")
        append_error("error.txt", problem_num, e)

    
if __name__== "__main__":
    sql_questions = load_questions_from_json(json_file_path="coding-questions-sql.json")
    #completed_upto = read_tracker("track.conf")
    # for i in range(completed_upto+1, len(sql_questions)):
    #     print(f"Appending output for testcases of problem at index {i}")
    #     append_output(sql_questions[i], i)
    append_output(sql_questions[2], 2)