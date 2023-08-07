from csv import reader, DictReader
import re 
import xml.etree.ElementTree as ET
import yaml
import json
from yaml.loader import SafeLoader
import numpy as np
import os
import random

def JsonParsing(path, alias, mat):
    print("JSON parsing")
    f = open(path)
    data = json.load(f)
    print("Aliasing")
    result = {}
    # Alias
    for key in data:
        new_key = key
        new_key = re.sub("[\(\[].*?[\)\]]", "", new_key)
        if new_key in alias:
            new_key = alias[new_key]
        result[new_key] = data[key]
    return result



def PiTecParsing(path):
    with open(path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for _ in range(18):
            _=next(csv_reader)
        csv_dict_reader = DictReader(read_obj, delimiter='\t')
        return list(csv_dict_reader)

def func(Dict, name, arg):
    previous = 0
    previousArg = 0
    lap = "Distance"
    lap2 = "Lap Distance"
    for each in Dict:
        new_each = {}
        for key in each:
            new_key = key
            new_key = re.sub("[\(\[].*?[\)\]]", "", new_key)
            new_each[new_key] = each[key]
        if lap not in new_each:
            lap = lap2
        if float(new_each[lap]) < arg:
            previous = float(new_each[name])
            previousArg = float(new_each[lap])
        else:
            xp = [previousArg, float(new_each[lap])]
            fp = [previous, float(new_each[name])]
            return np.interp(arg, xp, fp)
    return None

def func2(Dict, name, arg):
    previous = 0
    lap = "Distance"
    lap2 = "Lap Distance"
    for each in Dict:
        new_each = {}
        for key in each:
            new_key = key
            new_key = re.sub("[\(\[].*?[\)\]]", "", new_key)
            new_each[new_key] = each[key]
        if lap not in new_each:
            lap = lap2
        if float(new_each[lap]) < arg:
            previous = float(new_each[name])
        else:
            return previous
    return previous

def dictTrans(Dict, alias, mat):
    result = {}
    translation = {}
    for each in Dict:
        if not result: #if result dict is empty
            for key in each:
                new_key = key
                new_key = re.sub("[\(\[].*?[\)\]]", "", new_key)
                if new_key in alias:
                    new_key = alias[new_key]
                translation[key] = new_key
                new_list = []
                if each[key] is None:
                    new_list.append(0.0)
                else:
                    new_list.append(float(each[key]))
                result[new_key] = new_list
            if mat is not None:
                for mat_key in mat:
                    new_list = []
                    cond = mat[mat_key]
                    for key in result:
                        if key:
                            temp = cond.replace(key, str(result[key][-1]))
                            cond = temp
                    value = eval(cond)
                    new_list.append(value)
                    result[mat_key] = new_list
        else:
            tick = {}
            for key in each:
                if each[key] is not None:
                    if translation[key] not in tick:
                        result[translation[key]].append(float(each[key]))
                        tick[translation[key]] = True
            if mat is not None:
                for mat_key in mat:
                    cond = mat[mat_key]
                    for key in result:
                        if key:
                            temp = cond.replace(key, str(result[key][-1]))
                            cond = temp
                    value = eval(cond)
                    result[mat_key].append(value)
    return result

def subtractTransSquareCost(DictOne, DictTwo, channel, arg):
    cost = 0.0
    listOne = []
    listTwo = []
    for num in range(len(DictOne[arg])):
        listOne.append((DictOne[arg][num], DictOne[channel][num]))
    for num in range(len(DictTwo[arg])):
        listTwo.append((DictTwo[arg][num], DictTwo[channel][num]))
    listOne.sort()
    listTwo.sort()
    indexOne = 0
    indexTwo = 0
    for indexOne, valueOne in enumerate(listOne):
        while indexTwo<len(listTwo):
            valueTwo = listTwo[indexTwo]
            if(valueOne[0]<=valueTwo[0]):
                if indexTwo>0:
                    sub = valueOne[1]-valueTwo[1]
                    cost += sub**2
                break
            else:
                indexTwo += 1
    return cost

def subtractSquareCost(listOne, listTwo):
    cost = 0.0
    listOne.sort()
    listTwo.sort()
    indexOne = 0
    indexTwo = 0
    for indexOne, valueOne in enumerate(listOne):
        while indexTwo<len(listTwo):
            valueTwo = listTwo[indexTwo]
            if(valueOne[0]<=valueTwo[0]):
                if indexTwo>0:
                    sub = valueOne[1]-valueTwo[1]
                    cost += sub**2
                break
            else:
                indexTwo += 1
    return cost

def subtractSquareCost(listOne, listTwo):
    cost = 0.0
    listOne.sort()
    listTwo.sort()
    indexOne = 0
    indexTwo = 0
    for indexOne, valueOne in enumerate(listOne):
        while indexTwo<len(listTwo):
            valueTwo = listTwo[indexTwo]
            if(valueOne[0]<=valueTwo[0]):
                if indexTwo>0:
                    sub = valueOne[1]-valueTwo[1]
                    cost += sub**2
                break
            else:
                indexTwo += 1
    return cost

def subtractTransSquareCostInterp(DictOne, DictTwo, channel, arg):
    cost = 0.0
    listOne = []
    listTwo = []
    for num in range(len(DictOne[arg])):
        listOne.append((DictOne[arg][num], DictOne[channel][num]))
    for num in range(len(DictTwo[arg])):
        listTwo.append((DictTwo[arg][num], DictTwo[channel][num]))
    listOne.sort()
    listTwo.sort()
    indexOne = 0
    indexTwo = 0
    for indexOne, valueOne in enumerate(listOne):
        while indexTwo<len(listTwo):
            valueTwo = listTwo[indexTwo]
            if(valueOne[0]<=valueTwo[0]):
                if indexTwo>0:
                    x1 = listTwo[indexTwo-1][0]
                    x2 = listTwo[indexTwo][0]  
                    y1 = listTwo[indexTwo-1][1]  
                    y2 = listTwo[indexTwo][1]  
                    x = listOne[indexOne][0]
                    y = (((y2-y1)*(x-x1))/(x2-x1))+y1
                    sub = listOne[indexOne][1]-y
                    cost += sub**2
                break
            else:
                indexTwo += 1
    return cost

def subtractSquareCostInterp(listOne, listTwo):
    cost = 0.0
    listOne.sort()
    listTwo.sort()
    indexOne = 0
    indexTwo = 0
    for indexOne, valueOne in enumerate(listOne):
        while indexTwo<len(listTwo):
            valueTwo = listTwo[indexTwo]
            if(valueOne[0]<=valueTwo[0]):
                if indexTwo>0:
                    x1 = listTwo[indexTwo-1][0]
                    x2 = listTwo[indexTwo][0]  
                    y1 = listTwo[indexTwo-1][1]  
                    y2 = listTwo[indexTwo][1]  
                    x = listOne[indexOne][0]
                    y = (((y2-y1)*(x-x1))/(x2-x1))+y1
                    sub = listOne[indexOne][1]-y
                    cost += sub**2
                break
            else:
                indexTwo += 1
    return cost

def subtractTransSquareCostRegres(DictOne, DictTwo, channel, arg):
    cost = 0.0
    def getlinear(x,y):
        def inner(x1):
            return m * x1 + b
        m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) * np.sum(x))
        b = (np.sum(y) - m *np.sum(x)) / len(x)
        return inner
    regressOne = getlinear(DictOne[arg], DictOne[channel])
    regressTwo = getlinear(DictTwo[arg], DictTwo[channel])
    N_max = max(DictOne[arg])
    N_min = min(DictOne[arg])
    step = (N_max-N_min)/len(DictOne[arg])
    for x in range(N_min, N_max, step):
        sub = regressOne(x)-regressTwo(x)
        cost += sub**2
    return cost

def subtractSquareCostRegres(listOne, listTwo):
    cost = 0.0
    def getlinear(list_of_tuples):
        def inner(x1):
            return m * x1 + b
        x = np.array([ele[0] for ele in list_of_tuples])
        y = np.array([ele[1] for ele in list_of_tuples])
        m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) * np.sum(x))
        b = (np.sum(y) - m *np.sum(x)) / len(x)
        return inner
    regressOne = getlinear(listOne)
    regressTwo = getlinear(listTwo)
    N_max = max(listOne,key=lambda item:item[0])[0]
    N_min = min(listOne,key=lambda item:item[0])[0]
    step = (N_max-N_min)/len(listOne)
    for x in np.arange(N_min, N_max, step):
        sub = regressOne(x)-regressTwo(x)
        cost += sub**2
    return cost

def subtractSquareCostLowPass(listOne, listTwo):
    cost = 0.0
    listOne.sort()
    listTwo.sort()
    indexOne = 0
    indexTwo = 0
    #
    #
    # Low-pass
    alpha = 0.75
    previous = None
    filteredOne = []
    for each in listOne:
        if previous is None:
            previous = alpha*each[1]
            filteredOne.append((each[0], previous))
            continue
        filtered_value = alpha*each[1]+(1-alpha)*previous
        previous = filtered_value
        filteredOne.append((each[0], previous))
    previous = None
    filteredTwo = []
    for each in listTwo:
        if previous is None:
            previous = alpha*each[1]
            filteredTwo.append((each[0], previous))
            continue
        filtered_value = alpha*each[1]+(1-alpha)*previous
        previous = filtered_value
        filteredTwo.append((each[0], previous))
    # Low-pass end
    #
    #
    for indexOne, valueOne in enumerate(filteredOne):
        while indexTwo<len(filteredTwo):
            valueTwo = filteredTwo[indexTwo]
            if(valueOne[0]<=valueTwo[0]):
                if indexTwo>0:
                    sub = valueOne[1]-valueTwo[1]
                    cost += sub**2
                break
            else:
                indexTwo += 1
    return cost

def subtract(DictOne, DictTwo, step, out_list):
    arg = -step
    result = []
    while(True):
        arg+=step
        DictLocal = {}
        for each in out_list:
            one = func(DictOne, each, arg)
            two = func(DictTwo, each, arg)
            if one is not None and two is not None:
                DictLocal.update({each: (one-two)})
            else:
                return result
        result.append(DictLocal)

def squarecost(outcome):
    result = 0.0
    for each in outcome:
        for every in each.keys():
            result += each[every]**2
    return result

def xmlScalarReading(path, name):
    tree = ET.parse(path)
    root = tree.getroot()
    for param in root.iter(name):
        return float(param[1].text)
    return None

def xmlScalarWriting(path, name, value):
    tree = ET.parse(path)
    root = tree.getroot()
    for param in root.iter(name):
        param[1].text = str(value)
        tree.write(path)
        return True
    return False

def xmlScalarShift(path, name, shift):
    tree = ET.parse(path)
    root = tree.getroot()
    for param in root.iter(name):
        value = float(param[1].text) + shift
        param[1].text = str(value)
        tree.write(path)
        return True
    return False

def xmlScalarScale(path, name, scale):
    tree = ET.parse(path)
    root = tree.getroot()
    for param in root.iter(name):
        value = float(param[1].text) * scale
        param[1].text = str(value)
        tree.write(path)
        return True
    return False

def xmlTextReading(path, name):
    tree = ET.parse(path)
    root = tree.getroot()
    for param in root.iter(name):
        return param[1].text
    return None

def xmlTextWriting(path, name, text):
    tree = ET.parse(path)
    root = tree.getroot()
    for param in root.iter(name):
        param[1].text = text
        tree.write(path)
        break

def mat2str(matrix):
    result = "["
    width = matrix.shape[1]
    for each in range(matrix.size):
        result += str(matrix.item(each))
        remaind = (each+1)%width
        if each+1==matrix.size:
            result += "]"
            return result
        if remaind == 0:
            result += ";"
        result += " "

def matrix_column_shift(matrix, column, shift):
    result = matrix.copy()
    for col in column:
        for i in range(col, result.size, result.shape[1]):
            result.itemset(i, result.item(i)+shift)
    return result
