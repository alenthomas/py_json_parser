#!/bin/python3
import re
from pprint import pprint

def string_parser(data):
    if data[0] == '"':
        data = data[1:]
        index = data.find('"')
        return [data[:index], data[index+1:]]

def colon_parser(data):
    if data[0] == ":":
        return [":", data[1:]]

def number_parser(data):
    length = None
    if data:
        match = re.match("^(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)", data)
        if match:
            length = len(match[0])
            try:
                return [int(match[0]), data[length:]]
            except ValueError:
                try:
                    return [float(match[0]), data[length:]]
                except ValueError:
                    return None

def boolean_parser(data):
    if data[0:4] == "true":
        return [True, data[4:]]
    elif data[0:5] == "false":
        return [False, data[5:]]

def null_parser(data):
    if data[0:4] == "null":
        return [None, data[4:]]

def comma_parser(data):
    if data[0] == ",":
        return [",", data[1:]]

def object_parser(data):
    parsed_dict = {}
    if data[0] is not "{":
        return None
    data = data[1:]
    while data[0] is not "}":
        result = string_parser(data)
        if result is None:
            raise SyntaxError
        key = result[0]
        result = colon_parser(result[1])
        if result is None:
            raise SyntaxError
        data = result[1]
        result = all_parser(data)
        if result is None:
            raise SyntaxError
        parsed_dict[key]=result[0]
        data = result[1]
        result = comma_parser(data)
        if result is not None:
            data = result[1]
        elif data[0] is not "}":
            raise SyntaxError
        if data[0] is "}":
            return [parsed_dict, data[1:]]
    return [parsed_dict, data[1:]]

def array_parser(data):
    parsed_array = []
    if data[0] is not "[":
        return None
    data = data[1:]
    while len(data) > 0:
        result = all_parser(data)
        if result is not None:
            parsed_array.append(result[0])
            data = result[1]
            result = comma_parser(data)
            if result is not None:
                data = result[1]
            elif data[0] is not "]":
                raise SyntaxError
        if data[0] == "]":
            return [parsed_array, data[1:]]

def all_parser(data):
    parsers = (string_parser, number_parser, boolean_parser,
               null_parser, array_parser, object_parser)

    for parser in parsers:
        result = parser(data)
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

    parsed_data = all_parser(data)
    pprint(parsed_data[0], indent=2)

if __name__ == "__main__":
    interface()
