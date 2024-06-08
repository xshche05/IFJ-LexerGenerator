#ifndef COMPILERTEMPLATE_TOKEN_ARRAY_H
#define COMPILERTEMPLATE_TOKEN_ARRAY_H

#include <stdlib.h>
#include "token.h"

typedef struct {
    TOKEN_DATA_TYPE_NAME token;
    char *lexeme;
} token_data_t;


typedef struct {
    token_data_t *data;
    size_t size;
    size_t capacity;
    size_t index;
} token_array_t;


void token_array_init();

void token_array_push(TOKEN_DATA_TYPE_NAME token, const char *lexeme);

token_data_t token_array_get_next();

void token_array_print_on_index(int index);

void token_array_print();

void token_array_free();

#endif //COMPILERTEMPLATE_TOKEN_ARRAY_H
