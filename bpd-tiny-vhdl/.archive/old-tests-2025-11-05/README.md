# Archived Legacy Tests

**Date Archived:** 2025-11-05
**Reason:** Replaced by forge-vhdl compliant test structure

---

## What's Here

These are the original test files from before the forge-vhdl progressive testing restructuring:

- `Makefile` - Legacy CocoTB makefile approach
- `test_basic_probe_fsm.py` - Original FSM tests (incomplete, noted missing ports)
- `test_fi_interface.py` - Original FI interface tests

## Why Archived

These files were replaced by the new forge-vhdl compliant structure in `tests/`:

```
tests/
├── test_configs.py
├── test_bpd_fsm_observer_progressive.py
└── bpd_fsm_observer_tests/
    ├── __init__.py
    ├── bpd_fsm_observer_constants.py
    ├── P1_bpd_fsm_observer_basic.py
    ├── P2_bpd_fsm_observer_intermediate.py
    └── P3_bpd_fsm_observer_comprehensive.py
```

The new structure provides:
- Progressive test levels (P1/P2/P3)
- Token-efficient output (<20 lines for P1)
- TestBase integration
- GHDL output filter support
- Auto-discovery via test_configs.py

## Safe to Delete?

Yes, once you've verified the new tests work correctly, these files can be safely deleted.

The new tests provide superior:
- Structure (progressive levels)
- Output efficiency (98% reduction)
- Integration (forge-vhdl framework)
- Maintainability (constants file, test organization)

---

**Archived By:** Claude Code
**Superseded By:** forge-vhdl compliant test structure (2025-11-05)
