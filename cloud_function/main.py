from flask import Request, jsonify
import functions_framework
from base import GrammarParser
import traceback

@functions_framework.http
def parse_expression(request: Request):
    """
    Google Cloud Function to parse expressions and return lexical, syntax, and semantic analysis.
    
    Expected request body:
    {
        "expression": "int x = 5"
    }
    
    Returns JSON response with all analysis results.
    """
    
    # Handle CORS for browser requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    # Set CORS headers for actual request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        # Validate request method
        if request.method != 'POST':
            return jsonify({
                "error": "Method not allowed. Use POST method.",
                "status": "error"
            }), 405, headers
        
        # Get request data
        request_json = request.get_json(silent=True)
        
        if not request_json:
            return jsonify({
                "error": "Invalid JSON in request body",
                "status": "error"
            }), 400, headers
        
        # Extract expression from request
        expression = request_json.get('expression', '').strip()
        
        if not expression:
            return jsonify({
                "error": "Missing or empty 'expression' field in request body",
                "status": "error",
                "example": {
                    "expression": "int x = 5"
                }
            }), 400, headers
        
        # Initialize parser
        parser = GrammarParser()
        
        # Parse the expression
        result = parser.parse_input(expression)
        
        # Prepare response data
        response_data = {
            "input_expression": expression,
            "status": "success" if result == "success" else "error",
            "result_type": result,
            "lexical_analysis": {
                "tokens": []
            },
            "syntax_analysis": {
                "accepted": result in ["success", "semantic_error"],
                "parse_tree": None
            },
            "semantic_analysis": {
                "errors": parser.semantic_errors,
                "variables_declared": {}
            }
        }
        
        # Add lexical analysis results (tokens)
        for lexeme, token_type, category in parser.lexemes_tokens:
            response_data["lexical_analysis"]["tokens"].append({
                "lexeme": lexeme,
                "token_type": token_type,
                "category": category
            })
        
        # Add parse tree if syntax was successful
        if parser.parse_tree and result in ["success", "semantic_error"]:
            response_data["syntax_analysis"]["parse_tree"] = serialize_parse_tree(parser.parse_tree)
        
        # Add semantic analysis results
        if result in ["success", "semantic_error"]:
            response_data["semantic_analysis"]["variables_declared"] = dict(parser.semantic_analyzer.variables)
        
        # Always return 200 for successful parsing attempts (even if there are parsing errors)
        # Only use 400/500 for request format issues or server errors
        status_code = 200
        
        return jsonify(response_data), status_code, headers
        
    except Exception as e:
        # Handle unexpected errors
        error_response = {
            "error": f"Internal server error: {str(e)}",
            "status": "error",
            "traceback": traceback.format_exc()
        }
        return jsonify(error_response), 500, headers

def serialize_parse_tree(node):
    """
    Convert ParseNode tree structure to JSON-serializable format.
    """
    if not node:
        return None
    
    return {
        "value": node.value,
        "children": [serialize_parse_tree(child) for child in node.children] if node.children else []
    }

# For local testing with functions-framework
if __name__ == "__main__":
    import functions_framework
    import os
    
    # Set default port if not specified
    port = int(os.environ.get('PORT', 8080))
    
    print(f"Starting Functions Framework server on port {port}")
    print("Test your function at: http://localhost:{port}")
    print("\nExample request:")
    print("curl -X POST http://localhost:{port} \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"expression\": \"int x = 5\"}'")
    
    # This will be handled by functions-framework CLI when run properly
    functions_framework._http_view_func_registry.clear()
    functions_framework.create_app(target=parse_expression, debug=True).run(
        host='0.0.0.0', 
        port=port, 
        debug=True
    )
