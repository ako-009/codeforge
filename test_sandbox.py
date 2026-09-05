"""
Phase 2 test: Docker sandbox executor.
Tests 3 cases: success, error, timeout.
Run with: python test_sandbox.py
"""
from app.sandbox.executor import execute_code

def test_success():
    print("TEST 1: Normal code")
    result = execute_code("print('hello from sandbox')")
    print(f"  stdout   : {result['stdout'].strip()}")
    print(f"  stderr   : {result['stderr'].strip()}")
    print(f"  exit_code: {result['exit_code']}")
    print(f"  timed_out: {result['timed_out']}")
    assert result['stdout'].strip() == 'hello from sandbox'
    assert result['exit_code'] == 0
    print("  PASSED\n")

def test_syntax_error():
    print("TEST 2: Syntax error")
    result = execute_code("def broken(:\n    pass")
    print(f"  stdout   : {result['stdout'].strip()}")
    print(f"  stderr   : {result['stderr'].strip()[:80]}")
    print(f"  exit_code: {result['exit_code']}")
    assert result['exit_code'] != 0
    print("  PASSED\n")

def test_timeout():
    print("TEST 3: Infinite loop (should timeout in 10s)")
    result = execute_code("while True: pass")
    print(f"  stdout   : {result['stdout'].strip()}")
    print(f"  stderr   : {result['stderr'].strip()}")
    print(f"  timed_out: {result['timed_out']}")
    assert result['timed_out'] == True
    print("  PASSED\n")

if __name__ == "__main__":
    test_success()
    test_syntax_error()
    test_timeout()
    print("All Phase 2 tests passed!")
