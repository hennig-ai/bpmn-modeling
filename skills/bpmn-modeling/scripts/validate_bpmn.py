"""Validates a BPMN model by initializing the navigator.

Loads the BPMN schema and hierarchy, then initializes the navigator
with the given data file. Outputs basic statistics about the loaded
process description.

Exit Codes:
    0: Validation successful
    1: Validation failed

Usage:
    python validate_bpmn.py <data_file> [validation_level]

Layout assumption:
    This script expects a sibling ``references/`` directory containing
    ``bpmn-schema.md``, ``bpmn-hierarchy.md`` and ``rules/``::

        <root>/
            scripts/validate_bpmn.py
            references/
                bpmn-schema.md
                bpmn-hierarchy.md
                rules/*.md

    ``<root>`` is derived from ``__file__``; no absolute path or CLI
    argument for the metadata directory is required.

Validation Levels:
    The optional third argument selects which rule set is applied. If
    omitted, "best_practice" is used.

    spec_v2:
        Applies all rules required by the BPMN 2.0 specification
        (includes the basic rule set).
    best_practice (default):
        Applies spec_v2 rules plus additional best-practice rules
        recommended for clean, maintainable BPMN models.
    personal:
        Applies the best_practice rule set, additionally includes any
        rule explicitly marked as ``personal: include`` and skips any
        rule marked as ``personal: skip``. Useful for project- or
        author-specific rule customizations.
"""

import sys
import tomllib
from pathlib import Path

from basic_framework import (
    proc_frame_start,
    proc_frame_end
)
from basic_framework.proc_frame import log_and_raise
from bpmn_lib.navigator import create_navigator
from bpmn_lib.validation import BPMNValidationError

SCHEMA_FILENAME: str = "bpmn-schema.md"
HIERARCHY_FILENAME: str = "bpmn-hierarchy.md"


def get_version() -> str:
    """Reads the project version from pyproject.toml.

    Locates pyproject.toml relative to this module and extracts the
    version from the [project] section.

    Returns:
        The version number as string (e.g. "1.0.0")

    Raises:
        FileNotFoundError: If pyproject.toml is not found
        KeyError: If [project].version is not defined
    """
    project_root = Path(__file__).parent.parent
    pyproject_path = project_root / "pyproject.toml"

    if not pyproject_path.exists():
        log_and_raise(FileNotFoundError(f"pyproject.toml not found: {pyproject_path}"))

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    if "project" not in data:
        log_and_raise(KeyError("[project] section missing in pyproject.toml"))

    if "version" not in data["project"]:
        log_and_raise(KeyError("[project].version missing in pyproject.toml"))

    version: str = data["project"]["version"]
    return version


def main() -> None:
    """Main function - initializes navigator and outputs statistics."""
    #proc_frame_start("validate_bpmn", get_version(), "config.ini")
    proc_frame_start("validate_bpmn", get_version(), error_only=True)

    try:
        if len(sys.argv) < 2:
            log_and_raise(ValueError("Usage: python validate_bpmn.py <data_file> [validation_level]"))

        print(f"Validating BPMN model...")

        data_file: str = sys.argv[1]
        validation_level: str = sys.argv[2] if len(sys.argv) >= 3 else "best_practice"
        metadata_dir: Path = (Path(__file__).parent.parent / "references").resolve()
        schema_file: str = str(metadata_dir / SCHEMA_FILENAME)
        hierarchy_file: str = str(metadata_dir / HIERARCHY_FILENAME)

        # Create navigator via bpmn_lib
        navigator = create_navigator(
            schema_file=schema_file,
            data_file=data_file,
            hierarchy_file=hierarchy_file,
            report_target=sys.stdout,
            rules_dir=str(metadata_dir / "rules"),
            validation_level=validation_level
        )

        # Output statistics
        element_count = len(navigator.m_element_mapping)
        process_count = len(navigator.m_process_elements)

        print(f"Validation successful.")
        proc_frame_end()

    except BPMNValidationError as e:
        print(f"Validation failed: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"System error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
