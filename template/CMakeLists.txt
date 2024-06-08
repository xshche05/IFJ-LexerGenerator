cmake_minimum_required(VERSION 3.16)
project(CompilerTemplate C)

set(CMAKE_C_STANDARD 11)

# DEBUG
add_definitions(-DDEBUG)

include_directories(
        parts
        utils
        utils/token_array
        parts/lexer
)

add_executable(CompilerTemplate main.c
        utils/token_array/token_array.c
        parts/lexer/lexer.c
)
