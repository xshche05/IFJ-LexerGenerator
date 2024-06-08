# Description: This file contains the configuration for the lexer.

# Configuration of predefined sets
letters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
letters_lower = set("abcdefghijklmnopqrstuvwxyz")
letters_upper = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
printable = set(chr(i) for i in range(32, 127))
digits = set("0123456789")
whitespaces = set(" \t")
white_symbols = set(" \t\n\r")
newline = set("\n\r")
# Can be extended with more custom sets, TODO: Change if needed

# Starting state
start_state = "START"  # TODO: Change to if needed
max_token_lexeme_len = 256  # Maximum length of a token lexeme, TODO: Change if needed

