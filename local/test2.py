import subprocess
import json
import re

cmd = [
    "gallery-dl",
    "-v",
    "-J",
    "--cookies-from-browser", "firefox",
    "https://www.youtube.com/watch?v=qU3n_ue5o6E"
]

result = subprocess.run(
    cmd,
    capture_output=True,
    text=True
)

print("Exit code:", result.returncode)
print("STDERR:", result.stderr)
print("STDOUT:", result.stdout)

if re.search(r"\b403\s+Forbidden\b", result.stderr, re.I):
    raise PermissionError("gallery-dl encountered HTTP 403")

data = json.loads(result.stdout)

if not data:
    raise ValueError("gallery-dl returned empty JSON")