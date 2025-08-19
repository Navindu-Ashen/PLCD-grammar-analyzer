# PLCD Grammar Analyzer

A comprehensive Programming Language Concepts and Design (PLCD) project that implements a complete compiler frontend with lexical analysis, syntax analysis, and semantic analysis. The project consists of a Python-based grammar parser deployed as a Google Cloud Function and a Next.js frontend for interactive grammar analysis.

## Features

### Lexical Analysis
- **Token Classification**: Supports multiple token categories:
  - **Keywords**: `int`, `double`, `string`, `bool`, `if`, `else`, `while`, `return`, `void`
  - **Identifiers**: Variable names (x, y, z, sum, count, etc.)
  - **Operators**: `+`, `-`, `*`, `/`, `=`
  - **Delimiters**: `()`, `{}`, `;`
  - **Literals**: integers (1, 2, 3), decimals (3.14), strings ("hello"), booleans (true/false)

### Syntax Analysis
- **Context-Free Grammar**: Implements a formal grammar for parsing variable declarations and expressions
- **Parse Tree Generation**: Creates detailed parse trees for valid syntax
- **Error Detection**: Comprehensive syntax error reporting with position information

### Semantic Analysis
- **Variable Declaration Tracking**: Maintains symbol table for declared variables
- **Type Checking**: Enforces type compatibility between declarations and assignments
- **Semantic Error Detection**: Reports semantic errors such as:
  - Undeclared variable usage
  - Duplicate variable declarations
  - Type mismatches

## Architecture

### Backend (Cloud Function)
- **Python-based parser** using PLY (Python Lex-Yacc)
- **Google Cloud Functions** deployment for scalable API
- **RESTful API** with CORS support for frontend integration
- **Comprehensive error handling** and response formatting

### Frontend (Next.js)
- **React-based interface** for interactive grammar analysis
- **TypeScript** for type safety
- **Tailwind CSS** for modern styling
- **Real-time parsing** with API integration

## Supported Grammar

The parser supports the following language constructs:

### Variable Declarations
```cpp
int x = 5;
double pi = 3.14;
string name = "John";
bool flag = true;
int y;  // Declaration without initialization
```

### Expressions
```cpp
x + y * 2
(a + b) * c
```

### Examples of Valid Input
- `int x = 5`
- `double pi = 3.14`
- `string name = "John"`
- `bool flag = true`
- `x + y * 2`
- `(a + b) * c`

## Installation & Setup

### Prerequisites
- Python 3.12
- Node.js 18+
- Google Cloud SDK (for cloud deployment)

### Backend Setup

1. **Navigate to cloud function directory:**
   ```bash
   cd cloud_function
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally:**
   ```bash
   python main.py
   ```

4. **Test the API:**
   ```bash
   curl -X POST http://localhost:8080 \
     -H 'Content-Type: application/json' \
     -d '{"expression": "int x = 5"}'
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   ```
   http://localhost:3000
   ```

## Deployment

### Google Cloud Functions

1. **Deploy the function:**
   ```bash
   cd cloud_function
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Frontend Deployment

The Next.js frontend can be deployed to:
- **Vercel** (recommended)
- **Netlify**
- **Google Cloud Run**

## API Documentation

### Parse Expression Endpoint

**URL:** `POST /parse_expression`

**Request Body:**
```json
{
  "expression": "int x = 5"
}
```

**Response (Success):**
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
      "children": [...]
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

**Response (Error):**
```json
{
  "input_expression": "int x = \"hello\"",
  "status": "error",
  "result_type": "semantic_error",
  "semantic_analysis": {
    "errors": [
      "Semantic Error: Cannot assign string value to integer variable 'x'"
    ]
  }
}
```

## Testing

### Manual Testing Examples

1. **Valid Declaration:**
   ```
   Input: int x = 5
   Expected: ✓ Success
   ```

2. **Type Mismatch:**
   ```
   Input: int x = "hello"
   Expected: ✗ Semantic Error
   ```

3. **Undeclared Variable:**
   ```
   Input: y + 5
   Expected: ✗ Semantic Error
   ```

4. **Syntax Error:**
   ```
   Input: int x =
   Expected: ✗ Syntax Error
   ```

## Project Structure

```
PLCD-grammar-analyzer/
├── README.md
├── cloud_function/           # Backend API
│   ├── base.py              # Core parser implementation
│   ├── main.py              # Cloud Function entry point
│   ├── requirements.txt     # Python dependencies
│   ├── deploy.sh           # Deployment script
│   └── README.md           # Backend documentation
├── frontend/               # Next.js frontend
│   ├── app/               # App router pages
│   ├── public/            # Static assets
│   ├── package.json       # Node.js dependencies
│   ├── next.config.ts     # Next.js configuration
│   └── README.md          # Frontend documentation
```

## Learning Objectives

This project demonstrates understanding of:

- **Compiler Design Principles**: Lexical, syntax, and semantic analysis phases
- **Formal Language Theory**: Context-free grammars and parse trees
- **Symbol Table Management**: Variable tracking and scope handling
- **Type Systems**: Static type checking and type compatibility
- **Cloud Architecture**: Serverless deployment patterns
- **Full-Stack Development**: API design and frontend integration
