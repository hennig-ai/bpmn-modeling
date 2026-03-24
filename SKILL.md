---
name: bpmn-modeling-light
description: >
  This skill generates and modifies BPMN process models in Markdown table format
  according to `references/bpmn-schema.md`. It is used exclusively when the user
  explicitly wants to create, extend, or modify a BPMN model. Trigger terms include
  BPMN, Start Event, Sequence Flow, Gateway, User Task, and other BPMN-specific terms.
  Do not trigger for general process descriptions without BPMN context, for other
  model types (e.g. data model), or for general BPMN questions without a modeling request.
metadata:
  version: "2.0"
---

# BPMN Modeling Light — Skill

## Trigger Examples

Examples that trigger:
- "Create a BPMN model for an order process"
- "Model this as BPMN"
- "Add an Exclusive Gateway" (in the context of an existing BPMN model)
- "Let's modify the BPMN model order-process.md" (modification of an existing BPMN file)

**Do NOT trigger for:**
- "Let's describe a process" (no BPMN context)
- "Model an order process" (no explicit BPMN context)
- "Create a data model" (different model type)
- General process descriptions without BPMN context
- General BPMN questions without a modeling request

---

## Reference Files

This skill works with the following reference documents in the same repository:

| File | Purpose |
|------|---------|
| `references/bpmn-instance-example.md` | Reference instance: authoritative table format and example data |
| `references/bpmn-hierarchy.md` | Inheritance hierarchy of BPMN elements, `element_type` overview |
| `references/event-detail-tables.md` | Event definition tables and their relationship to `element_type` |
| `references/bpmn-schema.md` | Complete schema documentation of all tables, columns, constraints, value domains |

### Loading Strategy

**MUST load before every modeling task:**
- `references/bpmn-instance-example.md` — authoritative table format and FK relationship patterns
- `references/bpmn-hierarchy.md` — `element_type` mapping
- `references/event-detail-tables.md` — event definition delineation

**Consult as needed:**
- `references/bpmn-schema.md` — only when a specific table definition is unclear (e.g. columns, constraints, value domains of a particular table)

---

## Mode Detection

Determine the mode at the start of each interaction:

### Mode A: New Model
- User describes a process without an existing model
- User wants to "create a new model"
- → Generate a complete new model from scratch

### Mode B: Modification
- User provides an existing model (Markdown tables) and describes changes
- User wants to add, remove, or modify elements
- → Adopt the existing model, apply targeted modifications, output the complete model

**When unclear**: Explicitly ask whether an existing model is present.

---

## Output Format

- Use **exclusively** the Markdown table format from `references/bpmn-instance-example.md`
- All tables with `## TableName` as heading
- Output the complete model (not just modified tables)
- No additional explanations between tables
- Explanations of design decisions **before** or **after** the model, not within it

---

## Rules

### 1. Format Conformity
- Use **EXACTLY** the Markdown table format from `references/bpmn-instance-example.md`
- No deviations in formatting, column order, or structure
- Column names exactly as defined in the schema
- Empty/unfilled optional fields: `##!empty!##` as placeholder value

### 2. Table Order
Tables must be output in the following canonical order. Tables without data rows are omitted (see Rule 3).

1. `bpmn_model`
2. `bpmn_process`
3. `bpmn_element`
4. `message_definition`
5. `signal_definition`
6. `error_definition`
7. `process_element`
8. `activity`
9. `task`
10. `service_task`
11. `user_task`
12. `script_task`
13. `business_rule_task`
14. `subprocess`
15. `call_activity`
16. `event`
17. `message_event_definition`
18. `timer_event_definition`
19. `error_event_definition`
20. `signal_event_definition`
21. `sequence_flow`
22. `gateway`
23. `message_flow`
24. `association`
25. `pool`
26. `lane`
27. `lane_element`
28. `data_object`
29. `data_store`
30. `text_annotation`
31. `data_input`
32. `data_output`
33. `data_association`

### 3. Table Generation — CRITICAL
- **NEVER output empty tables**
- A table is ONLY included in the output if it contains at least one data row (not just the header)
- **FORBIDDEN**: Tables with only a header row and no data rows
- **ALLOWED**: Only tables with header + at least one data row
- The order of actually generated tables must follow the list above (Rule 2)

### 4. Primary Keys (PK)
- Format: three-digit integers with leading zeros (e.g. `001`, `002`)
- Exception: `bpmn_model_id` — format `YYYYMMDD_HHMM_SS_NNN` (e.g. `20251026_1730_56_001`)
- Unique within each table
- For new entries: highest existing PK + 1
- Existing PKs are NEVER changed

### 5. Foreign Keys (FK) — Referential Integrity
- FK values MUST exist in the referenced table
- Schema notation: `<table>.<column>` indicates the reference target
- FK values must be semantically meaningful (not arbitrary)
- During modifications: verify all existing FKs for consistency after the change

### 6. CRITICAL: element_type Population

#### Base Rule
`element_type` contains the MOST SPECIFIC type in the inheritance hierarchy **that has its own `bpmn_element_id`**.

#### Determination Algorithm
1. Identify all tables in which the element has entries
2. Find the DEEPEST table that references `bpmn_element_id` as FK
3. The table name (without prefix/suffix) = element_type

#### Specialization via Subtype Tables vs. Type Columns

The schema uses two mechanisms for specialization:

| Mechanism | element_type | Specialization via |
|-----------|--------------|-------------------|
| **Subtype table** | Table name | Separate table with its own PK |
| **Type column** | Parent table name | Column in the parent table |

#### Overview of All Element Types and Their Specialization

| element_type | Further specialization | Column/Table |
|--------------|----------------------|--------------|
| `event` | event_type (start, end, intermediate_catch, intermediate_throw, boundary) | `event.event_type` |
| `event` | event_definition_type (message, timer, error, signal, none, ...) | `event.event_definition_type` |
| `gateway` | gateway_type (exclusive, inclusive, parallel, event_based, complex) | `gateway.gateway_type` |
| `gateway` | gateway_direction (converging, diverging, mixed) | `gateway.gateway_direction` |
| `subprocess` | is_transaction, triggered_by_event | `subprocess.*` |
| `service_task` | - | Subtype table of `task` |
| `user_task` | - | Subtype table of `task` |
| `script_task` | - | Subtype table of `task` |
| `business_rule_task` | - | Subtype table of `task` |
| `call_activity` | - | Subtype table of `activity` |
| `sequence_flow` | is_default, condition_expression | `sequence_flow.*` |
| `data_object` | is_collection, state | `data_object.*` |

#### IMPORTANT: Event Definitions are NOT bpmn_elements
The tables `message_event_definition`, `timer_event_definition`, `error_event_definition`, `signal_event_definition` have NO `bpmn_element_id` — they reference `event_id`. Therefore, for events with a definition, the `element_type` is always `event`; specialization is done via `event.event_definition_type`.

#### IMPORTANT: Gateways Have NO Subtype Tables
There are no separate tables for `exclusive_gateway`, `parallel_gateway`, etc. The `element_type` is always `gateway`; specialization is done via `gateway.gateway_type`.

#### Common Mistakes to Avoid

**Tasks:**
❌ WRONG: element_type='task' for a User Task
✅ CORRECT: element_type='user_task'

❌ WRONG: element_type='activity' for a Service Task
✅ CORRECT: element_type='service_task'

**Events:**
❌ WRONG: element_type='message_event_definition' for a Message Event
✅ CORRECT: element_type='event' (specialization via event.event_definition_type='message')

**Gateways:**
❌ WRONG: element_type='exclusive_gateway' for an XOR Gateway
✅ CORRECT: element_type='gateway' (specialization via gateway.gateway_type='exclusive')

❌ WRONG: element_type='parallel_gateway' for an AND Gateway
✅ CORRECT: element_type='gateway' (specialization via gateway.gateway_type='parallel')

### 7. Data Integrity
- Observe all constraints defined in the schema
- Use only values from defined value domains (see `references/bpmn-schema.md`)
- Ensure inheritance relationships are consistent
- Every executable process (`is_executable=true`) must have at least one start event and one end event

---

## Workflow

### Mode A: New Model

1. Fully understand the business requirements — ask for clarification if anything is unclear
2. Map BPMN concepts to database structures (reference: `references/bpmn-hierarchy.md`)
3. Generate `bpmn_model_id` using the format `YYYYMMDD_HHMM_SS_001` (current date)
4. Populate all tables top to bottom (canonical order, Rule 2)
5. Output the complete model

### Mode B: Modification

1. Analyze the existing model — capture all PKs, FKs, and relationships
2. Clarify desired changes with the user if needed
3. Modify only the affected tables
4. New entries: PK = current maximum + 1
5. Deleted elements: verify and clean up all dependent FK references
6. Output the **complete** model (not just modified tables)

### When Unclear
- Ask specifically about missing details
- Resolve ambiguities before output
- Confirm critical design decisions (e.g. transaction subprocess, event-based gateway)
- Point out potential BPMN conformity issues

---

## Quality Assurance

The following checks MUST be performed before every output:

1. **Element type correctness**: Verify `element_type` for EVERY entry in `bpmn_element`
2. **FK validation**: Validate all foreign key relationships across tables
3. **BPMN conformity**: Verify all validation rules from `references/bpmn-schema.md`
4. **Process completeness**: For `is_executable=true` — at least one start event and one end event present?
5. **Connectivity**: Are all flow objects reachable via sequence flows?
6. **No empty tables**: Remove all tables without data rows from the output
7. **Table order**: Does the order match the canonical order (Rule 2)?
8. **PK uniqueness**: Are all PKs unique within their table?

---

## Automated Validation

The skill includes a validation script (`validate_bpmn.py`) that programmatically validates BPMN models against the schema and hierarchy.

### Trigger

- **Explicit**: The user requests validation (e.g. "Validate the model", "Check the BPMN file")
- **Automatic**: After the skill has completed ALL modeling changes for a given request. Do NOT run validation after each atomic change — only once the entire modeling task is finished and the model file has been written.

### Invocation

Save the model to a Markdown file, then run:
```bash
python <skill-path>/validate_bpmn.py <model_file>
```

The script writes all output to stdout (results and errors).

### Auto-Repair Loop

When validation reports errors:

1. **Analyze** the validation output
2. **Categorize** each error:
   - **Clearly resolvable**: The correct fix can be unambiguously derived from the schema, hierarchy, and model context (e.g. wrong `element_type`, missing FK, incorrect PK format) → fix automatically
   - **Ambiguous**: The fix requires a design decision or additional information from the user (e.g. missing process elements, contradictory relationships) → ask the user before proceeding
3. **Apply** all clear fixes to the model
4. **Re-validate** by running the script again
5. **Repeat** until validation passes or only ambiguous errors remain that require user input

### Important

- Never suppress or ignore validation errors
- Never skip validation to save time — it is a mandatory quality gate
- If validation fails repeatedly on the same error, do not loop indefinitely — present the issue to the user after 2 failed repair attempts

---

## Error Handling

When BPMN rules are violated:
- Inform the user about the specific rule violation
- Suggest a conforming alternative
- Do NOT create non-conforming models

When requirements are contradictory:
- Explicitly name the contradiction
- Ask which requirement takes priority
- Only model after clarification
