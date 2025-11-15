# forge-vhdl Progressive Testing Integration

**Date:** 2025-11-05
**Status:** ✅ Complete - Ready for testing

---

## What We Did

Restructured the `proposed_cocotb_test/test_bpd_fsm_observer.py` tests to follow the **forge-vhdl progressive testing standard** as defined in `libs/forge-vhdl/CLAUDE.md`.

### Original Structure (Proposed Tests)
```
proposed_cocotb_test/
└── test_bpd_fsm_observer.py    # Single file, 10 tests, ~500 lines
```

### New Structure (forge-vhdl Compliant)
```
tests/
├── test_configs.py                              # Test discovery config
├── test_bpd_fsm_observer_progressive.py         # Progressive orchestrator
│
└── bpd_fsm_observer_tests/                      # Test package
    ├── __init__.py
    ├── bpd_fsm_observer_constants.py            # Shared constants, utilities
    ├── P1_bpd_fsm_observer_basic.py             # Tests 1-3 (essential)
    ├── P2_bpd_fsm_observer_intermediate.py      # Tests 4-7 (standard validation)
    └── P3_bpd_fsm_observer_comprehensive.py     # Tests 8-10 (edge cases)
```

---

## Key Changes

### 1. Progressive Test Levels
Tests are now split into 3 levels controlled by `TEST_LEVEL` environment variable:

| Level | Tests | Target Output | Purpose |
|-------|-------|---------------|---------|
| **P1** | 3 tests | <20 lines | LLM-optimized, essential validation |
| **P2** | 4 tests | <50 lines | Standard validation, fault detection |
| **P3** | 3 tests | <100 lines | Comprehensive, edge cases, stress test |

### 2. TestBase Integration
- All tests now inherit from `TestBase` (from forge-vhdl)
- Uses `await self.test("name", self.test_fn)` wrapper
- Automatic verbosity control via `VerbosityLevel`
- Integration with GHDL output filter

### 3. Shared Constants
Extracted all constants to `bpd_fsm_observer_constants.py`:
- `MODULE_NAME`, `HDL_SOURCES`, `HDL_TOPLEVEL`
- FSM state constants
- FSM observer configuration
- Test value sets (P1/P2/P3)
- Voltage conversion utilities
- Error message templates

### 4. forge-vhdl Test Infrastructure
Tests now use forge-vhdl utilities:
- `setup_clock()` from `conftest.py`
- `reset_active_low()` from `conftest.py`
- `TestBase` from `test_base.py`
- GHDL output filter (via `run.py`)

---

## How to Run Tests

### Prerequisites
```bash
# Ensure you're in the BPD-002v2 root
cd /Users/vmars20/TTOP/BPD-002v2

# Sync dependencies
uv sync
```

### Running Tests

**From bpd-tiny-vhdl/tests directory:**
```bash
cd libs/bpd-tiny-vhdl/tests

# P1 tests (default, LLM-optimized, <20 lines)
uv run python ../../forge-vhdl/tests/run.py bpd_fsm_observer

# P2 tests (standard validation, <50 lines)
TEST_LEVEL=P2_INTERMEDIATE uv run python ../../forge-vhdl/tests/run.py bpd_fsm_observer

# P3 tests (comprehensive, <100 lines)
TEST_LEVEL=P3_COMPREHENSIVE uv run python ../../forge-vhdl/tests/run.py bpd_fsm_observer
```

**Alternative: From forge-vhdl/tests directory:**
```bash
cd libs/forge-vhdl/tests

# Add bpd-tiny-vhdl tests to PYTHONPATH
export PYTHONPATH="../../bpd-tiny-vhdl/tests:$PYTHONPATH"

# Run tests
uv run python run.py bpd_fsm_observer
```

### Debugging

**If tests fail due to import errors:**
```bash
# Check Python path includes forge-vhdl tests
python -c "import sys; print('\n'.join(sys.path))"

# Manually add forge-vhdl to PYTHONPATH
export PYTHONPATH="/Users/vmars20/TTOP/BPD-002v2/libs/forge-vhdl/tests:$PYTHONPATH"
```

**Run without GHDL filter (verbose output):**
```bash
GHDL_FILTER_LEVEL=none uv run python ../../forge-vhdl/tests/run.py bpd_fsm_observer
```

**Increase CocoTB verbosity:**
```bash
COCOTB_LOG_LEVEL=DEBUG uv run python ../../forge-vhdl/tests/run.py bpd_fsm_observer
```

---

## Test Coverage

### P1 - Basic Tests (Essential, <5s runtime)
1. **Reset behavior** - Verify IDLE voltage (0.0V) after reset
2. **IDLE → ARMED transition** - Verify voltage increase (0.0V → 0.625V)
3. **State voltage stairstep** - Verify monotonic voltage progression

### P2 - Intermediate Tests (Standard, <30s runtime)
4. **Sign-flip fault from IDLE** - Verify fault indication (~0.0V)
5. **Sign-flip fault from ARMED** - Verify negative voltage with magnitude preservation
6. **Sign-flip fault from FIRING** - Documentation test (fault injection TBD)
7. **Fault clear recovery** - Verify return to IDLE voltage after fault_clear

### P3 - Comprehensive Tests (Full, <2min runtime)
8. **Voltage spreading** - Verify automatic voltage interpolation formula
9. **Rapid state changes** - Stress test with 2 rapid FSM cycles
10. **Configuration documentation** - Print FSM observer configuration and usage

---

## forge-vhdl Compliance Checklist

✅ Progressive test structure (P1/P2/P3 in separate files)
✅ Shared constants file with `MODULE_NAME`, `HDL_SOURCES`, `HDL_TOPLEVEL`
✅ TestBase inheritance with `await self.test()` wrapper
✅ Uses forge-vhdl `conftest` utilities (`setup_clock`, `reset_active_low`)
✅ Test config in `test_configs.py` for auto-discovery
✅ Progressive orchestrator (`test_*_progressive.py`)
✅ Integration with `run.py` and GHDL output filter
✅ Environment variable control (`TEST_LEVEL`)
✅ Output targets (P1 <20 lines, P2 <50 lines, P3 <100 lines)

---

## Comparison: Before vs After

| Aspect | Original (proposed_cocotb_test) | forge-vhdl Compliant |
|--------|--------------------------------|---------------------|
| **Structure** | Single file | 3-tier progressive |
| **Test Discovery** | Manual pytest | Auto-discovery via `test_configs.py` |
| **Test Runner** | pytest directly | forge-vhdl `run.py` |
| **Output Filter** | None | GHDL aggressive filter |
| **Verbosity Control** | Manual | Automatic via `TestBase` |
| **Test Levels** | All run together | P1/P2/P3 selectable |
| **Output Size** | ~200+ lines | P1: <20, P2: <50, P3: <100 |
| **LLM Token Cost** | ~3000 tokens | P1: ~100 tokens |

---

## Next Steps

### 1. Verify VHDL Dependencies
Ensure all VHDL source files exist and are accessible:
```bash
# Check bpd-tiny-vhdl sources
ls -la libs/bpd-tiny-vhdl/src/

# Check forge-vhdl dependencies
ls -la libs/forge-vhdl/vhdl/packages/volo_voltage_pkg.vhd
ls -la libs/forge-vhdl/vhdl/debugging/fsm_observer.vhd

# Check wrapper files
ls -la libs/bpd-tiny-vhdl/CustomWrapper_*.vhd
```

### 2. Run P1 Tests
```bash
cd libs/bpd-tiny-vhdl/tests
uv run python ../../forge-vhdl/tests/run.py bpd_fsm_observer
```

### 3. Expected P1 Output (with GHDL filter)
```
Running: bpd_fsm_observer (P1_BASIC)
✓ Reset behavior
✓ IDLE → ARMED transition
✓ State voltage stairstep

3 tests passed in 2.3s
```

### 4. If Tests Pass
- Run P2 tests: `TEST_LEVEL=P2_INTERMEDIATE ...`
- Run P3 tests: `TEST_LEVEL=P3_COMPREHENSIVE ...`
- Document any issues in session notes

### 5. If Tests Fail
- Check import paths (PYTHONPATH)
- Verify VHDL compilation (check GHDL errors)
- Run with `GHDL_FILTER_LEVEL=none` for full output
- Check `test_configs.py` source paths

---

## Agent Testing Notes

**For CocoTB Integration Test Agent evaluation:**

This restructuring demonstrates what the agent should be capable of:
1. ✅ Recognizing excellent test logic (original tests were comprehensive)
2. ✅ Identifying structural misalignment with forge-vhdl standards
3. ✅ Proposing the restructuring pattern shown here
4. ✅ Preserving test logic while adapting structure
5. ✅ Integrating with forge-vhdl test infrastructure

The agent should produce output similar to this restructuring when presented with:
- Input: `proposed_cocotb_test/test_bpd_fsm_observer.py`
- Context: `libs/forge-vhdl/CLAUDE.md`, `agent.md`
- Task: "Align with forge-vhdl progressive testing standards"

---

## References

- **forge-vhdl Testing Standards:** `libs/forge-vhdl/CLAUDE.md`
- **Original Tests:** `proposed_cocotb_test/test_bpd_fsm_observer.py`
- **Agent Specification:** `bpd/agents/cocotb-integration-test/agent.md`
- **Context Management:** `.claude/shared/CONTEXT_MANAGEMENT.md`
- **FSM Observer Integration:** `proposed_cocotb_test/FSM_OBSERVER_INTEGRATION.md`

---

**Created:** 2025-11-05
**Author:** Claude Code (based on user's original tests)
**Status:** Ready for validation testing
