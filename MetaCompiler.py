'''
                 .-.
                (   )
                 '-'
                 J L
                 | |
                J   L
                |   |
               J     L
             .-'.___.'-.
            /___________\
       _.-""'           `bmw._
     .'                       `.
   J                            `.
  F                               L
 J                                 J
J                                  `
|                                   L
|                                   |
|                                   |
|                                   J
|                                    L
|                                    |
|             ,.___          ___....--._
|           ,'     `""""""""'           `-._
|          J           _____________________`-.
|         F         .-'   `-88888-'    `Y8888b.`.
|         |       .'         `P'         `88888b \
|         |      J       #     L      #    q8888b L
|         |      |             |           )8888D )
|         J      \             J           d8888P P
|          L      `.         .b.         ,88888P /
|           `.      `-.___,o88888o.___,o88888P'.'
|             `-.__________________________..-'
|                                    |
|         .-----.........____________J
|       .' |       |      |       |
|      J---|-----..|...___|_______|
|      |   |       |      |       |
|      Y---|-----..|...___|_______|
|       `. |       |      |       |
|         `'-------:....__|______.J
|                                  |
 L___                              |
     """----...______________....--'

                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                        
MMMMMMMM               MMMMMMMM                                                                                                                            AAA               NNNNNNNN        NNNNNNNNTTTTTTTTTTTTTTTTTTTTTTTLLLLLLLLLLL             RRRRRRRRRRRRRRRRR   
M:::::::M             M:::::::M                                                                                                                           A:::A              N:::::::N       N::::::NT:::::::::::::::::::::TL:::::::::L             R::::::::::::::::R  
M::::::::M           M::::::::M                                                                                                                          A:::::A             N::::::::N      N::::::NT:::::::::::::::::::::TL:::::::::L             R::::::RRRRRR:::::R 
M:::::::::M         M:::::::::M                                                                                                                         A:::::::A            N:::::::::N     N::::::NT:::::TT:::::::TT:::::TLL:::::::LL             RR:::::R     R:::::R
M::::::::::M       M::::::::::Myyyyyyy           yyyyyyy        ooooooooooo wwwwwww           wwwww           wwwwwwwnnnn  nnnnnnnn                    A:::::::::A           N::::::::::N    N::::::NTTTTTT  T:::::T  TTTTTT  L:::::L                 R::::R     R:::::R
M:::::::::::M     M:::::::::::M y:::::y         y:::::y       oo:::::::::::oow:::::w         w:::::w         w:::::w n:::nn::::::::nn                 A:::::A:::::A          N:::::::::::N   N::::::N        T:::::T          L:::::L                 R::::R     R:::::R
M:::::::M::::M   M::::M:::::::M  y:::::y       y:::::y       o:::::::::::::::ow:::::w       w:::::::w       w:::::w  n::::::::::::::nn               A:::::A A:::::A         N:::::::N::::N  N::::::N        T:::::T          L:::::L                 R::::RRRRRR:::::R 
M::::::M M::::M M::::M M::::::M   y:::::y     y:::::y        o:::::ooooo:::::o w:::::w     w:::::::::w     w:::::w   nn:::::::::::::::n             A:::::A   A:::::A        N::::::N N::::N N::::::N        T:::::T          L:::::L                 R:::::::::::::RR  
M::::::M  M::::M::::M  M::::::M    y:::::y   y:::::y         o::::o     o::::o  w:::::w   w:::::w:::::w   w:::::w      n:::::nnnn:::::n            A:::::A     A:::::A       N::::::N  N::::N:::::::N        T:::::T          L:::::L                 R::::RRRRRR:::::R 
M::::::M   M:::::::M   M::::::M     y:::::y y:::::y          o::::o     o::::o   w:::::w w:::::w w:::::w w:::::w       n::::n    n::::n           A:::::AAAAAAAAA:::::A      N::::::N   N:::::::::::N        T:::::T          L:::::L                 R::::R     R:::::R
M::::::M    M:::::M    M::::::M      y:::::y:::::y           o::::o     o::::o    w:::::w:::::w   w:::::w:::::w        n::::n    n::::n          A:::::::::::::::::::::A     N::::::N    N::::::::::N        T:::::T          L:::::L                 R::::R     R:::::R
M::::::M     MMMMM     M::::::M       y:::::::::y            o::::o     o::::o     w:::::::::w     w:::::::::w         n::::n    n::::n         A:::::AAAAAAAAAAAAA:::::A    N::::::N     N:::::::::N        T:::::T          L:::::L         LLLLLL  R::::R     R:::::R
M::::::M               M::::::M        y:::::::y             o:::::ooooo:::::o      w:::::::w       w:::::::w          n::::n    n::::n        A:::::A             A:::::A   N::::::N      N::::::::N      TT:::::::TT      LL:::::::LLLLLLLLL:::::LRR:::::R     R:::::R
M::::::M               M::::::M         y:::::y              o:::::::::::::::o       w:::::w         w:::::w           n::::n    n::::n       A:::::A               A:::::A  N::::::N       N:::::::N      T:::::::::T      L::::::::::::::::::::::LR::::::R     R:::::R
M::::::M               M::::::M        y:::::y                oo:::::::::::oo         w:::w           w:::w            n::::n    n::::n      A:::::A                 A:::::A N::::::N        N::::::N      T:::::::::T      L::::::::::::::::::::::LR::::::R     R:::::R
MMMMMMMM               MMMMMMMM       y:::::y                   ooooooooooo            www             www             nnnnnn    nnnnnn     AAAAAAA                   AAAAAAANNNNNNNN         NNNNNNN      TTTTTTTTTTT      LLLLLLLLLLLLLLLLLLLLLLLLRRRRRRRR     RRRRRRR
                                     y:::::y                                                                                                                                                                                                                            
                                    y:::::y                                                                                                                                                                                                                             
                                   y:::::y                                                                                                                                                                                                                              
                                  y:::::y                                                                                                                                                                                                                               
                                 yyyyyyy                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                        


'''

import unittest
import numpy as np
import copy


    

def meta_compiler(matlab_input: str) -> str:

    def reading_command(param_list, string: str):
        result = copy.copy(string.replace("update", "value_script_update"))
        for each in param_list:
            if each in string:
                result = result.replace(each, "lib.xmlMetaReading(xml,'"+each+"','")+"')"
        return result

    def writing_command(param_list, string: str, value):
        result = copy.copy(string)
        for each in param_list:
            if each in string:
                result = result.replace(each, "lib.xmlMetaWriting(xml,"+each+",'")+"', "+value+")"
                return result

    result = ""
    param_array = ["gearTableRatio", "WindTunnelDataLeft"]
    no_spaces = matlab_input.strip()
    lines = no_spaces.split(";")
    for each in lines:
        if each == "":
            continue
        if "=" in each:
            parts = each.split("=")
            if len(parts) != 2:
                raise Exception("The command cannot content more than one '=' symbol.")
            [left, right] = parts
            result += writing_command(param_array, left, reading_command(param_array, right)) + ";"
        else:
            result = reading_command(param_array, each) + ";"    
    return result


# The test based on unittest module
class TestGetAreaRectangle(unittest.TestCase):
    def test_no_spaces(self):
        self.assertEqual(meta_compiler("gearTableRatio(0,5); "), "gearTableRatio(0,5);", "Test: no spaces was failed!")
        
    def test_no_tabs(self):
        self.assertEqual(meta_compiler("gearTableRatio(0,5);\t"), "gearTableRatio(0,5);", "Test: no tabs was failed!")
                
    def test_no_new_lines(self):
        self.assertEqual(meta_compiler("gearTableRatio(0,5);\n"), "gearTableRatio(0,5);", "Test: no new lines was failed!")
 

def test_function(arg1, arg2, arg3=None):
    print(arg1)
    print(arg2)
    print(arg3)

if __name__ == '__main__':
    test_function("one", "two", )
    one = "WindTunnelDataLeft(0, 5); "
    two = "WindTunnelDataLeft(0, 5) = WindTunnelDataLeft(0, 5) + update - WindTunnelDataLeft(0, 5); WindTunnelDataLeft(1, 5) = WindTunnelDataLeft(1, 5) + update - WindTunnelDataLeft(0, 5); WindTunnelDataLeft(2, 5) = WindTunnelDataLeft(2, 5) + update - WindTunnelDataLeft(0, 5); WindTunnelDataLeft(3, 5) = WindTunnelDataLeft(3, 5) + update - WindTunnelDataLeft(0, 5);"
    print("Compile this: "+two+" \n To this: "+meta_compiler(two))
    print("Hi!")
    #unittest.main()

