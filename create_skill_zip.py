"""Create a ZIP file for Claude.ai Skill upload with forward slashes (Linux-compatible)."""

import zipfile
import os

ZIP_OUTPUT = "bpmn-modeling-skill.zip"
SKILL_DIR = os.path.join("skills", "bpmn-modeling")
EXCLUDE_FILES = {"nulltxt.txt"}
EXCLUDE_DIRS = {"__pycache__"}

with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(SKILL_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for filename in files:
            if filename in EXCLUDE_FILES:
                continue
            filepath: str = os.path.join(root, filename)
            # Replace base path and ensure forward slashes for Linux
            arcname: str = filepath.replace(SKILL_DIR, "bpmn-modeling", 1).replace(os.sep, "/")
            zf.write(filepath, arcname)
            print(f"  + {arcname}")

print(f"\nCreated: {ZIP_OUTPUT}")
