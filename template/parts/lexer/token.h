#ifndef TOKEN_H_
#define TOKEN_H_

#include "options.h"

typedef enum {
    TOKEN_LEFT_BRACE,
    TOKEN_RIGHT_BRACE,
    TOKEN_LEFT_BRACKET,
    TOKEN_RIGHT_BRACKET,
    TOKEN_COLON,
    TOKEN_COMMA,
    TOKEN_ADDITION,
    TOKEN_MULTIPLICATION,
    TOKEN_DIVISION,
    TOKEN_ASSIGNMENT,
    TOKEN_EQUAL_TO,
    TOKEN_SUBTRACTION,
    TOKEN_ARROW,
    TOKEN_LESS_THAN,
    TOKEN_LESS_THAN_OR_EQUAL_TO,
    TOKEN_GREATER_THAN,
    TOKEN_GREATER_THAN_OR_EQUAL_TO,
    TOKEN_IS_NIL,
    TOKEN_LOGICAL_NOT,
    TOKEN_NOT_EQUAL_TO,
    TOKEN_LOGICAL_OR,
    TOKEN_LOGICAL_AND,
    TOKEN_CLOSED_RANGE,
    TOKEN_HALF_OPEN_RANGE,
    TOKEN_IDENTIFIER,
    TOKEN_INTEGER,
    TOKEN_FLOAT,
    TOKEN_STRING,
    TOKEN_IF,
    TOKEN_ELSE,
    TOKEN_WHILE,
    TOKEN_FOR,
    TOKEN_RETURN,
    TOKEN_BREAK,
    TOKEN_CONTINUE,
    TOKEN_INT_TYPE,
    TOKEN_INT_NILLABLE_TYPE,
    TOKEN_STRING_TYPE,
    TOKEN_STRING_NILLABLE_TYPE,
    TOKEN_FLOAT_TYPE,
    TOKEN_FLOAT_NILLABLE_TYPE,
    TOKEN_BOOL_TYPE,
    TOKEN_BOOL_NILLABLE_TYPE,
    TOKEN_VAR,
    TOKEN_FUNC,
    TOKEN_LET,
    TOKEN_UNDERSCORE,
    TOKEN_TRUE_LITERAL,
    TOKEN_FALSE_LITERAL,
    TOKEN_NIL_LITERAL
} TOKEN_DATA_TYPE_NAME;

static char *map_array[] = {
"TOKEN_LEFT_BRACE",
"TOKEN_RIGHT_BRACE",
"TOKEN_LEFT_BRACKET",
"TOKEN_RIGHT_BRACKET",
"TOKEN_COLON",
"TOKEN_COMMA",
"TOKEN_ADDITION",
"TOKEN_MULTIPLICATION",
"TOKEN_DIVISION",
"TOKEN_ASSIGNMENT",
"TOKEN_EQUAL_TO",
"TOKEN_SUBTRACTION",
"TOKEN_ARROW",
"TOKEN_LESS_THAN",
"TOKEN_LESS_THAN_OR_EQUAL_TO",
"TOKEN_GREATER_THAN",
"TOKEN_GREATER_THAN_OR_EQUAL_TO",
"TOKEN_IS_NIL",
"TOKEN_LOGICAL_NOT",
"TOKEN_NOT_EQUAL_TO",
"TOKEN_LOGICAL_OR",
"TOKEN_LOGICAL_AND",
"TOKEN_CLOSED_RANGE",
"TOKEN_HALF_OPEN_RANGE",
"TOKEN_IDENTIFIER",
"TOKEN_INTEGER",
"TOKEN_FLOAT",
"TOKEN_STRING",
"TOKEN_IF",
"TOKEN_ELSE",
"TOKEN_WHILE",
"TOKEN_FOR",
"TOKEN_RETURN",
"TOKEN_BREAK",
"TOKEN_CONTINUE",
"TOKEN_INT_TYPE",
"TOKEN_INT_NILLABLE_TYPE",
"TOKEN_STRING_TYPE",
"TOKEN_STRING_NILLABLE_TYPE",
"TOKEN_FLOAT_TYPE",
"TOKEN_FLOAT_NILLABLE_TYPE",
"TOKEN_BOOL_TYPE",
"TOKEN_BOOL_NILLABLE_TYPE",
"TOKEN_VAR",
"TOKEN_FUNC",
"TOKEN_LET",
"TOKEN_UNDERSCORE",
"TOKEN_TRUE_LITERAL",
"TOKEN_FALSE_LITERAL",
"TOKEN_NIL_LITERAL"
};

#endif