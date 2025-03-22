import os
import subprocess
from lark import Lark
from lark.exceptions import UnexpectedToken, UnexpectedCharacters
from langs.rust import *


def get_bad_text(code, line, column):
    lines = code.splitlines()

    # Lines and column are 1 based.
    line = lines[line - 1]

    # Whitespace handling
    whitespace = len(line) - len(line.lstrip())
    column -= whitespace
    line = line.lstrip()

    return line[: column - 1] + f"\x1b[31m{line[column - 1]}\x1b[0m{line[column:]}"


def compile(code, file_name):
    parser = Lark(grammar, start=start, parser=parser_alg, transformer=Tree())
    try:
        parsed = parser.parse(code)
    except UnexpectedToken as e:
        print(f"""{os.path.join(os.getcwd(), file_name + '.lm')}:{e.line}:{e.column}
Error:\x1b[31m Unexpcted token:\x1b[0m '{e.token}'

    {get_bad_text(code, e.line, e.column)}""")
        exit()
    except UnexpectedCharacters as e:
        print(f"""{os.path.join(os.getcwd(), file_name + '.lm')}:{e.line}:{e.column}
Error:\x1b[31m Unexpcted character:\x1b[0m '{e.char}'

    {get_bad_text(code, e.line, e.column)}""")
        exit()
    try:
        subprocess.run(["rustc", "-", "-o", file_name], input=str(parsed), text=True)
    except subprocess.SubprocessError as e:
        print("Compilation failed: ", e)


def run(code, file_name):
    compile(code, file_name)
    os.system(f"./{file_name}")


def source(code, file_name):
    parser = Lark(grammar, start=start, parser=parser_alg, transformer=Tree())

    with open(file_name + file_type, "w+") as f:
        f.write(str(parser.parse(code)))
    print("Source code generated.")


def import_file(input_file):
    if not os.path.isfile(input_file):
        print("File not found. Please enter a valid path.")
        return
    if not input_file.endswith(".lm"):
        print("Please enter a '.lm' file")
        return
    return open(input_file, "r").read()
