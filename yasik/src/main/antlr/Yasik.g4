grammar Yasik;

// Parser rules

start: assignment | arithmeticExpr;

assignment: functionCall ('=' | '+=' | '-=') arithmeticExpr;

arithmeticExpr: term (('+'|'-') term)*;

term: factor (('*'|'/') factor)*;

factor: REALNUMBER | '(' arithmeticExpr ')' | ('-' | '+') factor | functionCall | ID | NUMBER;

yasik_slice: NUMBER | NUMBER? ':' NUMBER?;

functionCall: (ID'.')?ID '(' yasik_slice (',' yasik_slice)? ')';

ID: [a-zA-Z_][0-9a-zA-Z_]*; // keyword

REALNUMBER: [0-9]* '.' [0-9]+;

NUMBER: [0-9]+;

// Skip whitespaces
WS: [ \t\r\n]+ -> skip;
