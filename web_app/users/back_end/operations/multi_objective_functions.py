
from numpy import array

#+----------------------------------------------------------------------------------------------+#

def functions(cp) :   # Objective functions
    f1 = - cp.cpQos()["responseTime"]
    f2 = - cp.cpQos()["price"]
    f3 = cp.cpQos()["reliability"]
    return array([f1,f2,f3])

#+----------------------------------------------------------------------------------------------+#


def dominates(sol1 , sol2) : # verify if sol1 dominates sol2
    F = functions(sol1.cp)
    G = functions(sol2.cp)
    # Domination condition F not worse than G in all functions and better at least once 
    if (F >= G).all() and (F > G).any() : 
        return True


    