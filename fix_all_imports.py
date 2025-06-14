#!/usr/bin/env python3
"""
Script to fix imports across the entire project.
This script searches through all Python files and updates imports
to use the correct package prefix (backend.).
"""

import os
import re
import sys
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix imports in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has any imports that need fixing
    patterns = [
        r'from\s+(api|core|models|schemas|utils)\.',
        r'import\s+(api|core|models|schemas|utils)\.'
    ]
    
    needs_fixing = False
    for pattern in patterns:
        if re.search(pattern, content):
            needs_fixing = True
            break
    
    if not needs_fixing:
        return 0  # No changes needed
    
    # Fix imports with correct backend. prefix
    fixed_content = re.sub(
        r'from\s+(api|core|models|schemas|utils)\.', 
        r'from backend.\1.', 
        content
    )
    fixed_content = re.sub(
        r'import\s+(api|core|models|schemas|utils)\.', 
        r'import backend.\1.', 
        fixed_content
    )
    
    if fixed_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed imports in {file_path}")
        return 1  # Changes made
    
    return 0  # No changes needed

def main():
    # Get project root directory
    root_dir = Path(__file__).parent
    backend_dir = root_dir / 'backend'
    
    if not backend_dir.exists():
        print(f"Backend directory not found at {backend_dir}")
        sys.exit(1)
    
    # Process all Python files in the backend directory
    count = 0
    for subdir, dirs, files in os.walk(backend_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                count += fix_imports_in_file(file_path)
    
    print(f"Fixed imports in {count} files")

if __name__ == "__main__":
    main()
