import subprocess
import json
import re

cmd = [
    "gallery-dl",
    "-v",
    "-J",
    "--cookies-from-browser", "firefox",
    "https://www.tiktok.com/@fruit.story739/video/7697687396497902862?is_from_webapp=1&sender_device=pc"
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