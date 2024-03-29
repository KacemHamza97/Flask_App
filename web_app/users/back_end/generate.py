import json
import os
from pickle import load

from flask import current_app, session
from flask_login import current_user
from numpy import array

# +----------------------------------------------------------------------------------------------+#
from web_app.users.back_end.algorithms.abc_genetic import abc_genetic
from web_app.users.back_end.algorithms.moabc_nsga2 import moabc_nsga2
from web_app.users.back_end.data_structure.Problem import Problem


def generate_solution():
    # JSON FILE INPUT
    pathad = "C:/Users/mizou/OneDrive/Bureau/Flask-App/web_app/static/files/admin_settings/parameters.json"
    with open(pathad) as json_file:
        data = json.load(json_file)

    if current_user.is_authenticated:
        pathd = os.path.join(current_app.root_path, f"static/files/users_uploads/{current_user.id}/submits")
        file_name = os.listdir(pathd)[-1]
        with open(pathd + "/" + file_name) as file:
            user_input = json.load(file)
    else:
        pathd = os.path.join(current_app.root_path, f"static/files/users_uploads/None/submits")
        file_name = os.listdir(pathd)[-1]
        with open(pathd + "/" + file_name) as file:
            user_input = json.load(file)

    n_act =len(user_input["activities"])
    # +----------------------------------------------------------------------------------------------+#
    # problem init
    p = Problem(user_input)
    # +----------------------------------------------------------------------------------------------+#
    # import parameters

    mcn = int(data["MCN"])
    sn = int(data["SN"])
    sq = int(data["SQ"])
    n = int(data["N"])
    # executing algorithm
    if session["algorithm"] == "Single-objective":
        # cp
        cp = float(data["CP"])
        # scp
        scp = float(data["SCP"])
        solutions = [abc_genetic(problem=p, SN=sn, SQ=sq, MCN=mcn, SCP=scp, N=n, CP=cp)]

    elif session["algorithm"] == "Multi-objective":
        solutions = moabc_nsga2(problem=p, SN=sn, SQ=sq, MCN=mcn, N=n)

    solution_services = []
    for sol in solutions:
        services = []
        for act in range(n_act):
            services.append(sol.cp.getService(act))
        solution_services.append(services)  # list of cp , each cp is [service1,...service n] and the index                              # represents n_act
    return solution_services, [sol.cp.cpQos() for sol in solutions], user_input["activities"]
