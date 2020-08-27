"""
------------------------------------------------------------------------------
    @file       constants.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      ...

    @version    0.1
    @date       2020-08-26

    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

import re

KEYWORD_CONSANTS = ('true', 'false', 'this', 'null')
KEYWORDS         = ('class', 'constructor', 'function', 'method', 'filed', 'static', 'var', 'int', 'char', 'boolean', 
                    'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return')
TYPES            = ('int', 'void', 'boolean', 'char')

SYMBOLS     = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '>', '<', '=', '~')
SKIPABLE    = ('"', '\'', ' ', '\t', '\n')
OP          = ('+', '-', '*', '/', '&', '|', '<', '>', '=')
UNARY_OP    = ('-', '~')
MAX_INTEGER = 0b111111111111111 # Binary for => 32767

# Regular expressions
R_IDENTIFIER = r"^([_a-zA-Z]+|[_a-zA-Z][_a-zA-Z0-9]+)$"
R_STRING     = r"^\".*\"$"
R_SINGLE_LINE_COMMENT = r"\/\/.*"
R_MULTI_LINE_COMMENT  = re.compile(r"\/\*.*?\*\/", re.DOTALL)

XML_REPLACE = { "<": "&lt;", ">": "&gt;", '"': "&quot;", "&": "&amp;" }


def remove_all_comments(code):
    """ Remove all comments from code. """
    for comment in re.findall(R_SINGLE_LINE_COMMENT, code) + re.findall(R_MULTI_LINE_COMMENT, code):
        code = code.replace(comment, "")
    return code