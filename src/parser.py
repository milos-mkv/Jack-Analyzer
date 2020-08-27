"""
------------------------------------------------------------------------------
    @file       parser.py
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
from src.tokenizer import Tokenizer
from src.symbol_table import SymbolTable
from src.variable import Variable
from copy import copy

CLASSES     = []
SUBROUTINES = []

class Parser(object):

    def __init__(self, tokenizer):
        """ Constructs parser object. """
        self.xml_data     = []                  # For xml export.
        self.symbol_table = SymbolTable()       # Create symbol table for class scope.
        self.tokenizer    = tokenizer           # Tokenizer.
        self.token        = None                # Current token.
        self.compile_class()

    def check_for_value(self, value):
        """ Check if current token has expected value. """
        self.token = self.tokenizer.advance()
        if self.token.value != value:
            raise Exception("Error: Excpected value => '{0}' but got => '{1}'".format(value, self.token.value))
        
        if self.token.value in XML_REPLACE.keys():
            self.xml_data.append("<{0}> {1} </{0}>".format(self.token.type, XML_REPLACE[self.token.value]))
        else:
            self.xml_data.append(self.token.__str__())

    def check_for_identifier(self):
        """ Check if current token is valid identifier. """
        self.token = self.tokenizer.advance()
        if self.token.type != "identifier" or (not re.match(R_IDENTIFIER, self.token.value)):
            raise Exception("Error: Identifier name not valid => '{0}'".format(self.token.value))
        self.xml_data.append(self.token.__str__())

    def check_for_type(self):
        """ Check if current token has valid type. """
        self.token = self.tokenizer.advance()
        if self.token.value not in list(TYPES) + CLASSES:
            raise Exception("Error: Not valid type => '{0}'".format(self.token.value))
        self.xml_data.append(self.token.__str__())

    def check_for_operator(self):
        """ Check if current token is operator. """
        self.token = self.tokenizer.advance()
        if self.token.value not in OP:
            raise Exception("Error: Invalid operator => '{0}'".format(self.token.value))
        
        if self.token.value in XML_REPLACE.keys():
            self.xml_data.append("<{0}> {1} </{0}>".format(self.token.type, XML_REPLACE[self.token.value]))
        else:
            self.xml_data.append(self.token.__str__())

    def compile_class(self):
        """
            Compile class.
            -------------------------------------------------------------
            Rule => 'class' className '{' classVarDec* subroutineDec* '}'
            -------------------------------------------------------------
        """
        self.xml_data.append("<class>")             # Xml rep: <class>
        self.check_for_value('class')               # Xml rep:    <keyword> class </keyword>
        self.check_for_identifier()                 # Xml rep:    <identifier> className </identifier>

        CLASSES.append(self.token.value)            # Add class name to list of classes.

        self.check_for_value('{')                   # Xml rep:    <symbol> { </symbol>

        while self.tokenizer.next().value != "}":       
            self.token = self.tokenizer.advance()

            if self.token.value in ['static', 'field']:
                self.compile_class_var_dec()        # Compile class variable declarations.

            elif self.token.value in ['constructor', 'function', 'method']:
                self.compile_subroutine_dec()       # Compile class subroutine declarations.

        self.check_for_value("}")                   # Xml rep:    <symbol> } </symbol>
        self.xml_data.append("</class>")            # Xml rep: </class>

    def compile_class_var_dec(self): 
        """
            Compile class variable declarations.
            -------------------------------------------------------------
            Rule => ('static' | 'field') type varName (',', varName)* ';'
            -------------------------------------------------------------
        """
        self.xml_data.append("<classVarDec>")       # Xml rep: <classVarDec>
        variable = Variable()

        self.xml_data.append(self.token.__str__())  # Xml rep:    <keyword> ('static' | 'field') </keyword>
        variable.kind = self.token.value

        self.check_for_type()                       # Xml rep:    <keyword> type </keyword>
        variable.type = self.token.value

        self.check_for_identifier()                 # Xml rep:    <identifier> varName </identifier>
        variable.name = self.token.value

        self.symbol_table.add(variable)             # Add variable to class scope symbol table.

        while self.tokenizer.next().value != ";":
            self.check_for_value(",")               # Xml rep:     <symbol> , </symbol>
            self.check_for_identifier()             # Xml rep:     <identifier> varName </identifier>
            v = copy(variable)
            v.name = self.token.value
            self.symbol_table.add(v)                # Add variable to class scope symbol table.
        
        self.check_for_value(";")                   # Xml rep:     <symbol> ; </symbol>
        self.xml_data.append("</classVarDec>")      # Xml rep: </classVarDec>

    def compile_subroutine_dec(self): 
        """
            Compile class subroutine declarations.
            -------------------------------------------------------------------------------------------------------------------
            Rule => ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
            -------------------------------------------------------------------------------------------------------------------
        """
        self.xml_data.append("<subroutineDec>")     # Xml rep: <subroutineDec>
        self.xml_data.append(self.token.__str__())  # Xml rep:     <keyword> ('constructor' | 'function' | 'method')) </keyword>
        self.check_for_type()                       # Xml rep:     <keyword> type </keyword>
        self.check_for_identifier()                 # Xml rep:     <identifier> subroutineName </identifier>

        SUBROUTINES.append(self.token.value)        # Add subroutine name to subroutine list.

        self.check_for_value("(")                   # Xml rep:     <symbol> ( </symbol>
        self.compile_parameter_list()               # Compile parameter list.
        self.check_for_value(")")                   # Xml rep:     <symbol> ) </symbol>
        self.compile_subroutine_body()              # Compile subroutine body.
        self.xml_data.append("</subroutineDec>")    # Xml rep: </subroutineDec>

    def compile_parameter_list(self): 
        """
            Compile parameter list.
            ---------------------------------------------
            Rule => ((type varName) (',' type varName)*)?
            ---------------------------------------------
        """
        self.xml_data.append("<parameterList>")     # Xml rep: <parameterList>
        if self.tokenizer.next().value != ")":
            self.check_for_type()                   # Xml rep:     <keyword> type </keyword>
            self.check_for_identifier()             # Xml rep:     <identifier> varName </identifier>
            while self.tokenizer.next().value == ",":         
                self.check_for_value(",")           # Xml rep:     <symbol> , </symbol>
                self.check_for_type()               # Xml rep:     <keyword> type </keyword>
                self.check_for_identifier()         # Xml rep:     <identifier> varName </identifier>
        self.xml_data.append("</parameterList>")    # Xml rep: </parameterList>

    def compile_subroutine_body(self): 
        """
            Compile subroutine body.
            ----------------------------------
            Rule => '{' varDec* statements '}'
            ----------------------------------
        """
        self.xml_data.append("<subroutineBody>")    # Xml rep: <subroutineBody>
        self.check_for_value("{")                   # Xml rep:     <symbol> { </symbol>
        while self.tokenizer.next().value == "var":
            self.compile_var_dec()                  # Compile variable declarations.
        self.compile_statements()                   # Compile statements.

        self.check_for_value("}")                   # Xml rep:     <symbol> } </symbol>
        self.xml_data.append("</subroutineBody>")   # Xml rep: </subroutineBody>

    def compile_var_dec(self): 
        """
            Compile variable declarations.
            ----------------------------------------------
            Rule => 'var' type varName (',', varName)* ';'
            ----------------------------------------------
        """
        self.xml_data.append("<varDec>")            # Xml rep: <varDec>
        self.check_for_value("var")                 # Xml rep:     <keyword> var </keyword>
        self.check_for_type()                       # Xml rep:     <keyword> type </keyword>
        self.check_for_identifier()                 # Xml rep:     <identifier> varName </identifier>
        while self.tokenizer.next().value != ";":
            self.check_for_value(",")               # Xml rep:     <symbol> ; </symbol>
            self.check_for_identifier()             # Xml rep:     <identifier> varName </identifier>
        self.check_for_value(";")                   # Xml rep:     <symbol> ; </symbol>
        self.xml_data.append("</varDec>")           # Xml rep: </varDec>

    def compile_statements(self): 
        """
            Compile statements.
            -----------------------------------------------------------------------------------
            Rule => letStatement | ifStatement | whileStatement | doStatement | returnStatement
            -----------------------------------------------------------------------------------
        """
        self.xml_data.append("<statements>")        # Xml rep: <statements>
        while self.tokenizer.next().value != "}":
            token = self.tokenizer.next().value
            if token == 'let':
                self.compile_let_statement()        # Compile let statement.
            elif token == 'while':
                self.compile_while_statement()      # Compile while statement.
            elif token == 'if':
                self.compile_if_statement()         # Compile if statement.
            elif token == 'do':
                self.compile_do_statement()         # Compile do statement.
            elif token == 'return':
                self.compile_return_statement()     # Compile return statement.
        self.xml_data.append("</statements>")       # Xml rep: </statements>

    def compile_let_statement(self): 
        """
            Compile let statement.
            --------------------------------------------------------------
            Rule => 'let' varName ('[' expression ']')? '=' expression ';'
            --------------------------------------------------------------
        """
        self.xml_data.append("<letStatement>")      # Xml rep: <letStatement>
        self.check_for_value("let")                 # Xml rep:     <keyword> let </keyword>
        self.check_for_identifier()                 # Xml rep:     <identifier> varName </identifier>
        var = self.symbol_table.find(self.token.value) 
        if self.tokenizer.next().value == '[':
            self.check_for_value("[")               # Xml rep:     <symbol> [ </symbol>
            self.compile_expression("]")            # Compile expression.
            self.check_for_value("]")               # Xml rep:     <symbol> ] </symbol>
        self.check_for_value("=")                   # Xml rep:     <symbol> = </symbol>
        self.compile_expression(";")                # Compile expression.
        self.check_for_value(";")                   # Xml rep:     <symbol> ; </symbol>
        self.xml_data.append("</letStatement>")     # Xml rep: </letStatement>

    def compile_while_statement(self): 
        """
            Compile while statement.
            -----------------------------------------------------
            Rule => 'while' '(' expression ')' '{' statements '}'
            -----------------------------------------------------
        """
        self.xml_data.append("<whileStatement>")    # Xml rep: <whileStatement>
        self.check_for_value("while")               # Xml rep:     <keyword> while </keyword>
        self.check_for_value("(")                   # Xml rep:     <symbol> ( </symbol>
        self.compile_expression(")")                # Compile expression.
        self.check_for_value(")")                   # Xml rep:     <symbol> ) </symbol>
        self.check_for_value("{")                   # Xml rep:     <symbol> { </symbol>
        self.compile_statements()                   # Compile statements.
        self.check_for_value("}")                   # Xml rep:     <symbol> } </symbol>
        self.xml_data.append("</whileStatement>")   # Xml rep: </whileStatement>

    def compile_if_statement(self): 
        """
            Compile if statement.
            -------------------------------------------------------------------------------
            Rule => 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
            -------------------------------------------------------------------------------
        """
        self.xml_data.append("<ifStatement>")       # Xml rep: <ifStatement>
        self.check_for_value("if")                  # Xml rep:     <keyword> if </keyword>
        self.check_for_value("(")                   # Xml rep:     <symbol> ( </symbol>
        self.compile_expression(")")                # Compile expression.
        self.check_for_value(")")                   # Xml rep:     <symbol> ) </symbol>
        self.check_for_value("{")                   # Xml rep:     <symbol> { </symbol>
        self.compile_statements()                   # Compile statements.
        self.check_for_value("}")                   # Xml rep:     <symbol> } </symbol>
        if self.tokenizer.next().value == 'else':
            self.check_for_value('else')            # Xml rep:     <keyword> else </keyword>
            self.check_for_value('{')               # Xml rep:     <symbol> { </symbol>
            self.compile_statements()               # Compile statements.
            self.check_for_value('}')               # Xml rep:     <symbol> } </symbol>
        self.xml_data.append("</ifStatement>")      # Xml rep: </ifStatement>

    def compile_do_statement(self): 
        """
            Compile do statement.
            -------------------------------
            Rule => 'do' subroutineCall ';'
            -------------------------------
        """
        self.xml_data.append("<doStatement>")       # Xml rep: <doStatement>
        self.check_for_value("do")                  # Xml rep:     <keword> do </keyword>
        self.compile_subroutine_call()              # Compile subroutine call.
        self.check_for_value(";")                   # Xml rep:     <symbol> ; </symbol>
        self.xml_data.append("</doStatement>")      # Xml rep: </doStatement>

    def compile_return_statement(self): 
        """
            Compile return statement.
            --------------------------------
            Rule => 'return' expression? ';'
            --------------------------------
        """
        self.xml_data.append("<returnStatement>")   # Xml rep: <returnStatement>
        self.check_for_value("return")              # Xml rep:     <keword> return </keyword>
        if self.tokenizer.next().value != ";":
            self.compile_expression(';')
        self.check_for_value(";")                   # Xml rep:     <symbol> ; </symbol>
        self.xml_data.append("</returnStatement>")  # Xml rep: </returnStatement>
    
    def compile_subroutine_call(self): 
        """
            Compile subroutine call.
            ---------------------------------------------------------------------------------------------------------------
            Rule => subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
            ---------------------------------------------------------------------------------------------------------------
        """
        self.xml_data.append("<subroutineCall>")    # Xml rep: <subroutineCall>
        self.check_for_identifier()                 # Xml rep:     <identifier> subroutineName | (className | varName) </identifier>
        if self.tokenizer.next().value == ".":
            self.check_for_value(".")               # Xml rep:     <symbol> . </symbol>
            self.check_for_identifier()             # Xml rep:     <identifier> subroutineName </identifier>
        self.check_for_value("(")                   # Xml rep:     <symbol> ( </symbol>
        self.compile_expression_list()              # Compile expression list.
        self.check_for_value(")")                   # Xml rep:     <symbol> ) </symbol>
        self.xml_data.append("</subroutineCall>")   # Xml rep: </subroutineCall>

    def compile_expression(self, *end): 
        """
            Compile expression.
            -----------------------
            Rule => term (op term)*
            -----------------------
        """
        self.xml_data.append("<expression>")        # Xml rep:<expression>
        self.compile_term()                         # Compile term.
        while self.tokenizer.next().value not in end:
            self.check_for_operator()               # Xml rep:     <symbol> operator </symbol>
            self.compile_term()                     # Compile term.
        self.xml_data.append("</expression>")       # Xml rep: </expression>
        
    def compile_term(self): 
        """
            Compile term.
            ----------------------------------------------------------------------------------
            Rule => integerConstant | stringConstant | keywordConstant | unaryOp term | 
                    varName |  varName'[' expression ']' | subroutineCall | '(' expression ')'
            ----------------------------------------------------------------------------------
        """
        self.xml_data.append("<term>")                  # Xml rep: <term>
        if self.tokenizer.next().type in ["integerConstant", "stringConstant"] or self.tokenizer.next().value in KEYWORD_CONSANTS:
            self.token = self.tokenizer.advance()   
            self.xml_data.append(self.token.string())   # Xml rep:     <integerConstant | stringConstant | keyword> value </integerConstant | stringConstant | keyword>
        elif self.tokenizer.next().value in UNARY_OP:
            self.token = self.tokenizer.advance()
            self.xml_data.append(self.token.string())   # Xml rep:     <symbol> unaryOp </symbol>
            self.compile_term()                         # Compile term.
        elif self.tokenizer.next().value == "(":
            self.check_for_value("(")                   # Xml rep:     <symbol> ( </symbol>
            self.compile_expression(")")                # Compile expression.
            self.check_for_value(")")                   # Xml rep:     <symbol> ) </symbol>
        else:
            self.check_for_identifier()                 # Xml rep:     <identifier> varName </identifier>
            var = self.symbol_table.find(self.token.value)
            if self.tokenizer.next().value == "[":
                self.check_for_value("[")               # Xml rep:     <symbol> [ </symbol>
                self.compile_expression("]")            # Compile expression.
                self.check_for_value("]")               # Xml rep:     <symbol> ] </symbol>
            elif self.tokenizer.next().value == ".":
                self.check_for_value(".")               # Xml rep:     <symbol> . </symbol>
                self.check_for_identifier()             # Xml rep:     <identifier> subroutineName </identifier>
                self.check_for_value("(")               # Xml rep:     <symbol> ( </symbol>
                self.compile_expression_list()          # Compile expression list.
                self.check_for_value(")")               # Xml rep:     <symbol> ) </symbol>
            elif self.tokenizer.next().value == "(":
                self.check_for_value("(")               # Xml rep:     <symbol> ( </symbol>
                self.compile_expression_list()          # Compile expression list.
                self.check_for_value(")")               # Xml rep:     <symbol> ) </symbol>
        self.xml_data.append("</term>")                 # Xml rep: </term>

    def compile_expression_list(self): 
        """
            Compile expression list.
            ---------------------------------------
            Rule => (expression (',' expression)*)?
            ---------------------------------------
        """
        self.xml_data.append("<expressionList>")        # Xml rep: <expressionList>
        if self.tokenizer.next().value != ")":
            self.compile_expression(",", ")")           # Compile expression.
            while self.tokenizer.next().value == ",":
                self.check_for_value(",")               # Xml rep:     <symbol> , </symbol>
                self.compile_expression(",", ")")
        self.xml_data.append("</expressionList>")       # Xml rep: </expressionList>

    def export_xml(self, file_name):
        """ Export code structure to file in xml format. """
        with open("xml-export/{0}.structure.xml".format(file_name), "w") as xml_file:
            for line in self.xml_data:
                 xml_file.write(line + "\n")