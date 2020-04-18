from web_app.users.back_end.data_structure.Service import Service

def generateCandidates(input):
    candidates = list()
    for i in range(input["n_act"]):
        candidates.append([])
        for candidate in input[str(i)]:
            service = Service(**candidate)
            if candidate["matchingState"] == "precise":
                candidates[i].append(service)
            candidates[i].append(service)
    return candidates

#+----------------------------------------------------------------------------------------------+#


class Problem:

    # constructor

    def __init__(self , input):
        self.__actGraph = input["actGraph"]
        self.__candidates = generateCandidates(input)
        self.__constraints = input["constraints"]
        try :
            self.__weights = input["weights"]
        except :
            None


    # get attributs

    def getActGraph(self):
        return self.__actGraph

    def getCandidates(self):
        return self.__candidates

    def getWeights(self):
        try :
            return self.__weights
        except :
            return None

    def getConstraints(self):
        return self.__constraints