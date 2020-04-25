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

    # +----------------------------------------------------------------------------------------------+#
    # problem init
    p = Problem(user_input)
    # +----------------------------------------------------------------------------------------------+#
    # import parameters

    n_act = user_input["n_act"]
    n_candidates = 0
    for act in range(n_act):
        n_candidates += len(user_input[str(act)]) // n_act

    if data["MCN"] == "":
        with open("model.pkl", 'rb') as file:
            model_mcn = load(file)
        # preparing prediction
        Xnew = array([n_act, n_candidates]).reshape(-1, 2)
        # predict mcn
        mcn = model_mcn.predict(Xnew)
    else:
        mcn = int(data["MCN"])

    if data["SN"] == "":
        # sn
        if user_input["n_act"] < 10:
            sn = 20
        elif user_input["n_act"] < 20:
            sn = 30
        elif user_input["n_act"] < 30:
            sn = 40
        else:
            sn = 50
    else:
        sn = int(data["SN"])
    # sq
    if data["SQ"] == "":
        sq = mcn // 10 if mcn < 1000 else 100
    else:
        sq = int(data["SQ"])
    # executing algorithm
    if session["algorithm"] == "Single-objective":
        # cp
        cp = float(data["CP"])
        # scp
        scp = float(data["SCP"])
        solutions = abc_genetic(problem=p, SN=sn, SQ=sq, MCN=mcn, SCP=scp, N=20, CP=cp)

    elif session["algorithm"] == "Multi-objective":
        solutions = moabc_nsga2(problem=p, SN=sn, SQ=sq, MCN=mcn, N=10)

    # verifying constraints
    final_solutions = []
    for sol in solutions:
        if sol.cp.verifyConstraints(p.getConstraints()):
            final_solutions.append(sol.cp)

    if session["algorithm"] == "single" and len(final_solutions) > 5:
        final_solutions = final_solutions[:5]

    solution_services = []
    for sol in final_solutions:
        services = []
        for act in range(n_act):
            services.append(sol.getService(act))
        solution_services.append(services) #list of cp , each cp is [service1,...service n] and the index                              # represents n_act
    return solution_services, [sol.cpQos() for sol in final_solutions]
