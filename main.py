import sys
from config import *

input_file = "test_DKA.dka"

states = set()
transition_rules = []
final_states_token_map = {}
keywords_map = {}

includes = r"""// TODO include necessary headers
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "options.h"
#include "token.h"
"""

defines = f"""// TODO define necessary constants and macros
#define ADD_TOKEN(token, lexeme, c)     \\
    state = {start_state};              \\
    symbol_step_back(c);                \\
    token_append(token, lexeme);        \\
    
#define ID_TOKEN_NAME TOKEN_ID // TODO define ID token

#ifdef DEBUG
    #define DEBUG_PRINT(fmt, ...) fprintf(stderr, fmt, ##__VA_ARGS__)
#else
    #define DEBUG_PRINT(fmt, ...)
#endif

#define LEXICAL_ERR_CODE 99 // TODO define lexical error code
#define LEXICAL_ERR(fmt, ...) fprintf(stderr, fmt, ##__VA_ARGS__); \\
                              exit(LEXICAL_ERR_CODE); 
"""

predef_funcs = r"""
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
    if (v_token == _ID_TOKEN_) {
        v_token = validate_id_keyword(lexeme);
    }
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
"""


def get_states(file_data):
    for line in file_data.splitlines():
        if not line.startswith("#") and line != "":
            raw = line.strip()
            if raw.startswith("("):
                # Transition rule
                left = raw.split("->")[0].strip()

                left_state = left.split(",", 1)[0].strip()
                left_symbols_set = left.split(",", 1)[1].strip()[1:-2]

                # print(left_symbols_set)

                list_of_symbols = []
                eval("list_of_symbols.extend([" + left_symbols_set + "])")

                set_of_symbols = set()

                set_of_all_symbols = set(chr(i) for i in range(0, 127))

                for item in list_of_symbols:
                    # if item is not string
                    if not isinstance(item, str):
                        for symbol in item:
                            set_of_symbols.add(symbol)
                    else:
                        if len(item) == 1:
                            set_of_symbols.add(item)

                for item in list_of_symbols:
                    if isinstance(item, str):
                        not_symbol = item
                        if not_symbol.startswith("^") and len(not_symbol) == 2:
                            symb = not_symbol[1]
                            set_of_all_symbols.discard(symb)
                        elif len(not_symbol) > 2:
                            raise Exception(f"Can exclude only one symbol per set item got '{not_symbol}'")

                if len(set_of_symbols) == 0:
                    set_of_symbols = set_of_all_symbols
                elif len(set_of_all_symbols) != 0:
                    set_of_symbols = set_of_symbols & set_of_all_symbols

                right = raw.split("->")[1].strip()

                right_state = right
                right_state = right_state.replace("(", "")

                left_state = left_state.replace("(", "")

                states.add(left_state)
                states.add(right_state)

                transition_rules.append((left_state, set_of_symbols, right_state))

                pass
            elif raw.startswith("{"):
                # Final state
                # remove the curly braces
                raw = raw[1:-1]
                state = raw.split("=")[0].strip()
                token = raw.split("=")[1].strip()

                if not state.endswith("_F"):
                    raise Exception("Final state must end with _F")

                states.add(state)

                if state not in final_states_token_map.keys():
                    final_states_token_map[state] = token
            elif raw.startswith("?"):
                # Keyword
                # remove the question mark
                raw = raw[1:]
                keyword = raw.split("->")[0].strip()
                token = raw.split("->")[1].strip()
                keywords_map[keyword] = token


def generate_state_enum():
    enum_str = "typedef enum {\n"
    for state in states:
        enum_str += " " * 4 + state + ",\n"
    enum_str = enum_str[:-2]
    enum_str += "\n} fsm_state_t;\n\n"
    return enum_str


def generate_keyword_validation():
    out = "static TOKEN_DATA_TYPE_NAME validate_id_keyword(char *lexeme) {\n"
    for keyword in keywords_map.keys():
        out += " " * 4 + f"if (strcmp(lexeme, \"{keyword}\") == 0) return {keywords_map[keyword]};\n"
    out += " " * 4 + "return _ID_TOKEN_;\n"
    out += "}\n"
    return out


def generate_token_enum():
    enum_str = "typedef enum {\n"
    map_str = "static char *map_array[] = {\n"
    used_toks = set()
    for state in final_states_token_map.keys():
        if final_states_token_map[state] in used_toks:
            continue
        enum_str += " " * 4 + final_states_token_map[state] + ",\n"
        map_str += f"\"{final_states_token_map[state]}\",\n"
        used_toks.add(final_states_token_map[state])
    for keyword in keywords_map.values():
        if keyword not in final_states_token_map.values() and keyword not in used_toks:
            enum_str += " " * 4 + keyword + ",\n"
            map_str += f"\"{keyword}\",\n"
            used_toks.add(keyword)
        else:
            raise Exception(f"Keyword token {keyword} is already defined as final state token!\n"
                            "Please change the keyword token name or the final state name!")
    enum_str = enum_str[:-2]
    enum_str += "\n} TOKEN_DATA_TYPE_NAME;\n\n"
    map_str = map_str[:-2]
    map_str += "\n};\n\n"
    return enum_str + map_str


def generate_inner_switch_case(state):
    has_rule_flag = False
    out = (12 * " " + "string_clear(lexeme);\n" if state == start_state else "") + 12 * " " + "switch (symbol) {\n"
    for rule in transition_rules:
        # make case for each symbol
        if rule[0] == state:
            has_rule_flag = True
            prev_symbol = None
            len_seq = 0
            for symbol in sorted(rule[1]):
                if prev_symbol is None:
                    prev_symbol = symbol
                    len_seq = 1
                    out += 16 * " " + "case " + f"{repr(symbol)}"
                else:
                    if ord(prev_symbol) + 1 == ord(symbol):
                        prev_symbol = symbol
                        len_seq += 1
                    else:
                        if len_seq > 1:
                            out += f" ... {repr(prev_symbol)}:\n"
                        else:
                            out += ":\n"
                        out += 16 * " " + "case " + f"{repr(symbol)}"
                        prev_symbol = symbol
                        len_seq = 1
            if len_seq > 1:
                out += f" ... {repr(prev_symbol)}:\n"
            else:
                out += ":\n"
            out += 20 * " " + "state = " + rule[2] + ";\n"
            out += 20 * " " + "break;\n"
    padding_offset = 0
    if has_rule_flag:
        out += 16 * " " + "default:\n"
    else:
        out = ""
        padding_offset = -8
    if state.endswith("_F"):
        out += (20 + padding_offset) * " " + f"ADD_TOKEN({final_states_token_map[state]}, lexeme, symbol);\n"
    else:
        out += (20 + padding_offset) * " " + 'LEXICAL_ERR("Lexical error occurred")' + ";\n"

    if has_rule_flag:
        out += 20 * " " + "break;\n"
        out += 12 * " " + "}\n"
    return out


def generate_outer_switch_case():
    out = "void lexical_analyzer() {\n"
    out += r'DEBUG_PRINT("Lexical analysis started!\n");' + "\n"
    out += "fsm_state_t state = " + start_state + ";\n"
    out += "int flag = 1;\n"
    out += f"char *lexeme = malloc({max_token_lexeme_len} * sizeof(char));\n"
    out += "char symbol;\n"
    out += "while (flag) {\n"
    out += 4 * " " + "symbol = get_next_symbol();\n"
    out += 4 * " " + "if (symbol == EOF) flag = 0;\n"
    out += 4 * " " + "switch (state) {\n"
    for state in sorted(states):
        out += 8 * " " + "case " + state + ":\n"
        out += generate_inner_switch_case(state)
        out += 12 * " " + "break;\n"
    out += 4 * " " + "}\n"
    out += 4 * " " + "string_concat(lexeme, symbol);\n"
    out += "}\n"
    out += "free(lexeme);\n"
    out += r'DEBUG_PRINT("Lexical analysis successfully finished!\n");' + "\n"
    out += "}\n"
    return out


def state_is_reachable(state):
    for rule in transition_rules:
        if rule[2] == state and rule[0] != state:
            return state_is_reachable(rule[0])
        if state == start_state:
            return True
    return False


def check_if_all_states_are_reachable():
    for state in states:
        if not state_is_reachable(state):
            print(f"State {state} is not reachable!")
            return False
    return True


def check_if_rules_are_deterministic():
    for i in range(0, len(transition_rules)):
        for j in range(i + 1, len(transition_rules)):
            if transition_rules[i][0] == transition_rules[j][0]:
                if transition_rules[i][1] & transition_rules[j][1]:
                    print(f"Rules {transition_rules[i]} and {transition_rules[j]} are not deterministic!")
                    return False
    return True


def get_intervals(symbols):
    # interval is a tuple (symbol_start, symbol_end)
    intervals = []
    prev_symbol = None
    seq_len = 0
    temp_interval = None
    for symbol in sorted(symbols):
        if prev_symbol is None:
            prev_symbol = symbol
            seq_len = 1
            temp_interval = (symbol, symbol)
        else:
            if ord(prev_symbol) + 1 == ord(symbol):
                prev_symbol = symbol
                seq_len += 1
                temp_interval = (temp_interval[0], symbol)
            else:
                if seq_len > 1:
                    intervals.append((temp_interval[0], temp_interval[1]))
                else:
                    intervals.append((prev_symbol, prev_symbol))
                prev_symbol = symbol
                seq_len = 1
                temp_interval = (symbol, symbol)
    if seq_len > 1:
        intervals.append((temp_interval[0], temp_interval[1]))
    else:
        intervals.append((prev_symbol, prev_symbol))
    intervals.sort(key=lambda x: x[0] == x[1])
    out = []
    for interval in intervals:
        if interval[0] == interval[1]:
            out.append(repr(interval[0]))
        else:
            out.append(f"{repr(interval[0])}-{repr(interval[1])}")
    return out


def get_digraph():
    out = "digraph fsm {\n"
    out += "rankdir=LR;\n"
    out += "node [shape = doublecircle, width=1, height=1];\n"
    for state in final_states_token_map.keys():
        out += f"{state};\n"
    out += "node [shape = circle, width=1, height=1];\n"
    for rule in transition_rules:
        out += f"{rule[0]} -> {rule[2]} [label=\"{''.join(get_intervals(rule[1])).replace(chr(39), '')}\"];\n"
    out += "}\n"
    return out


graph_flag = False


def main():
    with open(input_file, "r") as file:
        file_data = file.read()

    get_states(file_data)
    if not check_if_all_states_are_reachable():
        return
    if not check_if_rules_are_deterministic():
        return
    if graph_flag:
        print(get_digraph())
        return
    c_out = "#include \"lexer.h\"\n\n"
    c_out += generate_state_enum()
    c_out += generate_keyword_validation()
    c_out += predef_funcs
    c_out += generate_outer_switch_case()

    h_out = """#ifndef LEXER_H_
#define LEXER_H_

"""
    h_out += includes + "\n"
    h_out += defines + "\n"
    h_out += "void lexical_analyzer();\n"
    h_out += "#endif\n"

    h_token = f"""#ifndef TOKEN_H_
#define TOKEN_H_

#include "options.h"

{generate_token_enum()}

#endif
"""

    with open("lexer.c", "w") as file:
        file.write(c_out)
    with open("lexer.h", "w") as file:
        file.write(h_out)
    with open("token.h", "w") as file:
        file.write(h_token)


if __name__ == "__main__":
    # get cmd line args and parse them
    args = sys.argv[1:]
    if len(args) == 1:
        if args[0] == "-h":
            print("Usage: python main.py <input_file> > output.c")
            sys.exit(0)
        else:
            input_file = args[0]
    else:
        if len(args) == 2 and args[0] == "-g":
            input_file = args[1]
            graph_flag = True
        else:
            print("Usage: python main.py <input_file> > output.c")
            sys.exit(1)
    main()
