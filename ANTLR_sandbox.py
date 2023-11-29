#!/usr/bin/env python3

from antlr4 import *
from CalcLexer import CalcLexer
from CalcParser import CalcParser
from calc_evaluator import CalcEvaluator

def main():
    print("Hey!!!!")
    for expression in ["lar(15, 1)+5*8"]:
    #expression = input("Enter an expression: ")
        input_stream = InputStream(expression)
    #lexer = CalcLexer(input_stream)
        lexer = CalcLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = CalcParser(token_stream)
        evaluator = CalcEvaluator()
        parser.addParseListener(evaluator)
        tree = parser.start()
        print(evaluator.getValue())
        print(tree.toStringTree(recog=parser))
    #calc_evaluator = CalcEvaluator()
    #CalcEvaluator.stack = tree
    #calc_evaluator.exitExpr(tree)
    #val = calc_evaluator.getValue()

if __name__ == '__main__':
    main()