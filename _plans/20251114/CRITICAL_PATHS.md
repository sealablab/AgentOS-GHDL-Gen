# Critical Paths Reference
**Quick path mapping for AgentOS-GHDL-Gen migration**

---

## Source → Destination Mapping

### Core Platform

| Source (FORGE-v5) | Destination | Type | Notes |
|-------------------|-------------|------|-------|
| `forge-platform/MCC_CustomInstrument.vhd` | `sys/forge-platform/MCC_CustomInstrument.vhd` | COPY | THE interface |
| `forge-platform/FORGE_App_Wrapper.vhd` | `sys/forge-platform/FORGE_App_Wrapper.vhd` | COPY | 3-layer template |
| `forge-platform/README.md` | `sys/forge-platform/README.md` | COPY | FORGE guide |
| `forge-platform/L1-FORGE-MCC-TOP/` | `sys/forge-platform/L1-FORGE-MCC-TOP/` | COPY | Layer 1 docs |
| `forge-platform/L2-FORGE-App.md` | `sys/forge-platform/L2-FORGE-App.md` | COPY | Layer 2 spec |
| `forge-platform/L3-AppMain.md` | `sys/forge-platform/L3-AppMain.md` | COPY | Layer 3 spec |

### Git Submodules

| Repository | Destination | Type | URL |
|------------|-------------|------|-----|
| moku-models | `libs/moku-models/` | SUBMODULE | github.com/sealablab/moku-models-v4 |
| riscure-models | `libs/riscure-models/` | SUBMODULE | github.com/sealablab/riscure-models-v4 |
| forge-vhdl | `libs/forge-vhdl/` | COPY | (content from FORGE-v5/libs/forge-vhdl/) |

### Testing Infrastructure

| Source (FORGE-v5) | Destination | Type | Notes |
|-------------------|-------------|------|-------|
| `libs/forge-vhdl/python/forge_cocotb/test_base.py` | `tools/testing/test_base.py` | COPY | P1/P2/P3 base |
| `libs/forge-vhdl/python/forge_cocotb/conftest.py` | `tools/testing/conftest.py` | COPY | Setup utils |
| `libs/forge-vhdl/python/forge_cocotb/runner.py` | `tools/testing/runner.py` | COPY | Test runner |
| `libs/forge-vhdl/python/forge_cocotb/mcc_utils.py` | `tools/testing/mcc_utils.py` | COPY | CustomWrapper utils |
| `libs/forge-vhdl/scripts/ghdl_output_filter.py` | `tools/ghdl-filter/ghdl_output_filter.py` | COPY | 98% reduction |

### Tools

| Source (FORGE-v5) | Destination | Type | Notes |
|-------------------|-------------|------|-------|
| `tools/forge-codegen/` | `tools/forge-codegen/` | COPY | Entire directory |
| `tools/forge-codegen/forge_codegen/basic_serialized_datatypes/` | `tools/forge-codegen/forge_codegen/basic_serialized_datatypes/` | COPY | 23-type system |
| `tools/forge-codegen/forge_codegen/generator/` | `tools/forge-codegen/forge_codegen/generator/` | COPY | YAML → VHDL |
| `tools/forge-codegen/tests/` | `tools/forge-codegen/tests/` | COPY | 69 unit tests |

### Examples

| Source (FORGE-v5) | Destination | Type | Notes |
|-------------------|-------------|------|-------|
| `examples/basic-probe-driver/` | `examples/basic-probe-driver/` | COPY | Entire directory |
| `examples/basic-probe-driver/vhdl/FORGE_ARCHITECTURE.md` | `examples/basic-probe-driver/vhdl/FORGE_ARCHITECTURE.md` | COPY | ⭐ READ FIRST |
| `examples/counter/` | `examples/counter/` | COPY | Minimal example |

### Documentation

| Source (FORGE-v5) | Destination | Type | Notes |
|-------------------|-------------|------|-------|
| `libs/forge-vhdl/docs/VHDL_CODING_STANDARDS.md` | `docs/standards/VHDL_CODING_STANDARDS.md` | COPY | |
| `libs/forge-vhdl/docs/COCOTB_TROUBLESHOOTING.md` | `docs/standards/COCOTB_TROUBLESHOOTING.md` | COPY | |
| `docs/FORGE-V5/Progressive Testing/README.md` | `docs/standards/PROGRESSIVE_TESTING.md` | COPY | |
| `examples/basic-probe-driver/vhdl/FORGE_ARCHITECTURE.md` | `docs/architecture/FORGE_ARCHITECTURE.md` | COPY | |
| `docs/FORGE-V5/Moku Platforms/` | `docs/platforms/` | COPY | Platform guides |

### Agents

| Source (FORGE-v5/.claude/agents/) | Destination (agent-os/agents/) | Type | Notes |
|------------------------------------|-------------------------------|------|-------|
| `cocotb-integration-test/` | `cocotb-integration-test/` | COPY | ✅ TESTED |
| `forge-vhdl-component-generator/` | `vhdl-generator/` | COPY + RENAME | Update paths |
| `cocotb-progressive-test-designer/` | `test-designer/` | COPY + RENAME | Update paths |
| `cocotb-progressive-test-runner/` | `test-runner/` | COPY + RENAME | Update paths |
| `deployment-orchestrator/` | `deployer/` | COPY + RENAME | Update paths |

| Source (FORGE-v6/AI/) | Destination | Type | Notes |
|-----------------------|-------------|------|-------|
| `Agent-Pipeline.md` | `agent-os/agents/PIPELINE.md` | COPY | Workflow doc |
| `validate_agent_inputs.md` | `agent-os/agents/validate_agent_inputs.md` | COPY | Input validation |

---

## Import Path Updates Required

### Testing Framework Imports

**Old Path** (forge_cocotb):
```python
from forge_cocotb.test_base import TestBase
from forge_cocotb.conftest import setup_clock, reset_active_low
from forge_cocotb import mcc_utils
```

**New Path** (tools.testing):
```python
# Option 1: Absolute import (requires package setup)
from tools.testing.test_base import TestBase
from tools.testing.conftest import setup_clock, reset_active_low
from tools.testing import mcc_utils

# Option 2: Relative import (from test files)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../tools/testing'))
from test_base import TestBase
from conftest import setup_clock, reset_active_low
import mcc_utils

# Option 3: Create package (RECOMMENDED)
# Add tools/testing/__init__.py
# Add tools/__init__.py
# Then use: from tools.testing import TestBase, setup_clock, reset_active_low
```

**Files to Update**:
- `examples/basic-probe-driver/platform_tests/wrapper/*.py`
- Any new test files

---

## Agent Path References to Update

### Agent Markdown Files

**Pattern to Find**:
```markdown
.claude/agents/cocotb-progressive-test-designer/
.claude/agents/cocotb-progressive-test-runner/
```

**Replace With**:
```markdown
agent-os/agents/test-designer/
agent-os/agents/test-runner/
```

**Files to Update**:
- `agent-os/agents/*/agent.md`
- `agent-os/agents/PIPELINE.md`
- `agent-os/agents/validate_agent_inputs.md`

### Agent Internal References

**Pattern to Find**:
```markdown
libs/forge-vhdl/
tools/forge-codegen/
examples/basic-probe-driver/
```

**Action**: These paths are STILL CORRECT (no change needed)

---

## GHDL Filter Path

### From Test Runner

**Old Reference** (in runner.py):
```python
filter_cmd = "ghdl_output_filter.py"  # Assumes in PATH
```

**New Reference**:
```python
import os
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
filter_path = os.path.join(repo_root, 'tools', 'ghdl-filter', 'ghdl_output_filter.py')
filter_cmd = f"python {filter_path}"
```

**Alternatively**, add to PATH:
```bash
export PATH=$PATH:/Users/johnycsh/AgentOS-GHDL-Gen/tools/ghdl-filter
```

---

## Verification Commands

### Check Submodules
```bash
git submodule status
# Should show commit hashes, not dashes

ls libs/moku-models/moku_models/
ls libs/riscure-models/riscure_models/
# Should see Python files
```

### Check Testing Framework
```bash
ls tools/testing/
# Should see: test_base.py, conftest.py, runner.py, mcc_utils.py

grep "class TestBase" tools/testing/test_base.py
# Should find TestBase class definition
```

### Check forge-codegen
```bash
ls tools/forge-codegen/forge_codegen/basic_serialized_datatypes/
# Should see: types.py, metadata.py, mapper.py, converters.py, voltage.py, time.py
```

### Check BPD Example
```bash
ls examples/basic-probe-driver/vhdl/
# Should see: FORGE_ARCHITECTURE.md, CustomWrapper_bpd_forge.vhd, BPD_forge_shim.vhd, BPD_forge_main.vhd

grep "FORGE" examples/basic-probe-driver/vhdl/FORGE_ARCHITECTURE.md
# Should find FORGE references
```

### Check Agent Adaptations
```bash
grep -r ".claude/agents" agent-os/agents/
# Should show which files still reference old path
# Goal: zero results after updates
```

---

## Package Setup (Recommended)

To make `tools.testing` importable as a package:

**1. Create `tools/__init__.py`**:
```python
# tools/__init__.py
"""Development tools for AgentOS-GHDL-Gen"""
```

**2. Create `tools/testing/__init__.py`**:
```python
# tools/testing/__init__.py
"""Progressive testing framework (P1/P2/P3) with GHDL filter integration"""

from .test_base import TestBase
from .conftest import setup_clock, reset_active_low
from . import mcc_utils

__all__ = ['TestBase', 'setup_clock', 'reset_active_low', 'mcc_utils']
```

**3. Update imports in test files**:
```python
from tools.testing import TestBase, setup_clock, reset_active_low
```

**4. Add to PYTHONPATH or install as editable**:
```bash
# Option 1: PYTHONPATH
export PYTHONPATH=/Users/johnycsh/AgentOS-GHDL-Gen:$PYTHONPATH

# Option 2: Editable install (requires pyproject.toml)
pip install -e .
```

---

## Common Issues & Quick Fixes

### Issue: Submodule not initialized
**Symptom**: `libs/moku-models/` is empty
**Fix**: `git submodule update --init --recursive`

### Issue: Import error in tests
**Symptom**: `ModuleNotFoundError: No module named 'forge_cocotb'`
**Fix**: Update imports to `tools.testing` (see Import Path Updates above)

### Issue: GHDL filter not found
**Symptom**: `FileNotFoundError: ghdl_output_filter.py`
**Fix**: Update runner.py to use absolute path (see GHDL Filter Path above)

### Issue: Agent path references broken
**Symptom**: Agent markdown mentions `.claude/agents/`
**Fix**: Replace with `agent-os/agents/` (see Agent Path References above)

---

## Quick Copy-Paste Commands

### Step 2: Migrate forge-platform
```bash
cp -r /Users/johnycsh/Forge/FORGE-v5/forge-platform/* sys/forge-platform/
```

### Step 3: Git submodules
```bash
git submodule add https://github.com/sealablab/moku-models-v4.git libs/moku-models
git submodule add https://github.com/sealablab/riscure-models-v4.git libs/riscure-models
git submodule update --init --recursive
cp -r /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/* libs/forge-vhdl/
```

### Step 4: Testing infrastructure
```bash
cp /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/python/forge_cocotb/*.py tools/testing/
cp /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/scripts/ghdl_output_filter.py tools/ghdl-filter/
```

### Step 5: forge-codegen
```bash
cp -r /Users/johnycsh/Forge/FORGE-v5/tools/forge-codegen/* tools/forge-codegen/
```

### Step 6: BPD example
```bash
cp -r /Users/johnycsh/Forge/FORGE-v5/examples/basic-probe-driver examples/
```

### Step 7: Documentation
```bash
cp /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/docs/VHDL_CODING_STANDARDS.md docs/standards/
cp /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/docs/COCOTB_TROUBLESHOOTING.md docs/standards/
cp /Users/johnycsh/Forge/FORGE-v5/examples/basic-probe-driver/vhdl/FORGE_ARCHITECTURE.md docs/architecture/
```

### Step 8: Agents
```bash
cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/cocotb-integration-test agent-os/agents/
cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/forge-vhdl-component-generator agent-os/agents/vhdl-generator
cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/cocotb-progressive-test-designer agent-os/agents/test-designer
cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/cocotb-progressive-test-runner agent-os/agents/test-runner
cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/deployment-orchestrator agent-os/agents/deployer
cp /Users/johnycsh/Forge/FORGE-v6/AI/Agent-Pipeline.md agent-os/agents/PIPELINE.md
cp /Users/johnycsh/Forge/FORGE-v6/AI/validate_agent_inputs.md agent-os/agents/
```

---

**End of CRITICAL_PATHS.md**

Use this as a quick reference during migration. See MIGRATION_PLAN.md for detailed rationale.
