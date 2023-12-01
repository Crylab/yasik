# Generated from Calc.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\21")
        buf.write("X\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\3\2\3\2\3\3\3\3\3\3\3\4\3\4")
        buf.write("\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3")
        buf.write("\13\3\13\3\f\3\f\3\r\3\r\7\r<\n\r\f\r\16\r?\13\r\3\16")
        buf.write("\7\16B\n\16\f\16\16\16E\13\16\3\16\3\16\6\16I\n\16\r\16")
        buf.write("\16\16J\3\17\6\17N\n\17\r\17\16\17O\3\20\6\20S\n\20\r")
        buf.write("\20\16\20T\3\20\3\20\2\2\21\3\3\5\4\7\5\t\6\13\7\r\b\17")
        buf.write("\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21\3\2\6")
        buf.write("\5\2C\\aac|\6\2\62;C\\aac|\3\2\62;\5\2\13\f\17\17\"\"")
        buf.write("\2\\\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2")
        buf.write("\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23")
        buf.write("\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3")
        buf.write("\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\3!\3\2\2\2\5#\3\2\2\2")
        buf.write("\7&\3\2\2\2\t)\3\2\2\2\13+\3\2\2\2\r-\3\2\2\2\17/\3\2")
        buf.write("\2\2\21\61\3\2\2\2\23\63\3\2\2\2\25\65\3\2\2\2\27\67\3")
        buf.write("\2\2\2\319\3\2\2\2\33C\3\2\2\2\35M\3\2\2\2\37R\3\2\2\2")
        buf.write("!\"\7?\2\2\"\4\3\2\2\2#$\7-\2\2$%\7?\2\2%\6\3\2\2\2&\'")
        buf.write("\7/\2\2\'(\7?\2\2(\b\3\2\2\2)*\7-\2\2*\n\3\2\2\2+,\7/")
        buf.write("\2\2,\f\3\2\2\2-.\7,\2\2.\16\3\2\2\2/\60\7\61\2\2\60\20")
        buf.write("\3\2\2\2\61\62\7*\2\2\62\22\3\2\2\2\63\64\7+\2\2\64\24")
        buf.write("\3\2\2\2\65\66\7.\2\2\66\26\3\2\2\2\678\7<\2\28\30\3\2")
        buf.write("\2\29=\t\2\2\2:<\t\3\2\2;:\3\2\2\2<?\3\2\2\2=;\3\2\2\2")
        buf.write("=>\3\2\2\2>\32\3\2\2\2?=\3\2\2\2@B\t\4\2\2A@\3\2\2\2B")
        buf.write("E\3\2\2\2CA\3\2\2\2CD\3\2\2\2DF\3\2\2\2EC\3\2\2\2FH\7")
        buf.write("\60\2\2GI\t\4\2\2HG\3\2\2\2IJ\3\2\2\2JH\3\2\2\2JK\3\2")
        buf.write("\2\2K\34\3\2\2\2LN\t\4\2\2ML\3\2\2\2NO\3\2\2\2OM\3\2\2")
        buf.write("\2OP\3\2\2\2P\36\3\2\2\2QS\t\5\2\2RQ\3\2\2\2ST\3\2\2\2")
        buf.write("TR\3\2\2\2TU\3\2\2\2UV\3\2\2\2VW\b\20\2\2W \3\2\2\2\b")
        buf.write("\2=CJOT\3\b\2\2")
        return buf.getvalue()


class CalcLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    ID = 12
    REALNUMBER = 13
    NUMBER = 14
    WS = 15

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'='", "'+='", "'-='", "'+'", "'-'", "'*'", "'/'", "'('", "')'", 
            "','", "':'" ]

    symbolicNames = [ "<INVALID>",
            "ID", "REALNUMBER", "NUMBER", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "ID", "REALNUMBER", "NUMBER", 
                  "WS" ]

    grammarFileName = "Calc.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


