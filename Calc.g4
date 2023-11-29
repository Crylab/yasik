grammar Calc;

// Parser rules
start: assignment | arithmeticExpr;

assignment: functionWritingCall ('=' | '+=' | '-=') arithmeticExpr;

arithmeticExpr: term (('+'|'-') term)*;

term: factor (('*'|'/') factor)*;

factor: REALNUMBER | '(' arithmeticExpr ')' | ('-' | '+') factor | functionReadingCall | ID | NUMBER;

functionWritingCall: ID '(' NUMBER ',' NUMBER ')' | ID | ID '(' NUMBER ':' NUMBER ',' NUMBER ')' | ID '(' NUMBER ',' NUMBER ':' NUMBER ')';

functionReadingCall: ID '(' NUMBER ',' NUMBER ')';

ID: [a-zA-Z]+; // keyword

REALNUMBER: [0-9]* '.' [0-9]+;

NUMBER: [0-9]+;

// Skip whitespaces
WS: [ \t\r\n]+ -> skip;