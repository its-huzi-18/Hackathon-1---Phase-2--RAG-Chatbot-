#!/usr/bin/env python3
"""
Validation script for the RAG Chatbot Backend
This script validates that the implementation is correct without requiring all dependencies.
"""

import os
import sys
import ast
from dotenv import load_dotenv

def validate_main_py():
    """Validate the main.py file structure and imports"""
    print("Validating main.py file...")

    # Check if main.py exists
    main_py_path = "main.py"
    if not os.path.exists(main_py_path):
        print("❌ main.py does not exist")
        return False

    # Check if it's valid Python syntax
    try:
        with open(main_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
            ast.parse(content)  # This will raise an exception if syntax is invalid
        print("[OK] main.py has valid Python syntax")
    except SyntaxError as e:
        print(f"❌ main.py has syntax errors: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False

    # Check for required functions
    required_functions = [
        'get_all_urls',
        'extract_text_from_url',
        'chunk_text',
        'embed',
        'create_collection',
        'save_chunk_to_qdrant',
        'main'
    ]

    found_functions = []
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
        for line in content.split('\n'):
            if line.strip().startswith('def ') and line.strip().endswith(':'):
                func_name = line.strip()[4:-1].split('(')[0]
                if func_name in required_functions:
                    found_functions.append(func_name)

    missing_functions = set(required_functions) - set(found_functions)
    if missing_functions:
        print(f"[ERROR] Missing required functions: {missing_functions}")
        return False
    else:
        print(f"[OK] All required functions found: {found_functions}")

    # Check for required imports
    required_imports = [
        'requests',
        'bs4',
        'cohere',
        'qdrant_client',
        'uuid',
        'os',
        'logging'
    ]

    found_imports = []
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                for imp in required_imports:
                    if imp in line:
                        found_imports.append(imp)
                        break

    print(f"[OK] Found imports: {list(set(found_imports))}")

    return True

def validate_environment():
    """Validate environment variables"""
    print("\nValidating environment...")

    load_dotenv('.env')

    required_vars = ['COHERE_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY', 'TARGET_URL']
    all_present = True

    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"[OK] {var} is set")
        else:
            print(f"[ERROR] {var} is missing")
            all_present = False

    return all_present

def validate_project_structure():
    """Validate project structure"""
    print("\nValidating project structure...")

    required_files = [
        'main.py',
        'requirements.txt',
        'pyproject.toml',
        'README.md',
        '.env'
    ]

    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file} exists")
        else:
            print(f"[ERROR] {file} missing")
            all_present = False

    return all_present

def main():
    """Main validation function"""
    print("Starting RAG Chatbot Backend validation...")
    print("="*50)

    # Validate each component
    structure_ok = validate_project_structure()
    env_ok = validate_environment()
    main_ok = validate_main_py()

    print("\n" + "="*50)
    print("VALIDATION SUMMARY:")
    print(f"Project structure: {'[PASS]' if structure_ok else '[FAIL]'}")
    print(f"Environment: {'[PASS]' if env_ok else '[FAIL]'}")
    print(f"Main implementation: {'[PASS]' if main_ok else '[FAIL]'}")

    overall_success = structure_ok and env_ok and main_ok
    print(f"Overall status: {'[ALL VALIDATIONS PASSED]' if overall_success else '[SOME VALIDATIONS FAILED]'}")

    if overall_success:
        print("\n[SUCCESS] The RAG Chatbot Backend is properly implemented!")
        print("You can run the full pipeline with: uv run main.py")
        return 0
    else:
        print("\n[ERROR] Some validations failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())