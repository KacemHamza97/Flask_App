import json
import os
from datetime import datetime
from flask import current_app

def add_file(file, user, type = "input"):
    try:
        file_to_save = json.load(file)
    except:
        file_to_save = json.loads(file)
    directory_name = str(user.id)
    pathd = os.path.join(current_app.root_path, "static/files/users_uploads")
    if directory_name not in os.listdir(pathd):
        os.makedirs(pathd + "/" + directory_name)
        os.makedirs(pathd + "/" + directory_name + "/" + "submits")
        os.makedirs(pathd + "/" + directory_name + "/" + "results")
    file_name = str(datetime.now()).replace('-', '_').replace(':', '_')[:19]
    if type == "input":
        filepath = os.path.join(current_app.root_path, f"static/files/users_uploads/{user.id}/submits/", file_name + ".json")
    elif type == "output":
        filepath = os.path.join(current_app.root_path, f"static/files/users_uploads/{user.id}/results/", file_name + ".json")
    with open(filepath, 'w') as f:
        json.dump(file_to_save, f,indent=4)


def input_data(solution_services):
    data = {"solutions":[]}
    for sol in solution_services:
        solution = {}
        for i in range(len(sol)):
            solution[f"{i}"] = sol[i].getId()
        data["solutions"].append(solution)
    return json.dumps(data)

# str(datetime.now()) : '2020-04-09 19:20:11.139622'
#file_name : year_month_day hour_min_seconde [:16]

