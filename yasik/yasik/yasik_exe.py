#!/usr/bin/env python3

from antlr4 import *
from yasik_interpreter import YasikEvaluator

def main():
    print("Hey!!!!")
    for expression in ["lar", 
                       "lar(5)", 
                       "lar(5,6)", 
                       "cat.lar", 
                       "cat.lar(5)", 
                       "cat.lar(5,6)", 
                       "lar(5:16)", 
                       "lar(5:16,7:18)", 
                       "cat.lar(5:16)", 
                       "cat.lar(5:16,7:18)", 
                       "lar(5:)", 
                       "lar(5:,7:)", 
                       "cat.lar(5:)", 
                       "cat.lar(5:,7:)", 
                       "lar(:16)", 
                       "lar(:16,:18)",                        
                       "cat.lar(:16)", 
                       "cat.lar(:16,:18)",
                       "lar += cat.lar(5:)", 
                       "lar = cat.lar(5:)",
                       "lar = lar(1,2); lar(1,1) = lar(1,3)",
                       "var1 = lar(1,2); lar(1,1) = var1"]:
    #expression = input("Enter an expression: ")
        input_stream = InputStream(expression)
    #lexer = CalcLexer(input_stream)
        lexer = YasikLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = YasikParser(token_stream)
        evaluator = YasikEvaluator()
        parser.addParseListener(evaluator)
        tree = parser.code()
        print(tree.toStringTree(recog=parser))
    #calc_evaluator = CalcEvaluator()
    #CalcEvaluator.stack = tree
    #calc_evaluator.exitExpr(tree)
    #val = calc_evaluator.getValue()

if __name__ == '__main__':
    main()