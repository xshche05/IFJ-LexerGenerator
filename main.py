import sys

input_file = "input.dka"

states = set()
transition_rules = []
final_states_token_map = {}

letters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
letters_lower = set("abcdefghijklmnopqrstuvwxyz")
letters_upper = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
digits = set("0123456789")
whitespaces = set(" \t")  # whitespace symbols
white_symbols = set(" \t\n\r")  # ALL whitesymbols (whitespace + newline)
newline = set("\n\r")  # newline symbols

keywords_map = {}

start_state = "START"

id_token = "ID"

max_token_lexeme_len = 256

includes = r"""// TODO include necessary headers
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
"""

defines = f"""// TODO define necessary constants and macros
#define LEXICAL_ERR 99
#define add_token(token, lexeme, c)     \\
    state = {start_state};              \\
    symbol_step_back(c);                \\
    token_append(token, lexeme);        \\
"""

predef_funcs = r"""
// TODO function to get next source code symbol
char get_next_symbol() {
    return getc(stdin);
}

// TODO function to "un get" last symbol
void symbol_step_back(char c) {
    ungetc(c, stdin);
}

token_t validate_id_keyword(char *lexeme);

// TODO function to save parsed token, MAKE IDENTIFIER validation to get keywords tokens, add tokens to some kind of list, to get them from during syntax analysis
void token_append(token_t token, char *lexeme) {
    token_t v_token = token;
""" + f"    if (v_token == {id_token}) " + "{" + r"""
        v_token = validate_id_keyword(lexeme);
    }
    printf("%s : \"%s\"\n", map_array[v_token], lexeme);
}

// TODO function to concatenate char to string
void string_concat(char *str, char c) {
    int len = strlen(str);
    str[len] = c;
    str[len+1] = '\0';
}

// TODO function to clear string
void string_clear(char *str) {
    str[0] = '\0';
}

// TODO function to delete last char from string
void string_del_last(char *str) {
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

                for item in list_of_symbols:
                    for symbol in item:
                        set_of_symbols.add(symbol)

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
        enum_str += " "*4 + state + ",\n"
    enum_str = enum_str[:-2]
    enum_str += "\n} fsm_state_t;\n\n"
    return enum_str


def generate_keyword_validation():
    out = "token_t validate_id_keyword(char *lexeme) {\n"
    for keyword in keywords_map.keys():
        out += " "*4 + f"if (strcmp(lexeme, \"{keyword}\") == 0) return {keywords_map[keyword]};\n"
    out += " "*4 + f"return {id_token};\n"
    out += "}\n"
    return out


def generate_token_enum():
    enum_str = "typedef enum {\n"
    map_str = "char *map_array[] = {\n"
    for state in final_states_token_map.keys():
        enum_str += " "*4 + final_states_token_map[state] + ",\n"
        map_str += f"\"{final_states_token_map[state]}\",\n"
    for keyword in keywords_map.values():
        if keyword not in final_states_token_map.values():
            enum_str += " "*4 + keyword + ",\n"
            map_str += f"\"{keyword}\",\n"
        else:
            raise Exception(f"Keyword token {keyword} is already defined as final state token!\n"
                            "Please change the keyword token name or the final state name!")
    enum_str = enum_str[:-2]
    enum_str += "\n} token_t;\n\n"
    map_str = map_str[:-2]
    map_str += "\n};\n\n"
    return enum_str + map_str


def generate_inner_switch_case(state):
    has_rule_flag = False
    out = (12*" " + "string_clear(lexeme);\n" if state == start_state else "") + 12*" " + "switch (symbol) {\n"
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
                    out += 16*" " + "case " + f"{repr(symbol)}"
                else:
                    if ord(prev_symbol) + 1 == ord(symbol):
                        prev_symbol = symbol
                        len_seq += 1
                    else:
                        if len_seq > 1:
                            out += f" ... {repr(prev_symbol)}:\n"
                        else:
                            out += ":\n"
                        out += 16*" " + "case " + f"{repr(symbol)}"
                        prev_symbol = symbol
                        len_seq = 1
            if len_seq > 1:
                out += f" ... {repr(prev_symbol)}:\n"
            else:
                out += ":\n"
            out += 20*" " + "state = " + rule[2] + ";\n"
            out += 20*" " + "break;\n"
    padding_offset = 0
    if has_rule_flag:
        out += 16*" " + "default:\n"
    else:
        out = ""
        padding_offset = -8
    if state.endswith("_F"):
        out += (20+padding_offset)*" " + f"add_token({final_states_token_map[state]}, lexeme, symbol);\n"
    else:
        out += (20+padding_offset)*" " + "exit(LEXICAL_ERR)" + ";\n"

    if has_rule_flag:
        out += 20 * " " + "break;\n"
        out += 12 * " " + "}\n"
    return out


def generate_outer_switch_case():
    out = "void lexical_analyzer() {\n"
    out += "fsm_state_t state = " + start_state + ";\n"
    out += "int flag = 1;\n"
    out += f"char *lexeme = malloc({max_token_lexeme_len} * sizeof(char));\n"
    out += "char symbol;\n"
    out += "while (flag) {\n"
    out += 4*" " + "symbol = get_next_symbol();\n"
    out += 4*" " + "if (symbol == EOF) flag = 0;\n"
    out += 4*" " + "switch (state) {\n"
    for state in sorted(states):
        out += 8*" " + "case " + state + ":\n"
        out += generate_inner_switch_case(state)
        out += 12*" " + "break;\n"
    out += 4*" " + "}\n"
    out += 4 * " " + "string_concat(lexeme, symbol);\n"
    out += "}\n"
    out += "}\n"
    return out


def state_is_reachable(state):
    for rule in transition_rules:
        if rule[2] == state:
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
        for j in range(i+1, len(transition_rules)):
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
    out = []
    for interval in intervals:
        if interval[0] == interval[1]:
            out.append(repr(interval[0]))
        else:
            out.append(f"{repr(interval[0])}-{repr(interval[1])}")
    return out


def main():
    with open(input_file, "r") as file:
        file_data = file.read()

    get_states(file_data)
    if not check_if_all_states_are_reachable():
        return
    if not check_if_rules_are_deterministic():
        return
    print(includes)
    print(defines)
    print(generate_state_enum())
    print(generate_token_enum())
    print(predef_funcs)
    print(generate_keyword_validation())
    print(generate_outer_switch_case())


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
        print("Usage: python main.py <input_file> > output.c")
        sys.exit(1)
    main()

