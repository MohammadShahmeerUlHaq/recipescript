"""
Test Runner for RecipeScript Compiler
Runs all test files and reports results
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from compiler import run_file

def main():
    """Run all test files"""
    test_files = [
        'test1.recipe',
        'test2.recipe',
        'test3.recipe',
        'test4.recipe',
        'test5.recipe',
        'test6.recipe',
        'test7_input_auto.recipe',
    ]
    
    print("=" * 60)
    print("RecipeScript Compiler - Test Suite")
    print("=" * 60)
    
    results = []
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n{'=' * 60}")
            print(f"Running: {test_file}")
            print(f"{'=' * 60}")
            success = run_file(test_file)
            results.append((test_file, success))
        else:
            print(f"\n❌ Test file not found: {test_file}")
            results.append((test_file, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_file, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_file}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    main()
