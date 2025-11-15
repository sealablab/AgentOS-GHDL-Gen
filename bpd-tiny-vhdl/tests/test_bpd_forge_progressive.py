"""
Progressive CocoTB tests for BPD FORGE Architecture.

Test Levels:
- P1 (BASIC): FORGE control scheme validation, safe defaults
- P2 (INTERMEDIATE): FSM state transitions, timing
- P3 (COMPREHENSIVE): Edge cases, fault handling, full integration

Usage:
    # Run P1 tests (default, LLM-optimized)
    uv run python tests/run.py bpd_forge

    # Run P2 tests (comprehensive validation)
    TEST_LEVEL=P2_INTERMEDIATE uv run python tests/run.py bpd_forge

Author: Moku Instrument Forge Team
Date: 2025-11-05
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import appropriate test level based on environment
test_level = os.environ.get('TEST_LEVEL', 'P1_BASIC')

if test_level == 'P1_BASIC':
    from bpd_forge_tests.P1_bpd_forge_basic import *
elif test_level == 'P2_INTERMEDIATE':
    # TODO: Create P2 tests
    print("P2 tests not yet implemented, falling back to P1")
    from bpd_forge_tests.P1_bpd_forge_basic import *
elif test_level == 'P3_COMPREHENSIVE':
    # TODO: Create P3 tests
    print("P3 tests not yet implemented, falling back to P1")
    from bpd_forge_tests.P1_bpd_forge_basic import *
else:
    print(f"Unknown test level: {test_level}, falling back to P1")
    from bpd_forge_tests.P1_bpd_forge_basic import *
