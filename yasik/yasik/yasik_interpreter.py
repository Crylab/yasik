from antlr4 import *
from parser_generated.YasikLexer import YasikLexer
from parser_generated.YasikParser import YasikParser
from parser_generated.YasikListener import YasikListener

class YasikEvaluator(YasikListener):
    def __init__(self):
        self.param_list = {"lar": (210, 215)}    # Substitute it by function call
        self.variables = []

    # Exit a parse tree produced by YasikParser#code.
    def exitCode(self, ctx:YasikParser.CodeContext):
        print(ctx.getText())
        print("Good morning from exitCode.")
        pass

    # Exit a parse tree produced by YasikParser#start.
    def exitStart(self, ctx:YasikParser.StartContext):
        print(ctx.getText())
        print("Good morning from exitStart.")
        pass

    # Exit a parse tree produced by YasikParser#assignment.
    def exitAssignment(self, ctx:YasikParser.AssignmentContext):
        if ctx.getChildCount() == 3:
            left_in = ctx.children[0].getText()
            right = ctx.children[2].getText()+")"
            symbol = ctx.children[1].getText()[0]
            if "self.xmlManager.xmlMetaReading" not in left_in:
                left = left_in
                prefix = "="
                if symbol != "=":
                    prefix = "="+left+"+"
                content = left+prefix+right
            else:
                left = left_in.replace("self.xmlManager.xmlMetaReading", "self.xmlManager.xmlMetaWriting")[:-1]
                prefix = ", "
                if symbol != "=":
                    prefix = ", "+left_in+symbol
                content = left+prefix+right

            element = ctx.children[0].children[0]
            element.symbol.text = content
            ctx.children.clear()
            ctx.children.append(element)
            

    # Exit a parse tree produced by YasikParser#arithmeticExpr.
    def exitArithmeticExpr(self, ctx:YasikParser.ArithmeticExprContext):
        print("Good morning from exitArithmeticExpr.")
        pass

    # Exit a parse tree produced by YasikParser#term.
    def exitTerm(self, ctx:YasikParser.TermContext):
        print("Good morning from exitTerm.")
        pass

    # Exit a parse tree produced by YasikParser#factor.
    def exitFactor(self, ctx:YasikParser.FactorContext):
        print("Good morning from exitFactor.")
        pass
    '''
    class MySlice:
        def __init__(self, subtree: YasikParser.Yasik_sliceContext):
            self.begin = subtree.
            self.end = end

            def __to
    '''
    # Exit a parse tree produced by YasikParser#yasik_slice.
    def exitYasik_slice(self, ctx:YasikParser.Yasik_sliceContext):

        def sub(content):
            element = ctx.children[0]
            element.symbol.text = content
            ctx.children.clear()
            ctx.children.append(element)

        if ctx.getChildCount() == 1: # N
            sub(ctx.children[0].getText()+":"+str(int(ctx.children[0].getText())+1))

        if ctx.getChildCount() == 2:
            if ctx.children[0].getText() == ":": # :N
                sub("0:"+ctx.children[1].getText())
            else: # N:
                sub(ctx.children[0].getText()+":MAXLIMITKEYWORD")
            
        if ctx.getChildCount() == 3: # N:N
            sub(ctx.children[0].getText()+":"+ctx.children[2].getText())

        print("Good morning from exitYasik_slice.")
        pass

    # Exit a parse tree produced by YasikParser#functionCall.
    def exitFunctionCall(self, ctx:YasikParser.FunctionCallContext):        
    
        zero_string = "0:1"

        def sub(name, first_slice, second_slice, prefix=""):

            content = "self.xmlManager.xmlMetaReading(xml, '"+prefix+name+"', '("+first_slice+", "+second_slice+")')"
            if "MAXLIMITKEYWORD)" in content:
                content = content.replace("MAXLIMITKEYWORD)", str(self.param_list[name][1])+")")
            if "MAXLIMITKEYWORD," in content:
                content = content.replace("MAXLIMITKEYWORD,", str(self.param_list[name][0])+",")
            element = ctx.children[0]
            element.symbol.text = content
            ctx.children.clear()
            ctx.children.append(element)

        if ctx.getChildCount() == 1: # param
            if ctx.children[0].getText() in self.param_list:
                sub(ctx.children[0].getText(), zero_string, zero_string)

        if ctx.getChildCount() == 3: # category.param
            sub(ctx.children[2].getText(), zero_string, zero_string, prefix=ctx.children[0].getText()+".")

        if ctx.getChildCount() == 4: # param(Slice)
            sub(ctx.children[0].getText(), ctx.children[2].getText(), zero_string)
         
        if ctx.getChildCount() == 6: 
            if ctx.children[1].getText() == ".": # category.param(Slice)
                sub(ctx.children[2].getText(), ctx.children[4].getText(), zero_string, prefix=ctx.children[0].getText()+".")

            else: # param(Slice, Slice)
                sub(ctx.children[0].getText(), ctx.children[2].getText(), ctx.children[4].getText())                

        if ctx.getChildCount() == 8: # category.param(Slice, Slice)
            sub(ctx.children[2].getText(), ctx.children[4].getText(), ctx.children[6].getText(), prefix=ctx.children[0].getText()+".") 
        
            
