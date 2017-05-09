#!/bin/python3

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

def jparser(string):
    val = colon_parser(string)
    if val:
        return val
    else:
        raise SyntaxError

def interface():
    json_string = input("Enter JSON: ").replace(' ', '').strip()
    partial = jparser(json_string)
    print(partial)

interface()
