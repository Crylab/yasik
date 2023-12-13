grammar Yasik;

// Parser rules

code: start (';' start)* ';'?;

start: assignment | arithmeticExpr;

assignment
    : left=functionCall assignmentType=('=' | '+=' | '-=' | '*=' | '/=') right=arithmeticExpr;

arithmeticExpr: term (('+'|'-') term)*;

term: factor (('*'|'/') factor)*;

factor: REALNUMBER | '(' arithmeticExpr ')' | ('-' | '+') factor | functionCall | NUMBER;

yasik_slice: NUMBER | NUMBER? ':' NUMBER?;

functionCall: (ID'.')?ID ('(' left=yasik_slice (',' right=yasik_slice)? ')')?;

ID: [a-zA-Z_][0-9a-zA-Z_]*; // keyword

REALNUMBER: [0-9]* '.' [0-9]+;

NUMBER: [0-9]+;

// Skip whitespaces
WS: [ \t\r\n]+ -> skip;
