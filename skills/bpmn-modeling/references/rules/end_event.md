# Elementregeln: End-Event

**Hierarchie-Ebene:** end_event

**Uebergeordnete Regeln:** Es gelten zusaetzlich die Regeln aus [flow_object.md](flow_object.md)

---

| rule_id | level | element_type | where_clause | assertion | description | message_template | spec_reference | spec_verified | personal |
|---------|-------|-------------|-------------|-----------|-------------|-----------------|----------------|---------------|----------|
| END-001 | spec_v2 | end_event | | COUNT(outgoing_flows) == 0 | Ein End-Event darf keine ausgehenden Sequence Flows besitzen. | End-Event {element_id} has outgoing sequence flows | BPMN 2.0.2, Section 10.5.4 | no | |
| END-002 | spec_v2 | end_event | | COUNT(incoming_flows) >= 1 | Ein End-Event muss mindestens einen eingehenden Sequence Flow haben. | End-Event {element_id} has no incoming sequence flows | BPMN 2.0.2, Section 10.5.4 | no | |
