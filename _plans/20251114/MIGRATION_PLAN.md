# AgentOS-GHDL-Gen Migration Plan
**Date:** 2025-11-13
**Status:** Ready for Execution
**Session Handoff Document**

---

## Executive Summary

We are migrating proven VHDL development infrastructure from **FORGE-v5** (production) and **FORGE-v6** (aspirational refactor) into **AgentOS-GHDL-Gen**, preserving the "Train Like You Fight" philosophy while integrating with Agent-OS workflow automation.

**Core Strategy**: Use FORGE-v6's clean directory structure as the "map" while transplanting FORGE-v5's production-proven code and __incoming_stuff's successful agent workflows.

**Key Innovation Preserved**: Progressive testing framework with 98% GHDL output reduction for LLM-friendly workflows.

---

## Context: What We Discovered

### Three Source Repositories

**1. FORGE-v5** (`/Users/johnycsh/Forge/FORGE-v5`)
- **Status**: Production-ready (v2.0.0)
- **What it has**:
  - CustomWrapper foundation (`forge-platform/MCC_CustomInstrument.vhd`)
  - 3-layer FORGE architecture (proven in Basic Probe Driver)
  - Progressive testing (P1/P2/P3) with CocoTB
  - forge-codegen tool (23-type system, register packing)
  - 69 unit tests, comprehensive documentation
  - Git submodules: moku-models, riscure-models, forge-vhdl
- **What we're taking**: Almost everything

**2. FORGE-v6** (`/Users/johnycsh/Forge/FORGE-v6`)
- **Status**: Aspirational refactor
- **What it has**:
  - Clean directory structure (`sys/`, `libs/`, `examples/`, `AI/`)
  - Clear separation of concerns
  - FORGE-V6-FS-LAYOUT.md showing intended organization
- **What we're taking**: Directory structure pattern, organizational philosophy

**3. __incoming_stuff** (`/Users/johnycsh/AgentOS-GHDL-Gen/__incoming_stuff`)
- **Status**: Successful previous iteration
- **What it has**:
  - AI agent workflows (validated agent pipeline)
  - forge-vhdl progressive testing infrastructure
  - Agent definitions (cocotb-integration-test, etc.)
  - Documentation on "train like you fight"
- **What we're taking**: Agent patterns, testing framework details

### The "Train Like You Fight" Philosophy

**Core Principle**: Develop and test VHDL against the **actual production interface** - the CustomWrapper entity that runs inside Moku Multi-Instrument Mode.

**Why it matters**: Testing isolated VHDL components ≠ Testing in CustomWrapper context.

The CustomWrapper interface defines:
- 16 Control Registers (CR0-CR15) - network-settable
- 16 Status Registers (SR0-SR15) - network-readable
- Signed 16-bit I/O (InputA/B/C, OutputA/B/C)
- FORGE control scheme (CR0[31:29] for safe initialization)
- 125-200 MHz clock domains

**The Anchor**: `sys/forge-platform/MCC_CustomInstrument.vhd` is THE authoritative interface.

---

## Approved Filesystem Structure

```
AgentOS-GHDL-Gen/
├── agent-os/                           # Agent-OS orchestration layer
│   ├── product/                        # ✅ DONE (mission, roadmap, tech-stack)
│   ├── specs/                          # Feature specs (Agent-OS pattern)
│   └── agents/                         # Agent workflow automation
│       ├── requirements-gatherer/      # Phase 1
│       ├── vhdl-generator/             # Phase 2
│       ├── test-designer/              # Phase 3
│       ├── test-runner/                # Phase 4
│       └── deployer/                   # Phase 5
│
├── sys/                                # Platform foundation
│   ├── forge-platform/                 # ⭐ CustomWrapper + FORGE entities
│   │   ├── MCC_CustomInstrument.vhd   # THE interface (DO NOT MODIFY)
│   │   ├── FORGE_App_Wrapper.vhd      # 3-layer wrapper template
│   │   ├── L1-FORGE-MCC-TOP/          # Layer 1 (BRAM loader - future)
│   │   ├── L2-FORGE-App.md            # Layer 2 spec (shim)
│   │   ├── L3-AppMain.md              # Layer 3 spec (main)
│   │   └── README.md                  # Complete FORGE guide
│   ├── forge-platform-sim/            # Platform simulator (future)
│   ├── forge-models/                  # Platform abstractions
│   └── forge-scripts/                 # Build/deploy utilities
│
├── libs/                              # Git submodules
│   ├── moku-models/                   # ⭐ Submodule (sealablab/moku-models-v4)
│   ├── riscure-models/                # ⭐ Submodule (sealablab/riscure-models-v4)
│   └── forge-vhdl/                    # ⭐ VHDL components + testing framework
│       ├── vhdl/packages/             # Voltage packages (3v3, 5v0, 5v_bipolar)
│       ├── vhdl/utilities/            # forge_util_clk_divider, etc.
│       ├── vhdl/debugging/            # fsm_observer
│       ├── python/forge_cocotb/       # ⭐ Progressive testing framework
│       ├── tests/                     # Test examples
│       ├── CLAUDE.md                  # Testing standards guide
│       └── llms.txt                   # Quick reference
│
├── tools/                             # Development tools
│   ├── forge-codegen/                 # ⭐ YAML → VHDL generation
│   │   ├── forge_codegen/
│   │   │   ├── basic_serialized_datatypes/  # 23-type system
│   │   │   ├── generator/             # Code generation
│   │   │   ├── models/                # Pydantic models
│   │   │   └── templates/             # Jinja2 templates
│   │   └── tests/                     # 69 unit tests
│   ├── ghdl-filter/                   # GHDL output filter (98% reduction)
│   └── testing/                       # Testing utilities
│       ├── test_base.py               # P1/P2/P3 base class
│       ├── conftest.py                # Setup utilities
│       ├── runner.py                  # Progressive test runner
│       └── mcc_utils.py               # CustomWrapper test utilities
│
├── examples/                          # Reference implementations
│   ├── basic-probe-driver/            # ⭐ Production reference
│   │   ├── README.md
│   │   ├── BPD-RTL.yaml               # Register specification
│   │   ├── vhdl/
│   │   │   ├── FORGE_ARCHITECTURE.md  # ⭐ START HERE
│   │   │   ├── CustomWrapper_bpd_forge.vhd
│   │   │   ├── BPD_forge_shim.vhd     # Layer 2 example
│   │   │   ├── BPD_forge_main.vhd     # Layer 3 example
│   │   │   └── src/
│   │   └── platform_tests/            # P1/P2/P3 tests
│   └── counter/                       # Minimal example
│
├── docs/                              # Documentation
│   ├── README.md
│   ├── TRAIN_LIKE_YOU_FIGHT.md        # Philosophy guide
│   ├── AGENT_WORKFLOW.md              # Agent pipeline
│   ├── standards/                     # VHDL, CocoTB, testing standards
│   ├── architecture/                  # 3-layer, FORGE control scheme, types
│   └── platforms/                     # Moku-Go, Lab, Pro, Cloud Compile
│
├── .gitmodules                        # Submodule configuration
├── .gitignore
├── README.md
├── CLAUDE.md
└── MIGRATION_PLAN.md                  # This file
```

---

## Migration Steps (Detailed)

### Prerequisites

```bash
cd /Users/johnycsh/AgentOS-GHDL-Gen
# Verify we're in the right place
ls agent-os/product/mission.md  # Should exist
```

---

### Step 1: Create Directory Structure (15 mins)

**Purpose**: Establish the foundation before copying files.

```bash
# System foundation
mkdir -p sys/forge-platform
mkdir -p sys/forge-platform-sim
mkdir -p sys/forge-models
mkdir -p sys/forge-scripts

# Libraries (will be submodules)
mkdir -p libs/forge-vhdl

# Tools
mkdir -p tools/forge-codegen
mkdir -p tools/ghdl-filter
mkdir -p tools/testing

# Examples
mkdir -p examples

# Documentation
mkdir -p docs/standards
mkdir -p docs/architecture
mkdir -p docs/platforms
mkdir -p docs/reference

# Agent-OS agents (adapt existing structure)
mkdir -p agent-os/specs
# agent-os/agents/ may need reorganization (see Step 8)
```

**Verify**:
```bash
tree -L 2 -d .
# Should show sys/, libs/, tools/, examples/, docs/, agent-os/
```

---

### Step 2: Migrate sys/forge-platform (20 mins) ⭐ CRITICAL

**Purpose**: This IS "train like you fight" - the actual CustomWrapper interface.

**What we're copying**:
- `MCC_CustomInstrument.vhd` - THE authoritative interface (DO NOT MODIFY)
- `FORGE_App_Wrapper.vhd` - 3-layer wrapper template
- `README.md` - Complete FORGE platform guide
- Layer documentation (L1, L2, L3)

```bash
# Copy the entire forge-platform directory
cp -r /Users/johnycsh/Forge/FORGE-v5/forge-platform/* \
      sys/forge-platform/

# Verify critical files
ls -lh sys/forge-platform/MCC_CustomInstrument.vhd
ls -lh sys/forge-platform/FORGE_App_Wrapper.vhd
ls -lh sys/forge-platform/README.md

# Check file sizes (should be non-zero)
du -sh sys/forge-platform/
```

**Expected output**: ~100KB total, MCC_CustomInstrument.vhd ~8KB

**Why this matters**: This defines the production interface. All VHDL must integrate with `MCC_CustomInstrument`.

---

### Step 3: Setup Git Submodules (30 mins) ⭐ CRITICAL

**Purpose**: Link to platform models and VHDL library as git submodules.

**Gotcha**: Order matters - initialize git first, then add submodules.

```bash
# 1. Initialize git if not already done
git init
git add .gitignore MIGRATION_PLAN.md
git commit -m "Initial commit with migration plan"

# 2. Add moku-models submodule
git submodule add https://github.com/sealablab/moku-models-v4.git libs/moku-models

# 3. Add riscure-models submodule
git submodule add https://github.com/sealablab/riscure-models-v4.git libs/riscure-models

# 4. Initialize submodules
git submodule update --init --recursive

# 5. Verify submodules are populated
ls libs/moku-models/moku_models/
ls libs/riscure-models/riscure_models/

# Should see Python files, not empty directories
```

**For forge-vhdl**: Copy content directly (not submodule, we're integrating it):
```bash
cp -r /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/* \
      libs/forge-vhdl/

# Verify
ls libs/forge-vhdl/vhdl/packages/
ls libs/forge-vhdl/python/forge_cocotb/
```

**Verify submodules**:
```bash
cat .gitmodules
# Should show moku-models and riscure-models

git submodule status
# Should show commit hashes (not empty)
```

---

### Step 4: Migrate Testing Infrastructure (45 mins) ⭐ HIGH VALUE

**Purpose**: The 98% output reduction progressive testing framework is our competitive advantage.

**What we're extracting**:
- `test_base.py` - Base class with P1/P2/P3 support
- `conftest.py` - Setup utilities (setup_clock, reset_active_low)
- `runner.py` - Progressive test orchestrator
- `mcc_utils.py` - CustomWrapper test utilities
- `ghdl_filter.py` - GHDL output filter

```bash
# Copy progressive testing framework
cp /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/python/forge_cocotb/*.py \
   tools/testing/

# Copy GHDL filter
cp /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/scripts/ghdl_output_filter.py \
   tools/ghdl-filter/

# Verify critical files
ls -lh tools/testing/test_base.py
ls -lh tools/testing/conftest.py
ls -lh tools/testing/runner.py
ls -lh tools/testing/mcc_utils.py
ls -lh tools/ghdl-filter/ghdl_output_filter.py

# Check they're not empty
wc -l tools/testing/*.py
wc -l tools/ghdl-filter/*.py
```

**Expected**: Each file should be 100+ lines (non-trivial code).

**Path Adjustment Needed**: Tests importing from `forge_cocotb` will need to import from `tools.testing` instead.

**Document this**: Add to CRITICAL_PATHS.md

---

### Step 5: Migrate forge-codegen (30 mins)

**Purpose**: The 23-type system and register packing algorithm.

**User Decision**: YES, include automatic register packing.

```bash
# Copy the entire forge-codegen tool
cp -r /Users/johnycsh/Forge/FORGE-v5/tools/forge-codegen/* \
      tools/forge-codegen/

# Verify type system
ls tools/forge-codegen/forge_codegen/basic_serialized_datatypes/
# Should see: types.py, metadata.py, mapper.py, converters.py, voltage.py, time.py

# Verify generator
ls tools/forge-codegen/forge_codegen/generator/
# Should see: codegen.py, type_utilities.py

# Verify templates
ls tools/forge-codegen/forge_codegen/templates/
# Should see: main.vhd.j2, shim.vhd.j2

# Verify tests
ls tools/forge-codegen/tests/
# Should see multiple test_*.py files

# Check test count
find tools/forge-codegen/tests -name "test_*.py" | wc -l
# Should show ~10-15 test files (69 tests total)
```

**Verify functionality** (optional):
```bash
cd tools/forge-codegen
python -m pytest tests/ -v
# Should show 69 tests passing
```

---

### Step 6: Migrate BPD Reference Example (20 mins) ⭐ PRODUCTION-PROVEN

**Purpose**: Complete working example showing all FORGE patterns.

```bash
# Copy the complete BPD example
cp -r /Users/johnycsh/Forge/FORGE-v5/examples/basic-probe-driver \
      examples/

# Verify key files
ls -lh examples/basic-probe-driver/README.md
ls -lh examples/basic-probe-driver/BPD-RTL.yaml
ls -lh examples/basic-probe-driver/vhdl/FORGE_ARCHITECTURE.md
ls -lh examples/basic-probe-driver/vhdl/CustomWrapper_bpd_forge.vhd
ls -lh examples/basic-probe-driver/vhdl/BPD_forge_shim.vhd
ls -lh examples/basic-probe-driver/vhdl/BPD_forge_main.vhd

# Verify test structure
ls examples/basic-probe-driver/platform_tests/wrapper/
# Should see: run.py, test_configs.py, P1_*.py, P2_*.py files
```

**Path Adjustments Needed**:
- Tests may import from old paths
- See CRITICAL_PATHS.md for mappings

**Copy counter example** (optional):
```bash
cp -r /Users/johnycsh/Forge/FORGE-v5/examples/counter \
      examples/
```

---

### Step 7: Migrate Documentation (40 mins)

**Purpose**: Capture hard-won knowledge from FORGE-v5.

**Standards**:
```bash
# VHDL coding standards
cp /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/docs/VHDL_CODING_STANDARDS.md \
   docs/standards/

# CocoTB troubleshooting
cp /Users/johnycsh/Forge/FORGE-v5/libs/forge-vhdl/docs/COCOTB_TROUBLESHOOTING.md \
   docs/standards/

# Progressive testing guide
cp /Users/johnycsh/Forge/FORGE-v5/docs/FORGE-V5/Progressive\ Testing/README.md \
   docs/standards/PROGRESSIVE_TESTING.md
```

**Architecture**:
```bash
# FORGE architecture from BPD
cp /Users/johnycsh/Forge/FORGE-v5/examples/basic-probe-driver/vhdl/FORGE_ARCHITECTURE.md \
   docs/architecture/

# Copy other architecture docs
cp -r /Users/johnycsh/Forge/FORGE-v5/docs/FORGE-V5/Architecture/* \
      docs/architecture/
```

**Platform docs**:
```bash
cp -r /Users/johnycsh/Forge/FORGE-v5/docs/FORGE-V5/Moku\ Platforms/* \
      docs/platforms/

cp -r /Users/johnycsh/Forge/FORGE-v5/docs/FORGE-V5/Moku\ Cloud\ Compile \
      docs/platforms/

cp -r /Users/johnycsh/Forge/FORGE-v5/docs/FORGE-V5/GHDL \
      docs/platforms/
```

**Verify**:
```bash
find docs/standards -name "*.md" | wc -l  # Should be 3+
find docs/architecture -name "*.md" | wc -l  # Should be 5+
find docs/platforms -name "*.md" | wc -l  # Should be 5+
```

---

### Step 8: Migrate and Adapt Agent Definitions (1 hour) ⭐ CRITICAL

**Purpose**: Preserve the proven agent workflow while adapting to Agent-OS.

**Source Agents** (FORGE-v5/.claude/agents/):
- cocotb-integration-test (TESTED & VALIDATED)
- forge-vhdl-component-generator
- cocotb-progressive-test-designer
- cocotb-progressive-test-runner
- deployment-orchestrator
- hardware-debug

**Destination**: `agent-os/agents/` (renamed to fit Agent-OS pattern)

```bash
# Copy tested agent (keep name for now)
cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/cocotb-integration-test \
      agent-os/agents/

# Copy and rename other agents
cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/forge-vhdl-component-generator \
      agent-os/agents/vhdl-generator

cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/cocotb-progressive-test-designer \
      agent-os/agents/test-designer

cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/cocotb-progressive-test-runner \
      agent-os/agents/test-runner

cp -r /Users/johnycsh/Forge/FORGE-v5/.claude/agents/deployment-orchestrator \
      agent-os/agents/deployer

# Copy agent pipeline documentation
cp /Users/johnycsh/Forge/FORGE-v6/AI/Agent-Pipeline.md \
   agent-os/agents/PIPELINE.md

# Copy input validation
cp /Users/johnycsh/Forge/FORGE-v6/AI/validate_agent_inputs.md \
   agent-os/agents/
```

**Path Adjustments Needed**: Agent markdown files reference paths like:
- `libs/forge-vhdl/` → still correct
- `.claude/agents/` → now `agent-os/agents/`
- `tools/forge-codegen/` → still correct

**Verify**:
```bash
ls agent-os/agents/
# Should see: cocotb-integration-test, vhdl-generator, test-designer, test-runner, deployer, PIPELINE.md, validate_agent_inputs.md
```

**Agent-OS Integration**: These agents may need updating to work with Agent-OS task/spec patterns. Mark for review in morning session.

---

### Step 9: Create New Documentation (45 mins)

**Create `docs/TRAIN_LIKE_YOU_FIGHT.md`**:

This file explains the core philosophy. Content already drafted (see SESSION_HANDOFF_PROMPT.txt for full text).

Key points:
- Why CustomWrapper testing matters
- How we test (against production interface)
- Reference to `sys/forge-platform/MCC_CustomInstrument.vhd`
- Link to BPD example

**Create `docs/AGENT_WORKFLOW.md`**:

Explains the 5-phase agent pipeline:
1. Requirements Gathering
2. VHDL Generation
3. Test Design
4. Test Execution
5. Deployment

(Full content in SESSION_HANDOFF_PROMPT.txt)

**Create top-level `README.md`**:

Project overview linking to:
- `docs/TRAIN_LIKE_YOU_FIGHT.md`
- `docs/AGENT_WORKFLOW.md`
- `examples/basic-probe-driver/README.md`
- `sys/forge-platform/README.md`

**Create `CLAUDE.md`**:

AI-specific guidance (Tier 2 docs):
- Quick start for AI agents
- Directory structure
- "Train like you fight" summary
- Common tasks (running tests, deploying, etc.)
- Reference to FORGE-v5 CLAUDE.md for detailed patterns

---

### Step 10: Git Configuration (.gitmodules, .gitignore) (20 mins)

**Create `.gitmodules`** (if not created in Step 3):

```ini
[submodule "libs/moku-models"]
    path = libs/moku-models
    url = https://github.com/sealablab/moku-models-v4.git

[submodule "libs/riscure-models"]
    path = libs/riscure-models
    url = https://github.com/sealablab/riscure-models-v4.git
```

**Create comprehensive `.gitignore`**:

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
*.egg
*.egg-info/
dist/
build/
.venv/
venv/
env/
.pytest_cache/

# VHDL Simulation
sim_build/
*.vcd
*.ghw
*.cf
*.o
*.exe
*.a
work-obj93.cf

# Agent-OS
agent-os/specs/*.lock

# IDE / Editors
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Logs
*.log
.Claude_Logs/
*.tmp
*.bak

# GHDL
*.o
e~*.vhd

# Temporary
*.tar
*.zip
temp_bits.tar
pulled_config.json

# Obsidian (optional)
.obsidian/
.trash/
```

**Verify**:
```bash
cat .gitmodules
cat .gitignore

# Test ignore patterns
git status
# Should NOT show __pycache__, .venv, *.pyc, etc.
```

---

## Verification Procedures

### After Step 2 (forge-platform):
```bash
# Verify MCC_CustomInstrument.vhd exists and has content
grep -c "entity MCC_CustomInstrument" sys/forge-platform/MCC_CustomInstrument.vhd
# Should output: 1

grep "CR0\[31:29\]" sys/forge-platform/README.md
# Should find references to FORGE control scheme
```

### After Step 3 (submodules):
```bash
# Verify submodules are initialized
git submodule status
# Should show commit hashes, not dashes

# Verify moku-models content
python3 -c "from libs.moku_models import MOKU_GO_PLATFORM; print(MOKU_GO_PLATFORM)"
# Should print platform details
```

### After Step 4 (testing):
```bash
# Verify testing framework is complete
grep -c "class TestBase" tools/testing/test_base.py
# Should be > 0

grep "P1_BASIC\|P2_INTERMEDIATE\|P3_COMPREHENSIVE" tools/testing/runner.py
# Should find test level references
```

### After Step 6 (BPD example):
```bash
# Try running BPD tests (requires GHDL)
cd examples/basic-probe-driver/platform_tests/wrapper

# Check test structure
ls P1_*.py P2_*.py
# Should see test files

# Optional: Run if GHDL installed
# python run.py  # Should execute P1 tests
```

### Final Verification:
```bash
# Check overall structure
tree -L 2 -d .
# Should match proposed structure

# Check file counts
find sys/forge-platform -type f | wc -l  # Should be 10+
find tools/testing -type f | wc -l  # Should be 5+
find examples/basic-probe-driver -type f | wc -l  # Should be 30+
find docs -type f -name "*.md" | wc -l  # Should be 15+

# Check git status
git status
# Should show new files, tracked submodules
```

---

## Critical Gotchas & Solutions

### 1. Git Submodule Setup
**Problem**: Submodules can be finicky. Order matters.

**Solution**:
1. `git init` FIRST
2. Create `.gitignore` and commit it
3. THEN `git submodule add ...`
4. THEN `git submodule update --init --recursive`

**Verification**:
```bash
git submodule status
# Should show commit hashes (not dashes)
# If you see dashes: submodule not initialized

# Fix:
git submodule update --init --recursive
```

### 2. Testing Framework Path Adjustments
**Problem**: Tests import from `forge_cocotb` which is now at `tools.testing`.

**Affected Files**:
- `examples/basic-probe-driver/platform_tests/wrapper/*.py`
- Any new tests we create

**Solution**: Update imports:

**Before**:
```python
from forge_cocotb.test_base import TestBase
from forge_cocotb.conftest import setup_clock, reset_active_low
```

**After**:
```python
# Add to sys.path or use relative import
import sys
sys.path.insert(0, '../../../../tools/testing')
from test_base import TestBase
from conftest import setup_clock, reset_active_low
```

**Better Solution**: Create `tools/testing/__init__.py` and treat as package.

**Document in CRITICAL_PATHS.md**.

### 3. Agent Path References
**Problem**: Agents reference paths like `.claude/agents/` which is now `agent-os/agents/`.

**Affected Files**:
- All agent markdown files in `agent-os/agents/*/agent.md`
- `PIPELINE.md`

**Solution**:
1. Review each agent file
2. Update path references
3. Test one agent (cocotb-integration-test) first

**Example Changes**:
```markdown
# Before
See `.claude/agents/cocotb-progressive-test-designer/`

# After
See `agent-os/agents/test-designer/`
```

### 4. GHDL Filter Integration
**Problem**: `ghdl_output_filter.py` needs to be callable from test runners.

**Solution**:
```bash
# Option 1: Add to PATH
export PATH=$PATH:/Users/johnycsh/AgentOS-GHDL-Gen/tools/ghdl-filter

# Option 2: Update runner.py to use absolute path
# Edit tools/testing/runner.py to reference:
filter_path = os.path.join(repo_root, 'tools/ghdl-filter/ghdl_output_filter.py')
```

---

## Known Issues to Address Tomorrow

### Issue 1: Agent-OS Integration
**Status**: Agents copied but not adapted to Agent-OS task/spec patterns.

**Action Needed**:
- Review Agent-OS agent structure
- Adapt agent markdown to Agent-OS format
- Test cocotb-integration-test with Agent-OS

### Issue 2: Testing Framework as Package
**Status**: Testing utilities copied but not set up as importable package.

**Action Needed**:
- Create `tools/testing/__init__.py`
- Create `tools/__init__.py`
- Update sys.path or install as editable package

### Issue 3: Path Adjustments in Tests
**Status**: BPD tests may reference old import paths.

**Action Needed**:
- Review `examples/basic-probe-driver/platform_tests/wrapper/*.py`
- Update imports to new structure
- Test that P1 tests run

### Issue 4: pyproject.toml
**Status**: Not created yet.

**Action Needed**:
- Decide: Workspace mode (like FORGE-v5) or single package?
- Create pyproject.toml with dependencies
- Define: forge-codegen, moku-models, riscure-models, forge-vhdl as workspace members?

---

## Next Session Priorities

### Immediate Review (15 mins)
1. Verify this MIGRATION_PLAN.md makes sense
2. Clarify any ambiguous steps
3. Address concerns about Agent-OS integration

### Execute Migration (2-3 hours)
1. Run Steps 1-10 sequentially
2. Verify at each checkpoint
3. Document any deviations

### Test Scaffold (1 hour)
1. Run BPD P1 tests to verify infrastructure works
2. Fix path issues as they arise
3. Document fixes in CRITICAL_PATHS.md

### Agent Adaptation (1-2 hours)
1. Review one agent (cocotb-integration-test) in detail
2. Adapt to Agent-OS patterns
3. Test agent execution
4. Document adaptation pattern for other agents

---

## Success Criteria

**Migration Complete When**:
✅ All 10 steps executed without errors
✅ Git submodules initialized and populated
✅ BPD P1 tests run successfully
✅ Documentation is accessible and accurate
✅ At least one agent adapted to Agent-OS
✅ Path issues documented in CRITICAL_PATHS.md

**Ready for Development When**:
✅ Can create new VHDL component following FORGE patterns
✅ Can generate tests using adapted agents
✅ Can run progressive tests (P1/P2/P3)
✅ Can reference BPD as working example
✅ Agent workflow validated end-to-end

---

## Resources

**Key Files to Reference**:
- `sys/forge-platform/README.md` - FORGE platform guide
- `examples/basic-probe-driver/vhdl/FORGE_ARCHITECTURE.md` - 3-layer architecture
- `docs/standards/VHDL_CODING_STANDARDS.md` - Coding standards
- `docs/standards/COCOTB_TROUBLESHOOTING.md` - Testing gotchas
- `agent-os/agents/PIPELINE.md` - Agent workflow

**External References**:
- FORGE-v5: `/Users/johnycsh/Forge/FORGE-v5`
- FORGE-v6: `/Users/johnycsh/Forge/FORGE-v6`
- Incoming stuff: `/Users/johnycsh/AgentOS-GHDL-Gen/__incoming_stuff`

---

## Appendix: Why This Structure?

**`sys/`** - Platform foundation that rarely changes
- `forge-platform/` - THE CustomWrapper interface (authoritative)
- `forge-platform-sim/` - Platform simulator (future)
- Clear: "This is foundational, don't modify"

**`libs/`** - External dependencies as git submodules
- `moku-models/` - Platform specs (Pydantic models)
- `riscure-models/` - Probe specs (Pydantic models)
- `forge-vhdl/` - Reusable VHDL components + testing framework
- Clear: "These are libraries, not our code"

**`tools/`** - Development utilities we actively use
- `forge-codegen/` - YAML → VHDL generation
- `ghdl-filter/` - GHDL output filter
- `testing/` - Progressive testing framework
- Clear: "These are tools for development"

**`examples/`** - Reference implementations
- `basic-probe-driver/` - Production reference (START HERE)
- `counter/` - Minimal example
- Clear: "These are complete working examples"

**`agent-os/`** - Agent-OS orchestration
- `agents/` - Workflow automation agents
- `specs/` - Feature specifications
- `product/` - Mission, roadmap, tech stack
- Clear: "This is Agent-OS territory"

**`docs/`** - Documentation organized by topic
- `standards/` - Coding standards, testing standards
- `architecture/` - System design
- `platforms/` - Platform-specific guides
- Clear: "This is where we document"

---

**End of MIGRATION_PLAN.md**

**Next**: See SESSION_HANDOFF_PROMPT.txt for quick context loading tomorrow.
