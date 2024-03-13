import json

try:
    with open("coding-questions-sql.json", "r") as file:
        questions = json.load(file)
        questions = questions[:6]

    print(type(questions[0]["testcases"][0]["input"]))
    my_dict = json.loads(questions[0]["testcases"][0]["input"])
    print(type(my_dict))
    print(my_dict["headers"])
    # for item in questions:
    #     print(item["testcases"]["input"])

except Exception as e:
    print("Error:", e)