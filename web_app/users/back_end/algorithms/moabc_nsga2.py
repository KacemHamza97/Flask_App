from random import uniform, sample
from web_app.users.back_end.data_structure.CompositionPlan import CompositionPlan
from web_app.users.back_end.data_structure.Solution import Solution
from web_app.users.back_end.operations.genetic import BSG
from web_app.users.back_end.operations.multi_objective_functions import functions
from web_app.users.back_end.operations.multi_update import nonDominatedSort, updateSolutions

# SQ : condition for scouts , MCN : number of iterations , SN : number of ressources , N : n of bees
def moabc_nsga2(problem, SQ, MCN, SN, N):
    # solutions  initializing
    solutionsList = list()

    for i in range(SN):
        while 1:
            cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())
            if cp.verifyConstraints(problem.getConstraints()):
                solutionsList.append(Solution(cp=cp, fitness=0, functions=functions(cp), probability=0, limit=0))
                break

    # Algorithm
    for itera in range(MCN):
        # employed bees phase
        exploited = sample(solutionsList, N)  # selecting solutions for exploitation randomly
        U = list()
        U[:] = solutionsList
        for sol in exploited:
            cp1 = sol.cp
            cp2 = CompositionPlan(problem.getActGraph(), problem.getCandidates())  # randomly generated cp
            offsprings = BSG(cp1, cp2, problem.getConstraints(), problem.getCandidates())  # BSG
            # Adding offsprings
            U += [Solution(cp=cp, fitness=0, functions=functions(cp), probability=0, limit=0) for cp in offsprings]
        # end of employed bees phase

        fronts = nonDominatedSort(U)
        solutionsList = updateSolutions(solutionsList, fronts, method="crowdingSort")

        # Probability update
        s = sum([sol.fitness for sol in solutionsList])
        for sol in solutionsList:
            sol.probability = sol.fitness / s

        # onlooker bees phase
        probabilityList = [sol.probability for sol in solutionsList]
        a = min(probabilityList)
        b = max(probabilityList)
        U = list()
        U[:] = solutionsList
        for sol in solutionsList:
            if sol.probability > uniform(a, b):
                cp1 = sol.cp
                cp2 = CompositionPlan(problem.getActGraph(), problem.getCandidates())  # randomly generated cp
                offsprings = BSG(cp1, cp2, problem.getConstraints(), problem.getCandidates())  # BSG
                # Adding offsprings
                U += [Solution(cp=cp, fitness=0, functions=functions(cp), probability=0, limit=0) for cp in offsprings]

        # end of onlooker bees phase

        fronts = nonDominatedSort(U)
        solutionsList = updateSolutions(solutionsList, fronts, "crowdingSort")

        # scout bees phase
        update = 0
        U = list()
        U[:] = solutionsList
        for sol in solutionsList:
            if sol.limit >= SQ:
                sol.limit = 0
                while 1:
                    cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())  # randomly generated cp
                    if cp.verifyConstraints(problem.getConstraints()):
                        U.append(Solution(cp=cp, fitness=0, functions=functions(cp), probability=0, limit=0))
                        break
                update = 1
        # end of scout bees phase
        if update:
            fronts = nonDominatedSort(U)
            solutionsList = updateSolutions(solutionsList, fronts, "crowdingSort")

    # end of algorithm
    return fronts[0]
