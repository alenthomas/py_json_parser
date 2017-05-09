#!/bin/python3
import re

def string_parser(string):
    str_list = []
    if string[0] == '"':
        i = 1
        s = ''
        while string[i] is not '"':
            s = s + string[i]
            i = i + 1
        str_list.append(s)
        str_list.append(string[i+1:])
        return str_list

def colon_parser(string):
    str_list = []
    if string[0] == ':':
        str_list.append(string[0])
        str_list.append(string[1:])
        return str_list

def number_parser(string):
    exp = r'^[0-9]+'
    pattern = re.compile(exp)
    str_list = []
    if pattern.match(string[0]):
        s = ''
        i = 0
        while string[i] is not (',' or '}' or ']'):
            s = s + string[i]
            i = i+1
        str_list.append(s)
        str_list.append(string[i+1:])
        return str_list

def jparser(string):
    val = number_parser(string)
    if val:
        return val
    else:
        raise SyntaxError

def interface():
    json_string = input("Enter JSON: ").replace(' ', '').strip()
    partial = jparser(json_string)
    print(partial)

interface()
