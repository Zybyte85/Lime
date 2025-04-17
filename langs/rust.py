from lark import Transformer

parser_alg = "lalr"
file_type = ".rs"

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
        param_index = 2  # Skip till after name.
        if len(items) > 2 and isinstance(items[2], list):
            params = items[2]
            param_index = 3  # Skip to body after params.

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
        return items[0]

    def product_expr(self, items):
        return items[0]

    def addition(self, items):
        return f"{items[0]} + {items[1]}"

    def subtraction(self, items):
        return f"{items[0]} - {items[1]}"

    def multiplication(self, items):
        return f"{items[0]} * {items[1]}"

    def division(self, items):
        return f"{items[0]} / {items[1]}"

    def conditional(self, items):
        return items[0]

    def if_stmt(self, items):
        condition = items[0]
        body = items[1:]
        body_str = "\n        ".join(body)  # Indent inner statements
        return f"if {condition} {{\n        {body_str}\n    }}"

    def elif_stmt(self, items):
        return f"else {items[0]}"

    def else_stmt(self, items):
        body = items[0:]
        body_str = "\n        ".join(body)  # Indent inner statements
        return f"else {{\n        {body_str}\n    }}"

    def condition(self, items):
        return " ".join(items)

    def value(self, items):
        # Handle base values (numbers, variables, strings, function calls).
        value = items[0]

        # Special handling for string interpolation.
        if isinstance(value, str) and value.startswith('"') and "{" in value:
            content = value.strip('"')

            # Check for mixed content (text with variables and/or function calls).
            if "{" in content and "}" in content:
                # Extract all interpolated parts.
                parts = []
                format_str = content

                current_pos = 0
                while (
                    "{" in format_str[current_pos:] and "}" in format_str[current_pos:]
                ):
                    # Find the next interpolation.
                    start = format_str.find("{", current_pos)
                    end = format_str.find("}", start)

                    # If we found a valid interpolation.
                    if start != -1 and end != -1:
                        # Extract the variable or function call.
                        var = format_str[start + 1 : end]

                        # Found a function call.
                        if "(" in var and ")" in var:
                            format_str = (
                                format_str[:start] + "{}" + format_str[end + 1 :]
                            )
                            parts.append(var)

                        else:
                            # This is a simple variable, keep as is with Rust named parameter style.
                            pass

                        current_pos = start + 2  # Move past this interpolation.
                    else:
                        break

                if parts:
                    # We have function calls to add as parameters.
                    return f'"{format_str}"' + "".join(f", {part}" for part in parts)

                else:
                    # Only simple variables using Rust named parameter style.
                    return f'"{format_str}"'

            # Regular string without interpolation.
            return f'"{content}"'

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
