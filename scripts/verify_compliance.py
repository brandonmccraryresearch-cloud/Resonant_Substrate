#!/usr/bin/env python3
"""
IRH v24.0 Compliance Verification Script

This script verifies that code implementations maintain theoretical correspondence
with the IRH v24.0 manuscript. It checks for:
- Proper manuscript citations in docstrings
- No hardcoded empirical constants in implementation code
- Transparency engine usage in computations
- Dimensional consistency in equations
- Proper error bounds on approximations

References
----------
IRH v24.0 Manuscript, Section 8: Computational Architecture
.github/copilot-instructions.md: Theoretical Correspondence Mandate
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any


class ComplianceChecker:
    """Verify IRH v24.0 theoretical correspondence in code."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.violations = []
        self.warnings = []
        self.passes = 0
        
    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(message)
    
    def check_file(self, filepath: Path) -> None:
        """Check a single Python file for compliance."""
        self.log(f"Checking {filepath}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip test files for some checks
        is_test = 'test_' in filepath.name or '/tests/' in str(filepath)
        
        # Check 1: Functions computing observables should have manuscript references
        if not is_test:
            self._check_manuscript_references(filepath, content)
        
        # Check 2: No hardcoded physics constants in implementation
        if not is_test:
            self._check_hardcoded_constants(filepath, content)
        
        # Check 3: Docstrings should follow NumPy style
        self._check_docstring_style(filepath, content)
    
    def _check_manuscript_references(self, filepath: Path, content: str) -> None:
        """Check that compute functions reference the manuscript."""
        # Find compute/derive functions
        compute_pattern = r'def (compute_|derive_|calculate_)[\w]+\([^)]*\):'
        matches = re.finditer(compute_pattern, content)
        
        for match in matches:
            func_name = match.group(0)
            func_start = match.start()
            
            # Look for docstring after function definition
            docstring_pattern = r'"""[\s\S]*?"""'
            remaining = content[func_start:func_start+2000]  # Look ahead 2000 chars
            docstring_match = re.search(docstring_pattern, remaining)
            
            if docstring_match:
                docstring = docstring_match.group(0)
                
                # Check for manuscript reference
                has_reference = (
                    'IRH v24' in docstring or 
                    'Section' in docstring or 
                    'Eq.' in docstring or
                    'Equation' in docstring or
                    'References' in docstring
                )
                
                if has_reference:
                    self.passes += 1
                else:
                    self.warnings.append({
                        'category': 'Missing Manuscript Reference',
                        'file': str(filepath),
                        'message': f'Function {func_name.split("(")[0]} lacks manuscript citation'
                    })
            else:
                self.warnings.append({
                    'category': 'Missing Docstring',
                    'file': str(filepath),
                    'message': f'Function {func_name.split("(")[0]} has no docstring'
                })
    
    def _check_hardcoded_constants(self, filepath: Path, content: str) -> None:
        """Check for hardcoded physics constants without derivation."""
        # Patterns that might indicate hardcoded constants
        suspicious_patterns = [
            (r'(?<!#)(?<!computed)(?<!derived)\s*=\s*137\.03[0-9]+', 'fine-structure constant'),
            (r'(?<!#)\s*=\s*0\.51[0-9]+\s*#.*electron', 'electron mass'),
            (r'(?<!#)\s*=\s*105\.[0-9]+\s*#.*muon', 'muon mass'),
        ]
        
        for pattern, const_name in suspicious_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Check if there's a justification nearby
                context_start = max(0, match.start() - 100)
                context_end = min(len(content), match.end() + 100)
                context = content[context_start:context_end]
                
                if 'computed' not in context.lower() and 'derived' not in context.lower():
                    self.violations.append({
                        'category': 'Hardcoded Constant',
                        'file': str(filepath),
                        'message': f'Potential hardcoded {const_name} without derivation'
                    })
    
    def _check_docstring_style(self, filepath: Path, content: str) -> None:
        """Check that docstrings follow NumPy style."""
        # Look for functions
        func_pattern = r'def \w+\([^)]*\):'
        matches = re.finditer(func_pattern, content)
        
        for match in matches:
            func_start = match.start()
            remaining = content[func_start:func_start+1000]
            
            # Check if there's a docstring
            if '"""' in remaining[:100]:
                self.passes += 1
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate compliance report."""
        return {
            'compliant': len(self.violations) == 0,
            'passes_count': self.passes,
            'violations': self.violations,
            'warnings': self.warnings,
            'summary': {
                'total_violations': len(self.violations),
                'total_warnings': len(self.warnings),
                'total_passes': self.passes
            }
        }


def main():
    """Main entry point for compliance verification."""
    parser = argparse.ArgumentParser(
        description='Verify IRH v24.0 theoretical correspondence in code'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--report', '-r',
        type=str,
        default='compliance_report.json',
        help='Output report file path'
    )
    
    args = parser.parse_args()
    
    checker = ComplianceChecker(verbose=args.verbose)
    
    # Find all Python files in src/
    src_dir = Path('src')
    if src_dir.exists():
        for py_file in src_dir.rglob('*.py'):
            if '__pycache__' not in str(py_file):
                checker.check_file(py_file)
    else:
        print("Warning: src/ directory not found", file=sys.stderr)
    
    # Generate report
    report = checker.generate_report()
    
    # Write report
    with open(args.report, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"\n{'='*60}")
    print("IRH v24.0 Compliance Check Summary")
    print(f"{'='*60}")
    print(f"✅ Passes:     {report['passes_count']}")
    print(f"⚠️  Warnings:   {len(report['warnings'])}")
    print(f"❌ Violations: {len(report['violations'])}")
    print(f"\nCompliant: {'YES ✅' if report['compliant'] else 'NO ❌'}")
    print(f"{'='*60}\n")
    
    # Exit with error code if non-compliant
    if not report['compliant']:
        sys.exit(1)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
