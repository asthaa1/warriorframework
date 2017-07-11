"""
check your privilege...
"""
import ast
import sys
import pprint

f = open(sys.argv[1])
root = ast.parse(f.read())
for child in ast.iter_child_nodes(root):
    if isinstance(child, ast.FunctionDef):
        if ast.get_docstring(child) is None:
            print child.name, "No docstring"
        for sub_child in ast.walk(child):
            if isinstance(sub_child, ast.Print):
                print "no print allow here"
            if isinstance(sub_child, ast.Return):
                print "Found a return here"
    elif isinstance(child, ast.ClassDef):
        if ast.get_docstring(child) is None:
            print child.name, "No docstring"
        for sub_child in ast.walk(child):
            if isinstance(sub_child, ast.FunctionDef) and ast.get_docstring(sub_child) is None:
                print sub_child.name, "No docstring"
            if isinstance(sub_child, ast.Print):
                print "no print allow here"
            if isinstance(sub_child, ast.Return):
                print "Found a return here"
            if isinstance(sub_child, ast.Attribute) and sub_child.attr == 'pSubStep':
                print "Found a p"
            if isinstance(sub_child, ast.Attribute) and sub_child.attr == 'report_substep_status':
                print "Found a report_p"
    elif isinstance(child, ast.Str):
        print child.lineno, ":", child.s
    elif isinstance(child, ast.Expr):
        license_text = \
'''
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
        print child.value.s[:50], ":", child.value.s == license_text
