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
        
        # Look for the actual value in the parse tree
        def find_value_type(node):
            if not hasattr(node, 'children'):
                return 'unknown'
            
            for child in node.children:
                if hasattr(child, 'value'):
                    if child.value == 'number':
                        return 'int'
                    elif child.value == 'decimal':
                        return 'double'
                    elif child.value == 'string':
                        return 'string'
                    elif child.value == 'boolean':
                        return 'bool'
                    elif child.value == 'id':
                        # Get the variable name from the id node
                        if child.children and hasattr(child.children[0], 'value'):
                            var_name = child.children[0].value
                            if var_name in self.variables:
                                return self.variables[var_name]['type']
                            return 'undeclared'
                
                # Recursively search in children
                result = find_value_type(child)
                if result != 'unknown':
                    return result
            
            return 'unknown'
        
        return find_value_type(expression_node)
    
    def check_type_compatibility(self, declared_type: str, expression_node, var_name: str) -> Optional[str]:
        """Check if the expression type is compatible with the declared variable type"""
        expr_type = self.get_expression_type(expression_node)
        
        if expr_type == 'undeclared':
            return None  # This will be caught by check_variable
        
        if expr_type == 'unknown':
            return None  # Can't determine type, assume it's okay for now
        
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
    
    def reset(self):
        """Reset the analyzer for new input"""
        self.variables = {}

class ParseNode:
    """Node for parse tree representation"""
    def __init__(self, value: str, children: List['ParseNode'] = None):
        self.value = value
        self.children = children or []
    
    def add_child(self, child: 'ParseNode'):
        self.children.append(child)
    
    def display(self, level: int = 0, prefix: str = ""):
        """Display parse tree in a structured format"""
        print(f"{prefix}{'├── ' if level > 0 else ''}{self.value}")
        for i, child in enumerate(self.children):
            is_last = i == len(self.children) - 1
            new_prefix = prefix + ("    " if level > 0 and is_last else "│   " if level > 0 else "")
            child.display(level + 1, new_prefix)

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
        p[0] = ParseNode('Statement')
        p[0].add_child(p[1])
    
    def p_statement_expression(self, p):
        '''statement : expression'''
        p[0] = ParseNode('Statement')
        p[0].add_child(p[1])
    
    def p_statement_if(self, p):
        '''statement : if_statement'''
        p[0] = ParseNode('Statement')
        p[0].add_child(p[1])
    
    def p_statement_while(self, p):
        '''statement : while_statement'''
        p[0] = ParseNode('Statement')
        p[0].add_child(p[1])
    
    def p_declaration_int(self, p):
        '''declaration : INT ID ASSIGN expression'''
        p[0] = ParseNode('Declaration')
        p[0].add_child(ParseNode('int'))
        p[0].add_child(ParseNode(f'id({p[2]})'))
        p[0].add_child(ParseNode('='))
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
        p[0] = ParseNode('Declaration')
        p[0].add_child(ParseNode('double'))
        p[0].add_child(ParseNode(f'id({p[2]})'))
        p[0].add_child(ParseNode('='))
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
        p[0] = ParseNode('Declaration')
        p[0].add_child(ParseNode('string'))
        p[0].add_child(ParseNode(f'id({p[2]})'))
        p[0].add_child(ParseNode('='))
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
        p[0] = ParseNode('Declaration')
        p[0].add_child(ParseNode('bool'))
        p[0].add_child(ParseNode(f'id({p[2]})'))
        p[0].add_child(ParseNode('='))
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
        p[0] = ParseNode('Declaration')
        p[0].add_child(ParseNode('int'))
        p[0].add_child(ParseNode(f'id({p[2]})'))
        
        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'int', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
    
    def p_declaration_no_init_double(self, p):
        '''declaration : DOUBLE ID'''
        p[0] = ParseNode('Declaration')
        p[0].add_child(ParseNode('double'))
        p[0].add_child(ParseNode(f'id({p[2]})'))
        
        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'double', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
    
    def p_declaration_no_init_string(self, p):
        '''declaration : STRING_TYPE ID'''
        p[0] = ParseNode('Declaration')
        p[0].add_child(ParseNode('string'))
        p[0].add_child(ParseNode(f'id({p[2]})'))
        
        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'string', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
    
    def p_declaration_no_init_bool(self, p):
        '''declaration : BOOL_TYPE ID'''
        p[0] = ParseNode('Declaration')
        p[0].add_child(ParseNode('bool'))
        p[0].add_child(ParseNode(f'id({p[2]})'))
        
        # Semantic analysis: declare variable
        error = self.semantic_analyzer.declare_variable(p[2], 'bool', p.lineno(2))
        if error:
            self.semantic_errors.append(error)
    def p_expression(self, p):
        '''expression : term expression_prime'''
        p[0] = ParseNode('E')
        p[0].add_child(p[1])  # T
        p[0].add_child(p[2])  # E'
    
    def p_expression_prime_plus(self, p):
        '''expression_prime : PLUS term expression_prime'''
        p[0] = ParseNode("E'")
        p[0].add_child(ParseNode('+'))
        p[0].add_child(p[2])  # T
        p[0].add_child(p[3])  # E'
    
    def p_expression_prime_epsilon(self, p):
        '''expression_prime : '''
        p[0] = ParseNode("E' (ε)")
    
    def p_term(self, p):
        '''term : factor term_prime'''
        p[0] = ParseNode('T')
        p[0].add_child(p[1])  # F
        p[0].add_child(p[2])  # T'
    
    def p_term_prime_multiply(self, p):
        '''term_prime : MULTIPLY factor term_prime'''
        p[0] = ParseNode("T'")
        p[0].add_child(ParseNode('*'))
        p[0].add_child(p[2])  # F
        p[0].add_child(p[3])  # T'
    
    def p_term_prime_epsilon(self, p):
        '''term_prime : '''
        p[0] = ParseNode("T' (ε)")
    
    def p_factor_paren(self, p):
        '''factor : LPAREN expression RPAREN'''
        p[0] = ParseNode('F')
        p[0].add_child(ParseNode('('))
        p[0].add_child(p[2])  # E
        p[0].add_child(ParseNode(')'))
    
    def p_factor_id(self, p):
        '''factor : ID'''
        p[0] = ParseNode('F')
        id_node = ParseNode('id')
        id_node.add_child(ParseNode(p[1]))
        p[0].add_child(id_node)
        
        # Semantic analysis: check if variable is declared
        error = self.semantic_analyzer.check_variable(p[1])
        if error:
            self.semantic_errors.append(error)
    
    def p_factor_number(self, p):
        '''factor : NUMBER'''
        p[0] = ParseNode('F')
        num_node = ParseNode('number')
        num_node.add_child(ParseNode(str(p[1])))
        p[0].add_child(num_node)
    
    def p_factor_decimal(self, p):
        '''factor : DECIMAL'''
        p[0] = ParseNode('F')
        dec_node = ParseNode('decimal')
        dec_node.add_child(ParseNode(str(p[1])))
        p[0].add_child(dec_node)
    
    def p_factor_string(self, p):
        '''factor : STRING'''
        p[0] = ParseNode('F')
        str_node = ParseNode('string')
        str_node.add_child(ParseNode(p[1]))
        p[0].add_child(str_node)
    
    def p_factor_bool(self, p):
        '''factor : BOOL'''
        p[0] = ParseNode('F')
        bool_node = ParseNode('boolean')
        bool_node.add_child(ParseNode(p[1]))
        p[0].add_child(bool_node)
    
    # If statement grammar rules
    def p_if_statement(self, p):
        '''if_statement : IF LPAREN condition RPAREN'''
        p[0] = ParseNode('IfStatement')
        p[0].add_child(ParseNode('if'))
        p[0].add_child(ParseNode('('))
        p[0].add_child(p[3])  # condition
        p[0].add_child(ParseNode(')'))
    
    # While statement grammar rules
    def p_while_statement(self, p):
        '''while_statement : WHILE LPAREN condition RPAREN'''
        p[0] = ParseNode('WhileStatement')
        p[0].add_child(ParseNode('while'))
        p[0].add_child(ParseNode('('))
        p[0].add_child(p[3])  # condition
        p[0].add_child(ParseNode(')'))
    
    # Condition grammar rules for comparison expressions
    def p_condition_gt(self, p):
        '''condition : expression GT expression'''
        p[0] = ParseNode('Condition')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('>'))
        p[0].add_child(p[3])  # right expression
    
    def p_condition_lt(self, p):
        '''condition : expression LT expression'''
        p[0] = ParseNode('Condition')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('<'))
        p[0].add_child(p[3])  # right expression
    
    def p_condition_ge(self, p):
        '''condition : expression GE expression'''
        p[0] = ParseNode('Condition')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('>='))
        p[0].add_child(p[3])  # right expression
    
    def p_condition_le(self, p):
        '''condition : expression LE expression'''
        p[0] = ParseNode('Condition')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('<='))
        p[0].add_child(p[3])  # right expression
    
    def p_condition_eq(self, p):
        '''condition : expression EQ expression'''
        p[0] = ParseNode('Condition')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('=='))
        p[0].add_child(p[3])  # right expression
    
    def p_condition_ne(self, p):
        '''condition : expression NE expression'''
        p[0] = ParseNode('Condition')
        p[0].add_child(p[1])  # left expression
        p[0].add_child(ParseNode('!='))
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