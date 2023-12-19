import xml.etree.ElementTree as ET
import numpy as np
import os
import yaml
from copy import copy

def mat2str(matrix):
    if matrix.size == 1:
        return str(matrix.item(0))
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

class XMLFacade:
    def __init__(self, path: str):
        self.path = path
        self.readroot = ET.parse(path).getroot()
        self.tree = ET.parse(path)
        
    def xmlMetaWriting(self, name, position, value):  
        matrix_as_text = ""
        for param in self.tree.getroot().iter(name):
            matrix_as_text = param[1].text
            break
        if not matrix_as_text:
            raise Exception("There is no such parameter in xml file!")
        matrix_text = np.matrix(matrix_as_text)
        command = "matrix_text["+position[1:-1]+"]=value"        
        exec(command)
        updated_value = mat2str(matrix_text)        
        for param in self.tree.getroot().iter(name):
            param[1].text = updated_value

    def xmlMetaReading(self, name, position):
        matrix_as_text = ""
        for param in self.readroot.iter(name):
            matrix_as_text = param[1].text
            break
        if not matrix_as_text:
            raise Exception("There is no such parameter in xml file!")
        matrix_text = np.matrix(matrix_as_text)

        value = eval("matrix_text"+"["+position[1:-1]+"]")

        '''
        slices = position[1:-1].split(",")
        left_slice = slices[0].split(":")
        right_slice = slices[1].split(":")
        value = 0
        for each in range(int(left_slice[0]), int(left_slice[1])):
            for every in range(int(right_slice[0]), int(right_slice[1])):
                current_position = "("+str(each)+", "+str(every)+")"
                value += eval("matrix_text.item"+current_position)
        '''
        return value

    def write_to_file(self):
        self.readroot = copy(self.tree.getroot())
        self.tree.write(self.path)

def get_xml_param_list(path):
    tree = ET.parse(path)
    root = tree.getroot()
    param_list = []
    for each in root.findall('*'):
        for subeach in each.findall('*'):
            param_list.append(subeach.tag)
    return param_list

def get_xml_param_dict(path):
    tree = ET.parse(path)
    root = tree.getroot()
    param_dict = {}
    for each in root.findall('*'):
        for subeach in each.findall('*'):
            for value in subeach.findall('value'):
                m = np.matrix(value.text)
                shape = m.shape
                param_dict[subeach.tag] = shape
    return param_dict

class Test_Simulation:
    def __init__(self, xml) -> None:          
        self.xmlManager = XMLFacade(xml)

    def execute_meta_code(self, matlab_input: str):
        value = None
        try:
            value = mat2str(eval(matlab_input))
        except:
            exec(matlab_input)
        return value


    