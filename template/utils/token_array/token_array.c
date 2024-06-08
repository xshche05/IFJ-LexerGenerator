#include "token_array.h"

#include <stdio.h>
#include <string.h>

token_array_t *array = NULL;

void token_array_init() {
    array = malloc(sizeof(token_array_t));
    array->data = malloc(sizeof(token_data_t) * 1024);
    array->size = 0;
    array->capacity = 1024;
    array->index = -1;
}

void token_array_push(TOKEN_DATA_TYPE_NAME token, const char *lexeme) {
    char *token_lexeme = malloc(strlen(lexeme) + 1);
    strcpy(token_lexeme, lexeme);
    token_data_t token_data = {token, token_lexeme};
    if (array->size >= array->capacity - 20) {
        array->capacity *= 2;
        array->data = realloc(array->data, sizeof(token_data_t) * array->capacity);
        if (array->data == NULL) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(99); // TODO: define error code, or handle error in a better way
        }
    }
    array->data[array->size++] = token_data;
}

token_data_t token_array_get_next() {
    return array->data[++array->index];
}

void token_array_free() {
    for (size_t i = 0; i < array->size; i++) {
        free(array->data[i].lexeme);
    }
    free(array->data);
    free(array);
}

void token_array_print_on_index(int index) {
    if (index < array->size) {
        printf("%s : '%s'\n", map_array[array->data[index].token], array->data[index].lexeme);
    } else {
        fprintf(stderr, "Index out of bounds\n");
    }
}

void token_array_print() {
    for (size_t i = 0; i < array->size; i++) {
        token_array_print_on_index(i);
    }
}
