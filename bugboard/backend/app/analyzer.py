import os
import zipfile
import shutil
from typing import Dict, Tuple

def extract_and_analyze_project(zip_path: str, extract_dir: str) -> Dict[str, int]:
    """Extracts zip safely and counts files."""
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Basic zip-slip protection
        for member in zip_ref.namelist():
            member_path = os.path.abspath(os.path.join(extract_dir, member))
            if not member_path.startswith(os.path.abspath(extract_dir)):
                raise Exception("Attempted Zip-Slip attack")
        
        zip_ref.extractall(extract_dir)

    stats = {
        "file_count": 0,
        "python_file_count": 0,
        "test_file_count": 0
    }

    for root, _, files in os.walk(extract_dir):
        for file in files:
            stats["file_count"] += 1
            if file.endswith('.py'):
                stats["python_file_count"] += 1
            if file.startswith('test_') and file.endswith('.py') or file.endswith('_test.py'):
                stats["test_file_count"] += 1
                
    return stats

def get_code_snippet(file_path: str, line_number: int, context_lines: int = 5) -> str:
    """Reads a file and returns a code snippet around the given line number."""
    if not os.path.exists(file_path):
        return ""
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return ""

    if not lines or line_number <= 0 or line_number > len(lines):
        return ""
        
    start_idx = max(0, line_number - context_lines - 1)
    end_idx = min(len(lines), line_number + context_lines)
    
    snippet = ""
    for i in range(start_idx, end_idx):
        snippet += f"{i + 1}: {lines[i]}"
        
    return snippet

def deterministic_analyze(snippet: str) -> Tuple[str, str, str]:
    """Analyzes code snippet and returns (potential_cause, suggested_fix, reproduction_steps)."""
    snippet_lower = snippet.lower()
    
    if "email" in snippet_lower or "duplicate" in snippet_lower or "integrityerror" in snippet_lower:
        return (
            "Possible unique constraint violation or missing uniqueness check before insert.",
            "Add a try-except block to catch IntegrityError or query the database first to verify uniqueness.",
            "1. Submit a request with a duplicate email.\n2. Observe the unhandled server error."
        )
    elif "none" in snippet_lower or "nullable" in snippet_lower:
        return (
            "Possible null pointer exception or missing null check.",
            "Add a check for 'is not None' before accessing attributes or handle the case where the variable is None.",
            "1. Provide a payload that omits an optional but internally required field.\n2. Trigger the endpoint to see a NoneType error."
        )
    else:
        return (
            "General logic error or unhandled exception in the code block.",
            "Review the specific business logic around these lines, add proper error handling and logging.",
            "1. Follow standard usage path for this file/function.\n2. Observe unexpected behavior."
        )
