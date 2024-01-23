#!/usr/bin/env python
import subprocess
import os
import yaml
from copy import copy
command = "./gradlew" if os.name == "posix" else "gradlew.bat"
subprocess.run([command, "generateGrammarSource"])

## Tests generation
print("Testing code generation initialization")
# Make generation folder
try:  
    os.mkdir("./tests/test_generated/")
except OSError as error:  
    print(error) 
    
val = os.system("copy \".\\tests\\test_sample.xml\" \".\\tests\\test_generated\\test_sample.xml\"")
val = os.system("copy \".\\tests\\fake_simulation.py\" \".\\tests\\test_generated\\fake_simulation.py\"")

counter = 0

def test_sequential_file_generation(name: str, dict: dict, preambula, test_code):
    if name:
        with open("./tests/test_generated/"+name+".py", 'w+') as file:
            global counter
            tests = ""
            for test_number, (input_code, expected_code) in enumerate(dict.items()):
                current_test = test_code.replace("TEST_NUMBER", str(counter+test_number))
                current_test = current_test.replace("INPUT_CODE", str(input_code))
                current_test = current_test.replace("EXPECTED_CODE", str(expected_code))
                tests += current_test
            file.write(preambula+tests)
            counter += test_number+1
        print("Testing code file "+name+".py was sucessfully generated")

preambula_seq = "#Automatically generated test file\nimport sys\nimport pytest\nsys.path.insert(1, '../')\nfrom yasik.yasik_interpreter import yasik_compiler\n\n"    
test_code_seq = "def test_TEST_NUMBER():\n\tinput_code = \"INPUT_CODE\"\n\texpected_code = \"EXPECTED_CODE\"\n\tresult = yasik_compiler(input_code, {\"lar\": (210, 215)})\n\tif result != expected_code:\n\t\traise Exception(\"The input code:\\t\\t\"+input_code+\"\\nThe gotten result:\\t\\t\\t\"+result+\"\\nThe expected result:\\t\\t\\t\"+expected_code)\n\n\n"
preambula_int = "#Automatically generated test file\nimport sys\nimport os\nimport pytest\nsys.path.insert(1, '../')\nfrom yasik.yasik_interpreter import yasik_compiler\nimport fake_simulation\n\n"
test_code_int = "def test_TEST_NUMBER():\n\tinput_code = \"INPUT_CODE\"\n\texpected_code = \"EXPECTED_CODE\"\n\tscript_dir = os.path.dirname(os.path.abspath(__file__))\n\tfile_path = os.path.join(script_dir, \"test_sample.xml\")\n\tmatlab_code = yasik_compiler(input_code, fake_simulation.get_xml_param_dict(file_path))\n\tobj = fake_simulation.Test_Simulation(file_path)\n\tresult = obj.execute_meta_code(matlab_code)\n\tif str(result) != expected_code:\n\t\traise Exception(\"The input code:\\t\\t\"+input_code+\"\\nThe gotten result:\\t\\t\\t\"+str(result)+\"\\nThe expected result:\\t\\t\\t\"+expected_code)\n\n\n"
test_code_wrt = "def test_TEST_NUMBER():\n\tinput_code = \"INPUT_CODE\"\n\texpected_code = \"EXPECTED_CODE\"\n\tscript_dir = os.path.dirname(os.path.abspath(__file__))\n\tfile_path = os.path.join(script_dir, \"test_sample.xml\")\n\tmatlab_code = yasik_compiler(input_code, fake_simulation.get_xml_param_dict(file_path))\n\tname=input_code.split(\"(\")\n\treading_code = yasik_compiler(name[0]+\"(:, :)\", fake_simulation.get_xml_param_dict(file_path))\n\tobj = fake_simulation.Test_Simulation(file_path)\n\tresult_before = obj.execute_meta_code(reading_code)\n\t_ = obj.execute_meta_code(matlab_code)\n\tobj.xmlManager.write_to_file()\n\tresult_after = obj.execute_meta_code(reading_code)\n\tobj.xmlManager.restore_backup()\n\tif str(result_after) == str(result_before):\n\t\traise Exception(\"The input code:\t\t\"+input_code+\" doesnt cause any changes in XML file\")\n\tif str(result_after) != expected_code:\n\t\traise Exception(\"The input code:\\t\\t\"+input_code+\"\\nThe gotten result:\\t\\t\\t\"+str(result_after)+\"\\nThe expected result:\\t\\t\\t\"+expected_code)\n\n\n"

with open("./tests/testing_data.yaml", "r") as stream:
    try:
        categories = yaml.safe_load(stream)
        for each in categories:
            test_sequential_file_generation(each, categories[each], preambula_seq, test_code_seq)
    except yaml.YAMLError as exc:
        print(exc)

with open("./tests/testing_sample_data.yaml", "r") as stream:
    try:
        categories = yaml.safe_load(stream)
        for each in categories:
            test_sequential_file_generation(each, categories[each], preambula_int, test_code_int)
    except yaml.YAMLError as exc:
        print(exc)

with open("./tests/testing_sample_data_writing.yaml", "r") as stream:
    try:
        categories = yaml.safe_load(stream)
        for each in categories:
            test_sequential_file_generation(each, categories[each], preambula_int, test_code_wrt)
    except yaml.YAMLError as exc:
        print(exc)

print("Testing code was sucessfully generated")
