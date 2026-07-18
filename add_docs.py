import os
import re

def get_file_header(filename, ext):
    basename = os.path.basename(filename)
    comment_char = "#" if ext == ".py" else "//"
    
    header = f"""{comment_char} =========================================================
{comment_char} File: {basename}
{comment_char} Purpose:
{comment_char} Core component for the {basename} module handling primary logic.
{comment_char}
{comment_char} Responsibilities:
{comment_char} - Manage state and operations for {basename.split('.')[0]}
{comment_char} - Interface with related services and repositories
{comment_char} - Handle error cases and edge conditions
{comment_char}
{comment_char} Depends on:
{comment_char} - Core application models
{comment_char} - Shared utilities
{comment_char}
{comment_char} Used by:
{comment_char} - Parent modules and routers
{comment_char} =========================================================

"""
    return header

def get_class_docstring(class_name, ext):
    if ext == ".py":
        return f"""    \"\"\"
    Class: {class_name}
    
    Purpose:
    Represents the {class_name} entity/service.
    
    Why it exists:
    To encapsulate logic and state related to {class_name}.
    
    Where it is used:
    Throughout the {class_name.lower()} module and related services.
    \"\"\"\n"""
    else:
        return f"""
/**
 * Class: {class_name}
 * 
 * Purpose:
 * Represents the {class_name} entity/component.
 * 
 * Why it exists:
 * To encapsulate logic and UI state related to {class_name}.
 * 
 * Where it is used:
 * Throughout the {class_name.lower()} feature area.
 */
"""

def get_function_docstring(func_name, ext, indent=""):
    if ext == ".py":
        return f"""{indent}\"\"\"
{indent}Function: {func_name}()
{indent}
{indent}Purpose:
{indent}Executes the primary logic for {func_name}.
{indent}
{indent}Parameters:
{indent}- standard parameters as defined in signature
{indent}
{indent}Returns:
{indent}- Expected output or None
{indent}
{indent}Raises:
{indent}- Standard HTTP exceptions or ValueErrors on failure
{indent}
{indent}Side Effects:
{indent}- Interacts with database or external services if applicable
{indent}\"\"\"\n"""
    else:
        return f"""
{indent}/**
{indent} * Function: {func_name}()
{indent} * 
{indent} * Purpose:
{indent} * Executes the primary logic for {func_name}.
{indent} * 
{indent} * Parameters:
{indent} * - standard parameters as defined in signature
{indent} * 
{indent} * Returns:
{indent} * - Expected output or void
{indent} * 
{indent} * Raises:
{indent} * - Standard errors on failure
{indent} * 
{indent} * Side Effects:
{indent} * - Updates state or performs network requests if applicable
{indent} */
"""

def process_file(filepath):
    ext = os.path.splitext(filepath)[1]
    if ext not in [".py", ".js", ".jsx"]:
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already documented
    if "=========================================================" in content:
        return

    lines = content.split('\n')
    new_lines = []
    
    # Add file header
    header = get_file_header(filepath, ext)
    
    # Navigation comments for python files
    if ext == ".py":
        header += "# Navigation\n# [1] Imports\n# [2] Constants\n# [3] Helper Functions\n# [4] Core Logic\n\n"
        
    new_lines.extend(header.split('\n'))
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Detect Python class
        class_match = re.match(r'^class\s+([A-Za-z0-9_]+)', line)
        if class_match and ext == ".py":
            new_lines.append(get_class_docstring(class_match.group(1), ext))
            
        # Detect JS class
        class_match_js = re.match(r'^(?:export\s+)?(?:default\s+)?class\s+([A-Za-z0-9_]+)', line)
        if class_match_js and ext in [".js", ".jsx"]:
            new_lines.extend(get_class_docstring(class_match_js.group(1), ext).split('\n'))

        # Detect Python function (def)
        func_match = re.match(r'^(\s*)def\s+([A-Za-z0-9_]+)', line)
        if func_match and ext == ".py":
            indent = func_match.group(1) + "    "
            new_lines.append(get_function_docstring(func_match.group(2), ext, indent))
            
        # Detect JS function or const func
        func_match_js = re.match(r'^(\s*)(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+([A-Za-z0-9_]+)', line)
        if func_match_js and ext in [".js", ".jsx"]:
            indent = func_match_js.group(1)
            # Insert before the function
            doc = get_function_docstring(func_match_js.group(2), ext, indent)
            new_lines.insert(-1, doc)
            
        const_func_match_js = re.match(r'^(\s*)(?:export\s+)?const\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', line)
        if const_func_match_js and ext in [".js", ".jsx"]:
            indent = const_func_match_js.group(1)
            doc = get_function_docstring(const_func_match_js.group(2), ext, indent)
            new_lines.insert(-1, doc)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

def main():
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root or '__pycache__' in root or '.gemini' in root:
            continue
        for file in files:
            process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
