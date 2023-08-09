import os
import numpy as np
import copy

import re 
import yaml
import json
import math
import time 
from yaml.loader import SafeLoader


def surrogate(db, state):
    register = os.path.join(db, "register.yaml")
    states = []
    with open(register, "r") as stream:
        try:
            states = yaml.load(stream, Loader=SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

    # First lets check if list of state parameters is appropriate
    temp = copy.copy(state)
    temp["hash"] = "null_hash"
    if temp.keys() != states[0].keys():
        print("Set of keys isnt appropriate")
        return

    # Second lets check the available range
    max_bound = copy.copy(states[0])
    min_bound = copy.copy(states[0])
    del max_bound["hash"]
    del min_bound["hash"]
    for each in states:
        for every in each:
            if every != "hash":
                if each[every] > max_bound[every]:
                    max_bound[every] = each[every]
                if each[every] < min_bound[every]:
                    min_bound[every] = each[every]
    
    for each in state:
        if state[each] > max_bound[each]:
            print(each+": "+str(state[each])+" is beyond of the scope of available dataset.")
            return
        if state[each] < min_bound[each]:
            print(each+": "+str(state[each])+" is beyond of the scope of available dataset.")
            return

    # Lets find subset of points for interpolation
    subset = []
    for each in states:
        for every in each:
            if every != "hash":
                if state[every] < each[every] and each[every] < max_bound[every]:
                    max_bound[every] = each[every]
                if state[every] > each[every] and each[every] > min_bound[every]:
                    min_bound[every] = each[every]

    candidate = copy.copy(state)
    keysList = list(candidate.keys())

    def recursion(n_levels):
        if n_levels == 0:
            candidate[keysList[n_levels]] = max_bound[keysList[n_levels]]
            subset.append(copy.copy(candidate))
            candidate[keysList[n_levels]] = min_bound[keysList[n_levels]]
            subset.append(copy.copy(candidate))
        else:
            candidate[keysList[n_levels]] = max_bound[keysList[n_levels]]
            recursion(n_levels-1)
            candidate[keysList[n_levels]] = min_bound[keysList[n_levels]]
            recursion(n_levels-1)

    recursion(len(state)-1)

    # Lets compute the distance between POI and surrounded points
    def distance(one, two):
        dist = 0
        if one.keys() != two.keys():
            print("Two states are inconsistent.")
            return
        for each in one:
            dist += (one[each]-two[each])**2
        return math.sqrt(dist)

    dist = []
    for each in subset:
        dist.append(distance(each, state))
        
    # Fetching the data from corresponding files
    surrounders = []
    for points in subset:
        for each in states:
            temp = copy.copy(each)
            del temp["hash"]
            if temp == points:
                file_path = os.path.join(db, each["hash"]+".json")
                # Opening JSON file
                f = open(file_path)
                data = json.load(f)
                surrounders.append(data)
                # Closing file
                f.close()

    result = {}
    channels = list(surrounders[0].keys())
    for i in range(len(channels)):
        for each in range(len(surrounders)):
            if each == 0:
                result[channels[i]] = np.array(surrounders[each][channels[i]])*dist[each]
            else:
                result[channels[i]] += np.array(surrounders[each][channels[i]])*dist[each]
        result[channels[i]] /= sum(dist)
    return result



def dictTransJSON(Dict, alias, mat):
    result = {}    
    translation = {}
    for each in Dict:
        new_key = each
        new_key = re.sub("[\(\[].*?[\)\]]", "", new_key)
        if new_key in alias:
            new_key = alias[new_key]
        translation[each] = new_key
    for each in translation:
        result[translation[each]] = Dict[each]
    if mat is not None:
        for mat_key in mat:
            cond = mat[mat_key]
            origins = []
            for each in result:
                if cond.find(each) > -1:
                    origins.append(each)
            for each in origins:
                temp = cond.replace(each, "result['"+each+"']")
                cond = temp
            arr = eval(cond)
            result[mat_key] = arr
    return result
   

