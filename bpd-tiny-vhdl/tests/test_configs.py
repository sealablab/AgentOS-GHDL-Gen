"""
Test configurations for bpd-tiny-vhdl CocoTB tests.
Auto-discovered by run.py (from forge-vhdl) - no Makefile needed!

Module categories:
- fsm: FSM and control logic tests
- wrapper: CustomWrapper integration tests
- integration: Full system integration tests

Author: Adapted from forge-vhdl test infrastructure
Date: 2025-11-05
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import List

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"

# External dependencies
FORGE_VHDL = PROJECT_ROOT.parent / "forge-vhdl"
FORGE_VHDL_PKG = FORGE_VHDL / "vhdl" / "packages"
FORGE_VHDL_DEBUG = FORGE_VHDL / "vhdl" / "debugging"


@dataclass
class TestConfig:
    """Configuration for a single CocoTB test"""
    name: str
    sources: List[Path]
    toplevel: str
    test_module: str
    category: str = "misc"
    ghdl_args: List[str] = field(default_factory=lambda: ["--std=08"])


# ==================================================================================
# Test Configurations
# ==================================================================================

TESTS_CONFIG = {
    # === FORGE Architecture Tests ===

    "bpd_forge": TestConfig(
        name="bpd_forge",
        sources=[
            # Packages (bpd-tiny-vhdl)
            SRC_DIR / "basic_app_types_pkg.vhd",
            SRC_DIR / "basic_app_voltage_pkg.vhd",
            SRC_DIR / "basic_app_time_pkg.vhd",

            # FORGE infrastructure
            PROJECT_ROOT / "forge_common_pkg.vhd",
            PROJECT_ROOT / "BPD_forge_main.vhd",
            PROJECT_ROOT / "BPD_forge_shim.vhd",

            # Wrapper
            PROJECT_ROOT / "CustomWrapper_test_stub.vhd",
            PROJECT_ROOT / "CustomWrapper_bpd_forge.vhd",
        ],
        toplevel="customwrapper",  # Must be lowercase for GHDL
        test_module="test_bpd_forge_progressive",
        category="forge",
    ),

    # === FSM Observer Integration ===

    "bpd_fsm_observer": TestConfig(
        name="bpd_fsm_observer",
        sources=[
            # Packages (bpd-tiny-vhdl)
            SRC_DIR / "basic_app_types_pkg.vhd",
            SRC_DIR / "basic_app_voltage_pkg.vhd",
            SRC_DIR / "basic_app_time_pkg.vhd",

            # FSM Observer dependencies (forge-vhdl)
            FORGE_VHDL_PKG / "forge_voltage_5v_bipolar_pkg.vhd",
            FORGE_VHDL_DEBUG / "fsm_observer.vhd",

            # Core FSM
            SRC_DIR / "basic_probe_driver_custom_inst_main.vhd",

            # Wrapper with observer
            PROJECT_ROOT / "CustomWrapper_test_stub.vhd",
            PROJECT_ROOT / "CustomWrapper_bpd_with_observer.vhd",
        ],
        toplevel="customwrapper",  # Must be lowercase for GHDL
        test_module="test_bpd_fsm_observer_progressive",
        category="integration",
    ),

    # === Basic FSM Tests (legacy) ===

    "basic_probe_fsm": TestConfig(
        name="basic_probe_fsm",
        sources=[
            SRC_DIR / "basic_app_types_pkg.vhd",
            SRC_DIR / "basic_app_voltage_pkg.vhd",
            SRC_DIR / "basic_app_time_pkg.vhd",
            SRC_DIR / "basic_probe_driver_custom_inst_main.vhd",
        ],
        toplevel="basic_probe_driver_custom_inst_main",
        test_module="test_basic_probe_fsm",
        category="fsm",
    ),

    # === FI Interface Tests (legacy) ===

    "fi_interface": TestConfig(
        name="fi_interface",
        sources=[
            SRC_DIR / "basic_app_types_pkg.vhd",
            SRC_DIR / "basic_app_voltage_pkg.vhd",
            SRC_DIR / "basic_app_time_pkg.vhd",
            SRC_DIR / "basic_probe_driver_custom_inst_main.vhd",
        ],
        toplevel="basic_probe_driver_custom_inst_main",
        test_module="test_fi_interface",
        category="fsm",
    ),
}


# Helper functions for run.py integration
def get_test_config(module_name: str) -> TestConfig:
    """Get test configuration by module name"""
    if module_name not in TESTS_CONFIG:
        raise ValueError(f"Unknown test module: {module_name}")
    return TESTS_CONFIG[module_name]


def list_all_tests() -> List[str]:
    """List all available test modules"""
    return sorted(TESTS_CONFIG.keys())


def list_tests_by_category(category: str) -> List[str]:
    """List test modules by category"""
    return sorted([name for name, cfg in TESTS_CONFIG.items() if cfg.category == category])


# Compatibility aliases for forge-vhdl run.py
def get_test_names() -> List[str]:
    """Alias for list_all_tests()"""
    return list_all_tests()


def get_tests_by_category(category: str) -> List[str]:
    """Alias for list_tests_by_category()"""
    return list_tests_by_category(category)


def get_categories() -> List[str]:
    """Get list of all categories"""
    categories = set(cfg.category for cfg in TESTS_CONFIG.values())
    return sorted(categories)
