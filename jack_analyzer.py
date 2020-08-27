#!/usr/bin/python3

from src.tokenizer import Tokenizer
from src.parser import Parser
from src.constants import remove_all_comments
import os

def find_all_jack_files(directory):
    jack_files = []
    for r, d, f in os.walk(directory):
        for file in f:
            if '.jack' in file:
                jack_files.append(file)
    return jack_files

def compile_all_jack_files(jack_files):
    try:
        os.mkdir("xml-export")
    except:
        pass

    for jack_file in jack_files:
        with open(jack_file) as file:
            code = remove_all_comments(file.read())
            tokenizer = Tokenizer(code)
            tokenizer.export_xml(jack_file.replace(".jack", ""))
            try:
                parser = Parser(tokenizer)
                parser.export_xml(jack_file.replace(".jack", ""))
            except Exception as e:
                print(e)
                exit()

if __name__ == "__main__":
    jack_files = find_all_jack_files(".")
    compile_all_jack_files(jack_files)