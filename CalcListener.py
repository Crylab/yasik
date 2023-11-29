# Generated from Calc.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CalcParser import CalcParser
else:
    from CalcParser import CalcParser

# This class defines a complete listener for a parse tree produced by CalcParser.
class CalcListener(ParseTreeListener):

    # Enter a parse tree produced by CalcParser#start.
    def enterStart(self, ctx:CalcParser.StartContext):
        pass

    # Exit a parse tree produced by CalcParser#start.
    def exitStart(self, ctx:CalcParser.StartContext):
        pass


    # Enter a parse tree produced by CalcParser#assignment.
    def enterAssignment(self, ctx:CalcParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CalcParser#assignment.
    def exitAssignment(self, ctx:CalcParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CalcParser#arithmeticExpr.
    def enterArithmeticExpr(self, ctx:CalcParser.ArithmeticExprContext):
        pass

    # Exit a parse tree produced by CalcParser#arithmeticExpr.
    def exitArithmeticExpr(self, ctx:CalcParser.ArithmeticExprContext):
        pass


    # Enter a parse tree produced by CalcParser#term.
    def enterTerm(self, ctx:CalcParser.TermContext):
        pass

    # Exit a parse tree produced by CalcParser#term.
    def exitTerm(self, ctx:CalcParser.TermContext):
        pass


    # Enter a parse tree produced by CalcParser#factor.
    def enterFactor(self, ctx:CalcParser.FactorContext):
        pass

    # Exit a parse tree produced by CalcParser#factor.
    def exitFactor(self, ctx:CalcParser.FactorContext):
        pass


    # Enter a parse tree produced by CalcParser#functionWritingCall.
    def enterFunctionWritingCall(self, ctx:CalcParser.FunctionWritingCallContext):
        pass

    # Exit a parse tree produced by CalcParser#functionWritingCall.
    def exitFunctionWritingCall(self, ctx:CalcParser.FunctionWritingCallContext):
        pass


    # Enter a parse tree produced by CalcParser#functionReadingCall.
    def enterFunctionReadingCall(self, ctx:CalcParser.FunctionReadingCallContext):
        pass

    # Exit a parse tree produced by CalcParser#functionReadingCall.
    def exitFunctionReadingCall(self, ctx:CalcParser.FunctionReadingCallContext):
        pass



del CalcParser
