#!/usr/bin/env python3
"""
Run All OpenCog Agent Atoms Examples

This script executes all example files in sequence to demonstrate
the full range of agent atom types and patterns.
"""

import sys
import os
import importlib.util

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))


def run_example(filename, description):
    """Run a single example file"""
    print(f"\n{'#'*80}")
    print(f"# Running: {filename}")
    print(f"# {description}")
    print(f"{'#'*80}\n")
    
    try:
        # Import and run the example
        filepath = os.path.join(os.path.dirname(__file__), filename)
        spec = importlib.util.spec_from_file_location("example", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print(f"\n✓ {filename} completed successfully\n")
        return True
    except Exception as e:
        print(f"\n✗ Error running {filename}: {str(e)}\n")
        return False


def main():
    """Run all examples"""
    print("="*80)
    print("OpenCog Agent Atoms - Complete Example Suite")
    print("Agent Zero HCK Cognitive Architecture")
    print("="*80)
    
    examples = [
        ("01_basic_agent_atoms.py", "Basic agent atom types and relationships"),
        ("05_self_referential_atoms.py", "Self-referential and meta-cognitive atoms"),
        ("06_complex_agent_atoms.py", "Complex multi-agent patterns and hierarchies"),
    ]
    
    results = []
    for filename, description in examples:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            success = run_example(filename, description)
            results.append((filename, success))
        else:
            print(f"\n⚠ Skipping {filename} (file not found)")
            results.append((filename, False))
        
        # Pause between examples
        print("\n" + "-"*80)
        input("Press Enter to continue to next example...")
    
    # Print summary
    print("\n" + "="*80)
    print("Example Suite Summary")
    print("="*80)
    
    for filename, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {status}: {filename}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    print(f"\nTotal: {total} examples")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print("="*80)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
