#ifndef LEXER_H_
#define LEXER_H_

// TODO include necessary headers
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "options.h"
#include "token.h"

#define ID_TOKEN_NAME TOKEN_IDENTIFIER // TODO define ID token
#define LEXICAL_ERR_CODE 99 // TODO define lexical error code

// TODO define necessary constants and macros
#define ADD_TOKEN(token, lexeme, c)     \
    state = START;              \
    symbol_step_back(c);                \
    token_append(token, lexeme);        \

#ifdef DEBUG
    #define DEBUG_PRINT(fmt, ...) fprintf(stderr, fmt, ##__VA_ARGS__)
#else
    #define DEBUG_PRINT(fmt, ...)
#endif

#define LEXICAL_ERR(fmt, ...) fprintf(stderr, fmt, ##__VA_ARGS__); \
                              exit(LEXICAL_ERR_CODE); 

void lexical_analyzer();
#endif
