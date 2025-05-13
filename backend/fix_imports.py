#!/usr/bin/env python
# This script fixes import paths in all Python files in the api directory

import os
import re
import sys

def add_import_sys_path(file_content):
    # Check if sys.path.append is already in the file
    if "sys.path.append" in file_content:
        return file_content
    
    # Add import sys and os if they're not already imported
    if not "import sys" in file_content:
        if "import os" in file_content:
            file_content = re.sub(r'import os', 'import os\nimport sys', file_content)
        else:
            file_content = "import sys\nimport os\n" + file_content
    
    # Find a good place to insert the path modification
    lines = file_content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            insert_pos = i + 1
    
    # Insert the sys.path.append
    path_line = "\n# Add project root to Python path\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \"../..\"))))\n"
    lines.insert(insert_pos, path_line)
    return '\n'.join(lines)

def fix_ml_models_imports(file_content):
    # Replace any ml_models imports without changing the project root
    return file_content  # No need to modify because we're adding sys.path.append

def fix_backend_schemas_imports(file_content):
    # Replace backend.schemas with schemas
    return file_content.replace("from backend.schemas", "from schemas")

def fix_file(file_path):
    print(f"Fixing imports in {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "from ml_models" in content:
        content = add_import_sys_path(content)
        content = fix_ml_models_imports(content)
    
    if "from backend.schemas" in content:
        content = fix_backend_schemas_imports(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    api_dir = os.path.dirname(os.path.abspath(__file__)) + "/api"
    for file_name in os.listdir(api_dir):
        if file_name.endswith('.py'):
            file_path = os.path.join(api_dir, file_name)
            fix_file(file_path)
    print("Import paths fixed successfully.")

if __name__ == "__main__":
    main()
