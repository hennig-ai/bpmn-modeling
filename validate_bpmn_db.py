"""Validiert die BPMN-Datenbank durch Initialisierung des Navigators.

Laedt die BPMN-Konfiguration aus config.ini und initialisiert den Navigator.
Gibt grundlegende Statistiken zur geladenen Prozessbeschreibung aus.

Exit Codes:
    0: Validierung erfolgreich
    1: Validierung fehlgeschlagen

Usage:
    python src/validate_bpmn_db.py
"""

import os
import sys

from basic_framework import (
    proc_frame_start,
    proc_frame_end,
    log_msg,
    get_global_par,
)
from bpmn_lib.navigator import create_navigator

from engine.constants import SCHEMA_FILENAME, HIERARCHY_FILENAME
from utils.file_utils import get_version


def main() -> None:
    """Hauptfunktion - Initialisiert Navigator und gibt Statistiken aus."""
    proc_frame_start("validate_bpmn_db", get_version(), "config.ini")

    try:
        log_msg("=== BPMN Database Validation ===")
        print("=== BPMN Database Validation ===")
        print()

        # Konfigurationswerte ausgeben
        model_dir = get_global_par("model_schema_data", "process_description")
        schema_file = os.path.join(model_dir, SCHEMA_FILENAME)
        hierarchy_file = os.path.join(model_dir, HIERARCHY_FILENAME)
        data_file = get_global_par("data_file", "process_description")
        log_dir = "logs"
        schema_name = get_global_par("schema_name", "process_description")

        print("Konfiguration:")
        print(f"  model_dir:      {model_dir}")
        print(f"  schema_file:    {schema_file}")
        print(f"  data_file:      {data_file}")
        print(f"  hierarchy_file: {hierarchy_file}")
        print(f"  log_dir:        {log_dir}")
        print(f"  schema_name:    {schema_name}")
        print()

        # Navigator erstellen via bpmn_lib
        log_msg("Initialisiere Navigator...")
        navigator = create_navigator(
            schema_file=schema_file,
            data_file=data_file,
            hierarchy_file=hierarchy_file,
            log_dir=log_dir,
            schema_name=schema_name,
        )

        # Statistiken ausgeben
        element_count = len(navigator.m_element_mapping)
        process_count = len(navigator.m_process_elements)

        log_msg(f"Navigator initialisiert: {element_count} Elemente, {process_count} Prozesse")
        print("Navigator erfolgreich initialisiert!")
        print()
        print("Statistiken:")
        print(f"  Elemente gesamt:  {element_count}")
        print(f"  Prozesse:         {process_count}")

        # Prozess-Details ausgeben
        print()
        print("Prozesse:")
        for process_id, elements in navigator.m_process_elements.items():
            process_name = navigator.get_element_attribute(process_id, "name")
            print(f"  [{process_id}] {process_name}: {len(elements)} Elemente")

        # Start-Events finden und ausgeben
        print()
        print("Start-Events:")
        for process_id in navigator.m_process_elements.keys():
            start_events = navigator.get_all_start_events(process_id)
            for start_id in start_events:
                start_name = navigator.get_element_attribute(start_id, "name")
                print(f"  [{start_id}] {start_name}")

        print()
        print("=== Validation erfolgreich ===")
        log_msg("=== Validation erfolgreich ===")
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
