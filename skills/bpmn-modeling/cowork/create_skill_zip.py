"""Create a ZIP file for Claude.ai Cowork upload.

Builds the skill zip with:
- Cowork-specific SKILL.md (replaces the normal SKILL.md)
- Bundled wheels for offline installation
- Forward slashes for Linux compatibility
"""

import zipfile
import os
from pathlib import Path

# Paths relative to this script's location
SCRIPT_DIR: Path = Path(__file__).resolve().parent
SKILL_DIR: Path = SCRIPT_DIR.parent
REPO_ROOT: Path = SKILL_DIR.parent.parent
ZIP_OUTPUT: Path = REPO_ROOT / "bpmn-modeling-skill.zip"
COWORK_SKILL_MD: Path = SCRIPT_DIR / "SKILL.md"
WHEELS: list[Path] = sorted(SCRIPT_DIR.glob("*.whl"))

EXCLUDE_FILES: set[str] = {"nulltxt.txt"}
EXCLUDE_DIRS: set[str] = {"__pycache__", "cowork"}

if not WHEELS:
    raise FileNotFoundError(f"No .whl files found in {SCRIPT_DIR}")

with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
    # Pack skill files (excluding cowork/)
    for root, dirs, files in os.walk(SKILL_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for filename in files:
            if filename in EXCLUDE_FILES:
                continue
            filepath: Path = Path(root) / filename
            arcname: str = str(filepath.relative_to(SKILL_DIR.parent)).replace(os.sep, "/")

            # Replace normal SKILL.md with Cowork variant
            if filepath == SKILL_DIR / "SKILL.md":
                zf.write(COWORK_SKILL_MD, arcname)
                print(f"  + {arcname} (from cowork/SKILL.md)")
            else:
                zf.write(filepath, arcname)
                print(f"  + {arcname}")

    # Add wheels from cowork/
    for whl in WHEELS:
        arcname = f"bpmn-modeling/wheels/{whl.name}"
        zf.write(whl, arcname)
        print(f"  + {arcname}")

print(f"\nCreated: {ZIP_OUTPUT}")
