#include <stdio.h>
#include "token_array.h"
#include "lexer.h"

int main() {
    token_array_init();
    lexical_analyzer();
//    token_array_print();
    token_array_free();
    return 0;
}
