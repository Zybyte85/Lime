from lark import Transformer

start = "start"
parser_alg = "lalr"
file_type = ".rs"

grammar = """
    start: statement+

    // Modular statement definitions
    statement: print_stmt
             | function_def
             | variable_def
    
    variable_def: TYPE NAME "=" expression

    return_statement: "return" expression

    print_stmt: "print" "(" expression ")"

    function_def: TYPE NAME "(" PARAMS? ")" "{" statement* return_statement? "}"
    PARAMS: (TYPE NAME) ("," TYPE NAME)*

    expression: raw_expr
    raw_expr: NUMBER | NAME | ESCAPED_STRING | math_expr | func_call_expr
    func_call_expr: func_call
    func_call: NAME "(" PARAMS? ")"
    math_expr: NUMBER (math_op NUMBER)+

    math_op: "+" | "-" | "*" | "/"
    TYPE: "void" | "int" | "float" | "str" | "bool"

    // Imported tokens for common patterns
    %import common.ESCAPED_STRING
    %import common.CNAME -> NAME
    %import common.SIGNED_NUMBER -> NUMBER

    // Whitespace handling
    %import common.WS
    %ignore WS
"""

class Tree(Transformer):
    def start(self, items):
        # Combine all statements into a single program
        return "\n".join(items)

    def statement(self, items):
        return items[0]

    def function_def(self, items):
        # Items include: return type, function name, params, body statements
        # TODO: Get parameters to work
        return_type, name, *body = items
        rust_return_type = self._map_type_to_rust(return_type)
        body_str = "\n    ".join(body)  # Indent inner statements
        return f"fn {name}() -> {rust_return_type} {{\n    {body_str}\n}}"

    def return_statement(self, items):
        return f"return {items[0]};"

    def variable_def(self, items):
        return f"let {items[1]}: {self._map_type_to_rust(items[0])} = {items[2]};"

    def _map_type_to_rust(self, c_type):
        # Helper to map C++ types to Rust types
        return {"void": "()", "int": "i32", "float": "f64", "string": "&str"}.get(
            c_type, "&str"
        )  # Default to `&str` if type isn't listed

    def PARAMS(self, items):
        # Convert parameter definitions into Rust format
        return [
            f"{items[i + 1]}: {self._map_type_to_rust(items[i])}"
            for i in range(0, len(items), 2)
        ]

    def print_stmt(self, items):
        return f"println!({items[0]});"

    def raw_expr(self, items):
        return items[0]

    def expression(self, items):
        print(items[0])
        word_list = items[0].replace('"', "").split()
        vars = [word[1:-1] for word in word_list if word.startswith("{") and word.endswith("}")]
        
        if not vars:
            return items[0]

        return f"{items[0]}" + "".join(f", {var}={var}" for var in vars)
    
    def func_call(self, items):
        return f"{items[0]};"

    def func_call_expr(self, items):
        return '"{' + items[0] + '}"' + f", {items[0]}={items[0]}()"

    def TYPE(self, item):
        return item

    def NAME(self, item):
        return item

    def ESCAPED_STRING(self, item):
        return item

    def NUMBER(self, item):
        return item
    
    def math_expr(self, items):
        return items[0]
