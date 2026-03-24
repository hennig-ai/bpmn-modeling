"""Validates a BPMN model by initializing the navigator.

Loads the BPMN schema and hierarchy, then initializes the navigator
with the given data file. Outputs basic statistics about the loaded
process description.

Exit Codes:
    0: Validation successful
    1: Validation failed

Usage:
    python validate_bpmn.py <data_file>
"""

import sys
import tomllib
from pathlib import Path

from basic_framework import (
    proc_frame_start,
    proc_frame_end,
    log_msg,
)
from basic_framework.proc_frame import log_and_raise
from bpmn_lib.navigator import create_navigator

SCHEMA_FILENAME: str = "bpmn-schema.md"
HIERARCHY_FILENAME: str = "bpmn-hierarchy.md"


def get_version() -> str:
    """Reads the project version from pyproject.toml.

    Locates pyproject.toml relative to this module and extracts the
    version from the [project] section.

    Returns:
        The version number as string (e.g. "0.1.0")

    Raises:
        FileNotFoundError: If pyproject.toml is not found
        KeyError: If [project].version is not defined
    """
    project_root = Path(__file__).parent
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
    proc_frame_start("validate_bpmn", get_version())

    if len(sys.argv) < 2:
        log_and_raise(ValueError("Usage: python validate_bpmn.py <data_file>"))

    try:
        log_msg("=== BPMN Model Validation ===")

        # Resolve paths relative to script directory
        script_dir: Path = Path(__file__).parent
        references_dir: Path = script_dir / "references"
        schema_file: str = str(references_dir / SCHEMA_FILENAME)
        hierarchy_file: str = str(references_dir / HIERARCHY_FILENAME)
        data_file: str = sys.argv[1]
        log_dir: str = "logs"

        # Create navigator via bpmn_lib
        #log_msg("Initialize Navigator...")
        navigator = create_navigator(
            schema_file=schema_file,
            data_file=data_file,
            hierarchy_file=hierarchy_file
        )

        # Output statistics
        element_count = len(navigator.m_element_mapping)
        process_count = len(navigator.m_process_elements)

        #log_msg(f"Navigator initialized: {element_count} elements, {process_count} Processes")

        log_msg("=== Validation successfull ===")
        proc_frame_end()

    except Exception as e:
        log_msg(f"Validation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
