from antlr4 import *
from CalcLexer import CalcLexer
from CalcParser import CalcParser
from CalcListener import CalcListener

class CalcEvaluator(CalcListener):
    def __init__(self):
        self.result = ""
        self.byassignment = ""
        self.valuetoassign = ""
        self.param_list = ["lar"]    # Substitute it by function call
        self.factor_replace_dict = {}
        self.cycleParams = {}

    def exitStart(self, ctx: CalcParser.StartContext):
        if len(self.cycleParams) > 0:
            new_result = ""
            for each in range(self.cycleParams["lb"], self.cycleParams["ub"]):
                new_result += self.result.replace("TheCycleValueHere", str(each))+"; "
            self.result = new_result
        print("Hello from exitStart function!")
        if not self.result:
            self.result = self.valuetoassign

    def exitAssignment(self, ctx: CalcParser.AssignmentContext):        
        print(ctx.getChild(1))        
        if ctx.getChildCount() == 3:
            if ctx.getChild(1).getText() == "=":
                self.result += self.valuetoassign + ")"
            elif ctx.getChild(1).getText() == "+=":
                self.result += self.byassignment + "+(" + self.valuetoassign + "))"
            elif ctx.getChild(1).getText() == "-=":
                self.result += self.byassignment + "-(" + self.valuetoassign + "))"

    def exitFunctionReadingCall(self, ctx: CalcParser.FunctionReadingCallContext):
        if ctx.getChildCount() == 6:
            parameter_name = ctx.getChild(0).getText()
            column = ctx.getChild(2).getText()
            row = ctx.getChild(4).getText()
            string = "lib.xmlMetaReading(xml,'"+parameter_name+"','("+column+", "+row+")')"
            self.factor_replace_dict[ctx.getText()] = string
        else:
            print("Unknown syntax!")

    def exitFunctionWritingCall(self, ctx: CalcParser.FunctionWritingCallContext):    
        parameter_name = ctx.getChild(0).getText()
        if ctx.getChildCount() == 6:
            column = ctx.getChild(2).getText()
            row = ctx.getChild(4).getText()
            self.result = "lib.xmlMetaWriting(xml,'"+parameter_name+"','("+column+", "+row+")',"
            self.byassignment = "lib.xmlMetaReading(xml,'"+parameter_name+"','("+column+", "+row+")')"
        elif ctx.getChildCount() == 1:
            self.result = "lib.xmlMetaWriting(xml,'"+parameter_name+"','(0, 0)',"
            self.byassignment = "lib.xmlMetaReading(xml,'"+parameter_name+"','(0, 0)')"
        elif ctx.getChildCount() == 8:
            if ctx.getChild(3).getText() == ":":                     
                column = "TheCycleValueHere"
                row = ctx.getChild(6).getText()
                self.cycleParams = {"lb": int(ctx.getChild(2).getText()), "ub": int(ctx.getChild(4).getText())}                
                self.result = "lib.xmlMetaWriting(xml,'"+parameter_name+"','("+column+", "+row+")',"
                self.byassignment = "lib.xmlMetaReading(xml,'"+parameter_name+"','("+column+", "+row+")')"
            else:
                column = ctx.getChild(2).getText()
                row = "TheCycleValueHere"
                self.cycleParams = {"lb": int(ctx.getChild(4).getText()), "ub": int(ctx.getChild(6).getText())}
                self.result = "lib.xmlMetaWriting(xml,'"+parameter_name+"','("+column+", "+row+")',"
                self.byassignment = "lib.xmlMetaReading(xml,'"+parameter_name+"','("+column+", "+row+")')"
        else:
            print("Unknown syntax!")
   
    # Exit a parse tree produced by CalcParser#arithmeticExpr.
    def exitArithmeticExpr(self, ctx:CalcParser.ArithmeticExprContext):
        result = ctx.getText()
        for each in self.factor_replace_dict:
            if each in result:
                result = result.replace(each, self.factor_replace_dict[each])
        self.valuetoassign += result

    # Exit a parse tree produced by CalcParser#term.
    def exitTerm(self, ctx:CalcParser.TermContext):
        pass

    # Exit a parse tree produced by CalcParser#factor.
    def exitFactor(self, ctx:CalcParser.FactorContext):
        obj = ctx.getText()
        if obj.replace('.','',1).isdigit():
            return
        if "(" in obj or ")" in obj:
            return
        for each in self.param_list:
            if obj == each:
                self.factor_replace_dict[each] = "lib.xmlMetaReading(xml,'"+each+"','(0, 0)')"
        pass

    def getValue(self):
        return self.result
