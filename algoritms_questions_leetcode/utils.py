def update_tracker(file_name, problem_num):
    with open(file_name, "w") as f:
        f.write(str(problem_num))

def read_tracker(file_name):
    with open(file_name, "r") as f:
        return int(f.readline())

def append_error(file_name, problem_num, e:Exception):
    with open(file_name, "a") as f:
        f.write("\n" + str(problem_num) +" : " + str(e))