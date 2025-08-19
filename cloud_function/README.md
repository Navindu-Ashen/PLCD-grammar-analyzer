# Grammar Parser Cloud Function

A Google Cloud Function that provides lexical, syntactic, and semantic analysis for programming language expressions. This function parses variable declarations and mathematical expressions, returning detailed analysis results in JSON format.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Supported Grammar](#supported-grammar)
- [Installation](#installation)
- [Local Testing](#local-testing)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Project Structure](#project-structure)

## Overview

This cloud function analyzes programming language statements and expressions, providing comprehensive feedback on:
- **Lexical Analysis**: Token classification and categorization
- **Syntax Analysis**: Grammar validation and parse tree generation
- **Semantic Analysis**: Type checking and variable declaration validation

## Features

- ✅ **Multi-type Variable Declarations**: `int`, `double`, `string`, `bool`
- ✅ **Expression Parsing**: Mathematical expressions with operators `+`, `-`, `*`, `/`
- ✅ **Token Classification**: Keywords, identifiers, operators, delimiters, literals
- ✅ **Parse Tree Generation**: Complete syntax tree representation
- ✅ **Semantic Analysis**: Type compatibility checking and variable scope validation
- ✅ **Error Detection**: Detailed syntax and semantic error reporting
- ✅ **CORS Support**: Browser-compatible API endpoints

## Supported Grammar

### Keywords
- **Data Types**: `int`, `double`, `string`, `bool`
- **Control Flow**: `if`, `else`, `while`, `return`, `void`
- **Boolean Literals**: `true`, `false`

### Operators
- **Arithmetic**: `+`, `-`, `*`, `/`
- **Assignment**: `=`

### Delimiters
- **Parentheses**: `(`, `)`
- **Braces**: `{`, `}`
- **Semicolon**: `;`

### Literals
- **Integer**: `123`, `0`, `999`
- **Decimal**: `3.14`, `0.5`, `123.456`
- **String**: `"hello"`, `"world"`, `"test string"`
- **Boolean**: `true`, `false`

### Examples of Valid Statements
```
int x = 5
double pi = 3.14159
string name = "John"
bool flag = true
x + y * 2
(a + b) * c
```

## Installation

### Prerequisites
- Python 3.9+
- Google Cloud SDK (for deployment)
- pip (Python package manager)

### Local Setup
1. Clone or download the project files
2. Navigate to the project directory:
   ```bash
   cd /path/to/project
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Local Testing

### Start the Function Server
```bash
functions-framework --target=parse_expression --debug
```

The function will be available at `http://localhost:8080`

### Test with curl
```bash
# Test a simple variable declaration
curl -X POST http://localhost:8080 \
  -H 'Content-Type: application/json' \
  -d '{"expression": "int x = 5"}'

# Test a mathematical expression
curl -X POST http://localhost:8080 \
  -H 'Content-Type: application/json' \
  -d '{"expression": "x + y * 2"}'

# Test a decimal declaration
curl -X POST http://localhost:8080 \
  -H 'Content-Type: application/json' \
  -d '{"expression": "double pi = 3.14"}'
```

## Deployment

### Quick Deployment
Run the automated deployment script:
```bash
./deploy.sh
```

### Manual Deployment
```bash
gcloud functions deploy parse-expression \
  --gen2 \
  --runtime=python39 \
  --region=us-central1 \
  --source=. \
  --entry-point=parse_expression \
  --trigger=http \
  --allow-unauthenticated \
  --memory=512MB \
  --timeout=60s
```

## API Documentation

### Endpoint
- **URL**: `https://us-central1-cloudapi-465510.cloudfunctions.net/parse-expression`
- **Method**: `POST`
- **Content-Type**: `application/json`

### Request Structure

```json
{
  "expression": "string"
}
```

**Parameters:**
- `expression` (required): The programming statement or expression to analyze

### Response Structure

#### Success Response (200 OK)
```json
{
  "input_expression": "int x = 5",
  "status": "success",
  "result_type": "success",
  "lexical_analysis": {
    "tokens": [
      {
        "lexeme": "int",
        "token_type": "int",
        "category": "Keywords"
      },
      {
        "lexeme": "x",
        "token_type": "identifier",
        "category": "Identifier"
      },
      {
        "lexeme": "=",
        "token_type": "=",
        "category": "Operator"
      },
      {
        "lexeme": 5,
        "token_type": "integer",
        "category": "Literal"
      }
    ]
  },
  "syntax_analysis": {
    "accepted": true,
    "parse_tree": {
      "value": "Statement",
      "children": [
        {
          "value": "Declaration",
          "children": [
            {
              "value": "int",
              "children": []
            },
            {
              "value": "id(x)",
              "children": []
            },
            {
              "value": "=",
              "children": []
            },
            {
              "value": "E",
              "children": [...]
            }
          ]
        }
      ]
    }
  },
  "semantic_analysis": {
    "errors": [],
    "variables_declared": {
      "x": {
        "type": "int",
        "line_no": 1,
        "initialized": true
      }
    }
  }
}
```

#### Error Response (400 Bad Request)
```json
{
  "input_expression": "int x = \"hello\"",
  "status": "error",
  "result_type": "semantic_error",
  "lexical_analysis": {
    "tokens": [...]
  },
  "syntax_analysis": {
    "accepted": true,
    "parse_tree": {...}
  },
  "semantic_analysis": {
    "errors": [
      "Semantic Error: Cannot assign string value to integer variable 'x'"
    ],
    "variables_declared": {
      "x": {
        "type": "int",
        "line_no": 1,
        "initialized": false
      }
    }
  }
}
```

#### Invalid Request (400 Bad Request)
```json
{
  "error": "Missing or empty 'expression' field in request body",
  "status": "error",
  "example": {
    "expression": "int x = 5"
  }
}
```

### Response Fields

#### Root Level
- `input_expression`: The original expression sent in the request
- `status`: `"success"` or `"error"`
- `result_type`: `"success"`, `"syntax_error"`, or `"semantic_error"`

#### Lexical Analysis
- `tokens`: Array of token objects
  - `lexeme`: The actual text/value of the token
  - `token_type`: The specific type (e.g., "int", "identifier", "+")
  - `category`: The general category ("Keywords", "Identifier", "Operator", "Delimiter", "Literal")

#### Syntax Analysis
- `accepted`: Boolean indicating if syntax is valid
- `parse_tree`: Hierarchical representation of the parsed expression
  - `value`: Node name/value
  - `children`: Array of child nodes (recursive structure)

#### Semantic Analysis
- `errors`: Array of semantic error messages
- `variables_declared`: Object containing declared variables
  - Variable name as key, containing:
    - `type`: Variable data type
    - `line_no`: Line number where declared
    - `initialized`: Boolean indicating if variable was initialized

## Examples

### Valid Variable Declarations

#### Integer Declaration
**Request:**
```json
{"expression": "int count = 10"}
```

**Response:** Success with integer token analysis

#### String Declaration
**Request:**
```json
{"expression": "string message = \"Hello World\""}
```

**Response:** Success with string literal parsing

#### Boolean Declaration
**Request:**
```json
{"expression": "bool isActive = true"}
```

**Response:** Success with boolean literal analysis

### Mathematical Expressions

#### Simple Addition
**Request:**
```json
{"expression": "x + y"}
```

**Response:** Parse tree showing addition operation

#### Complex Expression
**Request:**
```json
{"expression": "(a + b) * c"}
```

**Response:** Parse tree with proper operator precedence

### Error Cases

#### Syntax Error
**Request:**
```json
{"expression": "int x ="}
```

**Response:** Syntax error with detailed message

#### Semantic Error
**Request:**
```json
{"expression": "int number = \"text\""}
```

**Response:** Type mismatch error

#### Undeclared Variable
**Request:**
```json
{"expression": "x + undeclaredVar"}
```

**Response:** Semantic error for undeclared variable

## Error Handling

### Client Errors (400)
- Missing or empty expression field
- Invalid JSON format
- Syntax errors in the expression
- Semantic errors (type mismatches, undeclared variables)

### Server Errors (500)
- Internal parsing errors
- Unexpected exceptions during analysis

### Method Errors (405)
- Using GET, PUT, DELETE, etc. instead of POST

## Project Structure

```
project/
├── main.py              # Cloud Function entry point
├── base.py              # Core parser implementation (unchanged)
├── requirements.txt     # Python dependencies
├── deploy.sh           # Deployment automation script
└── README.md           # This documentation
```

### File Descriptions

- **`main.py`**: Contains the Cloud Function that wraps the parser functionality and provides the HTTP API
- **`base.py`**: Original parser implementation with lexical, syntax, and semantic analysis
- **`requirements.txt`**: Lists all Python packages needed for the function
- **`deploy.sh`**: Automated script for deploying to Google Cloud Functions
- **`README.md`**: Complete documentation and usage guide
