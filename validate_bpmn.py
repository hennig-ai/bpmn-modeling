"""Validiert die BPMN-Datenbank durch Initialisierung des Navigators.

Laedt die BPMN-Konfiguration aus config.ini und initialisiert den Navigator.
Gibt grundlegende Statistiken zur geladenen Prozessbeschreibung aus.

Exit Codes:
    0: Validierung erfolgreich
    1: Validierung fehlgeschlagen

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
SCHEMA_NAME: str = "Aktor-Pipeline Schema"


def get_version() -> str:
    """Liest die Projektversion aus pyproject.toml.

    Sucht die pyproject.toml im Projektverzeichnis (relativ zu diesem Modul)
    und extrahiert die Version aus der [project] Sektion.

    Returns:
        Die Versionsnummer als String (z.B. "0.1.0")

    Raises:
        FileNotFoundError: Wenn pyproject.toml nicht gefunden wird
        KeyError: Wenn [project].version nicht definiert ist
    """
    project_root = Path(__file__).parent
    pyproject_path = project_root / "pyproject.toml"

    if not pyproject_path.exists():
        log_and_raise(FileNotFoundError(f"pyproject.toml nicht gefunden: {pyproject_path}"))

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    if "project" not in data:
        log_and_raise(KeyError("[project] Sektion fehlt in pyproject.toml"))

    if "version" not in data["project"]:
        log_and_raise(KeyError("[project].version fehlt in pyproject.toml"))

    version: str = data["project"]["version"]
    return version


def main() -> None:
    """Hauptfunktion - Initialisiert Navigator und gibt Statistiken aus."""
    #proc_frame_start("validate_bpmn", get_version(), "config.ini")
    proc_frame_start("validate_bpmn", get_version())

    if len(sys.argv) < 2:
        log_and_raise(ValueError("Usage: python validate_bpmn.py <data_file>"))

    try:
        log_msg("=== BPMN Model Validation ===")

        # Pfade relativ zum Skript-Verzeichnis auflösen
        script_dir: Path = Path(__file__).parent
        references_dir: Path = script_dir / "references"
        schema_file: str = str(references_dir / SCHEMA_FILENAME)
        hierarchy_file: str = str(references_dir / HIERARCHY_FILENAME)
        data_file: str = sys.argv[1]
        log_dir: str = "logs"
        schema_name: str = SCHEMA_NAME

        # Navigator erstellen via bpmn_lib
        #log_msg("Initialize Navigator...")
        navigator = create_navigator(
            schema_file=schema_file,
            data_file=data_file,
            hierarchy_file=hierarchy_file,
            log_dir=log_dir
        )

        # Statistiken ausgeben
        element_count = len(navigator.m_element_mapping)
        process_count = len(navigator.m_process_elements)

        #log_msg(f"Navigator initialized: {element_count} elements, {process_count} Processes")

        log_msg("=== Validation successfull ===")
        proc_frame_end()

    except Exception as e:
        print()
        print("=== Validation FEHLGESCHLAGEN ===")
        print()
        print(f"Fehler: {e}")
        log_msg(f"Validation fehlgeschlagen: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
