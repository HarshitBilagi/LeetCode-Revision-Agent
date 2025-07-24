import ast
import re
from database import update_problem_explanation

def explain_code_locally(code, language='python'):
    """Generate code explanation without LLM APIs using AST and pattern matching"""
    if not code or not code.strip():
        return "No code provided"
    
    if language.lower() == 'python':
        return explain_python_code(code)
    else:
        return explain_non_python_code(code, language)

def explain_python_code(code):
    """Analyze Python code using AST"""
    try:
        tree = ast.parse(code)
        explanation_parts = []
        
        # Analyze function structures
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        if functions:
            explanation_parts.append(f"Defines function(s): {', '.join(functions)}")
        
        if classes:
            explanation_parts.append(f"Defines class(es): {', '.join(classes)}")
        
        # Count algorithmic patterns
        loops = len([node for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While))])
        if loops:
            explanation_parts.append(f"Contains {loops} loop(s)")
        
        conditionals = len([node for node in ast.walk(tree) if isinstance(node, ast.If)])
        if conditionals:
            explanation_parts.append(f"Uses {conditionals} conditional statement(s)")
        
        # Check for common data structures
        list_comps = len([node for node in ast.walk(tree) if isinstance(node, ast.ListComp)])
        if list_comps:
            explanation_parts.append(f"Uses {list_comps} list comprehension(s)")
        
        dict_comps = len([node for node in ast.walk(tree) if isinstance(node, ast.DictComp)])
        if dict_comps:
            explanation_parts.append(f"Uses {dict_comps} dictionary comprehension(s)")
        
        # Check for recursion
        has_recursion = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                        if child.func.id == node.name:
                            has_recursion = True
                            break
        
        if has_recursion:
            explanation_parts.append("Uses recursion")
        
        # Check for common built-in functions
        builtin_funcs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in ['map', 'filter', 'reduce', 'zip', 'enumerate', 'sorted', 'max', 'min', 'sum']:
                    if func_name not in builtin_funcs:
                        builtin_funcs.append(func_name)
        
        if builtin_funcs:
            explanation_parts.append(f"Uses built-in functions: {', '.join(builtin_funcs)}")
        
        return ". ".join(explanation_parts) if explanation_parts else "Simple code structure"
        
    except SyntaxError:
        # If AST parsing fails, fall back to pattern matching
        return explain_with_patterns(code)
    except Exception as e:
        return f"Code analysis failed: {str(e)}"

def explain_non_python_code(code, language):
    """Explain non-Python code using pattern matching"""
    return f"Code analysis for {language}: {explain_with_patterns(code)}"

def explain_with_patterns(code):
    """Pattern-based fallback analysis for any language"""
    patterns = {
        'sorting': [r'\.sort\(\)', r'sorted\(', r'Arrays\.sort', r'std::sort', r'sort\('],
        'binary search': [r'left.*right.*mid', r'low.*high.*mid', r'binary.*search'],
        'two pointers': [r'left.*right', r'start.*end', r'i.*j.*while'],
        'dynamic programming': [r'dp\[', r'memo', r'cache', r'dp\s*='],
        'recursion': [r'return.*function_name\(', r'recursive'],
        'hash map/dictionary': [r'HashMap', r'unordered_map', r'dict\(', r'\{\}', r'Map\('],
        'sliding window': [r'window', r'left.*right.*while'],
        'backtracking': [r'backtrack', r'dfs.*return', r'visited'],
        'graph traversal': [r'adjacency', r'neighbors', r'graph', r'visited'],
        'tree traversal': [r'TreeNode', r'root', r'left.*right', r'inorder|preorder|postorder'],
        'greedy algorithm': [r'greedy', r'optimal.*choice'],
        'divide and conquer': [r'merge', r'divide', r'conquer'],
    }
    
    found_patterns = []
    code_lower = code.lower()
    
    for pattern_name, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, code_lower, re.IGNORECASE):
                if pattern_name not in found_patterns:
                    found_patterns.append(pattern_name)
                break
    
    if found_patterns:
        return f"Likely uses: {', '.join(found_patterns)}"
    else:
        # Basic structure analysis
        lines = len(code.split('\n'))
        return f"Code structure analysis - {lines} lines, manual review recommended"

def add_explanations_to_problems(problems):
    """Add explanations to problems that don't have them"""
    for problem in problems:
        if not problem.get('explanation'):
            explanation = explain_code_locally(problem['code'], problem['language'])
            problem['explanation'] = explanation
            
            # Update in database
            update_problem_explanation(problem['id'], explanation)
    
    return problems

def get_code_complexity_estimate(code):
    """Estimate code complexity"""
    try:
        tree = ast.parse(code)
        
        # Count nested structures for cyclomatic complexity estimate
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        if complexity <= 5:
            return "Low complexity"
        elif complexity <= 10:
            return "Medium complexity"
        else:
            return "High complexity"
            
    except:
        return "Complexity analysis unavailable"
