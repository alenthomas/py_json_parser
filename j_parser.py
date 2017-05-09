#!/bin/python3

def jparser(string):
    pass

def interface():
    json_string = input("Enter JSON: ").replace(' ', '').strip()
    partial = jparser(json_string)
    print(partial)

interface()
