import os
import subprocess
from lark import Lark
from langs.rust import *

def compile(code, file_name):
    parser = Lark(grammar, start=start, parser=parser_alg, transformer=Tree())
    try:
        parsed = parser.parse(code)
    except Exception as e:
        print(os.path.join(os.getcwd(), file_name + '.lm') + ':')
        print(e)
        exit() 
    try:
        subprocess.run(
            ['rustc', '-', '-o', file_name],
            input=str(parsed),
            text = True
        )
    except subprocess.SubprocessError as e:
        print("Compilation failed: ", e)

def run(code, file_name):
    compile(code, file_name)
    os.system(f"./{file_name}")

def source(code, file_name):
    parser = Lark(grammar, start=start, parser=parser_alg, transformer=Tree())
    
    with open(file_name + file_type, 'w+') as f:
        f.write(str(parser.parse(code)))
    print('Source code generated.')

def import_file(input_file):
    if not os.path.isfile(input_file):
        print('File not found. Please enter a valid path.')
        return
    if not input_file.endswith('.lm'):
        print("Please enter a '.lm' file")
        return
    return open(input_file, 'r').read()


