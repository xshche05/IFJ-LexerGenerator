# Lexical Analyser code (C) generator

## Recommendations
- **MAKE THE AUTOMATON DESIGN AS A FIRST STEP!!!!**
- Do not parse keywords as tokens, parse them as identifiers and then check if they are keywords.
- Read todo comments in the generated code.
- The generated code is not perfect, you may need to modify it to suit your needs.
- The generated code is not optimized, you may need to optimize it.
- The generated code is not tested, you may need to test it.

## Description
This is a simple lexical analyser code generator. It generates a C code that reads a file and tokenizes it. The tokens
are defined by a set of automaton rules. The rules are defined in a file with the following format (separated by newlines):
```
(PREVIOUS_STATE, {<set of transition symbols>}) -> NEXT_STATE
```
Where:
- `PREVIOUS_STATE` is the state that the automaton is in before the transition.
- `<set of transition symbols>` is the set of symbols that can make the transition.
- `NEXT_STATE` is the state that the automaton will be in after the transition.

As a starting state, use the state name `START`.

Additionally, you have to define tokens names for FINAL states. The format is:
```
{FINAL_STATE_F = 'TOKEN_NAME'}
```
Where:
- `FINAL_STATE_F` is the state that the automaton is in after the transition. Must be ended with `_F`.
- `TOKEN_NAME` is the name of the token that will be generated when the automaton reaches that state.

Lines that start with `#` are considered comments and are ignored.

### Example
The following is an example of a rules file:
```
# Automaton rules
(START, {'a', 'b'}) -> STATE1
(STATE1, {'a', 'b'}) -> STATE1
(STATE1, {'c'}) -> STATE2_F
# Tokens
{STATE2_F = 'TEST_TOKEN'}
```
Equivalent regular expression: `(ab)+[c]` for token `TEST_TOKEN`.

### Predefined char sets for transition symbols, can be configured inside python script, other sets can be added
- letters (a-z, A-Z)
- letters_lower (a-z)
- letters_upper (A-Z)
- digits (0-9)
- whitespaces
- white_symbols
- newline

## Usage
To generate the C code, run the following command:
```
python3 main.py <rules_file> > output.c
```
In output.c, you will find the generated code. The generated code contains enums, additional functions templates, 
and the main FSM function. You can modify the code to suit your needs.