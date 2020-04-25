from random import sample
from numpy.random import choice
from web_app.users.back_end.data_structure.CompositionPlan import CompositionPlan
from web_app.users.back_end.data_structure.Solution import Solution
from web_app.users.back_end.operations.genetic import BSG
from web_app.users.back_end.operations.multi_objective_functions import functions
from web_app.users.back_end.operations.multi_update import nonDominatedSort, updateSolutions


# SQ : condition for scouts , MCN : number of iterations , SN : number of ressources , N : n of bees
def moabc_nsga2(problem, SQ, MCN, SN, N):
    # solutions  initializing
    solutionsList = list()
    fronts = list()

    for i in range(SN):
        cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())
        solutionsList.append(Solution(cp=cp, functions=functions(cp), probability=0, limit=0))

    # Algorithm
    for itera in range(MCN):

        # employed bees phase
        exploited = sample(solutionsList, N)  # selecting solutions for exploitation randomly
        U = list()
        U[:] = solutionsList
        for sol in exploited:
            cp1 = sol.cp
            cp2 = CompositionPlan(problem.getActGraph(), problem.getCandidates())  # randomly generated
            offsprings = BSG(cp1, cp2, problem.getCandidates())  # BSG
            # Adding offsprings
            U += [Solution(cp=cp, functions=functions(cp), limit=0) for cp in offsprings]
        # end of employed bees phase

        fronts = nonDominatedSort(U)
        solutionsList = updateSolutions(solutionsList, fronts, method="crowdingSort")

        # onlooker bees phase
        U = list()
        U[:] = solutionsList
        pf = fronts[0]
        if len(pf) < 2:
            pf += fronts[1]
        for itera in range(N):
            # cp 1 randomly chosen from pf
            cp1 = choice(pf).cp
            # cp 2 randomly chosen from pf
            while 1:
                cp2 = choice(pf).cp
                if cp2 != cp1:
                    break
                offsprings = BSG(cp1, cp2, problem.getCandidates())  # BSG
                # Adding offsprings
                U += [Solution(cp=cp, functions=functions(cp), limit=0) for cp in offsprings]

        # end of onlooker bees phase

        fronts = nonDominatedSort(U)
        solutionsList = updateSolutions(solutionsList, fronts, "crowdingSort")

        # scout bees phase
        update = 0
        U = list()
        U[:] = solutionsList
        for sol in exploited:
            if sol.limit >= SQ and sol not in fronts[0]:
                sol.limit = 0
                cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())  # randomly generated cp
                U.append(Solution(cp=cp, functions=functions(cp), limit=0))
                update = 1
        # end of scout bees phase
        if update:
            fronts = nonDominatedSort(U)
            solutionsList = updateSolutions(solutionsList, fronts, "crowdingSort")

    # end of algorithm
    return fronts[0]
