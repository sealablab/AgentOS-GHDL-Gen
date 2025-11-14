════════════════════════════════════════════════════════════════════════════════
AGENTOS-GHDL-GEN: SESSION HANDOFF PROMPT
════════════════════════════════════════════════════════════════════════════════
Date: 2025-11-13
Status: Ready for migration execution
Complete details: See MIGRATION_PLAN.md
════════════════════════════════════════════════════════════════════════════════

## CONTEXT: WHERE WE ARE

I'm helping migrate proven VHDL development infrastructure into AgentOS-GHDL-Gen,
combining FORGE-v5 (production-ready), FORGE-v6 (clean structure), and
__incoming_stuff (successful workflows) into a coherent system.

**Current Working Directory**: `/Users/johnycsh/AgentOS-GHDL-Gen`

**What's Already Done**:
✅ agent-os/product/mission.md - Product vision
✅ agent-os/product/roadmap.md - 15-item development roadmap
✅ agent-os/product/tech-stack.md - Complete technology stack
✅ MIGRATION_PLAN.md - Comprehensive migration guide (THIS SESSION)

**What's Next**: Execute the 10-step migration plan.

════════════════════════════════════════════════════════════════════════════════

## THE CORE STRATEGY: "TRAIN LIKE YOU FIGHT"

**Philosophy**: Develop and test VHDL against the ACTUAL production interface -
the CustomWrapper entity that runs inside Moku Multi-Instrument Mode.

**The Anchor**: `sys/forge-platform/MCC_CustomInstrument.vhd` is THE authoritative
interface. All VHDL must integrate with it.

CustomWrapper defines:
- 16 Control Registers (CR0-CR15) - network-settable
- 16 Status Registers (SR0-SR15) - network-readable
- Signed 16-bit I/O (InputA/B/C, OutputA/B/C)
- FORGE control scheme (CR0[31:29] for safe initialization)
- 125-200 MHz clock domains

**Why this matters**: Testing isolated VHDL ≠ Testing in CustomWrapper context.
We test against the production interface from day one.

════════════════════════════════════════════════════════════════════════════════

## THREE SOURCE REPOSITORIES

**FORGE-v5** (`/Users/johnycsh/Forge/FORGE-v5`) - PRODUCTION (v2.0.0)
- CustomWrapper foundation (MCC_CustomInstrument.vhd)
- 3-layer FORGE architecture (proven in Basic Probe Driver)
- Progressive testing (P1/P2/P3) with 98% GHDL output reduction
- forge-codegen tool (23-type system, register packing)
- Git submodules: moku-models, riscure-models, forge-vhdl
→ WHAT WE'RE TAKING: Almost everything

**FORGE-v6** (`/Users/johnycsh/Forge/FORGE-v6`) - ASPIRATIONAL REFACTOR
- Clean directory structure (sys/, libs/, examples/, AI/)
- Clear separation of concerns
→ WHAT WE'RE TAKING: Directory pattern, organizational philosophy

**__incoming_stuff** (`/Users/johnycsh/AgentOS-GHDL-Gen/__incoming_stuff`)
- AI agent workflows (validated pipeline)
- forge-vhdl progressive testing infrastructure
- Documentation on "train like you fight"
→ WHAT WE'RE TAKING: Agent patterns, testing framework details

════════════════════════════════════════════════════════════════════════════════

## APPROVED FILESYSTEM STRUCTURE (Compact View)

AgentOS-GHDL-Gen/
├── agent-os/                    # Agent-OS orchestration
│   ├── product/                 # ✅ DONE (mission, roadmap, tech-stack)
│   ├── specs/                   # Feature specs
│   └── agents/                  # 5-phase workflow
│       ├── requirements-gatherer/
│       ├── vhdl-generator/
│       ├── test-designer/
│       ├── test-runner/
│       └── deployer/
│
├── sys/                         # Platform foundation
│   ├── forge-platform/          # ⭐ CustomWrapper + FORGE entities
│   │   ├── MCC_CustomInstrument.vhd  # THE interface
│   │   ├── FORGE_App_Wrapper.vhd     # 3-layer template
│   │   └── README.md                  # FORGE guide
│   ├── forge-platform-sim/      # Platform simulator
│   ├── forge-models/
│   └── forge-scripts/
│
├── libs/                        # Git submodules
│   ├── moku-models/             # ⭐ Submodule (platform specs)
│   ├── riscure-models/          # ⭐ Submodule (probe specs)
│   └── forge-vhdl/              # ⭐ VHDL components + testing
│       ├── vhdl/packages/       # Voltage packages
│       ├── python/forge_cocotb/ # ⭐ Progressive testing (98% reduction)
│       └── tests/
│
├── tools/                       # Development tools
│   ├── forge-codegen/           # ⭐ YAML → VHDL (23 types, packing)
│   ├── ghdl-filter/             # GHDL output filter
│   └── testing/                 # P1/P2/P3 framework
│
├── examples/
│   ├── basic-probe-driver/      # ⭐ Production reference (START HERE)
│   │   ├── vhdl/FORGE_ARCHITECTURE.md  # ⭐ READ THIS FIRST
│   │   └── platform_tests/      # P1/P2/P3 tests
│   └── counter/
│
├── docs/
│   ├── TRAIN_LIKE_YOU_FIGHT.md  # Philosophy guide
│   ├── AGENT_WORKFLOW.md        # 5-phase pipeline
│   ├── standards/               # VHDL, CocoTB, testing
│   ├── architecture/            # 3-layer, FORGE control, types
│   └── platforms/               # Moku guides
│
└── MIGRATION_PLAN.md            # ⭐ COMPLETE MIGRATION GUIDE

════════════════════════════════════════════════════════════════════════════════

## 10-STEP MIGRATION PLAN (QUICK REFERENCE)

See MIGRATION_PLAN.md for detailed instructions. This is the overview:

**Step 1** (15 min): Create directory structure
→ `mkdir -p sys/ libs/ tools/ examples/ docs/`

**Step 2** (20 min): Migrate sys/forge-platform ⭐ CRITICAL
→ Copy MCC_CustomInstrument.vhd (THE interface)
→ Source: /Users/johnycsh/Forge/FORGE-v5/forge-platform/*

**Step 3** (30 min): Setup git submodules ⭐ CRITICAL
→ Add moku-models, riscure-models as submodules
→ Copy forge-vhdl content
→ GOTCHA: Initialize git first, then add submodules

**Step 4** (45 min): Migrate testing infrastructure ⭐ HIGH VALUE
→ Copy progressive testing framework (test_base.py, runner.py, etc.)
→ Copy GHDL filter (98% output reduction)
→ Source: FORGE-v5/libs/forge-vhdl/python/forge_cocotb/*

**Step 5** (30 min): Migrate forge-codegen
→ Copy 23-type system + register packing
→ Source: FORGE-v5/tools/forge-codegen/*

**Step 6** (20 min): Migrate BPD reference example ⭐ PRODUCTION-PROVEN
→ Copy complete Basic Probe Driver
→ Source: FORGE-v5/examples/basic-probe-driver

**Step 7** (40 min): Migrate documentation
→ VHDL_CODING_STANDARDS.md, COCOTB_TROUBLESHOOTING.md
→ FORGE_ARCHITECTURE.md (from BPD)
→ Platform guides

**Step 8** (1 hour): Migrate and adapt agent definitions ⭐ CRITICAL
→ Copy agents from FORGE-v5/.claude/agents/
→ Rename: forge-vhdl-component-generator → vhdl-generator
→ GOTCHA: Update path references (.claude → agent-os)

**Step 9** (45 min): Create new documentation
→ TRAIN_LIKE_YOU_FIGHT.md (philosophy)
→ AGENT_WORKFLOW.md (5-phase pipeline)
→ Top-level README.md, CLAUDE.md

**Step 10** (20 min): Git configuration
→ .gitmodules, .gitignore

════════════════════════════════════════════════════════════════════════════════

## CRITICAL GOTCHAS (MUST READ)

**Gotcha 1: Git Submodule Order**
❌ DON'T: `git submodule add` before `git init`
✅ DO:
   1. `git init`
   2. Create .gitignore and commit
   3. `git submodule add ...`
   4. `git submodule update --init --recursive`

**Gotcha 2: Testing Framework Path Adjustments**
Problem: Tests import from `forge_cocotb` which is now at `tools.testing`
Solution: Update imports or create package structure
→ See CRITICAL_PATHS.md for mappings

**Gotcha 3: Agent Path References**
Problem: Agents reference `.claude/agents/` which is now `agent-os/agents/`
Solution: Review and update all agent markdown files
→ Test cocotb-integration-test first (it's validated)

**Gotcha 4: GHDL Filter Integration**
Problem: ghdl_output_filter.py needs to be callable from runners
Solution: Update PATH or modify runner.py to use absolute path

════════════════════════════════════════════════════════════════════════════════

## TOMORROW'S SESSION WORKFLOW

**Phase 1: Review (15 mins)**
1. Read this prompt
2. Review MIGRATION_PLAN.md (sections you're unclear on)
3. Ask clarifying questions
4. Confirm approach

**Phase 2: Execute Migration (2-3 hours)**
1. Run Steps 1-10 from MIGRATION_PLAN.md
2. Verify at each checkpoint
3. Document deviations in CRITICAL_PATHS.md

**Phase 3: Test Scaffold (1 hour)**
1. Try running BPD P1 tests
2. Fix path issues
3. Verify progressive testing works

**Phase 4: Agent Adaptation (1-2 hours)**
1. Review cocotb-integration-test agent
2. Adapt to Agent-OS patterns
3. Document adaptation approach

════════════════════════════════════════════════════════════════════════════════

## KEY DECISIONS MADE

**✓ Directory Structure**: Use FORGE-v6 pattern (sys/, libs/, tools/, examples/)
**✓ Register Packing**: YES, include forge-codegen with automatic packing
**✓ Git Strategy**: Copy files directly (lose history) + submodules for libs
**✓ Agent Integration**: Adapt to Agent-OS (not .claude/ hidden directory)
**✓ Priority**: "Train like you fight" - CustomWrapper testing is foundational

════════════════════════════════════════════════════════════════════════════════

## USER PREFERENCES (SESSION CONTINUITY)

**User wants**:
- Comprehensive handoff (this file + MIGRATION_PLAN.md + CRITICAL_PATHS.md)
- Review plan first tomorrow, THEN execute
- Focus on: Git submodule setup, testing framework compatibility, path adjustments
- Preserve the workflow: requirements → VHDL gen → test design → test run → deploy

**User concerns**:
- Don't lose the design/architecture
- Agent-OS integration must preserve proven workflow
- Testing framework must work with new structure

════════════════════════════════════════════════════════════════════════════════

## WHAT TO SAY TOMORROW

When you paste this prompt, say:

"Good morning! I'm resuming work on AgentOS-GHDL-Gen migration. I have the
session handoff prompt loaded. Let's review the migration plan together before
we start executing. I'd like to:

1. Quickly review MIGRATION_PLAN.md (15 mins)
2. Clarify any questions about the approach
3. Then execute the 10-step migration

Ready when you are!"

════════════════════════════════════════════════════════════════════════════════

## QUICK REFERENCE: FILE LOCATIONS

**Handoff Documents** (in AgentOS-GHDL-Gen/):
- MIGRATION_PLAN.md - Complete guide (15k tokens)
- SESSION_HANDOFF_PROMPT.txt - This file
- CRITICAL_PATHS.md - Path mapping reference

**Source Repositories**:
- FORGE-v5: /Users/johnycsh/Forge/FORGE-v5
- FORGE-v6: /Users/johnycsh/Forge/FORGE-v6
- __incoming_stuff: /Users/johnycsh/AgentOS-GHDL-Gen/__incoming_stuff

**Already Created**:
- agent-os/product/mission.md
- agent-os/product/roadmap.md
- agent-os/product/tech-stack.md

════════════════════════════════════════════════════════════════════════════════

## SUCCESS CRITERIA

**Migration Complete When**:
✅ All 10 steps executed
✅ Git submodules initialized
✅ BPD P1 tests run successfully
✅ Documentation accessible
✅ One agent adapted to Agent-OS
✅ Path issues documented

**Ready for Development When**:
✅ Can create VHDL following FORGE patterns
✅ Can generate tests with agents
✅ Can run P1/P2/P3 tests
✅ Can reference BPD as working example
✅ Agent workflow validated end-to-end

════════════════════════════════════════════════════════════════════════════════

## ADDITIONAL CONTEXT (IF NEEDED)

**3-Layer FORGE Architecture**:
- Layer 1: BRAM Loader (future) - deployment coordination
- Layer 2: Shim - Control Register → typed signals (auto-generated from YAML)
- Layer 3: Main - Application FSM (hand-written, zero CR knowledge)

**FORGE Control Scheme (CR0[31:29])**:
- CR0[31] = forge_ready (loader sets after deployment)
- CR0[30] = user_enable (user GUI toggle)
- CR0[29] = clk_enable (clock gating)
- global_enable = forge_ready AND user_enable AND clk_enable AND loader_done

**Progressive Testing (P1/P2/P3)**:
- P1: <20 lines output, <5s runtime, 3-5 basic tests (LLM-optimized)
- P2: <50 lines output, <30s runtime, comprehensive scenarios
- P3: <100 lines output, <2m runtime, exhaustive coverage

**98% Output Reduction**: GHDL filter removes noise, preserves errors/failures.

════════════════════════════════════════════════════════════════════════════════

END OF SESSION HANDOFF PROMPT

See MIGRATION_PLAN.md for complete detailed instructions.
See CRITICAL_PATHS.md for path mapping reference.

Good luck tomorrow! 🚀
