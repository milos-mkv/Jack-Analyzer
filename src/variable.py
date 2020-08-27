"""
------------------------------------------------------------------------------
    @file       variable.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      ...

    @version    0.1
    @date       2020-08-26

    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

class Variable(object):

    def __init__(self):
        """ Constructs variable object. """
        self.name = None    # Variable name (identifier)
        self.type = None    # Variable type (int, char, boolean, anyClassName)
        self.kind = None    # Variable kind (field, static, local, argument)
        self.id   = None    # Variable id   (id of certain kind)

    def __str__(self):
        """ Returns string representaion of object. """
        return "Name => {0}; Type => {1}; Kind => {2}; Id => {3};".format(self.name, self.type, self.kind, self.id)
