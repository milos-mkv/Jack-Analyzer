"""
------------------------------------------------------------------------------
    @file       token.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      ...

    @version    0.1
    @date       2020-08-26

    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""

class Token(object):

    def __init__(self, type, value):
        """ Constructs token object. """
        self.type = type
        self.value = value

    def __str__(self):
        """ Returns string representation of token object in xml format. """
        return "<{0}> {1} </{0}>".format(self.type, self.value)