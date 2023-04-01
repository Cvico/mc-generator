""" Some useful functions """
import numpy as np
import ROOT as r

def deltaPhi(p1, p2):
    res = p1 -p2
    while res > np.pi:
        res -= 2*np.pi
    while res < -np.pi:
        res += 2*np.pi
    return res

def get_files(opts):
    file_ = opts.mcaFile
    f = open(file_, "r")
    
    files = {}
    for line in f.readlines():
        if line[0] == "#" or line[0] == "": continue
        
        fields = line.replace(" ", "").replace("\n", "").split(";")
        filename, norm = fields[0].split(":")
        
        files[filename] = {"file" : filename, "norm" : norm, "useForRatio" : False}
        others = fields[1].split(",")
        for other in others:
            if "color" in other: files[filename]["color"] = eval("r."+other.split("=")[-1]) 
            if "useForRatio" in other: files[filename]["useForRatio"] = True
            if "legend_name" in other: files[filename]["legend"] = other.split("=")[1:]
    return files            
        