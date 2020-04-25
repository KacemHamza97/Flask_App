
from numpy import amin , amax , array

#+----------------------------------------------------------------------------------------------+#
# transform Solutions list into numpy matrix
from web_app.users.back_end.operations.multi_objective_functions import dominates


def transform(U) :
    return array([x.functions for x in U])

#+----------------------------------------------------------------------------------------------+#


# return max_pf - min_pf euclidean distance
def normalize(pf) :
    return array(amax(pf , axis = 0) - amin(pf , axis = 0))

#+----------------------------------------------------------------------------------------------+#


def remove_redundant(solutionsList):
    L = []
    for sol1 in solutionsList:
        for sol2 in solutionsList:
            if sol1 != sol2 and sol1.cp == sol2.cp:
                L.append(sol2)
    return [sol1 for sol1 in solutionsList if sol1 not in L]

#+----------------------------------------------------------------------------------------------+#

def nonDominatedSort(solutionsList) :
        solutionsList = remove_redundant(solutionsList)
        fronts = [[]]   
        SList = {}    
        NList = {} 
        for sol1 in solutionsList :
            Sp = list()   # list of solutions dominated by sol1
            Np = 0        # number of solutions which dominate sol1
            for sol2 in solutionsList :
                if dominates(sol1 , sol2) : 
                    Sp.append(sol2)
                elif dominates(sol2 , sol1) : 
                    Np += 1
            if Np == 0 :  
                fronts[0].append(sol1)   # pareto front
            SList[sol1] = Sp 
            NList[sol1] = Np

        i = 0  # front number 
        # updating fronts
        while len(fronts[i]) != 0 :
            f = []
            for sol1 in fronts[i] : 
                for sol2 in SList[sol1] :
                    NList[sol2] -= 1      # exclude ith front
                    if NList[sol2] == 0 : # sol2 no longer dominated
                        f.append(sol2)    # added to the next front
            i += 1
            fronts.append(f)

        return fronts


#+----------------------------------------------------------------------------------------------+#


def crowdingSort(front) :
    if len(front) > 2 :
        scoresList = list()
        for sol1 in front :
            score = list() # score of sol1
            for d in range(3) :
                high = []    # solutions with higher value in dimension d
                low =  []    # solutions with lower value in dimension  d
                for sol2 in front :
                    if sol2.functions[d] < sol1.functions[d]  :  # lower value found
                        low.append(sol2.functions[d])
                    if sol2.functions[d] > sol1.functions[d] :   # heigher value found
                        high.append(sol2.functions[d])
                if len(high) == 0 :  # no heigher value found
                    next_high = sol1.functions[d]
                    high.append(next_high)
                else :
                    next_high = min(high)  # smallest heigher value
                if len(low) == 0 :   # no lower value found
                    next_low = sol1.functions[d]
                    low.append(next_low)
                else :
                    next_low = max(low)    # biggest lower value
                
                # Making sure max_d != min_d
                max_d = max(high)
                min_d = min(low)
                if max_d == min_d : 
                    max_d = 1
                    min_d = 0

                score.append((next_high-next_low)/( max_d - min_d)) # normalized score
            scoresList.append(sum(score))

        # returning front sorted by DESC order based on crowdingScores
        return [x[1] for x in sorted(zip(scoresList , front) , key = lambda x:x[0] , reverse = True)]
    
    else :
        return front



#+----------------------------------------------------------------------------------------------+#


def normalized_Euclidean_Distance(a , b , norm) :
    # verifying that norm != 0
    for i in range(len(norm)) :
        if norm[i] == 0 :
            norm[i] = 1
    try : # a , b are numpy array type
        return ( ((a - b) / norm ) ** 2).sum(axis = 0) ** 0.5
    except :
        try : # a , b are Solution type
            return ( ((a.functions - b.functions) / norm) ** 2).sum(axis = 0) ** 0.5
        except : # a is Solution type and b is numpy array
            return ( ((a.functions - b) / norm) ** 2).sum(axis = 0) ** 0.5



#+----------------------------------------------------------------------------------------------+#

def updateSolutions(solutionsList , fronts , method , **kwargs) :
    i = 0   # front number
    S = []  # new solutionsList
    N = len(solutionsList)

    while i < len(fronts) and len(fronts[i]) <= N - len(S) : 
        # add fronts to S until space left is lower than front size
        S += fronts[i]
        i += 1

    if i < len(fronts) : 
        # selecting solutions from front based on method
        if method == "crowdingSort" :
            selection = crowdingSort(fronts[i])[0:N - len(S)]
            S += selection

    for sol in S :
        if sol in solutionsList :
            sol.limit += 1

        
    return S