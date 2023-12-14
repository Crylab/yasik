#!/usr/bin/env python
import subprocess
import os
import yaml


from copy import copy
command = "./gradlew" if os.name == "posix" else "gradlew.bat"
subprocess.run([command, "generateGrammarSource"])

# Tests generation

print("Testing code generation initialization")
counter = 0
def test_file_generation(name: str, dict: dict):
    if name:
        with open("./tests/test_generated/"+name+".py", 'w+') as file:
            global counter
            preambula = "#Automatically generated test file\nimport sys\nimport pytest\nsys.path.insert(1, '../')\nfrom yasik.yasik_interpreter import yasik_compiler\n\n"    
            test_code = "def test_TEST_NUMBER():\n\tinput_code = \"INPUT_CODE\"\n\texpected_code = \"EXPECTED_CODE\"\n\tresult = yasik_compiler(input_code)\n\tif result != expected_code:\n\t\traise Exception(\"The input code:\\t\\t\"+input_code+\"\\nThe gotten result:\\t\\t\\t\"+result+\"\\nThe expected result:\\t\\t\\t\"+expected_code)\n\n\n"
            tests = ""
            for test_number, (input_code, expected_code) in enumerate(dict.items()):
                current_test = test_code.replace("TEST_NUMBER", str(counter+test_number))
                current_test = current_test.replace("INPUT_CODE", input_code)
                current_test = current_test.replace("EXPECTED_CODE", expected_code)
                tests += current_test
            file.write(preambula+tests)
            counter += test_number+1
        print("Testing code file "+name+" was sucessfully generated")


with open("./tests/testing_data.yaml", "r") as stream:
    try:
        categories = yaml.safe_load(stream)
        for each in categories:
            test_file_generation(each, categories[each])
    except yaml.YAMLError as exc:
        print(exc)

print("Testing code was sucessfully generated")   
