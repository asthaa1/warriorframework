"""
check your privilege...
"""
import ast
import sys

f = open(sys.argv[1])
root = ast.parse(f.read())
for child in ast.iter_child_nodes(root):
    if isinstance(child, ast.FunctionDef):
        print "Checking docstring in func"
        for sub_child in ast.walk(child):
            if isinstance(sub_child, ast.Print):
                print "no print allow here"
    elif isinstance(child, ast.ClassDef):
        for sub_child in ast.walk(child):
            if isinstance(sub_child, ast.Print):
                print "no print allow here"
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
