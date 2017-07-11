"""
Use ast module to check custom rules enforced by warrior dev team
"""
import ast
import sys
import pprint

def func_check(node, kw=False):
    '''
    Function specific check
        Action - check return type
        Action - check pstep/psubstep buddy with report_step/report_substep_status
        check docstring
        check print statement - should use print_utils
        scan for class - class check
        scan for function - recursive function check
    '''
    status = True
    if ast.get_docstring(node) is None:
        print node.name, "doesn't contain any docstring"
        status = False

    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.FunctionDef):
            if kw and child.name.startswith("_"):
                print node.name, child.name, "should move to utils"
                status = False
            tmp_status = func_check(child, kw)
            status &= tmp_status
        elif isinstance(child, ast.ClassDef):
            tmp_status = class_check(child, kw)
            status &= tmp_status
        elif isinstance(child, ast.Print):
            print "no print allow here"
        elif isinstance(child, ast.Return):
            print "Found a return here"
        elif isinstance(child, ast.Attribute) and child.attr == 'pSubStep':
            print "Found a p"
        elif isinstance(child, ast.Attribute) and child.attr == 'report_substep_status':
            print "Found a report_p"

    return status

def class_check(node, kw=False):
    '''
    Class specific check
        Action - check private method, move to utils
        check docstring
        scan for class - recursive class check
        scan for function - function check
    '''
    status = True
    if ast.get_docstring(node) is None:
        print node.name, "doesn't contain any docstring"
        status = False

    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.FunctionDef):
            if kw and child.name.startswith("_"):
                print node.name, child.name, "should move to utils"
                status = False
            tmp_status = func_check(child, kw)
            status &= tmp_status
        elif isinstance(child, ast.ClassDef):
            tmp_status = class_check(child, kw)
            status &= tmp_status

    return status

def main(kw=False):
    """
    main method to build ast tree and call subseq functions
    Top level check
        license info
        scan for class - class check
        scan for function - function check
    """
    f = open(sys.argv[1])
    root = ast.parse(f.read())
    have_license = False
    status = True
    for child in ast.iter_child_nodes(root):
        if isinstance(child, ast.FunctionDef):
            status &= func_check(child, kw)
        elif isinstance(child, ast.ClassDef):
            status &= class_check(child, kw)
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
            if child.value.s == license_text:
                have_license = True

        status &= have_license
        return status

if __name__ == "__main__":
    if main():
        print "PASS"
        exit(0)
    else:
        print "FAIL"
        exit(1)
