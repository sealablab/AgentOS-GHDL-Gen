"""Test script for StdLogicReg and NetworkAppReg models."""

from forge_std_logic_reg import StdLogicReg
from forge_network_app_reg import NetworkAppReg


def test_std_logic_reg_defaults():
    """Test StdLogicReg with default values."""
    print("=" * 60)
    print("Test 1: StdLogicReg with defaults")
    print("=" * 60)
    reg = StdLogicReg()
    print(f"Model: {reg}")
    print(f"Dict: {reg.model_dump()}")
    print(f"JSON: {reg.model_dump_json(indent=2)}")
    print()


def test_std_logic_reg_custom():
    """Test StdLogicReg with custom values."""
    print("=" * 60)
    print("Test 2: StdLogicReg with custom values")
    print("=" * 60)
    reg = StdLogicReg(
        width=32,
        type_hint="custom_reg",
        descr="Test register"
    )
    print(f"Model: {reg}")
    print(f"Dict: {reg.model_dump()}")
    print()


def test_network_app_reg_defaults():
    """Test NetworkAppReg with default values."""
    print("=" * 60)
    print("Test 3: NetworkAppReg with defaults")
    print("=" * 60)
    reg = NetworkAppReg()
    print(f"Model: {reg}")
    print(f"Dict: {reg.model_dump()}")
    print(f"JSON: {reg.model_dump_json(indent=2)}")
    print()


def test_network_app_reg_custom():
    """Test NetworkAppReg with custom values."""
    print("=" * 60)
    print("Test 4: NetworkAppReg with custom values")
    print("=" * 60)
    reg = NetworkAppReg(
        width=16,
        type_hint="network_reg",
        descr="Custom network register",
        net_read_enabled="Y",
        net_write_enabled="Y",
        net_read_gated="N",
        net_write_gated="N"
    )
    print(f"Model: {reg}")
    print(f"Dict: {reg.model_dump()}")
    print()


def test_inheritance():
    """Test that NetworkAppReg inherits from StdLogicReg."""
    print("=" * 60)
    print("Test 5: Inheritance verification")
    print("=" * 60)
    network_reg = NetworkAppReg()
    std_reg = StdLogicReg()
    
    print(f"NetworkAppReg has 'width': {hasattr(network_reg, 'width')}")
    print(f"NetworkAppReg has 'type_hint': {hasattr(network_reg, 'type_hint')}")
    print(f"NetworkAppReg has 'descr': {hasattr(network_reg, 'descr')}")
    print(f"NetworkAppReg has 'net_read_enabled': {hasattr(network_reg, 'net_read_enabled')}")
    print(f"Is instance of StdLogicReg: {isinstance(network_reg, StdLogicReg)}")
    print(f"NetworkAppReg width (inherited): {network_reg.width}")
    print(f"StdLogicReg width: {std_reg.width}")
    print()


def test_validation():
    """Test model validation."""
    print("=" * 60)
    print("Test 6: Validation")
    print("=" * 60)
    try:
        # Valid model
        reg = NetworkAppReg(width=8, net_read_enabled="Y")
        print(f"✓ Valid model created: width={reg.width}, net_read_enabled={reg.net_read_enabled}")
        
        # Test that all required fields are present
        assert reg.width is not None
        assert reg.type_hint is not None
        assert reg.descr is not None
        assert reg.net_read_enabled is not None
        assert reg.net_write_enabled is not None
        assert reg.net_read_gated is not None
        assert reg.net_write_gated is not None
        print("✓ All required fields present")
        
    except Exception as e:
        print(f"✗ Validation error: {e}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Testing Pydantic Models: StdLogicReg & NetworkAppReg")
    print("=" * 60 + "\n")
    
    test_std_logic_reg_defaults()
    test_std_logic_reg_custom()
    test_network_app_reg_defaults()
    test_network_app_reg_custom()
    test_inheritance()
    test_validation()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
