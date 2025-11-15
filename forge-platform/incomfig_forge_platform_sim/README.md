# forge-platform-simulator

**Platform simulation infrastructure for Moku custom instrument testing**

## Overview

`forge-platform-simulator` provides behavioral models for Moku platform components, enabling realistic integration testing of custom FPGA instruments through CocoTB simulation.

**Key Components:**
- **OscilloscopeSimulator** - Time-series data capture from DUT signals
- **CloudCompileSimulator** - MCC Control Computer interface simulation
- **NetworkCRInterface** - Network-settable control registers (simulates MCC API)
- **SimulationBackend** - Unified platform simulation orchestration

### Oscilloscope Capture

```python
from forge_platform.simulators import OscilloscopeSimulator

# Initialize oscilloscope
scope = OscilloscopeSimulator(dut, {
    'sample_rate': 125e6,  # 125 MHz (Moku:Go)
    'channels': ['OutputC', 'OutputD']
})

# Capture for 10 microseconds
await scope.run(duration_ns=10000)

# Analyze data
data = scope.get_data('OutputC')
print(f"Captured {data['sample_count']} samples")

# Verify incrementing counter
assert scope.verify_incrementing('OutputC', start_sample=0, count=10)
```

### MCC Control Register Simulation

```python
from forge_platform.simulators import CloudCompileSimulator

# Initialize MCC simulator
mcc = CloudCompileSimulator(dut, {
    'control_registers': {
        0: 0xE0000000,  # FORGE control: forge_ready|user_enable|clk_enable
        1: 0x1234,      # Application-specific register
    }
})

# Apply control registers to DUT
await mcc.apply_control_registers()

# Update register (simulates network write)
await mcc.set_control_register(1, 0x5678)

# Check FORGE control state
print(mcc.forge_state)  # {'forge_ready': True, 'user_enable': True, ...}
```

## Use Cases

### Platform Integration Testing

Test custom instruments through the MCC CustomInstrument interface (Control0-15, InputA-D, OutputA-D) as they would run on actual Moku hardware:

```python
# Test BPD FSM state transitions via oscilloscope
scope = OscilloscopeSimulator(dut, {'channels': ['OutputC']})
await scope.run(duration_ns=50000)

# Verify IDLE → ARMED → FIRING state progression
states = [sample[1] & 0x3F for sample in scope.data['OutputC']]
assert states[0] == 0b000000  # IDLE
assert states[100] == 0b000001  # ARMED
assert states[200] == 0b000010  # FIRING
```

### FSM Debugging

Capture FSM state voltages encoded via `fsm_observer` component:

```python
# OutputD encodes FSM state as voltage for oscilloscope debugging
scope.add_external_channel('OutputD', dut.OutputD)
await scope.run(duration_ns=10000)

# Analyze voltage stairstep (IDLE=0V, ARMED=0.625V, FIRING=1.25V, etc.)
voltages = scope.get_data('OutputD')['values']
# ... voltage-to-state decoding ...
```

## Documentation

- **Quick Reference:** [llms.txt](llms.txt)
- **Design Guide:** [CLAUDE.md](CLAUDE.md)
- **Monorepo Architecture:** [../../CLAUDE.md](../../CLAUDE.md)

## Architecture

### Simulation Layers

```
MokuConfig (YAML)
    ↓
SimulationBackend
    ↓
┌─────────────────────┬───────────────────────┐
│ CloudCompileSimulator│ OscilloscopeSimulator │
│ (Control Registers) │ (Data Capture)        │
└─────────────────────┴───────────────────────┘
              ↓
         DUT (CustomWrapper)
```

### FORGE Control Scheme Integration

All simulators understand the FORGE control scheme (CR0[31:29]):
- **forge_ready** (CR0[31]) - Deployment complete
- **user_enable** (CR0[30]) - User control
- **clk_enable** (CR0[29]) - Clock gating

CloudCompileSimulator automatically validates FORGE control state.

## Development

### Running Tests

```bash
cd libs/forge-platform
pytest tests/
```

### Adding New Simulators

1. Create simulator class in `forge_platform/simulators/`
2. Add to `simulators/__init__.py` registry
3. Add tests in `tests/`
4. Update documentation

## Related Packages

- **forge-vhdl** - VHDL component library (uses platform simulators for integration tests)
- **moku-models** - Platform specifications (MokuConfig, voltage domains)
- **riscure-models** - Probe specifications (example integration)

## License

MIT License - See [LICENSE](../../LICENSE)

## Version

**1.0.0** - Initial release (2025-11-11)
