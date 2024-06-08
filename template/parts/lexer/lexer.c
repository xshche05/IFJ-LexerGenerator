#include "lexer.h"
#include "token_array.h"

typedef enum {
    DIV_F,
    RANGE_START_1,
    COMMA_F,
    FLOAT_F,
    ID_F,
    RANGE_CLOSED_F,
    MULT_F,
    NEQ_F,
    EQ_F,
    IS_NIL_F,
    PLUS_F,
    IS_NIL_1,
    AND_F,
    ASSIGN_F,
    RANGE_OPEN_F,
    TYPE_NILLABLE_F,
    START,
    GEQ_F,
    GREATER_F,
    LESS_F,
    COLON_F,
    LEQ_F,
    OR_F,
    NOT_F,
    ARROW_F,
    RANGE_START_2,
    ESCAPE,
    RPAREN_F,
    INT_F,
    OR_1,
    FLOAT_START,
    STRING_F,
    RBRACE_F,
    AND_1,
    LPAREN_F,
    COMMENT,
    STRING_START,
    MINUS_F,
    LBRACE_F
} fsm_state_t;

static TOKEN_DATA_TYPE_NAME validate_id_keyword(char *lexeme) {
    if (strcmp(lexeme, "if") == 0) return TOKEN_IF;
    if (strcmp(lexeme, "else") == 0) return TOKEN_ELSE;
    if (strcmp(lexeme, "while") == 0) return TOKEN_WHILE;
    if (strcmp(lexeme, "for") == 0) return TOKEN_FOR;
    if (strcmp(lexeme, "return") == 0) return TOKEN_RETURN;
    if (strcmp(lexeme, "break") == 0) return TOKEN_BREAK;
    if (strcmp(lexeme, "continue") == 0) return TOKEN_CONTINUE;
    if (strcmp(lexeme, "Int") == 0) return TOKEN_INT_TYPE;
    if (strcmp(lexeme, "Int?") == 0) return TOKEN_INT_NILLABLE_TYPE;
    if (strcmp(lexeme, "String") == 0) return TOKEN_STRING_TYPE;
    if (strcmp(lexeme, "String?") == 0) return TOKEN_STRING_NILLABLE_TYPE;
    if (strcmp(lexeme, "Double") == 0) return TOKEN_FLOAT_TYPE;
    if (strcmp(lexeme, "Double?") == 0) return TOKEN_FLOAT_NILLABLE_TYPE;
    if (strcmp(lexeme, "Bool") == 0) return TOKEN_BOOL_TYPE;
    if (strcmp(lexeme, "Bool?") == 0) return TOKEN_BOOL_NILLABLE_TYPE;
    if (strcmp(lexeme, "var") == 0) return TOKEN_VAR;
    if (strcmp(lexeme, "func") == 0) return TOKEN_FUNC;
    if (strcmp(lexeme, "let") == 0) return TOKEN_LET;
    if (strcmp(lexeme, "_") == 0) return TOKEN_UNDERSCORE;
    if (strcmp(lexeme, "true") == 0) return TOKEN_TRUE_LITERAL;
    if (strcmp(lexeme, "false") == 0) return TOKEN_FALSE_LITERAL;
    if (strcmp(lexeme, "nil") == 0) return TOKEN_NIL_LITERAL;
    return ID_TOKEN_NAME;
}

// TODO function to get next source code symbol
static char get_next_symbol() {
    return getc(stdin);
}

// TODO function to "un get" last symbol
static void symbol_step_back(char c) {
    ungetc(c, stdin);
}

// TODO function to save parsed token, MAKE IDENTIFIER validation to get keywords tokens, add tokens to some kind of 
// list, to get them from during syntax analysis
static void token_append(TOKEN_DATA_TYPE_NAME token, char *lexeme) {
    TOKEN_DATA_TYPE_NAME v_token = token;
    if (v_token == ID_TOKEN_NAME) {
        v_token = validate_id_keyword(lexeme);
    }
    token_array_push(v_token, lexeme);
    DEBUG_PRINT("%s : \"%s\"\n", map_array[v_token], lexeme);
}

// TODO function to concatenate char to string
static void string_concat(char *str, char c) {
    int len = strlen(str);
    str[len] = c;
    str[len+1] = '\0';
}

// TODO function to clear string
static void string_clear(char *str) {
    str[0] = '\0';
}

// TODO function to delete last char from string
static void string_del_last(char *str) {
    int len = strlen(str);
    str[len-1] = '\0';
}
void lexical_analyzer() {
DEBUG_PRINT("Lexical analysis started!\n");
fsm_state_t state = START;
int flag = 1;
char *lexeme = malloc(256 * sizeof(char));
char symbol;
while (flag) {
    symbol = get_next_symbol();
    if (symbol == EOF) flag = 0;
    switch (state) {
        case AND_1:
            switch (symbol) {
                case '&':
                    state = AND_F;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case AND_F:
            ADD_TOKEN(TOKEN_LOGICAL_AND, lexeme, symbol);
            break;
        case ARROW_F:
            ADD_TOKEN(TOKEN_ARROW, lexeme, symbol);
            break;
        case ASSIGN_F:
            switch (symbol) {
                case '=':
                    state = EQ_F;
                    break;
                default:
                    ADD_TOKEN(TOKEN_ASSIGNMENT, lexeme, symbol);
                    break;
            }
            break;
        case COLON_F:
            ADD_TOKEN(TOKEN_COLON, lexeme, symbol);
            break;
        case COMMA_F:
            ADD_TOKEN(TOKEN_COMMA, lexeme, symbol);
            break;
        case COMMENT:
            switch (symbol) {
                case '\n':
                case '\r':
                    state = START;
                    break;
                case ' ' ... '~':
                    state = COMMENT;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case DIV_F:
            switch (symbol) {
                case '/':
                    state = COMMENT;
                    break;
                default:
                    ADD_TOKEN(TOKEN_DIVISION, lexeme, symbol);
                    break;
            }
            break;
        case EQ_F:
            ADD_TOKEN(TOKEN_EQUAL_TO, lexeme, symbol);
            break;
        case ESCAPE:
            switch (symbol) {
                case 'n':
                case 'r':
                case 't':
                    state = STRING_START;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case FLOAT_F:
            switch (symbol) {
                case '0' ... '9':
                    state = FLOAT_F;
                    break;
                default:
                    ADD_TOKEN(TOKEN_FLOAT, lexeme, symbol);
                    break;
            }
            break;
        case FLOAT_START:
            switch (symbol) {
                case '0' ... '9':
                    state = FLOAT_F;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case GEQ_F:
            ADD_TOKEN(TOKEN_GREATER_THAN_OR_EQUAL_TO, lexeme, symbol);
            break;
        case GREATER_F:
            switch (symbol) {
                case '=':
                    state = GEQ_F;
                    break;
                default:
                    ADD_TOKEN(TOKEN_GREATER_THAN, lexeme, symbol);
                    break;
            }
            break;
        case ID_F:
            switch (symbol) {
                case '0' ... '9':
                case 'A' ... 'Z':
                case '_':
                case 'a' ... 'z':
                    state = ID_F;
                    break;
                case '?':
                    state = TYPE_NILLABLE_F;
                    break;
                default:
                    ADD_TOKEN(TOKEN_IDENTIFIER, lexeme, symbol);
                    break;
            }
            break;
        case INT_F:
            switch (symbol) {
                case '0' ... '9':
                    state = INT_F;
                    break;
                case '.':
                    state = FLOAT_START;
                    break;
                default:
                    ADD_TOKEN(TOKEN_INTEGER, lexeme, symbol);
                    break;
            }
            break;
        case IS_NIL_1:
            switch (symbol) {
                case '?':
                    state = IS_NIL_F;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case IS_NIL_F:
            ADD_TOKEN(TOKEN_IS_NIL, lexeme, symbol);
            break;
        case LBRACE_F:
            ADD_TOKEN(TOKEN_LEFT_BRACE, lexeme, symbol);
            break;
        case LEQ_F:
            ADD_TOKEN(TOKEN_LESS_THAN_OR_EQUAL_TO, lexeme, symbol);
            break;
        case LESS_F:
            switch (symbol) {
                case '=':
                    state = LEQ_F;
                    break;
                default:
                    ADD_TOKEN(TOKEN_LESS_THAN, lexeme, symbol);
                    break;
            }
            break;
        case LPAREN_F:
            ADD_TOKEN(TOKEN_LEFT_BRACKET, lexeme, symbol);
            break;
        case MINUS_F:
            switch (symbol) {
                case '>':
                    state = ARROW_F;
                    break;
                default:
                    ADD_TOKEN(TOKEN_SUBTRACTION, lexeme, symbol);
                    break;
            }
            break;
        case MULT_F:
            ADD_TOKEN(TOKEN_MULTIPLICATION, lexeme, symbol);
            break;
        case NEQ_F:
            ADD_TOKEN(TOKEN_NOT_EQUAL_TO, lexeme, symbol);
            break;
        case NOT_F:
            switch (symbol) {
                case '=':
                    state = NEQ_F;
                    break;
                default:
                    ADD_TOKEN(TOKEN_LOGICAL_NOT, lexeme, symbol);
                    break;
            }
            break;
        case OR_1:
            switch (symbol) {
                case '|':
                    state = OR_F;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case OR_F:
            ADD_TOKEN(TOKEN_LOGICAL_OR, lexeme, symbol);
            break;
        case PLUS_F:
            ADD_TOKEN(TOKEN_ADDITION, lexeme, symbol);
            break;
        case RANGE_CLOSED_F:
            ADD_TOKEN(TOKEN_CLOSED_RANGE, lexeme, symbol);
            break;
        case RANGE_OPEN_F:
            ADD_TOKEN(TOKEN_HALF_OPEN_RANGE, lexeme, symbol);
            break;
        case RANGE_START_1:
            switch (symbol) {
                case '.':
                    state = RANGE_START_2;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case RANGE_START_2:
            switch (symbol) {
                case '.':
                    state = RANGE_CLOSED_F;
                    break;
                case '<':
                    state = RANGE_OPEN_F;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case RBRACE_F:
            ADD_TOKEN(TOKEN_RIGHT_BRACE, lexeme, symbol);
            break;
        case RPAREN_F:
            ADD_TOKEN(TOKEN_RIGHT_BRACKET, lexeme, symbol);
            break;
        case START:
            string_clear(lexeme);
            switch (symbol) {
                case '\t' ... '\n':
                case '\r':
                case ' ':
                    state = START;
                    break;
                case '{':
                    state = LBRACE_F;
                    break;
                case '}':
                    state = RBRACE_F;
                    break;
                case '(':
                    state = LPAREN_F;
                    break;
                case ')':
                    state = RPAREN_F;
                    break;
                case ':':
                    state = COLON_F;
                    break;
                case ',':
                    state = COMMA_F;
                    break;
                case '+':
                    state = PLUS_F;
                    break;
                case '*':
                    state = MULT_F;
                    break;
                case '/':
                    state = DIV_F;
                    break;
                case '=':
                    state = ASSIGN_F;
                    break;
                case '-':
                    state = MINUS_F;
                    break;
                case '<':
                    state = LESS_F;
                    break;
                case '>':
                    state = GREATER_F;
                    break;
                case '?':
                    state = IS_NIL_1;
                    break;
                case '!':
                    state = NOT_F;
                    break;
                case '|':
                    state = OR_1;
                    break;
                case '&':
                    state = AND_1;
                    break;
                case '.':
                    state = RANGE_START_1;
                    break;
                case 'A' ... 'Z':
                case '_':
                case 'a' ... 'z':
                    state = ID_F;
                    break;
                case '0' ... '9':
                    state = INT_F;
                    break;
                case '"':
                    state = STRING_START;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case STRING_F:
            ADD_TOKEN(TOKEN_STRING, lexeme, symbol);
            break;
        case STRING_START:
            switch (symbol) {
                case ' ' ... '!':
                case '#' ... '[':
                case ']' ... '~':
                    state = STRING_START;
                    break;
                case '"':
                    state = STRING_F;
                    break;
                case '\\':
                    state = ESCAPE;
                    break;
                default:
                    LEXICAL_ERR("Lexical error occurred");
                    break;
            }
            break;
        case TYPE_NILLABLE_F:
            ADD_TOKEN(TOKEN_IDENTIFIER, lexeme, symbol);
            break;
    }
    string_concat(lexeme, symbol);
}
free(lexeme);
DEBUG_PRINT("Lexical analysis successfully finished!\n");
}
