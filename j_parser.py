#!/bin/python3
import re
from pprint import pprint

def string_parser(string):
    if string[0] == '"':
        string = string[1:]
        index = string.find('"')
        return [string[:index], string[index+1:]]

def colon_parser(string):
    if string[0] == ":":
        return [":", string[1:]]

def number_parser(string):
    length = None
    if string:
        regex = re.findall("^(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)", string)
        if regex:
            length = len(regex[0])
            try:
                return [int(regex[0]), string[length:]]
            except ValueError:
                try:
                    return [float(regex[0]), string[length:]]
                except ValueError:
                    return None

def boolean_parser(string):
    if string[0:4] == "true":
        return [True, string[4:]]
    elif string[0:5] == "false":
        return [False, string[5:]]

def null_parser(string):
    if string[0:4] == "null":
        return [None, string[4:]]

def comma_parser(string):
    if string[0] == ",":
        return [",", string[1:]]

def object_parser(string):
    parsed_dict = {}
    if string[0] is not "{":
        return None
    string = string[1:]
    while string[0] is not "}":
        result = string_parser(string)
        if result is None:
            raise SyntaxError
        key = result[0]
        result = colon_parser(result[1])
        if result is None:
            raise SyntaxError
        string = result[1]
        result = jparser(string)
        if result is None:
            raise SyntaxError
        parsed_dict[key]=result[0]
        string = result[1]
        result = comma_parser(string)
        if result is not None:
            string = result[1]
        elif string[0] is not "}":
            raise SyntaxError
        if string[0] is "}":
            return [parsed_dict, string[1:]]
    return [parsed_dict, string[1:]]

def array_parser(string):
    parsed_array = []
    if string[0] is not "[":
        return None
    string = string[1:]
    while len(string) > 0:
        result = jparser(string)
        if result is not None:
            parsed_array.append(result[0])
            string = result[1]
            result = comma_parser(string)
            if result is not None:
                string = result[1]
            elif string[0] is not "]":
                raise SyntaxError
        if string[0] == "]":
            return [parsed_array, string[1:]]

def jparser(string):
    parsers = (string_parser, number_parser, boolean_parser,
               null_parser, array_parser, object_parser)

    for parser in parsers:
        result = parser(string)
        if result:
            return result

def clean(data):
    data = data.replace("\n", "")
    data = data.replace("\t", "")
    data = data.replace(" ", "")
    return data

def interface():
    parsed_data = None

    with open("data.json", "r") as f:
        data = f.read()
    #data = input()
    data = clean(data)

    if data[0] == "{":
        parsed_data = object_parser(data)
    elif data[0] == "[":
        parsed_data = array_parser(data)

    pprint(parsed_data[0], indent=2)

interface()
