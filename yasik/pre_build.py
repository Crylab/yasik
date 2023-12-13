#!/usr/bin/env python
import subprocess
import os
from copy import copy
command = "./gradlew" if os.name == "posix" else "gradlew.bat"
subprocess.run([command, "generateGrammarSource"])

# Tests generation
test_sequence_reading_one_slice = {
                 "var":                  "var",
                 "var1":                 "var1",
                 # Without slices
                 "lar":                  "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:1, 0:1)')",
                 # With one slice
                 "lar(5)":               "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:6, 0:1)')",
                 "lar(5:16)":            "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:16, 0:1)')",
                 "lar(5:)":              "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:210, 0:1)')",                 
                 "lar(:5)":              "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:5, 0:1)')",
                 "lar(:)":               "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:210, 0:1)')",

                 # The same with category
                 "cat.lar":              "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:1, 0:1)')",
                 "cat.lar(5)":           "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 0:1)')",
                 "cat.lar(5:16)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 0:1)')",
                 "cat.lar(5:)":          "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 0:1)')",                 
                 "cat.lar(:5)":          "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:5, 0:1)')",
                 "cat.lar(:)":           "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 0:1)')",
                                    }

test_sequence_reading_two_slices_without_category = {
                 # With two slices
                 "lar(5, 6)":            "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:6, 6:7)')",
                 "lar(5, 6:16)":         "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:6, 6:16)')",
                 "lar(5, 6:)":           "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:6, 6:215)')",                 
                 "lar(5, :16)":          "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:6, 0:16)')",
                 "lar(5, :)":            "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:6, 0:215)')",

                 "lar(5:16, 6)":         "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:16, 6:7)')",
                 "lar(5:16, 6:16)":      "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:16, 6:16)')",
                 "lar(5:16, 6:)":        "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:16, 6:215)')",                 
                 "lar(5:16, :16)":       "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:16, 0:16)')",
                 "lar(5:16, :)":         "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:16, 0:215)')",
                 
                 "lar(5:, 6)":           "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:210, 6:7)')",
                 "lar(5:, 6:16)":        "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:210, 6:16)')",
                 "lar(5:, 6:)":          "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:210, 6:215)')",                 
                 "lar(5:, :16)":         "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:210, 0:16)')",
                 "lar(5:, :)":           "self.xmlManager.xmlMetaReading(xml, 'lar', '(5:210, 0:215)')",

                 "lar(:6, 6)":           "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:6, 6:7)')",
                 "lar(:6, 6:16)":        "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:6, 6:16)')",
                 "lar(:6, 6:)":          "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:6, 6:215)')",                 
                 "lar(:6, :16)":         "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:6, 0:16)')",
                 "lar(:6, :)":           "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:6, 0:215)')",
                 "lar(:, 6)":            "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:210, 6:7)')",
                 "lar(:, 6:16)":         "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:210, 6:16)')",
                 "lar(:, 6:)":           "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:210, 6:215)')",                 
                 "lar(:, :16)":          "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:210, 0:16)')",
                 "lar(:, :)":            "self.xmlManager.xmlMetaReading(xml, 'lar', '(0:210, 0:215)')",
                                                }

test_sequence_reading_two_slices_with_category = {
                 # With two slices
                 "cat.lar(5, 6)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 6:7)')",
                 "cat.lar(5, 6:16)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 6:16)')",
                 "cat.lar(5, 6:)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 6:215)')",                 
                 "cat.lar(5, :16)":      "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 0:16)')",
                 "cat.lar(5, :)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 0:215)')",

                 "cat.lar(5:16, 6)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 6:7)')",
                 "cat.lar(5:16, 6:16)":  "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 6:16)')",
                 "cat.lar(5:16, 6:)":    "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 6:215)')",                 
                 "cat.lar(5:16, :16)":   "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 0:16)')",
                 "cat.lar(5:16, :)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 0:215)')",

                 "cat.lar(5:, 6)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 6:7)')",
                 "cat.lar(5:, 6:16)":    "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 6:16)')",
                 "cat.lar(5:, 6:)":      "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 6:215)')",                 
                 "cat.lar(5:, :16)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 0:16)')",
                 "cat.lar(5:, :)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 0:215)')",

                 "cat.lar(:6, 6)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 6:7)')",
                 "cat.lar(:6, 6:16)":    "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 6:16)')",
                 "cat.lar(:6, 6:)":      "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 6:215)')",                 
                 "cat.lar(:6, :16)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 0:16)')",
                 "cat.lar(:6, :)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 0:215)')",

                 "cat.lar(:, 6)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 6:7)')",
                 "cat.lar(:, 6:16)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 6:16)')",
                 "cat.lar(:, 6:)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 6:215)')",                 
                 "cat.lar(:, :16)":      "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 0:16)')",
                 "cat.lar(:, :)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 0:215)')",
                                                }

test_sequence_reading_two_slices_with_category = {
                 # With two slices
                 "cat.lar(5, 6)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 6:7)')",
                 "cat.lar(5, 6:16)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 6:16)')",
                 "cat.lar(5, 6:)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 6:215)')",                 
                 "cat.lar(5, :16)":      "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 0:16)')",
                 "cat.lar(5, :)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:6, 0:215)')",

                 "cat.lar(5:16, 6)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 6:7)')",
                 "cat.lar(5:16, 6:16)":  "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 6:16)')",
                 "cat.lar(5:16, 6:)":    "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 6:215)')",                 
                 "cat.lar(5:16, :16)":   "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 0:16)')",
                 "cat.lar(5:16, :)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:16, 0:215)')",

                 "cat.lar(5:, 6)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 6:7)')",
                 "cat.lar(5:, 6:16)":    "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 6:16)')",
                 "cat.lar(5:, 6:)":      "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 6:215)')",                 
                 "cat.lar(5:, :16)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 0:16)')",
                 "cat.lar(5:, :)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(5:210, 0:215)')",

                 "cat.lar(:6, 6)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 6:7)')",
                 "cat.lar(:6, 6:16)":    "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 6:16)')",
                 "cat.lar(:6, 6:)":      "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 6:215)')",                 
                 "cat.lar(:6, :16)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 0:16)')",
                 "cat.lar(:6, :)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:6, 0:215)')",

                 "cat.lar(:, 6)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 6:7)')",
                 "cat.lar(:, 6:16)":     "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 6:16)')",
                 "cat.lar(:, 6:)":       "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 6:215)')",                 
                 "cat.lar(:, :16)":      "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 0:16)')",
                 "cat.lar(:, :)":        "self.xmlManager.xmlMetaReading(xml, 'cat.lar', '(0:210, 0:215)')",
                                                }

test_sequence_writing = {
                 "var1 = "


                        }

'''
test_sequence = [
                "lar += cat.lar(5:)", 
                "lar = cat.lar(5:)",
                "lar = lar(1,2); lar(1,1) = lar(1,3)",
                "var1 = lar(1,2); lar(1,1) = var1"]
'''


print("Testing code generation initialization")

def test_file_generation(name: str, dict: dict):
    with open("./tests/test_generated/"+name+".py", 'w+') as file:
        preambula = "#Automatically generated test file\nimport sys\nimport pytest\nsys.path.insert(1, '../')\nfrom yasik.yasik_interpreter import yasik_compiler\n\n"    
        test_code = "def test_TEST_NUMBER():\n\tinput_code = \"INPUT_CODE\"\n\texpected_code = \"EXPECTED_CODE\"\n\tresult = yasik_compiler(input_code)\n\tif result != expected_code:\n\t\traise Exception(\"The input code:\\t\\t\"+input_code+\"\\nThe gotten result:\\t\\t\\t\"+result+\"\\nThe expected result:\\t\\t\\t\"+expected_code)\n\n\n"
        tests = ""
        for test_number, (input_code, expected_code) in enumerate(dict.items()):
            current_test = test_code.replace("TEST_NUMBER", str(test_number))
            current_test = current_test.replace("INPUT_CODE", input_code)
            current_test = current_test.replace("EXPECTED_CODE", expected_code)
            tests += current_test
        file.write(preambula+tests)
    print("Testing code file "+name+" was sucessfully generated")

test_file_generation("test_sequence_reading_one_slice", test_sequence_reading_one_slice)
test_file_generation("test_sequence_reading_two_slices_without_category", test_sequence_reading_two_slices_without_category)
test_file_generation("test_sequence_reading_two_slices_with_category", test_sequence_reading_two_slices_with_category)


print("Testing code was sucessfully generated")
    

