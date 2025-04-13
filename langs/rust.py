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

    // Rules aren't allowed inside terminals. Fixed by changing from terminal (uppercase) to non-terminal rule.
    function_def: TYPE NAME "(" parameter_list? ")" "{" statement* return_statement? "}"
    parameter_list: parameter ("," parameter)*
    parameter: TYPE NAME

    // Restructered expression rules to avoid ambiguity via precedence hierarchy.
    expression: sum_expr

    sum_expr: product_expr
           | sum_expr ("+" | "-") product_expr

    product_expr: value
                | product_expr ("*" | "/") value

    value: NUMBER
         | NAME
         | ESCAPED_STRING
         | func_call

    // Allow for function calls with or without arguments.
    func_call: NAME "(" argument_list? ")"
    argument_list: expression ("," expression)*   

    TYPE: "void" | "int" | "float" | "str" | "bool"

    // Imported tokens for common patterns
    %import common.ESCAPED_STRING
    %import common.CNAME -> NAME
    %import common.SIGNED_NUMBER -> NUMBER
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
        # item: return type, name, params, body
        return_type = items[0]
        name = items[1]
        
        # Handle parameters.
        params = []
        param_index = 2 # Skip till after name.
        if len(items) > 2 and isinstance(items[2], list):
            params = items[2]
            param_index = 3 # Skip to body after params.
            
        # Get body statements by slicing the items list.
        body = items[param_index:]
        
        # Map to Rust return type.
        rust_return_type = self._map_type_to_rust(return_type)
        
        # Build the function with parameters.
        params_str = ", ".join(params)
        body_str = "\n    ".join(body)  # Indent inner statements
        
        return f"fn {name}({params_str}) -> {rust_return_type} {{\n    {body_str}\n}}"

    def parameter_list(self, items):
        return items

    def parameter(self, items):
        return f"{items[1]}: {self._map_type_to_rust(items[0])}"

    def return_statement(self, items):
        return f"return {items[0]};"

    def variable_def(self, items):
        return f"let {items[1]}: {self._map_type_to_rust(items[0])} = {items[2]};"

    def _map_type_to_rust(self, c_type):
        # Helper to map C++ types to Rust types
        return {"void": "()", "int": "i32", "float": "f64", "string": "&str"}.get(
            c_type, "&str"
        )  # Default to `&str` if type isn't listed

    def print_stmt(self, items):
        return f"println!({items[0]});"

    # Expression handling methods.
    def expression(self, items):
        return items[0]

    def sum_expr(self, items):
        # Handle binary operations with + and - (return expression).
        if len(items) == 1:
            return items[0]

        # Binary operation.
        elif len(items) == 3:
            return f"{items[0]} {items[1]} {items[2]}"

        return items[0]  # Fallback.

    def product_expr(self, items):
        if len(items) == 1:
            return items[0]

        elif len(items) == 3:
            return f"{items[0]} {items[1]} {items[2]}"

        return items[0]

    def value(self, items):
        # Handle base values (numbers, variables, strings, function calls).
        value = items[0]
        
        # Special handling for string interpolation.
        if isinstance(value, str) and value.startswith('"') and "{" in value:
            word_list = value.replace('"', "").split()
            vars = [word[1:-1] for word in word_list if word.startswith("{") and word.endswith("}")]
            
            if not vars:
                return value

            return f"{value}" + "".join(f", {var}" for var in vars)
        
        return value

    def func_call(self, items):
        # Handle function calls with or without arguments.
        if len(items) == 1:
            return f"{items[0]}()"

        elif len(items) == 2:
            return f"{items[0]}({items[1]})"

    def argument_list(self, items):
        return ", ".join(items)

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