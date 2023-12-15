#!/usr/bin/env python

from __future__ import annotations
from re import S

from ConfigSpace import Configuration, ConfigurationSpace, Float, Integer

import smac
from smac import Callback
from smac.intensifier import Intensifier
from smac import HyperparameterOptimizationFacade as HPOFacade
from smac import RunHistory, Scenario
from smac.runhistory import TrialInfo, TrialValue
 
import yaml
import json
from yaml.loader import SafeLoader
import numpy as np
import os
import time
import random
import xmltodict
from copy import copy
from subprocess import DEVNULL, STDOUT, check_call
import subprocess
import lib
import parallel
import xml.etree.ElementTree as ET
import Surrogate

import time
import threading
import sys

full_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..' ,'meta_compiler', 'meta_compiler'))
sys.path.insert(0, full_path)
import meta_compiler

class global_thread_memory():
    def __init__(self, config_path, mutex) -> None:
        print("Global thread memory initialization!")   
        self.mutex = mutex
        self.mutex.acquire()
        default_path = os.path.abspath(__file__ + "/../")
        self.absolut_register_path = os.path.abspath(default_path + "/global_thread_memory/register.json")

        # YAML parsing 
        with open(config_path, "r") as stream:
            try:
                config = yaml.load(stream, Loader=SafeLoader)
            except yaml.YAMLError as exc:
                print(exc)

        if not os.path.exists(self.absolut_register_path):
            empty_register = {"configs": [config["inputs"]], "trials": [], "xmls": []}
            json_object = json.dumps(empty_register)
            with open(self.absolut_register_path, "w") as outfile:
                outfile.write(json_object)
            self.n_config = 0
        else:
            with open(self.absolut_register_path, 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                self.n_config = None
                for i in range(len(json_object["configs"])):
                    if json_object["configs"][i] == config["inputs"]:
                        self.n_config = i
                        self.mutex.release()
                        return
            if self.n_config is None:
                self.n_config = len(json_object["configs"])
                json_object["configs"].append(config["inputs"])
                with open(self.absolut_register_path, "w") as jsonFile:
                    json.dump(json_object, jsonFile)
        self.mutex.release()

    def get_shortcut(self, configuration, budget = None):          
        self.mutex.acquire()
        if isinstance(configuration, dict):
            my_dict = configuration
        else:
            my_dict = dict(configuration)
        print("The shortcut request")
        if budget is not None:
            my_dict["budget"] = budget
        with open(self.absolut_register_path, 'r') as openfile: 
            # Reading from json file
            json_object = json.load(openfile)
            n_xml = None
            for i in range(len(json_object["xmls"])):
                if json_object["xmls"][i] == my_dict:
                    n_xml = i
                    break
            if n_xml is not None:
                for i in range(len(json_object["trials"])):
                    if json_object["trials"][i][0] == self.n_config and json_object["trials"][i][1] == n_xml:     
                        self.mutex.release()
                        return json_object["trials"][i][2]        
        self.mutex.release()
        return None

    def set_shortcut(self, configuration, cost, budget = None):  
        check = self.get_shortcut(configuration, budget=budget)
        if check is not None:
            print("The shortcut is already exists!")
            return
        self.mutex.acquire()
        if isinstance(configuration, dict):
            my_dict = configuration
        else:
            my_dict = dict(configuration)        
        if budget is not None:
            my_dict["budget"] = budget
        with open(self.absolut_register_path, 'r') as openfile: 
            # Reading from json file
            json_object = json.load(openfile)
            new_key_xml = len(json_object["xmls"])
            obj = (self.n_config, new_key_xml, cost)        
            json_object["xmls"].append(my_dict)
            json_object["trials"].append(obj)

        with open(self.absolut_register_path, 'w') as openfile: 
            json.dump(json_object, openfile)
        print("New shortcut was stored")
        self.mutex.release()


    def print(self):
        with open(self.absolut_register_path, 'r') as openfile: 
            # Reading from json file
            json_object = json.load(openfile)
            print(json_object)
            


def top_speed_simulation(config, param, data_ref_trans_laptimer, id, norm):
    default_path = os.path.abspath(__file__ + "/../")
    root = os.path.abspath(__file__ + "/../../../")
    car = config["config"]["racecar"]
    track = config["config"]["track"]
    short = car+"_"+(track[0:3].upper())
    config_path = car+"\\"+track+"\\"+short;
    
    simulated_top = os.path.join(root, "x64\\Release\\topSpeedOutput.txt")
    alias = config["output_aliasing"]
    mat = config["mat_outputs"]
    fastParse = os.path.join(root, "x64\\Release\\FastParser.exe")
    xml = os.path.join(root, "References\\LapTimer\\"+car+"\\"+track+"\\parametersAfterSetup"+id+".xml")
    exe = os.path.join(root, "x64\\Release\\SimTool.Console.exe")
    out_list = config["outputs"]
    exec_path = os.path.join(root, "x64\\Release")

    
    # Prepare the xml file
    print("Uploading the racecar configuration")
    state = {}
    for input in param:
        if input not in config["inputs"]:
            print("Error: Unknown parameter "+str(input))
            return 999999.9
        access_w = config["inputs"][input]["access_w"]
        access_r = config["inputs"][input]["access_r"]
        def_val = eval(access_r)
        state[input] = def_val
        exec("value_script_update = "+str(param[input])+"; "+access_w)

    # Run simulation
    print("Run simulation")
    try:
        os.chdir(exec_path)
        check_call(exe+" topspeed "+config_path+" -1 ", stdout=DEVNULL, stderr=STDOUT)
        os.chdir(default_path)
    except subprocess.CalledProcessError as e:
        print("Simulator was unable to complete the lap.")
        return 999999.9
    print("Simulation is over")

    # Restore the original xml file
    for input in param:
        access_w = config["inputs"][input]["access_w"]
        exec("value_script_update = "+str(state[input])+"; "+access_w)

    # Fetch the data
    if config["config"]["fast_parse"]:
        print("Data fast parsing")
        data_trans = lib.fast_parse(simulated_top, fastParse, alias, mat['topspeed'])
    else:
        print("Data parsing")
        data = lib.PiTecParsing(simulated_top)
        data_trans = lib.dictTrans(data, alias, mat["topspeed"])
    print("Data processing")

    # Cost calc
    cost = 0.0
    for input in param:
        for each in config["inputs"][input]["affect_on"]:
            arg = config["inputs"][input]["affect_on"][each]["wrt"]
            mult = config["inputs"][input]["affect_on"][each]["multiplicator"]
            cond = config["inputs"][input]["affect_on"][each]["filter"]
            cond_list = []
            if cond is not None:
                for every in out_list:
                    if every in cond:
                        cond_list.append(every)
            data_list_sim = []
            for idx in range(len(data_trans[each])):
                if "filter" in config["inputs"][input]["affect_on"][each] and config["inputs"][input]["affect_on"][each]["filter"] is not None:
                    cond = config["inputs"][input]["affect_on"][each]["filter"]
                    for every in cond_list:
                        data = data_trans[every][idx]
                        cond2 = cond.replace(every, str(data))
                        cond = cond2
                    cond_is_ok = eval(cond)
                else:
                    cond_is_ok = True
                fun_val = data_trans[each][idx]
                arg_val = data_trans[arg][idx]
                if cond_is_ok:
                    data_list_sim.append((arg_val, fun_val))
            data_list_ref = []
            for idx in range(len(data_ref_trans_laptimer[each])):
                if "filter" in config["inputs"][input]["affect_on"][each] and config["inputs"][input]["affect_on"][each]["filter"] is not None:
                    cond = config["inputs"][input]["affect_on"][each]["filter"]
                    for every in cond_list:
                        data = data_ref_trans_laptimer[every][idx]
                        cond2 = cond.replace(every, str(data))
                        cond = cond2
                    cond_is_ok = eval(cond)
                else:
                    cond_is_ok = True
                fun_val = data_ref_trans_laptimer[each][idx]
                arg_val = data_ref_trans_laptimer[arg][idx]
                if cond_is_ok:
                    data_list_ref.append((arg_val, fun_val))

            if config["inputs"][input]["affect_on"][each]["cost"] == "interp_square_cost":
                current_cost = lib.subtractSquareCostInterp(data_list_sim, data_list_ref)
            elif config["inputs"][input]["affect_on"][each]["cost"] == "closest_square_cost":
                current_cost = lib.subtractSquareCost(data_list_sim, data_list_ref)
            elif config["inputs"][input]["affect_on"][each]["cost"] == "regress_square_cost":
                current_cost = lib.subtractSquareCostRegres(data_list_sim, data_list_ref)
            elif config["inputs"][input]["affect_on"][each]["cost"] == "lowpass_square_cost":
                current_cost = lib.subtractSquareCostLowPass(data_list_sim, data_list_ref)
            else: 
                print("Error: Unknown type of cost function")
                return 999999.9
        if each not in norm:
            norm[each] = 1/current_cost
        cost += mult * norm[each] * current_cost
    print("Current cost is: "+str(cost))
    return cost

def laptimer_simulation(config, param, data_ref_trans_laptimer, id, norm, budget=9999.9):
    default_path = os.path.abspath(__file__ + "/../")
    root = os.path.abspath(__file__ + "/../../../")
    car = config["config"]["racecar"]
    track = config["config"]["track"]
    short = car+"_"+(track[0:3].upper())
    config_path = car+"\\"+track+"\\"+short
    simulated_laptimer = os.path.join(root, "References\\LapTimer\\"+config_path+"\\"+short+"_Data"+id+".txt")
    alias = config["output_aliasing"]
    mat = config["mat_outputs"]
    fastParse = os.path.join(root, "x64\\Release\\FastParser.exe")
    xml = os.path.join(root, "References\\LapTimer\\"+car+"\\"+track+"\\parametersAfterSetup"+id+".xml")
    exe = os.path.join(root, "x64\\Release\\SimTool.Console.exe")
    out_list = config["outputs"]
    exec_path = os.path.join(root, "x64\\Release")

    # Prepare the xml file
    print("Uploading the racecar configuration")
    state = {}
    for input in param:
        if input not in config["inputs"]:
            print("Error: Unknown parameter "+str(input))
            return 999999.9
        access_w = config["inputs"][input]["access_w"]
        access_r = config["inputs"][input]["access_r"]
        def_val = eval(access_r)
        state[input] = def_val
        exec("value_script_update = "+str(param[input])+"; "+access_w)

    # Run simulation
    print("Run simulation")
    try:
        os.chdir(exec_path)
        if id == "":
            check_call(exe+" laptimer "+config_path+" -1 "+str(budget), stdout=DEVNULL, stderr=STDOUT)
        else:
            check_call(exe+" laptimer "+config_path+" "+str(id)+" "+str(budget), stdout=DEVNULL, stderr=STDOUT)
        #os.chdir(default_path)
    except subprocess.CalledProcessError as e:
        print("Simulator was unable to complete the lap.")
        #os.chdir(default_path)
        return 999999.9
    print("Simulation is over")

    # Restore the original xml file
    for input in param:
        access_w = config["inputs"][input]["access_w"]
        exec("value_script_update = "+str(state[input])+"; "+access_w)

    # Fetch the data
    if config["config"]["fast_parse"]:
        print("Data fast parsing")
        data_trans = lib.fast_parse(simulated_laptimer, fastParse, alias, mat['laptimer'])
    else:
        print("Data parsing")
        data = lib.PiTecParsing(simulated_laptimer)
        data_trans = lib.dictTrans(data, alias, mat["laptimer"])
    print("Data processing")

    # Cost calc
    cost = 0.0
    for input in param:
        for each in config["inputs"][input]["affect_on"]:
            arg = config["inputs"][input]["affect_on"][each]["wrt"]
            mult = config["inputs"][input]["affect_on"][each]["multiplicator"]
            cond = config["inputs"][input]["affect_on"][each]["filter"]
            cond_list = []
            if cond is not None:
                for every in out_list:
                    if every in cond:
                        cond_list.append(every)
            data_list_sim = []
            for idx in range(len(data_trans[each])):
                if "filter" in config["inputs"][input]["affect_on"][each] and config["inputs"][input]["affect_on"][each]["filter"] is not None:
                    cond = config["inputs"][input]["affect_on"][each]["filter"]
                    for every in cond_list:
                        data = data_trans[every][idx]
                        cond2 = cond.replace(every, str(data))
                        cond = cond2
                    cond_is_ok = eval(cond)
                else:
                    cond_is_ok = True
                fun_val = data_trans[each][idx]
                arg_val = data_trans[arg][idx]
                if cond_is_ok:
                    data_list_sim.append((arg_val, fun_val))
            data_list_ref = []
            for idx in range(len(data_ref_trans_laptimer[each])):
                if "filter" in config["inputs"][input]["affect_on"][each] and config["inputs"][input]["affect_on"][each]["filter"] is not None:
                    cond = config["inputs"][input]["affect_on"][each]["filter"]
                    for every in cond_list:
                        data = data_ref_trans_laptimer[every][idx]
                        cond2 = cond.replace(every, str(data))
                        cond = cond2
                    cond_is_ok = eval(cond)
                else:
                    cond_is_ok = True
                fun_val = data_ref_trans_laptimer[each][idx]
                arg_val = data_ref_trans_laptimer[arg][idx]
                if cond_is_ok:
                    data_list_ref.append((arg_val, fun_val))

            if config["inputs"][input]["affect_on"][each]["cost"] == "interp_square_cost":
                current_cost = lib.subtractSquareCostInterp(data_list_sim, data_list_ref)
            elif config["inputs"][input]["affect_on"][each]["cost"] == "closest_square_cost":
                current_cost = lib.subtractSquareCost(data_list_sim, data_list_ref)
            elif config["inputs"][input]["affect_on"][each]["cost"] == "regress_square_cost":
                current_cost = lib.subtractSquareCostRegres(data_list_sim, data_list_ref)
            elif config["inputs"][input]["affect_on"][each]["cost"] == "lowpass_square_cost":
                current_cost = lib.subtractSquareCostLowPass(data_list_sim, data_list_ref)
            else: 
                print("Error: Unknown type of cost function")
                return 999999.9
        if each not in norm:
            norm[each] = 1/current_cost
        cost += mult * norm[each] * current_cost
    print("Current cost is: "+str(cost))
    return cost

class AbstractSimulation:
    def __init__(self) -> None:

        # File paths  
        absolute_path = os.path.dirname(__file__)
        yamlpath = os.path.join(absolute_path, "config.yaml")

        # YAML parsing 
        with open(yamlpath, "r") as stream:
            try:
                self.config = yaml.load(stream, Loader=SafeLoader)
            except yaml.YAMLError as exc:
                print(exc)
        
        # Abstract
        self.exe = self.config["simulation"][self.simulation_name]["exe"]
        self.result_data = self.config["simulation"][self.simulation_name]["data"]
        self.xml = self.config["simulation"][self.simulation_name]["xml"]   
        self.xmlManager = lib.XMLFacade(self.xml)

        # Reference data
        self.alias = self.config["output_aliasing"]
        self.mat = self.config["mat_outputs"]
        self.fastParse = self.config["config"]["fast_parse_exe"]
        self.initial_reference_loading()        

    def meta_compiler_antlr(self, matlab_input: str) -> str:
        param_list = lib.get_xml_param_list(self.xml)
        matlab_no_space = matlab_input.replace(" ", "")
        matlab_input_list = matlab_no_space.split(";")
        result = ""
        for each in matlab_input_list:
            if each == "":
                continue
            result += meta_compiler.meta_compiler(param_list, each) + ";"
        return result[:-1]

    def meta_compiler(self, matlab_input: str) -> str:

        def reading_command(param_list, string: str):
            result = copy(string.replace("update", "value_script_update"))
            for each in param_list:
                if each in string:
                    result = result.replace(each, "lib.xmlMetaReading(xml,'"+each+"','")+"')"
            return result

        def writing_command(param_list, string: str, value, assignment):
            result = copy(string)
            for each in param_list:
                if each in string:
                    position = result.replace(each, "")
                    if ":" in position: # Cycle of assignments
                        result = ""
                        numbers = position[1:-1].split(":")
                        if "," in numbers[0]:
                            numbers_sec = numbers[0].split(",")
                            for every in range(int(numbers_sec[1]), int(numbers[1])):
                                new_position = "("+numbers_sec[0]+","+str(every)+")"
                                result+=writing_command(param_list, each+new_position, value, assignment)+";"
                            return result[:-1]
                        else:
                            numbers_sec = numbers[1].split(",")
                            for every in range(int(numbers[0]), int(numbers_sec[0])):
                                new_position = "("+str(every)+","+numbers_sec[1]+")"
                                result+=writing_command(param_list, each+new_position, value, assignment)+";"
                            return result[:-1]
                    if assignment == "=":
                        result = "lib.xmlMetaWriting(xml,'"+each+"','"+position+"', "+value+")"
                    elif assignment == "+=":
                        result = "lib.xmlMetaWriting(xml,'"+each+"','"+position+"', lib.xmlMetaReading(xml, '"+each+"', '"+position+"')+"+value+")"
                    if assignment == "-=":
                        result = "lib.xmlMetaWriting(xml,'"+each+"','"+position+"', lib.xmlMetaReading(xml, '"+each+"', '"+position+"')-"+value+")"
                    return result
            return string+assignment+value

        result = ""
        param_array = lib.get_xml_param_list(self.xml)
        no_spaces = matlab_input.strip()
        no_fucking_spaces = no_spaces.replace(" ", "")
        lines = no_fucking_spaces.split(";")
        for each in lines:
            if each == "":
                continue
            if "=" in each:
                if "+=" in each:
                    parts = each.split("+=")
                    assignment = "+="
                elif "-=" in each:                    
                    parts = each.split("-=")                    
                    assignment = "+="
                else:
                    parts = each.split("=")                    
                    assignment = "="
                if len(parts) != 2:
                    raise Exception("The command cannot content more than one '=' symbol.")
                [left, right] = parts
                result += writing_command(param_array, left, reading_command(param_array, right), assignment) + ";"
            else:
                result = reading_command(param_array, each) + ";" 
        return result[:-1]

    def xml_get_state(self, param):
        xml = self.xml

        # Prepare the xml file
        print("Save the racecar configuration")
        state = {}
        for input in param:
            if input not in self.config["inputs"]:
                raise Exception("Error: Unknown parameter "+str(input))
            meta_access_r = self.config["inputs"][input]["access_r"]
            access_r = self.meta_compiler_antlr(meta_access_r)
            def_val = eval(access_r)
            state[input] = def_val
        return state

    def xml_load_state(self, param):
        xml = self.xml

        # Prepare the xml file
        print("Uploading the racecar configuration")
        for input in param:
            if input not in self.config["inputs"]:
                raise Exception("Error: Unknown parameter "+str(input))
            meta_access_w = self.config["inputs"][input]["access_w"]
            access_w = self.meta_compiler_antlr(meta_access_w)
            exec("value_script_update = "+str(param[input])+"; "+access_w)
        self.xmlManager.write_to_file()

    def initial_reference_loading(self):        
        reference3 = self.config["config"]["reference"]
        if self.config["config"]["fast_parse"]:        
            self.data_ref_trans_laptimer = lib.fast_parse(reference3, self.fastParse, self.alias, self.mat[self.simulation_name])
        else:    
            # Real car data loading laptimer
            data_ref_laptimer = lib.PiTecParsing(reference3)
            self.data_ref_trans_laptimer = lib.dictTrans(data_ref_laptimer, self.alias, self.mat[self.simulation_name])

    def load_sim_data(self):
        # Fetch the data
        if self.config["config"]["fast_parse"]:
            print("Data fast parsing")
            data_trans = lib.fast_parse(self.result_data, self.fastParse, self.alias, self.mat[self.simulation_name])
        else:
            print("Data parsing")
            data = lib.PiTecParsing(self.result_data)
            data_trans = lib.dictTrans(data, self.alias, self.mat[self.simulation_name])
        return data_trans

    def cost_progressive(self, param, data_trans):
        print("Cost progressive analysis!")                
        lap = "Distance"
        total_length = len(data_trans[lap])
        resultance_progression = {}
        for idx in range(total_length):
            short_data = {}
            for each in data_trans:
                short_data[each] = data_trans[each][:idx]
            if data_trans[lap][idx] > 1000:
                print("There it is!")
            try:
                cost = self.cost_computation(param, short_data)
            except:
                print("Fail with dist: "+str(data_trans[lap][idx]))
                continue
            print("Adding data to resultance")
            resultance_progression[data_trans[lap][idx]] = cost
        return resultance_progression


    def cost_computation(self, param, data_trans):
        # Cost calc
        cost = 0.0
        for input in param:
            for each in self.config["inputs"][input]["affect_on"]:
                arg = self.config["inputs"][input]["affect_on"][each]["wrt"]
                mult = self.config["inputs"][input]["affect_on"][each]["multiplicator"]
                cond = self.config["inputs"][input]["affect_on"][each]["filter"]
                cond_list = []
                if cond is not None:
                    for every in data_trans:
                        if every in cond:
                            cond_list.append(every)
                data_list_sim = []
                for idx in range(len(data_trans[each])):
                    if "filter" in self.config["inputs"][input]["affect_on"][each] and self.config["inputs"][input]["affect_on"][each]["filter"] is not None:
                        cond = self.config["inputs"][input]["affect_on"][each]["filter"]
                        for every in cond_list:
                            data = data_trans[every][idx]
                            cond2 = cond.replace(every, str(data))
                            cond = cond2
                        cond_is_ok = eval(cond)
                    else:
                        cond_is_ok = True
                    fun_val = data_trans[each][idx]
                    arg_val = data_trans[arg][idx]
                    if cond_is_ok:
                        data_list_sim.append((arg_val, fun_val))
                data_list_ref = []
                for idx in range(len(self.data_ref_trans_laptimer[each])):
                    if "filter" in self.config["inputs"][input]["affect_on"][each] and self.config["inputs"][input]["affect_on"][each]["filter"] is not None:
                        cond = self.config["inputs"][input]["affect_on"][each]["filter"]
                        for every in cond_list:
                            data = self.data_ref_trans_laptimer[every][idx]
                            cond2 = cond.replace(every, str(data))
                            cond = cond2
                        cond_is_ok = eval(cond)
                    else:
                        cond_is_ok = True
                    fun_val = self.data_ref_trans_laptimer[each][idx]
                    arg_val = self.data_ref_trans_laptimer[arg][idx]
                    if cond_is_ok:
                        data_list_ref.append((arg_val, fun_val))

                if self.config["inputs"][input]["affect_on"][each]["cost"] == "interp_square_cost":
                    current_cost = lib.subtractSquareCostInterp(data_list_sim, data_list_ref)
                elif self.config["inputs"][input]["affect_on"][each]["cost"] == "closest_square_cost":
                    current_cost = lib.subtractSquareCost(data_list_sim, data_list_ref)
                elif self.config["inputs"][input]["affect_on"][each]["cost"] == "regress_square_cost":
                    current_cost = lib.subtractSquareCostRegres(data_list_sim, data_list_ref)
                elif self.config["inputs"][input]["affect_on"][each]["cost"] == "lowpass_square_cost":
                    current_cost = lib.subtractSquareCostLowPass(data_list_sim, data_list_ref)
                else: 
                    print("Error: Unknown type of cost function")
                    return 999999.9
            if each not in self.dict[input]:
                self.dict[input][each] = 1/current_cost
            cost += mult * self.dict[input][each] * current_cost
        print("Current cost is: "+str(cost))
        return cost


class TSRsimulation(AbstractSimulation):
    def __init__(self, dict_in={}) -> None:        
        print("TSRSimulation connected!")
        self.simulation_name = "laptimer"   
        super().__init__()
        self.budget = 5000.0
        self.final_budget = 5000.0
        self.step_budget = 10.0
        self.exec_path = os.path.abspath(self.exe + "/../")
        self.total_sim_path = 0.0
        self.dict = dict_in
        
    @property
    def configspace(self) -> ConfigurationSpace:
        cs = ConfigurationSpace(seed=0)
        param_list = []
        for each in self.config["inputs"]:
            if self.config["inputs"][each]["usage"]:
                param_list.append(Float(each, (self.config["inputs"][each]["min_val"], self.config["inputs"][each]["max_val"]), default=self.config["inputs"][each]["init_val"]))
        cs.add_hyperparameters(param_list)
        return cs

    def simulation_call(self, budget):
        # Run simulation
        print("Run simulation")
        car = self.config["config"]["racecar"]
        track = self.config["config"]["track"]
        short = car+"_"+(track[0:3].upper())
        config_path = car+"\\"+track+"\\"+short
        try:
            os.chdir(self.exec_path)
            check_call(self.exe+" laptimer "+config_path+" -1 "+str(budget), stdout=DEVNULL, stderr=STDOUT)            
            #os.chdir(default_path)
        except subprocess.CalledProcessError as e:
            print("Simulator was unable to complete the lap.")
            #os.chdir(default_path)
            return False
        print("Simulation is over")
        self.total_sim_path += budget
        time.sleep(2.0)
        return True

    def get_total_path(self):
        return self.total_sim_path

    def simulation(self, configuration: Configuration, seed: int = 0, budget=None) -> float:
        if budget is not None:
            self.budget = budget
            print("Budget is: "+str(self.budget))
        else:
            self.budget = 5000.0
        state = self.xml_get_state(configuration)
        self.xml_load_state(configuration)
        result = self.simulation_call(self.budget)
        self.xml_load_state(state)        
        if not result:
            return 999999.9
        data_trans = self.load_sim_data()
        cost = float(self.cost_computation(configuration, data_trans))
        return cost

    def cost_progression_analysis(self, configuration: Configuration):
        
        self.budget = 5000.0
        state = self.xml_get_state(configuration)
        self.xml_load_state(configuration)
        result = self.simulation_call(self.budget)
        self.xml_load_state(state)        
        if not result:
            return None
        data_trans = self.load_sim_data()
        resultance = self.cost_progressive(configuration, data_trans)
        return resultance
    
    def budget_stretch(self):
        if self.budget < self.final_budget:
            self.budget += self.step_budget
            print("The budget was increased: " + str(self.budget))
        else:
            print("The budget was saturated")
    
class TSRsimulationMemory(TSRsimulation):
    def __init__(self, memory=None):
        super().__init__()
        self.memory=memory

    def simulation(self, configuration: Configuration, seed: int = 0, budget=None) -> float:
        if self.memory is not None:
            shortcut = self.memory.get_shortcut(configuration, budget=budget)
            if shortcut is not None:
                print("The simulation was shortcutted!")
                cost = shortcut

        if self.memory is None or shortcut is None:
            cost = super().simulation(configuration, seed=seed, budget=budget)
            
        if self.memory is not None:
            self.memory.set_shortcut(configuration, cost, budget=budget)
        return cost

class TSRMultithreadSimulation(TSRsimulationMemory):
    def __init__(self, id_in, dict_in={}, mutex=None, barrier=None, reference_init=True, sub_barrier=None, memory=None) -> None:        
        print("TSRMultithreadSimulation connected!")
        
        super().__init__(memory=memory)
        self.id = id_in
        self.dict=dict_in
        self.mutex=mutex
        self.barrier=barrier
        self.reference_init=reference_init
        self.sub_barrier=sub_barrier

        self.xml = self.xml[:-4]+id_in+self.xml[-4:]
        self.xmlManager.__init__(self.xml)
        self.result_data = self.result_data[:-4]+id_in+self.result_data[-4:]

    def simulation_call(self, budget):
        # Run simulation
        print("Run simulation")
        car = self.config["config"]["racecar"]
        track = self.config["config"]["track"]
        short = car+"_"+(track[0:3].upper())
        config_path = car+"\\"+track+"\\"+short
        try:
            os.chdir(self.exec_path)
            if self.id == "":
                check_call(self.exe+" laptimer "+config_path+" -1 "+str(budget), stdout=DEVNULL, stderr=STDOUT)
            else:
                check_call(self.exe+" laptimer "+config_path+" "+self.id+" "+str(budget), stdout=DEVNULL, stderr=STDOUT)
            #os.chdir(default_path)
        except subprocess.CalledProcessError as e:
            print("Simulator was unable to complete the lap.")
            #os.chdir(default_path)
            return False
        print("Simulation is over")
        self.total_sim_path += budget
        return True

    def simulation(self, configuration: Configuration, seed: int = 0, budget=None) -> float:
        if self.barrier is not None:
            self.barrier.wait()            
        
        if self.mutex is not None:
            self.mutex.acquire()            
            
        cost = super().simulation(configuration, seed=seed, budget=budget)

        if self.sub_barrier is not None:
            self.sub_barrier.wait()

        os.chdir(os.path.abspath(__file__ + "/../"))

        if self.mutex is not None:
            self.mutex.release()            
        return cost


class CustomCallback(Callback):

    def on_start(self, smbo: smac.main.smbo.SMBO) -> None:
        self.previous_cost = 999999.9
        self.initialized = False
        self.trials_counter = 0
        self.threshold = 0.1
        print("Let's start!")
        print("")

    def on_tell_end(self, smbo: smac.main.smbo.SMBO, info: TrialInfo, value: TrialValue) -> bool | None:
        self.trials_counter += 1

        #model.budget_stretch()

        if self.trials_counter == 9999:
            print(f"We just triggered to stop the optimization after {smbo.runhistory.finished} finished trials.")
            incumbent = smbo.intensifier.get_incumbent()
            assert incumbent is not None
            current_dict = smbo.runhistory.get
            print(f"Incumbent get dict {current_dict} finished trials.")
            return False

        return None
   
def high_level_management():
    # File paths    
    absolute_path = os.path.dirname(__file__)
    yamlpath = os.path.join(absolute_path, "config.yaml")

    # YAML parsing 
    with open(yamlpath, "r") as stream:
        try:
            config = yaml.load(stream, Loader=SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)
    
    out_list = []
    in_list = []
    for output in config["outputs"]:
        if config["outputs"][output]:
            out_list.append(output)
    for input in config["inputs"]:
        if config["inputs"][input]["usage"]:
            in_list.append(input)
    
    queue = []
    for index, input in enumerate(in_list):
        new_list = []
        new_list.append(input)
        if config["inputs"][input]["dependent"] is not None:
            for every in config["inputs"][input]["dependent"]:
                if every in in_list:
                    new_list.append(every)
        queue.append(new_list)

    def is_dependent(list1, list2):
        if list1 == list2:
            return False
        for every in list1:
            for each in list2:
                if every == each:
                    return True
        return False

    def merge(index1, index2, list_of_lists):
        for every in list_of_lists[index2]:
            if every not in list_of_lists[index1]:
                list_of_lists[index1].append(every)
        list_of_lists[index2].clear()

    done = False
    while not done:
        done = True
        for index in range(0, len(queue)):
            for index2 in range(index, len(queue)):
                if is_dependent(queue[index], queue[index2]):
                    done = False
                    merge(index, index2, queue)
    queue_exe = {}
    queue_exp = {}
    for each in queue:
        if not each:
            continue
        top_priority = len(in_list)+1
        for every in each:
            if "priority" not in config["inputs"][every] or config["inputs"][every]["priority"] is None:
                continue
            priority = config["inputs"][every]["priority"]
            if top_priority>priority:
                top_priority = priority
        while top_priority in queue_exe:
            top_priority += 1
        queue_exe[top_priority] = each
        queue_exp[top_priority] = [config["inputs"][every]["experiment"]]
        for every in each:
            particular_experiment = config["inputs"][every]["experiment"]
            if particular_experiment not in queue_exp[top_priority]:
                queue_exp[top_priority].append(particular_experiment)

    print(queue_exe)

    if config["config"]["parallel"]:
        print("Parallel")
    else:        
        if config["config"]["optimization"] == "nelder_mead":
            for key in sorted(queue_exe):
                # chunk
                local_in_list = queue_exe[key]
                local_exp = queue_exp[key]
                model = TSRsimulation("")
                result = Nelder_Mead_optimization(model.train, local_in_list, config)
                print(result)
        elif config["config"]["optimization"] == "gradient_descent":
            print("gradient_descent")

def Nelder_Mead_optimization(simulation, local_in_list, config):
    state = {}
    tolerance = {}
    print("Computing initial simplex of "+str(len(local_in_list)+1)+" points")
    for input in local_in_list:
        init_val = config["inputs"][input]["init_val"]
        state[input] = init_val
    prev_best = simulation(state)
    res = [[state, prev_best]]
    for input in local_in_list:
        state_updated = copy(state)
        init_val = config["inputs"][input]["init_val"]
        init_step = config["inputs"][input]["init_step"]
        tol = config["inputs"][input]["tolerance"]
        tolerance[input] = tol
        state_updated[input] = init_val+init_step
        local_cost = simulation(state_updated)
        res.append([state_updated, local_cost])
    print("Initial simplex was computed!")
    no_improv = 0
    iters = 0
    while(True):
        # order
        res.sort(key=lambda x: x[1])
        print("Brand new iteration:")
        print(res)
        best = res[0][1]
        dim = len(state)
        alpha=1.0
        if dim>2:
            gamma=1+(2/dim)
            rho=-(0.75-(1/(2*dim)))
            sigma=1-(1/dim)
        else:
            gamma=2
            rho=-0.5
            sigma=0.5
        no_improve_thr = 1e-3
        no_improv_break=100

        if best < prev_best - no_improve_thr:
            no_improv = 0
            prev_best = best
        else:
            no_improv += 1

        if no_improv >= no_improv_break:
            print("There is no improvement "+str(no_improv_break)+" times in a row. Best founded is:")
            print(res[0])
            return res[0]

        out_points = 0
        for input in local_in_list:
            arr = []
            for tup in res:
                arr.append(tup[0][input])
            max_val = max(arr)
            min_val = min(arr)
            width = (max_val-min_val)*2.0
            if width<tolerance[input]:
                out_points+=1
        if out_points>=len(local_in_list):
            print("Tolerance reached! The best set is:")
            print(res[0])                     
            for input in local_in_list:
                access_w = config["inputs"][input]["access_w"]
                exec("value_script_update = "+str(res[0][0][input])+"; "+access_w)
            return res[0]
        if no_improv >= no_improv_break:
            print("There is no improvement "+str(no_improv_break)+" times in a row. Best founded is:")
            print(res[0])
            return res[0]
        
        # centroid
        x0 = {}
        for key in state:
            x0[key] = 0.0
        for tup in res[:-1]:
            for key, value in tup[0].items():
                x0[key] += value/(len(res)-1)
        

        # reflection
        xr = {}
        for key in state:
            xr[key] = x0[key] + alpha*(x0[key] - res[-1][0][key])
        rscore = simulation(xr)
        if res[0][1] <= rscore < res[-2][1]:
            print("reflect")
            del res[-1]
            res.append([xr, rscore])
            continue

        # expansion
        if rscore < res[0][1]:
            xe = {}
            for key in state:
                xe[key] = x0[key] + gamma*(x0[key] - res[-1][0][key])                        
            escore = simulation(xe)
            print("expansion")
            if escore < rscore:
                del res[-1]
                res.append([xe, escore])
                continue
            else:
                del res[-1]
                res.append([xr, rscore])
                continue

        if dim==1:
            xc = {}
            for key in state:
                xc[key] = x0[key] + rho*(x0[key] - res[-1][0][key])                        
            cscore = simulation(xc)                                   
            del res[-1]
            res.append([xc, cscore])
        else:
            # contraction
            if rscore>=res[-2][1]:
                xc = {}
                for key in state:
                    xc[key] = x0[key] + rho*(x0[key] - res[-1][0][key])
                cscore = simulation(xc)
                if cscore < res[-2][1]:
                    print("contraction inside")
                    del res[-1]
                    res.append([xc, cscore])
                    continue
            else:
                xc = {}
                for key in state:
                    xc[key] = x0[key] - rho*(x0[key] - res[-1][0][key])
                cscore = simulation(xc)
                if cscore < res[-2][1]:
                    print("contraction outside")
                    del res[-1]
                    res.append([xc, cscore])
                    continue


            # reduction
            x1 = res[0][0]
            nres = [res[0]]
            print("reduction")

            for tup in res[1:]:
                redx = {}
                for key in state:
                    redx[key] = x1[key] + sigma*(tup[0][key] - x1[key])
                score = simulation(redx)
                nres.append([redx, score])
            res = nres
def main():    
    yamlpath = os.path.join(os.path.dirname(__file__), "config.yaml")
    mutex = threading.Lock()
    #memory_obj = global_thread_memory(yamlpath, mutex)
    print("simulation.py file is here!")
    model = TSRsimulationMemory(memory=memory_obj)

    conf_space=model.configspace

    # Scenario object specifying the optimization "environment"
    scenario = Scenario(conf_space, n_trials=9999, seed=132, output_directory="smac3")

    # Intensifyer object
    intensifier_obj = Intensifier(scenario, max_config_calls=1)

    # Initial design
    initial_design_obj = HPOFacade.get_initial_design(scenario, n_configs=0, additional_configs=[conf_space.get_default_configuration()])

    # Now we use SMAC to find the best hyperparameters
    smac_var = HPOFacade(
        scenario,
        model.train,
        overwrite=True,
        intensifier=intensifier_obj,
        initial_design=initial_design_obj,
        callbacks=[CustomCallback()],
        logging_level=999999,
    )
    incumbent = smac_var.optimize()

    print(incumbent.get_dictionary())
    
if __name__ == "__main__":
    default_path = os.path.abspath(__file__ + "/../")
    root = os.path.abspath(__file__ + "/../../../")
    xml = os.path.join(root, "References\\LapTimer\\F218\\Bahrain\\parametersAfterSetup12.xml")
    
    #high_level_management()
    main()


from csv import reader, DictReader
import re
from xml.dom.minidom import Element 
import xml.etree.ElementTree as ET
import yaml
import json
import numpy as np
from yaml.loader import SafeLoader
from subprocess import DEVNULL, STDOUT, check_call
import numpy as np
from copy import copy
import os
import random

# Function to parse a file quickly and perform data transformations
def fast_parse(file_path, fast_parse_exe, alias, mat):
    # Executes an external program to generate a JSON file from the input file
    check_call(fast_parse_exe + " " + file_path, stdout=DEVNULL, stderr=STDOUT)
    
    # Path to the generated JSON file
    jreference3 = file_path[:-3] + "json"
    
    # Opening the generated JSON file and loading its content into a Python dictionary
    with open(jreference3) as f:
        data = json.load(f)
    
    # Translating keys in the dictionary based on provided alias and mat parameters
    data_ref_trans_laptimer = dictTransJSON(data, alias, mat)
    
    return data_ref_trans_laptimer


# Function to perform dictionary key translations and data transformations
def dictTransJSON(Dict, alias, mat):
    result = {}
    translation = {}

    # Iterating through keys in the input dictionary
    for each in Dict:
        new_key = each
        
        # Removing certain patterns from the keys
        new_key = re.sub("[\(\[].*?[\)\]]", "", new_key)
        
        # Translating keys based on the provided alias mapping
        if new_key in alias:
            new_key = alias[new_key]
        
        translation[each] = new_key
    
    # Converting values to NumPy arrays for specific keys in the dictionary
    for each in translation:
        result[translation[each]] = np.array(Dict[each])
    
    # Applying custom logic ('mat') to generate and update new key-value pairs in the dictionary
    if mat is not None:
        for mat_key in mat:
            cond = mat[mat_key]
            origins = []
            
            # Finding keys that match certain conditions specified in 'mat'
            for each in result:
                if cond.find(each) > -1:
                    origins.append(each)
            
            # Modifying the conditions based on found keys
            for each in origins:
                temp = cond.replace(each, "result['" + each + "']")
                cond = temp
            
            # Evaluating the modified condition and updating the dictionary
            arr = eval(cond)
            result[mat_key] = arr
    
    return result


# Function to parse a specific type of CSV file
def PiTecParsing(path):
    with open(path, 'r') as read_obj:
        # Skipping the first 18 rows
        for _ in range(18):
            _ = next(read_obj)
        
        # Reading the file using csv.DictReader
        csv_dict_reader = DictReader(read_obj, delimiter='\t')
        return list(csv_dict_reader)


def dictTrans(Dict, alias, mat):
    result = {}         # Dictionary to store the transformed data
    translation = {}    # Dictionary to hold the translation of keys
    
    # Iterate through each dictionary in the input list 'Dict'
    for each in Dict:
        if not result:  # If the 'result' dictionary is empty
            # Handle keys and values for the initial dictionary
            for key in each:
                new_key = key
                new_key = re.sub("[\(\[].*?[\)\]]", "", new_key)  # Remove certain patterns from keys
                if new_key in alias:
                    new_key = alias[new_key]  # Translate keys based on the provided alias mapping
                translation[key] = new_key  # Store translation for future reference
                
                new_list = []
                # Convert values to float and handle None values
                if each[key] is None:
                    new_list.append(0.0)
                else:
                    new_list.append(float(each[key]))
                
                result[new_key] = new_list  # Store the transformed key-value pair
                
                # Apply custom logic ('mat') to generate and update new key-value pairs in the dictionary
                if mat is not None:
                    for mat_key in mat:
                        new_list = []
                        cond = mat[mat_key]
                        for key in result:
                            if key:
                                temp = cond.replace(key, str(result[key][-1]))  # Replace keys in the condition
                                cond = temp
                        value = eval(cond)  # Evaluate the condition and get the value
                        new_list.append(value)
                        result[mat_key] = new_list  # Store the new value in the result dictionary
        else:
            tick = {}
            # Handle keys and values after the first iteration
            for key in each:
                if each[key] is not None:
                    if translation[key] not in tick:
                        result[translation[key]].append(float(each[key]))  # Append values for existing keys
                        tick[translation[key]] = True
            
            # Apply custom logic ('mat') to generate and update new key-value pairs in the dictionary
            if mat is not None:
                for mat_key in mat:
                    cond = mat[mat_key]
                    for key in result:
                        if key:
                            temp = cond.replace(key, str(result[key][-1]))  # Replace keys in the condition
                            cond = temp
                    value = eval(cond)  # Evaluate the condition and get the value
                    result[mat_key].append(value)  # Append the new value to the result dictionary
    
    return result  # Return the transformed dictionary


def subtractSquareCost(listOne, listTwo):
    cost = 0.0  # Initialize the cost to 0
    
    # Sort both input lists in ascending order based on the first element of each tuple
    listOne.sort()
    listTwo.sort()
    
    indexOne = 0  # Initialize index for listOne
    indexTwo = 0  # Initialize index for listTwo
    
    # Iterate through each element of listOne using enumeration (provides index and value)
    for indexOne, valueOne in enumerate(listOne):
        # While the end of the dataset wasnt reached
        while indexTwo < len(listTwo):
            valueTwo = listTwo[indexTwo]  # Get the value from listTwo at the current index
            
            # Check if the value in listOne is less or equal than the value in listTwo
            if valueOne[0] <= valueTwo[0]:
                if indexTwo > 0:
                    # Calculate the difference between the second elements of the tuples and square it
                    sub = valueOne[1] - valueTwo[1]
                    cost += sub ** 2  # Add the squared difference to the cost
                break  # Break out of the while loop
            else:
                indexTwo += 1  # Move to the next element in listTwo
        
    return cost  # Return the total cost calculated

def subtractSquareCostInterp(listOne, listTwo):
    cost = 0.0  # Initialize the cost to 0
    
    # Sort both input lists in ascending order based on the first element of each tuple
    listOne.sort()
    listTwo.sort()
    
    indexOne = 0  # Initialize index for listOne
    indexTwo = 0  # Initialize index for listTwo
    # Iterate through each element of listOne using enumeration (provides index and value)
    for indexOne, valueOne in enumerate(listOne):
        # While the end of the dataset wasnt reached
        while indexTwo<len(listTwo):
            valueTwo = listTwo[indexTwo] # Get the value from listTwo at the current index
            
            # Check if the value in listOne is less or equal than the value in listTwo
            if(valueOne[0]<=valueTwo[0]):
                if indexTwo>0:
                    x1 = listTwo[indexTwo-1][0]
                    x2 = listTwo[indexTwo][0]  
                    y1 = listTwo[indexTwo-1][1]  
                    y2 = listTwo[indexTwo][1]  
                    x = listOne[indexOne][0]
                    # Compute the linearly intepolated value of the function
                    y = (((y2-y1)*(x-x1))/(x2-x1))+y1
                    sub = listOne[indexOne][1]-y
                    cost += sub**2 # Add the squared difference to the cost
                break
            else:
                indexTwo += 1  # Move to the next element in listTwo
    return cost # Return the total cost calculated

def subtractSquareCostRegres(listOne, listTwo):
    cost = 0.0  # Initialize the cost to 0
    # This function returns the linearly regressed dataset
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

    # Looking for a boundaries in listOne, since we are going to iterate through it
    N_max = max(listOne,key=lambda item:item[0])[0]
    N_min = min(listOne,key=lambda item:item[0])[0]

    # Compute the equal step per iteration
    step = (N_max-N_min)/len(listOne)

    # Iterate through the dataset
    for x in np.arange(N_min, N_max, step):
        sub = regressOne(x)-regressTwo(x)
        cost += sub**2 # Add the squared difference to the cost
    return cost

def subtractSquareCostLowPass(listOne, listTwo):
    cost = 0.0  # Initialize the cost to 0
    
    # Sort both input lists in ascending order based on the first element of each tuple
    listOne.sort()
    listTwo.sort()
    
    indexOne = 0  # Initialize index for listOne
    indexTwo = 0  # Initialize index for listTwo

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

def get_xml_param_list(path):
    tree = ET.parse(path)
    root = tree.getroot()
    param_list = []
    for each in root.findall('*'):
        for subeach in each.findall('*'):
            param_list.append(subeach.tag)
    return param_list



class XMLFacade:
    def __init__(self, path: str):
        self.path = path
        self.readroot = ET.parse(path).getroot()
        self.tree = ET.parse(path)
        
    def xmlMetaWriting(self, name, position, value):     
        def round_to_square(in_position):
            numbers = in_position[1:-1]
            result = "["+numbers.replace(",", "][")+"]"
            return result
        
        matrix_as_text = ""
        for param in self.tree.getroot().iter(name):
            matrix_as_text = param[1].text
            break
        if not matrix_as_text:
            raise Exception("There is no such parameter in xml file!")
        matrix_text = np.matrix(matrix_as_text)
        command = "matrix_text.A"+round_to_square(position)+"=value"
        exec(command)
        updated_value = mat2str(matrix_text)
        if matrix_text.size == 1:
            updated_value = str(value)
        for param in self.tree.getroot().iter(name):
            param[1].text = updated_value
            break

    def xmlMetaReading(self, name, position):
        matrix_as_text = ""
        for param in self.readroot.iter(name):
            matrix_as_text = param[1].text
            break
        if not matrix_as_text:
            raise Exception("There is no such parameter in xml file!")
        matrix_text = np.matrix(matrix_as_text)
        value = eval("matrix_text.item"+position)
        return value

    def write_to_file(self):
        self.readroot = copy(self.tree.getroot())
        self.tree.write(self.path)


