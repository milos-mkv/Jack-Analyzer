"""
------------------------------------------------------------------------------
    @file       tokenizer.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      ...

    @version    0.1
    @date       2020-08-26

    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
from src.constants import *
from src.token import Token

class Tokenizer(object):

    def __init__(self, code):
        """ Constructs tokenizer object. """
        self.code = code
        self.index = 0
        self.tokens = []
        self.get_all_tokens()
    
    def advance(self):
        """ Return next token and move token next cursor. """
        if self.index == len(self.tokens):
            return None
        token = self.tokens[self.index]
        self.index = self.index + 1
        return token

    def next(self):
        """ Return next token. """
        if self.index + 1 > len(self.tokens):
            return None
        return self.tokens[self.index]

    def export_xml(self, file_name):
        """ Save all tokens in xml file. """
        with open("xml-export/{0}.tokens.xml".format(file_name), "w") as xml_file:
            xml_file.write("<tokens>\n")
            for token in self.tokens:
                if token.value in XML_REPLACE.keys():
                    xml_file.write("\t<{0}> {1} </{0}>\n".format(token.type, XML_REPLACE[token.value]))
                else:
                    xml_file.write("\t<{0}> {1} </{0}>\n".format(token.type, token.value))
            xml_file.write("</tokens>")

    def get_all_tokens(self):
        """ Find all tokens in provided code and store them in token list. """
        word = ""
        begin_string = False
        i = 0

        while i < len(self.code):
            char = self.code[i]
            # Ignore white space
            if char in [' ', '\t', '\n'] and begin_string == False: 
                i = i + 1 
                word = "" 
                continue
            
            word = word + char
            if word in KEYWORDS and self.code[i + 1] in SYMBOLS + SKIPABLE:
                self.tokens.append(Token("keyword", word))
                word = ""
            elif char == '"' or begin_string: # Check for string
                if char == '"':
                    begin_string = not begin_string
                if not begin_string:
                    self.tokens.append(Token("stringConstant", word[1:-1]))
                    word = ""
            elif word in SYMBOLS:
                self.tokens.append(Token("symbol", word))
                word = ""
            elif self.code[i + 1] in SKIPABLE + SYMBOLS:
                if word.isdigit():
                    self.tokens.append(Token("integerConstant", word))
                else:
                    self.tokens.append(Token("identifier", word))
                word = ""
            i = i + 1