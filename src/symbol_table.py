"""
------------------------------------------------------------------------------
    @file       symbol_table.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      ...

    @version    0.1
    @date       2020-08-26

    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

from copy import copy

STATIC, ARGUMENT, LOCAL, FIELD = "static", "argument", "local", "field"

class SymbolTable(object):

    def __init__(self):
        """ Constructs symbol table object. """
        self.variables  = []    # List of all variables in certain scope.
        self.field_id   = 0     # Id of next field varibale.
        self.argumen_id = 0     # Id of next argument variable.
        self.local_id   = 0     # Id of next local variable.
        self.static_id  = 0     # Id of next static variable.

    def add(self, variable):
        """ Add new variable to variable list. """
        var = copy(variable)

        if var.kind == STATIC:
            var.id = self.static_id
            self.static_id += 1
        if var.kind == ARGUMENT:
            var.id = self.argumen_id
            self.argumen_id += 1
        if var.kind == LOCAL:
            var.id = self.local_id
            self.local_id += 1
        if var.kind == FIELD:
            var.id = self.field_id
            self.field_id += 1
            
        self.variables.append(var)

    def print(self):
        """ Print all variables to standard output. """
        for var in self.variables:
            print(var)

    def find(self, name):
        for var in self.variables:
            if var.name == name:
                return var