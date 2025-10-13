import ply.lex as lex
import ply.yacc as yacc
from typing import Dict, List, Tuple, Any, Optional

class SemanticAnalyzer:
    """Semantic analyzer for variable declarations and type checking"""
    def __init__(self):
        self.variables: Dict[str, Dict[str, Any]] = {}  # Store declared variables

    def declare_variable(self, name: str, var_type: str, line_no: int = 1):
        """Declare a variable with type checking"""
        if name in self.variables:
            return f"Semantic Error: Variable '{name}' already declared at line {self.variables[name]['line_no']}"

        self.variables[name] = {
            'type': var_type,
            'line_no': line_no,
            'initialized': False
        }
        return None

    def check_variable(self, name: str) -> Optional[str]:
        """Check if variable is declared"""
        if name not in self.variables:
            return f"Semantic Error: Variable '{name}' not declared"
        return None

    def get_expression_type(self, expression_node) -> str:
        """Determine the type of an expression based on its parse tree structure"""
        if not expression_node or not hasattr(expression_node, 'children'):
            return 'unknown'

        # Check if this is an expression with operators
        operands_and_types = self._collect_operands_and_operators(expression_node)

        if len(operands_and_types['operands']) > 1:
            # This is a complex expression with operators
            return self._analyze_expression_with_operators(operands_and_types)
        elif len(operands_and_types['operands']) == 1:
            # Single operand expression
            return operands_and_types['operands'][0]
        else:
            # Fallback to old method
            return self._find_single_value_type(expression_node)

    def _collect_operands_and_operators(self, node):
        """Collect all operands and operators from an expression tree"""
        operands = []
        operators = []

        def traverse(node):
            if not hasattr(node, 'children'):
                return

            for child in node.children:
                if hasattr(child, 'production_rule'):
                    # Check for operators
                    if '+ →' in child.production_rule:
                        operators.append('+')
                    elif '* →' in child.production_rule:
                        operators.append('*')
                    elif 'ID →' in child.production_rule:
                        # Extract variable name
                        var_name = child.production_rule.split('ID → ')[1]
                        if var_name in self.variables:
                            operands.append(self.variables[var_name]['type'])
                        else:
                            operands.append('undeclared')
                    elif 'NUMBER →' in child.production_rule:
                        operands.append('int')
                    elif 'DECIMAL →' in child.production_rule:
                        operands.append('double')
                    elif 'STRING →' in child.production_rule:
                        operands.append('string')
                    elif 'BOOLEAN →' in child.production_rule:
                        operands.append('bool')

                # Recursively traverse children
                traverse(child)

        traverse(node)
        return {'operands': operands, 'operators': operators}

    def _analyze_expression_with_operators(self, operands_and_types):
        """Analyze expressions with operators for type compatibility"""
        operands = operands_and_types['operands']
        operators = operands_and_types['operators']

        if not operands:
            return 'unknown'

        # For expressions with operators, check type compatibility
        first_type = operands[0]

        for i, op in enumerate(operators):
            if i + 1 < len(operands):
                second_type = operands[i + 1]

                # Check if operation is valid between these types
                if not self._is_operation_valid(first_type, op, second_type):
                    return 'type_error'

                # For now, assume the result type is the same as the first operand
                # In a more sophisticated system, you'd have proper type promotion rules
                first_type = self._get_result_type(first_type, op, second_type)

        return first_type

    def _is_operation_valid(self, type1, operator, type2):
        """Check if an operation is valid between two types"""
        # Define valid operations for each type combination
        valid_ops = {
            ('int', '+', 'int'): True,
            ('int', '*', 'int'): True,
            ('double', '+', 'double'): True,
            ('double', '*', 'double'): True,
            ('double', '+', 'int'): True,
            ('int', '+', 'double'): True,
            ('double', '*', 'int'): True,
            ('int', '*', 'double'): True,
            ('string', '+', 'string'): True,  # String concatenation
        }

        return valid_ops.get((type1, operator, type2), False)

    def _get_result_type(self, type1, operator, type2):
        """Get the result type of an operation between two types"""
        # Simple type promotion rules
        if type1 == 'double' or type2 == 'double':
            return 'double'
        elif type1 == 'string' or type2 == 'string':
            return 'string'
        else:
            return type1

    def _find_single_value_type(self, node):
        """Find the type of a single value (fallback method)"""
        if not hasattr(node, 'children'):
            return 'unknown'

        for child in node.children:
            if hasattr(child, 'production_rule'):
                if 'NUMBER →' in child.production_rule:
                    return 'int'
                elif 'DECIMAL →' in child.production_rule:
                    return 'double'
                elif 'STRING →' in child.production_rule:
                    return 'string'
                elif 'BOOLEAN →' in child.production_rule:
                    return 'bool'
                elif 'ID →' in child.production_rule:
                    # Extract variable name
                    var_name = child.production_rule.split('ID → ')[1]
                    if var_name in self.variables:
                        return self.variables[var_name]['type']
                    return 'undeclared'

            # Recursively search in children
            result = self._find_single_value_type(child)
            if result != 'unknown':
                return result

        return 'unknown'

    def check_type_compatibility(self, declared_type: str, expression_node, var_name: str) -> Optional[str]:
        """Check if the expression type is compatible with the declared variable type"""
        expr_type = self.get_expression_type(expression_node)

        if expr_type == 'undeclared':
            return None  # This will be caught by check_variable

        if expr_type == 'unknown':
            return None  # Can't determine type, assume it's okay for now

        if expr_type == 'type_error':
            # Get more specific error message for type errors in expressions
            operands_and_types = self._collect_operands_and_operators(expression_node)
            return self._generate_type_error_message(operands_and_types, var_name)

        # Type compatibility rules
        if declared_type == expr_type:
            return None  # Perfect match

        # Some implicit conversions could be allowed here if needed
        # For now, we require exact type matches

        type_names = {
            'int': 'integer',
            'double': 'decimal',
            'string': 'string',
            'bool': 'boolean'
        }

        declared_name = type_names.get(declared_type, declared_type)
        expr_name = type_names.get(expr_type, expr_type)

        return f"Semantic Error: Cannot assign {expr_name} value to {declared_name} variable '{var_name}'"

    def _generate_type_error_message(self, operands_and_types, var_name):
        """Generate a specific error message for type errors in expressions"""
        operands = operands_and_types['operands']
        operators = operands_and_types['operators']

        if len(operands) >= 2 and len(operators) >= 1:
            type_names = {
                'int': 'integer',
                'double': 'decimal',
                'string': 'string',
                'bool': 'boolean'
            }

            type1_name = type_names.get(operands[0], operands[0])
            type2_name = type_names.get(operands[1], operands[1])
            op = operators[0]

            return f"Semantic Error: Cannot perform '{op}' operation between {type1_name} and {type2_name} in assignment to variable '{var_name}'"

        return f"Semantic Error: Type mismatch in expression assigned to variable '{var_name}'"

    def reset(self):
        """Reset the analyzer for new input"""
        self.variables = {}

class ParseNode:
    """Node for BNF derivation tree representation"""
    def __init__(self, value: str, children: List['ParseNode'] = None, production_rule: str = None):
        self.value = value
        self.children = children or []
        self.production_rule = production_rule  # Store the BNF production rule used

    def add_child(self, child: 'ParseNode'):
        self.children.append(child)

    def display(self, level: int = 0, prefix: str = ""):
        """Display BNF derivation tree in a structured format"""
        display_text = self.production_rule if self.production_rule else self.value
        print(f"{prefix}{'├── ' if level > 0 else ''}{display_text}")
        for i, child in enumerate(self.children):
            is_last = i == len(self.children) - 1
            new_prefix = prefix + ("    " if level > 0 and is_last else "│   " if level > 0 else "")
            child.display(level + 1, new_prefix)

class BNFDerivationGenerator:
    """Generate BNF derivation sequence using only expression, term, and factor"""

    def __init__(self):
        self.derivation_steps = []

    def generate_derivation_sequence(self, parse_tree, input_expression):
        """Generate BNF derivation sequence using only expression, term, factor"""
        self.derivation_steps = []

        if not parse_tree:
            return []

        # Analyze the input expression to determine structure
        self._analyze_expression_structure(input_expression)
        return self.derivation_steps

    def _analyze_expression_structure(self, expression):
        """Analyze expression structure and generate appropriate BNF rules"""
        # Remove spaces for easier parsing
        expr = expression.replace(' ', '')

        # Start with expression as the root
        self._generate_expression_rules(expr)

    def _generate_expression_rules(self, expr):
        """Generate BNF rules for expression based on structure"""
        # Check for addition at the top level (not inside parentheses)
        plus_pos = self._find_operator_position(expr, '+')
        if plus_pos != -1:
            self.derivation_steps.append("<expression> ::= <expression> + <term>")
            # Process left side (expression)
            left_part = expr[:plus_pos]
            self._generate_expression_rules(left_part)
            # Process right side (term)
            right_part = expr[plus_pos + 1:]
            self._generate_term_rules(right_part)
        else:
            # No addition, so expression -> term
            self.derivation_steps.append("<expression> ::= <term>")
            self._generate_term_rules(expr)

    def _generate_term_rules(self, expr):
        """Generate BNF rules for term based on structure"""
        # Check for multiplication at the top level (not inside parentheses)
        mult_pos = self._find_operator_position(expr, '*')
        if mult_pos != -1:
            self.derivation_steps.append("<term> ::= <term> * <factor>")
            # Process left side (term)
            left_part = expr[:mult_pos]
            self._generate_term_rules(left_part)
            # Process right side (factor)
            right_part = expr[mult_pos + 1:]
            self._generate_factor_rules(right_part)
        else:
            # No multiplication, so term -> factor
            self.derivation_steps.append("<term> ::= <factor>")
            self._generate_factor_rules(expr)

    def _generate_factor_rules(self, expr):
        """Generate BNF rules for factor based on structure"""
        # Check if it's parenthesized
        if expr.startswith('(') and expr.endswith(')'):
            self.derivation_steps.append("<factor> ::= ( <expression> )")
            # Process the expression inside parentheses
            inner_expr = expr[1:-1]
            self._generate_expression_rules(inner_expr)
        else:
            # It's a terminal (identifier or number)
            if expr.isdigit() or (expr.replace('.', '').isdigit() and expr.count('.') <= 1):
                # It's a number
                self.derivation_steps.append(f"<factor> ::= {expr}")
            else:
                # It's an identifier
                self.derivation_steps.append(f"<factor> ::= {expr}")

    def _find_operator_position(self, expr, operator):
        """Find the position of operator at the top level (not inside parentheses)"""
        paren_count = 0
        for i in range(len(expr) - 1, -1, -1):  # Search from right to left for left-associativity
            char = expr[i]
            if char == ')':
                paren_count += 1
            elif char == '(':
                paren_count -= 1
            elif char == operator and paren_count == 0:
                return i
        return -1

    def display_derivation(self):
        """Display the BNF derivation sequence"""
        print("\nBNF DERIVATION SEQUENCE:")
        print("=" * 80)

        # Show each derivation step as a production rule
        for i, step in enumerate(self.derivation_steps, 1):
            print(f"{step}")

        print("=" * 80)

class GrammarParser:
    def __init__(self):
        self.tokens = ('ID', 'NUMBER', 'DECIMAL', 'STRING', 'BOOL', 'INT', 'DOUBLE', 'STRING_TYPE', 'BOOL_TYPE',
                      'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'ASSIGN', 'LPAREN', 'RPAREN',
                      'LBRACE', 'RBRACE', 'SEMICOLON', 'IF', 'ELSE', 'WHILE', 'RETURN', 'VOID',
                      'GT', 'LT', 'GE', 'LE', 'EQ', 'NE')
        self.semantic_analyzer = SemanticAnalyzer()
        self.lexemes_tokens = []
        self.parse_tree = None
        self.parsing_successful = False
        self.semantic_errors = []
        self.bnf_derivation = BNFDerivationGenerator()
        self.input_expression = ""

        # Build lexer and parser
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)

    # Token rules
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_ASSIGN = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEMICOLON = r';'
    t_GE = r'>='
    t_LE = r'<='
    t_EQ = r'=='
    t_NE = r'!='
    t_GT = r'>'
    t_LT = r'<'
    t_ignore = ' \t'  # Ignore spaces and tabs

    # Reserved words
    reserved = {
        'int': 'INT',
        'double': 'DOUBLE',
        'string': 'STRING_TYPE',
        'bool': 'BOOL_TYPE',
        'true': 'BOOL',
        'false': 'BOOL',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'return': 'RETURN',
        'void': 'VOID',
    }

    def t_STRING(self, t):
        r'"[^"]*"'
        return t

    def t_DECIMAL(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Lexical Error: Illegal character '{t.value[0]}' at position {t.lexpos}")
        t.lexer.skip(1)

    # Grammar rules with parse tree construction and semantic analysis
    def p_statement_declaration(self, p):
        '''statement : declaration'''
        p[0] = ParseNode('statement', production_rule='statement → declaration')
        p[0].add_child(p[1])

    def p_statement_expression(self, p):
        '''statement : expression'''
        p[0] = ParseNode('statement', production_rule='statement → expression')
        p[0].add_child(p[1])

    def p_statement_if(self, p):
        '''statement : if_statement'''
        p[0] = ParseNode('statement', production_rule='statement → if_statement')
        p[0].add_child(p[1])

    def p_statement_while(self, p):
        '''statement : while_statement'''
        p[0] = ParseNode('statement', production_rule='statement → while_statement')
        p[0].add_child(p[1])

    def p_declaration_int(self, p):
        '''declaration : INT ID ASSIGN expression'''
        p[0] = ParseNode('declaration', production_rule='declaration → INT ID ASSIGN expression')
        p[0].add_child(ParseNode('INT', production_rule='INT → int'))
        p[0].add_child(ParseNode(f'ID({p[2]})', production_rule=f'ID → {p[2]}'))
        p[0].add_child(ParseNode('ASSIGN', production_rule='ASSIGN → ='))
        p[0].add_child(p[4])

        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'int', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
        else:
            # Check type compatibility
            type_error = self.semantic_analyzer.check_type_compatibility('int', p[4], p[2])
            if type_error:
                self.semantic_errors.append(type_error)
            else:
                self.semantic_analyzer.variables[p[2]]['initialized'] = True

    def p_declaration_double(self, p):
        '''declaration : DOUBLE ID ASSIGN expression'''
        p[0] = ParseNode('declaration', production_rule='declaration → DOUBLE ID ASSIGN expression')
        p[0].add_child(ParseNode('DOUBLE', production_rule='DOUBLE → double'))
        p[0].add_child(ParseNode(f'ID({p[2]})', production_rule=f'ID → {p[2]}'))
        p[0].add_child(ParseNode('ASSIGN', production_rule='ASSIGN → ='))
        p[0].add_child(p[4])

        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'double', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
        else:
            # Check type compatibility
            type_error = self.semantic_analyzer.check_type_compatibility('double', p[4], p[2])
            if type_error:
                self.semantic_errors.append(type_error)
            else:
                self.semantic_analyzer.variables[p[2]]['initialized'] = True

    def p_declaration_string(self, p):
        '''declaration : STRING_TYPE ID ASSIGN expression'''
        p[0] = ParseNode('declaration', production_rule='declaration → STRING_TYPE ID ASSIGN expression')
        p[0].add_child(ParseNode('STRING_TYPE', production_rule='STRING_TYPE → string'))
        p[0].add_child(ParseNode(f'ID({p[2]})', production_rule=f'ID → {p[2]}'))
        p[0].add_child(ParseNode('ASSIGN', production_rule='ASSIGN → ='))
        p[0].add_child(p[4])

        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'string', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
        else:
            # Check type compatibility
            type_error = self.semantic_analyzer.check_type_compatibility('string', p[4], p[2])
            if type_error:
                self.semantic_errors.append(type_error)
            else:
                self.semantic_analyzer.variables[p[2]]['initialized'] = True

    def p_declaration_bool(self, p):
        '''declaration : BOOL_TYPE ID ASSIGN expression'''
        p[0] = ParseNode('declaration', production_rule='declaration → BOOL_TYPE ID ASSIGN expression')
        p[0].add_child(ParseNode('BOOL_TYPE', production_rule='BOOL_TYPE → bool'))
        p[0].add_child(ParseNode(f'ID({p[2]})', production_rule=f'ID → {p[2]}'))
        p[0].add_child(ParseNode('ASSIGN', production_rule='ASSIGN → ='))
        p[0].add_child(p[4])

        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'bool', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
        else:
            # Check type compatibility
            type_error = self.semantic_analyzer.check_type_compatibility('bool', p[4], p[2])
            if type_error:
                self.semantic_errors.append(type_error)
            else:
                self.semantic_analyzer.variables[p[2]]['initialized'] = True

    def p_declaration_no_init_int(self, p):
        '''declaration : INT ID'''
        p[0] = ParseNode('declaration', production_rule='declaration → INT ID')
        p[0].add_child(ParseNode('INT', production_rule='INT → int'))
        p[0].add_child(ParseNode(f'ID({p[2]})', production_rule=f'ID → {p[2]}'))

        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'int', p.lineno(2))
        if error:
            self.semantic_errors.append(error)

    def p_declaration_no_init_double(self, p):
        '''declaration : DOUBLE ID'''
        p[0] = ParseNode('declaration', production_rule='declaration → DOUBLE ID')
        p[0].add_child(ParseNode('DOUBLE', production_rule='DOUBLE → double'))
        p[0].add_child(ParseNode(f'ID({p[2]})', production_rule=f'ID → {p[2]}'))

        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'double', p.lineno(2))
        if error:
            self.semantic_errors.append(error)

    def p_declaration_no_init_string(self, p):
        '''declaration : STRING_TYPE ID'''
        p[0] = ParseNode('declaration', production_rule='declaration → STRING_TYPE ID')
        p[0].add_child(ParseNode('STRING_TYPE', production_rule='STRING_TYPE → string'))
        p[0].add_child(ParseNode(f'ID({p[2]})', production_rule=f'ID → {p[2]}'))

        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'string', p.lineno(2))
        if error:
            self.semantic_errors.append(error)

    def p_declaration_no_init_bool(self, p):
        '''declaration : BOOL_TYPE ID'''
        p[0] = ParseNode('declaration', production_rule='declaration → BOOL_TYPE ID')
        p[0].add_child(ParseNode('BOOL_TYPE', production_rule='BOOL_TYPE → bool'))
        p[0].add_child(ParseNode(f'ID({p[2]})', production_rule=f'ID → {p[2]}'))

        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'bool', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
    def p_expression(self, p):
        '''expression : term expression_prime'''
        p[0] = ParseNode('expression', production_rule='expression → term expression_prime')
        p[0].add_child(p[1])  # term
        p[0].add_child(p[2])  # expression_prime

    def p_expression_prime_plus(self, p):
        '''expression_prime : PLUS term expression_prime'''
        p[0] = ParseNode("expression_prime", production_rule='expression_prime → + term expression_prime')
        p[0].add_child(ParseNode('+', production_rule='+ → +'))
        p[0].add_child(p[2])  # term
        p[0].add_child(p[3])  # expression_prime

    def p_expression_prime_epsilon(self, p):
        '''expression_prime : '''
        p[0] = ParseNode("expression_prime", production_rule='expression_prime → ε')

    def p_term(self, p):
        '''term : factor term_prime'''
        p[0] = ParseNode('term', production_rule='term → factor term_prime')
        p[0].add_child(p[1])  # factor
        p[0].add_child(p[2])  # term_prime

    def p_term_prime_multiply(self, p):
        '''term_prime : MULTIPLY factor term_prime'''
        p[0] = ParseNode("term_prime", production_rule='term_prime → * factor term_prime')
        p[0].add_child(ParseNode('*', production_rule='* → *'))
        p[0].add_child(p[2])  # factor
        p[0].add_child(p[3])  # term_prime

    def p_term_prime_epsilon(self, p):
        '''term_prime : '''
        p[0] = ParseNode("term_prime", production_rule='term_prime → ε')

    def p_factor_paren(self, p):
        '''factor : LPAREN expression RPAREN'''
        p[0] = ParseNode('factor', production_rule='factor → ( expression )')
        p[0].add_child(ParseNode('(', production_rule='( → ('))
        p[0].add_child(p[2])  # expression
        p[0].add_child(ParseNode(')', production_rule=') → )'))

    def p_factor_id(self, p):
        '''factor : ID'''
        p[0] = ParseNode('factor', production_rule=f'factor → ID')
        p[0].add_child(ParseNode(f'ID({p[1]})', production_rule=f'ID → {p[1]}'))

        # Semantic analysis - Check if variable is declared
        error = self.semantic_analyzer.check_variable(p[1])
        if error:
            self.semantic_errors.append(error)

    def p_factor_number(self, p):
        '''factor : NUMBER'''
        p[0] = ParseNode('factor', production_rule=f'factor → NUMBER')
        p[0].add_child(ParseNode(f'NUMBER({p[1]})', production_rule=f'NUMBER → {p[1]}'))

    def p_factor_decimal(self, p):
        '''factor : DECIMAL'''
        p[0] = ParseNode('factor', production_rule=f'factor → DECIMAL')
        p[0].add_child(ParseNode(f'DECIMAL({p[1]})', production_rule=f'DECIMAL → {p[1]}'))

    def p_factor_string(self, p):
        '''factor : STRING'''
        p[0] = ParseNode('factor', production_rule=f'factor → STRING')
        p[0].add_child(ParseNode(f'STRING({p[1]})', production_rule=f'STRING → {p[1]}'))

    def p_factor_bool(self, p):
        '''factor : BOOL'''
        p[0] = ParseNode('factor', production_rule=f'factor → BOOL')
        p[0].add_child(ParseNode(f'BOOL({p[1]})', production_rule=f'BOOL → {p[1]}'))

    # If statement grammar rules
    def p_if_statement(self, p):
        '''if_statement : IF LPAREN condition RPAREN'''
        p[0] = ParseNode('if_statement', production_rule='if_statement → IF LPAREN condition RPAREN')
        p[0].add_child(ParseNode('IF', production_rule='IF → if'))
        p[0].add_child(ParseNode('LPAREN', production_rule='LPAREN → ('))
        p[0].add_child(p[3])  # condition
        p[0].add_child(ParseNode('RPAREN', production_rule='RPAREN → )'))

    # While statement grammar rules
    def p_while_statement(self, p):
        '''while_statement : WHILE LPAREN condition RPAREN'''
        p[0] = ParseNode('while_statement', production_rule='while_statement → WHILE LPAREN condition RPAREN')
        p[0].add_child(ParseNode('WHILE', production_rule='WHILE → while'))
        p[0].add_child(ParseNode('LPAREN', production_rule='LPAREN → ('))
        p[0].add_child(p[3])  # condition
        p[0].add_child(ParseNode('RPAREN', production_rule='RPAREN → )'))

    # Condition grammar rules for comparison expressions
    def p_condition_gt(self, p):
        '''condition : expression GT expression'''
        p[0] = ParseNode('condition', production_rule='condition → expression GT expression')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('GT', production_rule='GT → >'))
        p[0].add_child(p[3])  # right expression

    def p_condition_lt(self, p):
        '''condition : expression LT expression'''
        p[0] = ParseNode('condition', production_rule='condition → expression LT expression')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('LT', production_rule='LT → <'))
        p[0].add_child(p[3])  # right expression

    def p_condition_ge(self, p):
        '''condition : expression GE expression'''
        p[0] = ParseNode('condition', production_rule='condition → expression GE expression')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('GE', production_rule='GE → >='))
        p[0].add_child(p[3])  # right expression

    def p_condition_le(self, p):
        '''condition : expression LE expression'''
        p[0] = ParseNode('condition', production_rule='condition → expression LE expression')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('LE', production_rule='LE → <='))
        p[0].add_child(p[3])  # right expression

    def p_condition_eq(self, p):
        '''condition : expression EQ expression'''
        p[0] = ParseNode('condition', production_rule='condition → expression EQ expression')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('EQ', production_rule='EQ → =='))
        p[0].add_child(p[3])  # right expression

    def p_condition_ne(self, p):
        '''condition : expression NE expression'''
        p[0] = ParseNode('condition', production_rule='condition → expression NE expression')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('NE', production_rule='NE → !='))
        p[0].add_child(p[3])  # right expression

    def p_error(self, p):
        if p:
            print(f"Syntax Error: Unexpected token {p.type} ('{p.value}') at position {p.lexpos}")
        else:
            print("Syntax Error: Unexpected end of input")
        self.parsing_successful = False

    def tokenize_input(self, input_string: str):
        """Tokenize input and populate lexemes_tokens list"""
        self.lexemes_tokens = []
        self.semantic_analyzer.reset()  # Reset semantic analyzer

        self.lexer.input(input_string)

        print("\n" + "="*60)
        print("LEXICAL ANALYSIS")
        print("="*60)
        print(f"{'Lexeme':<15} {'Token Type':<15} {'Category':<12} {'Position':<10}")
        print("-"*70)

        while True:
            tok = self.lexer.token()
            if not tok:
                break

            # Categorize tokens according to your specification
            token_category = ""
            token_type = ""

            if tok.type in ['INT', 'DOUBLE', 'STRING_TYPE', 'BOOL_TYPE', 'IF', 'ELSE', 'WHILE', 'RETURN', 'VOID']:
                token_category = "Keywords"
                token_type = {
                    'INT': 'int',
                    'DOUBLE': 'double',
                    'STRING_TYPE': 'string',
                    'BOOL_TYPE': 'bool',
                    'IF': 'if',
                    'ELSE': 'else',
                    'WHILE': 'while',
                    'RETURN': 'return',
                    'VOID': 'void'
                }.get(tok.type)
            elif tok.type == 'ID':
                token_category = "Identifier"
                token_type = "identifier"
            elif tok.type in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'ASSIGN', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE']:
                token_category = "Operator"
                token_type = {
                    'PLUS': '+',
                    'MINUS': '-',
                    'MULTIPLY': '*',
                    'DIVIDE': '/',
                    'ASSIGN': '=',
                    'GT': '>',
                    'LT': '<',
                    'GE': '>=',
                    'LE': '<=',
                    'EQ': '==',
                    'NE': '!='
                }.get(tok.type)
            elif tok.type in ['LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON']:
                token_category = "Delimiter"
                token_type = {
                    'LPAREN': '(',
                    'RPAREN': ')',
                    'LBRACE': '{',
                    'RBRACE': '}',
                    'SEMICOLON': ';'
                }.get(tok.type)
            elif tok.type in ['NUMBER', 'DECIMAL', 'STRING', 'BOOL']:
                token_category = "Literal"
                token_type = {
                    'NUMBER': 'integer',
                    'DECIMAL': 'decimal',
                    'STRING': 'string',
                    'BOOL': 'boolean'
                }.get(tok.type)
            else:
                token_category = "Other"
                token_type = tok.type

            self.lexemes_tokens.append((tok.value, token_type, token_category))

            print(f"{str(tok.value):<15} {token_type:<15} {token_category:<12} {tok.lexpos:<10}")

        print("="*70)

    def parse_input(self, input_string: str):
        """Parse the input string and generate parse tree"""
        self.parsing_successful = True
        self.semantic_errors = []
        self.input_expression = input_string

        try:
            # First tokenize
            self.tokenize_input(input_string)

            # Then parse
            print("\n" + "="*60)
            print("SYNTAX AND SEMANTIC ANALYSIS")
            print("="*60)

            result = self.parser.parse(input_string, lexer=self.lexer)

            # Filter out undeclared variable errors (allow undeclared variables)
            self.semantic_errors = [error for error in self.semantic_errors
                                   if not ("not declared" in error)]

            # Check for syntax errors first
            if not self.parsing_successful:
                print("✗ SYNTAX ERROR: Input rejected due to syntax error")
                return "syntax_error"

            # Check for semantic errors
            if self.semantic_errors:
                print("✗ SEMANTIC ERRORS FOUND:")
                for error in self.semantic_errors:
                    print(f"  - {error}")
                return "semantic_error"

            # If we get here, both syntax and semantics are OK
            if result is not None:
                self.parse_tree = result
                print("✓ SYNTAX: Input string accepted by the grammar")
                print("✓ SEMANTICS: No semantic errors found")

                print("\n" + "="*60)
                print("PARSE TREE")
                print("="*60)
                self.parse_tree.display()
                print("="*60)

                # Generate and display BNF derivation sequence
                derivation_steps = self.bnf_derivation.generate_derivation_sequence(self.parse_tree, input_string)
                self.bnf_derivation.display_derivation()

                return "success"
            else:
                print("✗ SYNTAX ERROR: Input rejected by the grammar")
                return "syntax_error"

        except Exception as e:
            print(f"✗ PARSING FAILED: {str(e)}")
            self.parsing_successful = False
            return "syntax_error"

    def parse_input_silent(self, input_string: str):
        """Parse input and return structured data without printing to stdout"""
        self.parsing_successful = True
        self.semantic_errors = []
        self.input_expression = input_string

        try:
            # First tokenize (without printing)
            self.lexemes_tokens = []
            self.semantic_analyzer.reset()

            self.lexer.input(input_string)

            # Collect tokens
            while True:
                tok = self.lexer.token()
                if not tok:
                    break

                # Categorize tokens
                token_category = ""
                token_type = ""

                if tok.type in ['INT', 'DOUBLE', 'STRING_TYPE', 'BOOL_TYPE', 'IF', 'ELSE', 'WHILE', 'RETURN', 'VOID']:
                    token_category = "Keywords"
                    token_type = {
                        'INT': 'int', 'DOUBLE': 'double', 'STRING_TYPE': 'string',
                        'BOOL_TYPE': 'bool', 'IF': 'if', 'ELSE': 'else',
                        'WHILE': 'while', 'RETURN': 'return', 'VOID': 'void'
                    }.get(tok.type)
                elif tok.type == 'ID':
                    token_category = "Identifier"
                    token_type = "identifier"
                elif tok.type in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'ASSIGN', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE']:
                    token_category = "Operator"
                    token_type = {
                        'PLUS': '+', 'MINUS': '-', 'MULTIPLY': '*', 'DIVIDE': '/',
                        'ASSIGN': '=', 'GT': '>', 'LT': '<', 'GE': '>=',
                        'LE': '<=', 'EQ': '==', 'NE': '!='
                    }.get(tok.type)
                elif tok.type in ['LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON']:
                    token_category = "Delimiter"
                    token_type = {
                        'LPAREN': '(', 'RPAREN': ')', 'LBRACE': '{',
                        'RBRACE': '}', 'SEMICOLON': ';'
                    }.get(tok.type)
                elif tok.type in ['NUMBER', 'DECIMAL', 'STRING', 'BOOL']:
                    token_category = "Literal"
                    token_type = {
                        'NUMBER': 'integer', 'DECIMAL': 'decimal',
                        'STRING': 'string', 'BOOL': 'boolean'
                    }.get(tok.type)
                else:
                    token_category = "Other"
                    token_type = tok.type

                self.lexemes_tokens.append((tok.value, token_type, token_category))

            # Parse
            result = self.parser.parse(input_string, lexer=self.lexer)

            # Filter out undeclared variable errors (allow undeclared variables)
            self.semantic_errors = [error for error in self.semantic_errors
                                   if not ("not declared" in error)]

            # Set parse tree
            if result is not None and self.parsing_successful:
                self.parse_tree = result

            # Determine result status
            if not self.parsing_successful:
                return "syntax_error"
            elif self.semantic_errors:
                return "semantic_error"
            elif result is not None:
                return "success"
            else:
                return "syntax_error"

        except Exception as e:
            self.parsing_successful = False
            return "syntax_error"

# Interactive user input
def main():
    parser = GrammarParser()

    print("Enhanced Grammar Parser with Token Classification")
    print("Supports:")
    print("  - Keywords: int, double, string, bool, if, else, while, return, void")
    print("  - Identifiers: variable names (x, y, z, sum, count, etc.)")
    print("  - Operators: +, -, *, /, =, >, <, >=, <=, ==, !=")
    print("  - Delimiters: (), {}, ;")
    print("  - Literals: integers (1, 2, 3), decimals (3.14), strings (\"hello\"), booleans (true/false)")
    print("  - Variable declarations and expressions")
    print("  - Conditional statements: if(condition)")
    print("  - Loop statements: while(condition)")
    print("  - Syntax and semantic error detection")
    print("Examples:")
    print("  'int x = 5'")
    print("  'double pi = 3.14'")
    print("  'string name = \"John\"'")
    print("  'bool flag = true'")
    print("  'x + y * 2'")
    print("  'if(x > 9)'")
    print("  'while(i < 7)'")
    print("  'if(count >= 10)'")
    print("  'while(value != 0)'")
    print("Type 'quit' or 'exit' to stop\n")

    while True:
        try:
            user_input = input("Enter a statement to parse: ").strip()

            # Check for quit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            # Skip empty input
            if not user_input:
                print("Please enter a valid statement.\n")
                continue

            # Parse the input
            result = parser.parse_input(user_input)

            print("\n" + "="*60)
            print("FINAL RESULT")
            print("="*60)
            if result == "success":
                print("✓ ACCEPTED: Statement is syntactically and semantically correct")
            elif result == "syntax_error":
                print("✗ REJECTED: Statement contains SYNTAX ERROR")
            elif result == "semantic_error":
                print("✗ REJECTED: Statement contains SEMANTIC ERROR")
            else:
                print("✗ REJECTED: Statement contains syntax or semantic errors")
            print("="*60)

            # Ask if user wants to continue
            print("\n" + "-"*60)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()
