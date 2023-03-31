""" Some useful functions """
import numpy as np
def deltaPhi(p1, p2):
    res = p1 -p2
    while res > np.pi:
        res -= 2*np.pi
    while res < -np.pi:
        res += 2*np.pi
    return res