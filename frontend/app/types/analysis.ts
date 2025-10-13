export interface Token {
  category: string;
  lexeme: string | number;
  token_type: string;
}

export interface Variable {
  initialized: boolean;
  line_no: number;
  type: string;
}

export interface BnfDerivationStep {
  rule: string;
  step: number;
}

export interface AnalysisResponse {
  input_expression: string;
  lexical_analysis: {
    tokens: Token[];
  };
  result_type: string;
  semantic_analysis: {
    errors: string[];
    variables_declared: Record<string, Variable>;
  };
  status: string;
  syntax_analysis: {
    accepted: boolean;
    errors?: string[];
    bnf_derivation?: BnfDerivationStep[];
  };
}
