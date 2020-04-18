from math import inf
from random import sample, uniform
from web_app.users.back_end.data_structure.CompositionPlan import CompositionPlan
from web_app.users.back_end.data_structure.Solution import Solution
from web_app.users.back_end.operations.genetic import crossover, mutate
from web_app.users.back_end.operations.multi_update import remove_redundant
from web_app.users.back_end.operations.single_objective_function import fit
from web_app.users.back_end.operations.single_update import updateMinMax, updateBest


# SN : n of ressources , SQ : condition for scouts , MCN : number of iterations
# N : n of bees , CP : crossover probability
def abc_genetic(problem, SN, SQ, MCN, SCP, N, CP):
    # solutions initializing
    solutionsList = list()
    best_solutions = []

    minQos = {'responseTime': inf, 'price': inf, 'availability': inf, 'reliability': inf}
    maxQos = {'responseTime': 0, 'price': 0, 'availability': 0, 'reliability': 0}

    for i in range(SN):
        cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())
        solutionsList.append(Solution(cp=cp, fitness=0, probability=0, limit=0))

    # minQos maxQos and fitness initializing
    updateMinMax(solutionsList, minQos, maxQos, problem.getWeights())

    # initializing best_solution
    best_solution = max(solutionsList, key=lambda sol: sol.fitness)

    # +----------------------------------------------------------------------------------------------+#

    # Algorithm
    for itera in range(MCN):
        # employed bees phase
        exploited = sample(solutionsList, N)  # Generating positions list for exploitation
        for sol in exploited:
            random = CompositionPlan(problem.getActGraph(), problem.getCandidates())  # randomly generated cp
            offspring = crossover(sol.cp, random, CP)  # Crossover operation
            new_fitness = fit(offspring, minQos, maxQos, problem.getWeights())
            # checking if offspring fitness is better than parent fitness
            if new_fitness > sol.fitness:
                sol.cp = offspring
                sol.fitness = new_fitness
                sol.probability = 0
                sol.limit = 0
            else:
                sol.limit += 1
        # end of employed bees phase

        updateBest(solutionsList, best_solution)

        # Probability update
        s = sum([sol.fitness for sol in solutionsList])
        for sol in exploited:
            sol.probability = sol.fitness / s

        # onlooker bees phase
        probabilityList = [sol.probability for sol in solutionsList]
        a = min(probabilityList)
        b = max(probabilityList)
        for sol in exploited:
            if sol.probability >= uniform(a, b):
                offspring = crossover(sol.cp, best_solution.cp, CP)  # Crossover operation
                new_fitness = fit(offspring, minQos, maxQos, problem.getWeights())
                # checking if offspring fitness is better than parent fitness
                if new_fitness > sol.fitness:
                    sol.cp = offspring
                    sol.fitness = new_fitness
                    sol.probability = 0
                    sol.limit = 0
                    updateBest(solutionsList, best_solution, sol)
                else:
                    sol.limit += 1
        # end of onlooker bees phase

        # scout bees phase
        update = 0
        for sol in exploited:
            if sol.limit >= SQ:  # verifying scouts condition
                if itera >= SCP*MCN:  # change of scouts behaviour condition to mutating
                    # choose randomly a service to mutate
                    service = sol.cp.randomService()
                    neighborsList = problem.getCandidates()[service.getActivity()]
                    neighbor = service.getNeighbor(neighborsList)
                    # mutation operation
                    new = mutate(sol.cp, neighbor)
                    sol.cp = new
                    sol.fitness = fit(new, minQos, maxQos, problem.getWeights())
                    sol.probability = 0
                    sol.limit = 0

                else:  # searching for new ressources to exploit
                    random = CompositionPlan(problem.getActGraph(), problem.getCandidates())
                    if random.verifyConstraints(problem.getConstraints()):
                        sol.cp = random
                        sol.fitness = fit(sol.cp, minQos, maxQos, problem.getWeights())
                        sol.probability = 0
                        sol.limit = 0
                update = 1

        # end of scout bees phase
        if update:
            updateBest(solutionsList, best_solution)

        updateMinMax(solutionsList, minQos, maxQos, problem.getWeights(), best_solution)
        best_solutions.append(best_solution)

    # end of algorithm
    return sorted(remove_redundant(best_solutions), key=lambda sol: sol.fitness, reverse=True)
