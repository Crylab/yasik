# Generated from Calc.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\21")
        buf.write("U\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\3\2\3\2\5\2\23\n\2\3\3\3\3\3\3\3\3\3\4\3\4\3\4\7")
        buf.write("\4\34\n\4\f\4\16\4\37\13\4\3\5\3\5\3\5\7\5$\n\5\f\5\16")
        buf.write("\5\'\13\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6")
        buf.write("\63\n\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7L\n")
        buf.write("\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\2\2\t\2\4\6\b\n\f\16")
        buf.write("\2\5\3\2\3\5\3\2\6\7\3\2\b\t\2X\2\22\3\2\2\2\4\24\3\2")
        buf.write("\2\2\6\30\3\2\2\2\b \3\2\2\2\n\62\3\2\2\2\fK\3\2\2\2\16")
        buf.write("M\3\2\2\2\20\23\5\4\3\2\21\23\5\6\4\2\22\20\3\2\2\2\22")
        buf.write("\21\3\2\2\2\23\3\3\2\2\2\24\25\5\f\7\2\25\26\t\2\2\2\26")
        buf.write("\27\5\6\4\2\27\5\3\2\2\2\30\35\5\b\5\2\31\32\t\3\2\2\32")
        buf.write("\34\5\b\5\2\33\31\3\2\2\2\34\37\3\2\2\2\35\33\3\2\2\2")
        buf.write("\35\36\3\2\2\2\36\7\3\2\2\2\37\35\3\2\2\2 %\5\n\6\2!\"")
        buf.write("\t\4\2\2\"$\5\n\6\2#!\3\2\2\2$\'\3\2\2\2%#\3\2\2\2%&\3")
        buf.write("\2\2\2&\t\3\2\2\2\'%\3\2\2\2(\63\7\17\2\2)*\7\n\2\2*+")
        buf.write("\5\6\4\2+,\7\13\2\2,\63\3\2\2\2-.\t\3\2\2.\63\5\n\6\2")
        buf.write("/\63\5\16\b\2\60\63\7\16\2\2\61\63\7\20\2\2\62(\3\2\2")
        buf.write("\2\62)\3\2\2\2\62-\3\2\2\2\62/\3\2\2\2\62\60\3\2\2\2\62")
        buf.write("\61\3\2\2\2\63\13\3\2\2\2\64\65\7\16\2\2\65\66\7\n\2\2")
        buf.write("\66\67\7\20\2\2\678\7\f\2\289\7\20\2\29L\7\13\2\2:L\7")
        buf.write("\16\2\2;<\7\16\2\2<=\7\n\2\2=>\7\20\2\2>?\7\r\2\2?@\7")
        buf.write("\20\2\2@A\7\f\2\2AB\7\20\2\2BL\7\13\2\2CD\7\16\2\2DE\7")
        buf.write("\n\2\2EF\7\20\2\2FG\7\f\2\2GH\7\20\2\2HI\7\r\2\2IJ\7\20")
        buf.write("\2\2JL\7\13\2\2K\64\3\2\2\2K:\3\2\2\2K;\3\2\2\2KC\3\2")
        buf.write("\2\2L\r\3\2\2\2MN\7\16\2\2NO\7\n\2\2OP\7\20\2\2PQ\7\f")
        buf.write("\2\2QR\7\20\2\2RS\7\13\2\2S\17\3\2\2\2\7\22\35%\62K")
        return buf.getvalue()


class CalcParser ( Parser ):

    grammarFileName = "Calc.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "'+='", "'-='", "'+'", "'-'", "'*'", 
                     "'/'", "'('", "')'", "','", "':'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "ID", "REALNUMBER", "NUMBER", "WS" ]

    RULE_start = 0
    RULE_assignment = 1
    RULE_arithmeticExpr = 2
    RULE_term = 3
    RULE_factor = 4
    RULE_functionWritingCall = 5
    RULE_functionReadingCall = 6

    ruleNames =  [ "start", "assignment", "arithmeticExpr", "term", "factor", 
                   "functionWritingCall", "functionReadingCall" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    ID=12
    REALNUMBER=13
    NUMBER=14
    WS=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(CalcParser.AssignmentContext,0)


        def arithmeticExpr(self):
            return self.getTypedRuleContext(CalcParser.ArithmeticExprContext,0)


        def getRuleIndex(self):
            return CalcParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)




    def start(self):

        localctx = CalcParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.state = 16
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 14
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 15
                self.arithmeticExpr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionWritingCall(self):
            return self.getTypedRuleContext(CalcParser.FunctionWritingCallContext,0)


        def arithmeticExpr(self):
            return self.getTypedRuleContext(CalcParser.ArithmeticExprContext,0)


        def getRuleIndex(self):
            return CalcParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)




    def assignment(self):

        localctx = CalcParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_assignment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18
            self.functionWritingCall()
            self.state = 19
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CalcParser.T__0) | (1 << CalcParser.T__1) | (1 << CalcParser.T__2))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 20
            self.arithmeticExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CalcParser.TermContext)
            else:
                return self.getTypedRuleContext(CalcParser.TermContext,i)


        def getRuleIndex(self):
            return CalcParser.RULE_arithmeticExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticExpr" ):
                listener.enterArithmeticExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticExpr" ):
                listener.exitArithmeticExpr(self)




    def arithmeticExpr(self):

        localctx = CalcParser.ArithmeticExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_arithmeticExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.term()
            self.state = 27
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CalcParser.T__3 or _la==CalcParser.T__4:
                self.state = 23
                _la = self._input.LA(1)
                if not(_la==CalcParser.T__3 or _la==CalcParser.T__4):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 24
                self.term()
                self.state = 29
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CalcParser.FactorContext)
            else:
                return self.getTypedRuleContext(CalcParser.FactorContext,i)


        def getRuleIndex(self):
            return CalcParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)




    def term(self):

        localctx = CalcParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.factor()
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CalcParser.T__5 or _la==CalcParser.T__6:
                self.state = 31
                _la = self._input.LA(1)
                if not(_la==CalcParser.T__5 or _la==CalcParser.T__6):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 32
                self.factor()
                self.state = 37
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REALNUMBER(self):
            return self.getToken(CalcParser.REALNUMBER, 0)

        def arithmeticExpr(self):
            return self.getTypedRuleContext(CalcParser.ArithmeticExprContext,0)


        def factor(self):
            return self.getTypedRuleContext(CalcParser.FactorContext,0)


        def functionReadingCall(self):
            return self.getTypedRuleContext(CalcParser.FunctionReadingCallContext,0)


        def ID(self):
            return self.getToken(CalcParser.ID, 0)

        def NUMBER(self):
            return self.getToken(CalcParser.NUMBER, 0)

        def getRuleIndex(self):
            return CalcParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactor" ):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactor" ):
                listener.exitFactor(self)




    def factor(self):

        localctx = CalcParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_factor)
        self._la = 0 # Token type
        try:
            self.state = 48
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 38
                self.match(CalcParser.REALNUMBER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 39
                self.match(CalcParser.T__7)
                self.state = 40
                self.arithmeticExpr()
                self.state = 41
                self.match(CalcParser.T__8)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 43
                _la = self._input.LA(1)
                if not(_la==CalcParser.T__3 or _la==CalcParser.T__4):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 44
                self.factor()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 45
                self.functionReadingCall()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 46
                self.match(CalcParser.ID)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 47
                self.match(CalcParser.NUMBER)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionWritingCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CalcParser.ID, 0)

        def NUMBER(self, i:int=None):
            if i is None:
                return self.getTokens(CalcParser.NUMBER)
            else:
                return self.getToken(CalcParser.NUMBER, i)

        def getRuleIndex(self):
            return CalcParser.RULE_functionWritingCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionWritingCall" ):
                listener.enterFunctionWritingCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionWritingCall" ):
                listener.exitFunctionWritingCall(self)




    def functionWritingCall(self):

        localctx = CalcParser.FunctionWritingCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_functionWritingCall)
        try:
            self.state = 73
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                self.match(CalcParser.ID)
                self.state = 51
                self.match(CalcParser.T__7)
                self.state = 52
                self.match(CalcParser.NUMBER)
                self.state = 53
                self.match(CalcParser.T__9)
                self.state = 54
                self.match(CalcParser.NUMBER)
                self.state = 55
                self.match(CalcParser.T__8)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 56
                self.match(CalcParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 57
                self.match(CalcParser.ID)
                self.state = 58
                self.match(CalcParser.T__7)
                self.state = 59
                self.match(CalcParser.NUMBER)
                self.state = 60
                self.match(CalcParser.T__10)
                self.state = 61
                self.match(CalcParser.NUMBER)
                self.state = 62
                self.match(CalcParser.T__9)
                self.state = 63
                self.match(CalcParser.NUMBER)
                self.state = 64
                self.match(CalcParser.T__8)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 65
                self.match(CalcParser.ID)
                self.state = 66
                self.match(CalcParser.T__7)
                self.state = 67
                self.match(CalcParser.NUMBER)
                self.state = 68
                self.match(CalcParser.T__9)
                self.state = 69
                self.match(CalcParser.NUMBER)
                self.state = 70
                self.match(CalcParser.T__10)
                self.state = 71
                self.match(CalcParser.NUMBER)
                self.state = 72
                self.match(CalcParser.T__8)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionReadingCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CalcParser.ID, 0)

        def NUMBER(self, i:int=None):
            if i is None:
                return self.getTokens(CalcParser.NUMBER)
            else:
                return self.getToken(CalcParser.NUMBER, i)

        def getRuleIndex(self):
            return CalcParser.RULE_functionReadingCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionReadingCall" ):
                listener.enterFunctionReadingCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionReadingCall" ):
                listener.exitFunctionReadingCall(self)




    def functionReadingCall(self):

        localctx = CalcParser.FunctionReadingCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_functionReadingCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(CalcParser.ID)
            self.state = 76
            self.match(CalcParser.T__7)
            self.state = 77
            self.match(CalcParser.NUMBER)
            self.state = 78
            self.match(CalcParser.T__9)
            self.state = 79
            self.match(CalcParser.NUMBER)
            self.state = 80
            self.match(CalcParser.T__8)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





