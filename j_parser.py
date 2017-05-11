#!/bin/python3
import re
exp = r'^[0-9]+'
pattern = re.compile(exp)

def string_parser(string):
    str_list = []
    if string[0] == '"':
        i = 1
        s = ''
        while string[i] is not '"': # str[i:].find('"')
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
    str_list = []
    if pattern.match(string[0]):
        s = ''
        i = 0
        #while string[i] is not (',' or '}' or ']'):
        while pattern.match(string[i]):
            s = s + string[i]
            i = i+1
        str_list.append(s)
        str_list.append(string[i:])
        return str_list

def boolean_parser(string):
    str_list = []
    if string[0:4] == "true":
        str_list.append(string[0:4])
        str_list.append(string[4:])
        return str_list
    elif string[0:5] == "false":
        str_list.append(string[0:5])
        str_list.append(string[5:])
        return str_list

def null_parser(string):
    str_list = []
    if string[0:4] == "null":
        str_list.append(string[0:4])
        str_list.append(string[4:])
        return str_list

def comma_parser(string):
    str_list = []
    if string[0] == ',':
        str_list.append(string[0])
        str_list.append(string[1:])
        return str_list

def object_parser(string):
    str_list = []
    if string[0] == '{':
        str_list.append(string[0])
        if string[1] is not '"':
            raise SyntaxError
        str_list.append(string[1:])
        return str_list
    elif string[0] == "}":
        str_list.append(string[0])
        str_list.append(string[1:])
        return str_list
def array_parser(string):
    str_list = []
    #if string[0] == '[':
    str_list.append(string[0])
    str_list.append(string[1:])
    return str_list

def jparser(string):
    if not string:
        return final_val
    elif string[0] == '[' or string[0] == "]":
        result = array_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
    elif string[0] == "{" or string[0] == "}":
        result = object_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
        else:
            raise SyntaxError
    elif string[0] == '"':
        result=string_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
        else:
            raise SyntaxError
    elif pattern.match(string[0]):
        result = number_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
        else:
            raise SyntaxError
    elif string[0] == ":":
        result = colon_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
        else:
            raise SyntaxError
    elif string[0:4] == "true":
        result = boolean_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
        else:
            raise SyntaxError
    elif string[0:5] == "false":
        result = boolean_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
        else:
            raise SyntaxError
    elif string[0:4] == "null":
        result = null_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
        else:
            raise SyntaxError
    elif string[0] == ',':
        result = comma_parser(string)
        if result:
            #print(result)
            final_val.append(result[0])
            return jparser(result[1])
        else:
            raise SyntaxError
    else:
        raise SyntaxError

def clean(data):
    data = data.replace('\n', '')
    data = data.replace(' ', '')
    return data

def interface():
    global final_val
    final_val = []
    with open("data.json", "r") as f:
        data = f.read()
    data = clean(data)
    #json_string = input("Enter JSON: ").replace(' ', '').strip()
    partial = jparser(data)
    print(partial)

interface()
