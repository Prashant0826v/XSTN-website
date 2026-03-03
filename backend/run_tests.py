"""Run tests and save output to a file."""
import subprocess
import sys

result = subprocess.run(
    [sys.executable, 'manage.py', 'test', 'tests.test_all', '--verbosity=2'],
    capture_output=True, text=True
)

with open('test_output.log', 'w', encoding='utf-8') as f:
    f.write("=== STDERR (Test Results) ===\n")
    f.write(result.stderr)
    f.write("\n=== STDOUT ===\n")
    f.write(result.stdout)
    f.write(f"\n=== EXIT CODE: {result.returncode} ===\n")

print(f"Exit code: {result.returncode}")
print(f"Output written to test_output.log")
