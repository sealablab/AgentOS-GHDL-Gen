# forge-platform Design Guide

**Version:** 1.0.0
**Purpose:** Platform simulation infrastructure for Moku custom instrument testing
**Audience:** Human developers and AI agents

---

## Executive Summary

`forge-platform` provides behavioral models for Moku platform components (oscilloscope, MCC Control Computer), enabling realistic integration testing of custom FPGA instruments through CocoTB simulation.

**Key Innovation:** Test custom instruments through the **MCC CustomInstrument interface** (Control0-15, InputA-D, OutputA-D) with oscilloscope waveform capture - achieving platform-realistic integration testing without physical hardware.

**Use Case:** Validate BPD (Basic Probe Driver) FSM state transitions, pulse timing, and fault handling as it would run on Moku:Go hardware with oscilloscope attached.

---

## Architecture Overview

### Simulation Layers

```
┌────────────────────────────────────────────────────┐
│ Test Code (Python/CocoTB)                         │
│  - Define test scenarios                           │
│  - Configure MokuConfig                            │
│  - Analyze captured waveforms                      │
└────────────────────────────────────────────────────┘
                     ↓
┌────────────────────────────────────────────────────┐
│ SimulationBackend (Orchestration Layer)           │
│  - MokuConfig parsing                              │
│  - Multi-instrument coordination                   │
│  - Inter-slot routing                              │
└────────────────────────────────────────────────────┘
                     ↓
┌──────────────────────┬─────────────────────────────┐
│ CloudCompileSimulator│ OscilloscopeSimulator       │
│  - CR0-15 management │  - Waveform capture         │
│  - FORGE validation  │  - Multi-channel support    │
│  - Network CR API    │  - Analysis helpers         │
└──────────────────────┴─────────────────────────────┘
                     ↓
┌────────────────────────────────────────────────────┐
│ DUT (VHDL CustomWrapper)                          │
│  - CustomWrapper_bpd_forge.vhd                     │
│  - MCC CustomInstrument interface                  │
│  - Control0-15, InputA-D, OutputA-D                │
└────────────────────────────────────────────────────┘
```

### Three Testing Levels

**Level 1: Unit Tests** (forge-vhdl agents)
- Test individual VHDL components directly
- No MCC interface, no platform simulation
- Example: Test `forge_util_clk_divider.vhd` entity ports

**Level 2: Integration Tests** (forge-platform - THIS PACKAGE)
- Test through MCC CustomInstrument interface
- Simulate MCC Control Computer + Oscilloscope
- Example: Test BPD CustomWrapper with oscilloscope capture

**Level 3: Hardware Tests** (actual Moku hardware)
- Deploy to physical Moku platform
- Real oscilloscope, real DAC/ADC
- Example: BPD running on Moku:Go with DS1120A probe

**forge-platform targets Level 2** - the critical gap between unit tests and hardware.

---

## Core Components

### 1. OscilloscopeSimulator

**Purpose:** Behavioral model of Moku Oscilloscope instrument

**File:** `forge_platform/simulators/oscilloscope.py` (341 lines)

#### Initialization

```python
from forge_platform.simulators import OscilloscopeSimulator

scope = OscilloscopeSimulator(dut, settings={
    'sample_rate': 125e6,          # Sampling rate (Hz) - default 125 MHz
    'channels': ['OutputC', 'OutputD'],  # Auto-discover if not specified
    'decimation': 1,               # Sample rate reduction factor
    'trigger_mode': 'auto',        # 'auto' | 'normal' | 'single' (future)
    'trigger_level': 0,            # Trigger threshold (future)
})
```

**Auto-Discovery:**
- If `channels` not specified, auto-discovers OutputA/B/C/D
- Also looks for `count_out`, `debug_bus`, `probe_out` (common test signals)
- Defaults to `['OutputC']` if nothing found (BPD debug bus convention)

#### Data Capture

```python
# Capture for 10 microseconds
await scope.run(duration_ns=10000)

# Stop early (if needed)
scope.stop_capture()
```

**Sampling:**
- Sample period = `(1e9 / sample_rate) * decimation` nanoseconds
- For 125 MHz, sample_period = 8 ns (one clock cycle)
- Decimation=10 → sample every 80 ns (useful for long captures)

#### Data Retrieval

```python
# Get all captured data for one channel
data = scope.get_data('OutputC')
# Returns: {
#     'time': [t1, t2, t3, ...],      # Timestamps in ns
#     'values': [v1, v2, v3, ...],    # Signal values (int)
#     'sample_count': N                # Total samples
# }

# Get all channels
all_data = scope.get_data()  # Returns dict of all channels

# Get specific sample
value_at_100 = scope.get_value_at_sample('OutputC', sample_index=100)

# Get latest value
latest = scope.get_latest_value('OutputC')
```

#### Waveform Analysis Helpers

```python
# Verify incrementing counter (with wrap-around detection)
assert scope.verify_incrementing(
    channel='OutputC',
    start_sample=0,
    count=10
)

# Clear data for multi-run tests
scope.clear_data()

# Get statistics
stats = scope.get_statistics()
# Returns: {
#     'channels': ['OutputC', 'OutputD'],
#     'sample_rate': 125e6,
#     'decimation': 1,
#     'effective_sample_rate': 125e6,
#     'total_samples': 1250,
#     'capture_active': False,
#     'samples_per_channel': {'OutputC': 625, 'OutputD': 625}
# }
```

#### External Channel Routing (Inter-Slot Connections)

```python
# Simulate Slot 1 Output → Slot 2 Input routing
scope = OscilloscopeSimulator(slot2_dut, {'channels': ['InputA']})

# Route Slot 1 OutputA to Slot 2 InputA
scope.add_external_channel('InputA', slot1_dut.OutputA)

# Now scope captures slot1_dut.OutputA as 'InputA'
await scope.run(duration_ns=10000)
```

#### Signal Reading (Handles Signed/Unsigned)

```python
# Automatically detects signed vs unsigned signals:
# - If signal has .signed_integer, reads as signed
# - Otherwise reads as unsigned
# - Handles undefined/high-impedance as 0

# Example internal logic:
def _read_signal_value(signal):
    if hasattr(signal.value, 'signed_integer'):
        return int(signal.value.signed_integer)  # Signed
    else:
        return int(signal.value)  # Unsigned
```

---

### 2. CloudCompileSimulator

**Purpose:** Simulates MCC Control Computer interface for CloudCompile custom instruments

**File:** `forge_platform/simulators/cloud_compile.py` (200+ lines)

#### Initialization

```python
from forge_platform.simulators import CloudCompileSimulator

mcc = CloudCompileSimulator(dut, settings={
    'control_registers': {
        0: 0xE0000000,  # CR0: FORGE control [31:29] + app registers
        1: 0x1234,      # CR1: Application register
        # ... up to CR15
    },
    'bitstream': 'path/to/bitstream.bin'  # Informational only in sim
})
```

#### Control Register Application

```python
# Apply all control registers from settings
await mcc.apply_control_registers()

# Applies to DUT.Control0, DUT.Control1, ..., DUT.Control15
# Default to 0 for any registers not in settings
```

#### Dynamic Control Register Updates

```python
# Set individual control register (simulates network write)
await mcc.set_control_register(register=1, value=0x5678)

# Read control register
value = mcc.get_control_register(register=1)  # Returns 0x5678
```

#### FORGE Control Scheme Validation

```python
# FORGE state is automatically tracked from CR0[31:29]
print(mcc.forge_state)
# {
#     'forge_ready': True,   # CR0[31]
#     'user_enable': True,   # CR0[30]
#     'clk_enable': True,    # CR0[29]
#     'loader_done': True    # Assumed True in simulation
# }

# Validate FORGE ready (all 4 conditions True)
assert mcc.validate_forge_ready()

# Set FORGE control bits
await mcc.set_forge_ready()      # CR0[31] = 1
await mcc.set_user_enable()      # CR0[30] = 1
await mcc.set_clk_enable()       # CR0[29] = 1
```

**FORGE Control Bits (CR0[31:29]):**
- **forge_ready** (CR0[31]) - Set by loader when deployment complete
- **user_enable** (CR0[30]) - User control (GUI toggle)
- **clk_enable** (CR0[29]) - Clock gating control
- **loader_done** - Internal signal (always True in simulation)

**Global Enable Logic:**
```vhdl
global_enable = forge_ready AND user_enable AND clk_enable AND loader_done
```

#### Internal Tracking

```python
# Applied control register values
mcc.applied_crs  # Dict[int, int] - CR values currently applied to DUT

# Control register bank (includes updates)
mcc.control_registers  # Dict[int, int] - All CR values
```

---

### 3. NetworkCRInterface

**Purpose:** Network-settable control register bank (simulates MCC API)

**File:** `forge_platform/network_cr.py`

**Capabilities:**
- Register read/write with optional network delay simulation
- Atomic multi-register updates
- Register change callbacks
- FORGE control scheme tracking

**Status:** Advanced feature, not required for basic testing

---

### 4. SimulationBackend

**Purpose:** Unified platform simulation orchestration

**File:** `forge_platform/simulation_backend.py`

**Capabilities:**
- Multi-instrument coordination (multiple slots)
- MokuConfig-driven setup (platform, instruments, routing)
- Inter-slot signal routing
- Timing synchronization across instruments

**Status:** Advanced feature for multi-slot testing

---

## Usage Patterns

### Pattern 1: BPD Platform Integration Test

**Goal:** Verify BPD FSM state transitions through MCC interface

```python
import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from forge_platform.simulators import CloudCompileSimulator, OscilloscopeSimulator

@cocotb.test()
async def test_bpd_fsm_states_platform(dut):
    """Test BPD FSM state progression via platform simulation"""

    # Start clock (125 MHz Moku:Go)
    clock = Clock(dut.Clk, 8, units="ns")
    cocotb.start_soon(clock.start())

    # Initialize MCC simulator
    mcc = CloudCompileSimulator(dut, {
        'control_registers': {
            0: 0xE0000000,  # FORGE: forge_ready|user_enable|clk_enable
            1: 0b00000001,  # arm_enable = 1 (BPD lifecycle control)
        }
    })

    # Apply FORGE control + initial registers
    dut.Reset.value = 1
    await Timer(100, units='ns')
    dut.Reset.value = 0
    await Timer(100, units='ns')

    await mcc.apply_control_registers()

    # Initialize oscilloscope
    scope = OscilloscopeSimulator(dut, {
        'sample_rate': 125e6,
        'channels': ['OutputC']  # FSM state in OutputC[5:0]
    })

    # Capture FSM state transitions
    await scope.run(duration_ns=10000)  # 10 μs

    # Analyze state progression
    data = scope.get_data('OutputC')
    states = [value & 0x3F for value in data['values']]  # Extract state bits [5:0]

    # Verify IDLE → ARMED transition
    assert states[0] == 0b000000  # IDLE
    assert 0b000001 in states     # ARMED appears

    print(f"FSM states captured: {set(states)}")
```

### Pattern 2: FSM Observer Oscilloscope Debugging

**Goal:** Capture FSM state voltages via `fsm_observer` component

```python
@cocotb.test()
async def test_bpd_fsm_observer_voltages(dut):
    """Test fsm_observer voltage encoding for oscilloscope debugging"""

    # NOTE: Uses CustomWrapper_bpd_with_observer.vhd (has fsm_observer)

    clock = Clock(dut.Clk, 8, units="ns")
    cocotb.start_soon(clock.start())

    # Initialize MCC + oscilloscope
    mcc = CloudCompileSimulator(dut, {
        'control_registers': {0: 0xE0000000, 1: 0b00000001}
    })

    dut.Reset.value = 1
    await Timer(100, units='ns')
    dut.Reset.value = 0
    await Timer(100, units='ns')

    await mcc.apply_control_registers()

    # Capture OutputD (fsm_observer voltage encoding)
    scope = OscilloscopeSimulator(dut, {
        'sample_rate': 125e6,
        'channels': ['OutputD']
    })

    await scope.run(duration_ns=50000)  # 50 μs

    # Analyze voltage stairstep
    data = scope.get_data('OutputD')
    voltages = data['values']  # Digital codes (16-bit signed)

    # Convert to voltage (±5V range: -32768 → -5V, 32767 → +5V)
    voltage_scale = 5.0 / 32768.0
    voltages_v = [v * voltage_scale for v in voltages]

    # Verify voltage progression (example encoding)
    # IDLE = 0.0V, ARMED = 0.625V, FIRING = 1.25V, etc.
    # (Exact encoding depends on fsm_observer configuration)

    print(f"Voltage range: {min(voltages_v):.3f}V to {max(voltages_v):.3f}V")
```

### Pattern 3: Pulse Timing Validation

**Goal:** Verify BPD generates correct pulse durations

```python
@cocotb.test()
async def test_bpd_pulse_timing(dut):
    """Verify trigger and intensity pulse durations"""

    clock = Clock(dut.Clk, 8, units="ns")
    cocotb.start_soon(clock.start())

    # Configure BPD pulse durations
    mcc = CloudCompileSimulator(dut, {
        'control_registers': {
            0: 0xE0000000,  # FORGE control
            1: 0b00000011,  # arm_enable=1, ext_trigger_in=1
            2: 0x1234,      # trig_out_voltage (signed mV)
            3: 0x0064,      # trig_out_duration = 100 ns
            4: 0x5678,      # intensity_voltage (signed mV)
            5: 0x00C8,      # intensity_duration = 200 ns
        }
    })

    dut.Reset.value = 1
    await Timer(100, units='ns')
    dut.Reset.value = 0
    await Timer(100, units='ns')

    await mcc.apply_control_registers()

    # Capture pulse outputs
    scope = OscilloscopeSimulator(dut, {
        'sample_rate': 125e6,
        'channels': ['OutputA', 'OutputB']  # trig_out_active, intensity_out_active
    })

    await scope.run(duration_ns=5000)  # 5 μs

    # Measure pulse widths
    trig_data = scope.get_data('OutputA')
    intensity_data = scope.get_data('OutputB')

    # Find pulse start/end (value transitions from 0 → 0xFFFF → 0)
    trig_times = trig_data['time']
    trig_values = trig_data['values']

    # Calculate pulse width (count samples where value == 0xFFFF)
    trig_pulse_samples = sum(1 for v in trig_values if v == 0xFFFF)
    trig_pulse_width_ns = trig_pulse_samples * 8  # 8 ns per sample @ 125 MHz

    # Verify within tolerance
    assert abs(trig_pulse_width_ns - 100) < 16, \
        f"Trigger pulse: expected 100 ns, got {trig_pulse_width_ns} ns"

    print(f"Trigger pulse: {trig_pulse_width_ns} ns")
    print(f"Intensity pulse: {intensity_pulse_width_ns} ns")
```

### Pattern 4: Control Register Live Updates

**Goal:** Test dynamic control register updates (simulates GUI changes)

```python
@cocotb.test()
async def test_control_register_updates(dut):
    """Test runtime control register changes"""

    clock = Clock(dut.Clk, 8, units="ns")
    cocotb.start_soon(clock.start())

    # Initial setup
    mcc = CloudCompileSimulator(dut, {
        'control_registers': {0: 0xE0000000, 1: 0x1000}
    })

    dut.Reset.value = 0
    await Timer(100, units='ns')
    await mcc.apply_control_registers()

    scope = OscilloscopeSimulator(dut, {'channels': ['OutputC']})

    # Capture initial state
    await scope.run(duration_ns=1000)
    initial_state = scope.get_latest_value('OutputC') & 0x3F

    # Update control register mid-simulation (simulates user GUI change)
    await mcc.set_control_register(1, 0x2000)

    # Capture new state
    scope.clear_data()
    await scope.run(duration_ns=1000)
    new_state = scope.get_latest_value('OutputC') & 0x3F

    # Verify state changed
    assert new_state != initial_state, "State should change after CR update"
```

---

## Design Principles

### 1. Behavioral, Not Cycle-Accurate

**Philosophy:** Functional accuracy suitable for verification, not hardware simulation

**Implications:**
- OscilloscopeSimulator captures waveforms, but timing may differ from hardware
- Focus on verifying **state transitions** and **patterns**, not absolute timing
- Use relative timing checks (pulse A ends before pulse B starts) not absolute (pulse is exactly 100.0 ns)

### 2. Minimal API Surface

**Philosophy:** Keep simulators simple and focused

**OscilloscopeSimulator:**
- Core: `__init__()`, `run()`, `get_data()`
- Helpers: `get_latest_value()`, `verify_incrementing()`, `get_statistics()`
- Advanced: `add_external_channel()` for routing

**CloudCompileSimulator:**
- Core: `__init__()`, `apply_control_registers()`, `set_control_register()`
- FORGE: `validate_forge_ready()`, `forge_state` property

### 3. FORGE Control Scheme Awareness

**All simulators understand FORGE control:**
- CR0[31] = forge_ready
- CR0[30] = user_enable
- CR0[29] = clk_enable
- global_enable = forge_ready AND user_enable AND clk_enable AND loader_done

**CloudCompileSimulator automatically:**
- Parses CR0[31:29]
- Tracks FORGE state
- Provides validation methods

### 4. MokuConfig Integration (Future)

**Current:** Manual simulator setup in test code

**Future:** MokuConfig-driven setup via SimulationBackend

```yaml
# moku_config.yaml (future)
platform: moku_go
slots:
  - slot: 1
    instrument: CloudCompile
    bitstream: bpd_forge.bit
    control_registers:
      0: 0xE0000000
      1: 0x1234
  - slot: 2
    instrument: Oscilloscope
    channels: [1, 2]
    sample_rate: 125e6
```

```python
# Future API
from forge_platform import SimulationBackend

backend = SimulationBackend('moku_config.yaml')
await backend.setup(dut)
await backend.run(duration_ns=10000)
data = backend.get_oscilloscope_data(slot=2, channel=1)
```

---

## Integration with FORGE Workflow

### Component Development (Unit Tests)

**Workflow:**
```
forge-new-component
  → forge-vhdl-component-generator
  → cocotb-progressive-test-designer
  → cocotb-progressive-test-runner
```

**Testing Level:** Unit tests (direct entity testing)
**Tools:** forge-vhdl test infrastructure
**Location:** `libs/forge-vhdl/tests/`

### Platform Integration Testing (System Tests)

**Workflow:**
```
[User has working CustomWrapper]
  → platform-integration-test (new agent)
  → Uses forge-platform simulators
  → Tests through MCC CustomInstrument interface
```

**Testing Level:** Integration tests (platform-realistic)
**Tools:** OscilloscopeSimulator + CloudCompileSimulator
**Location:** `examples/basic-probe-driver/vhdl/tests/` (or similar)

**Key Difference:**
- **Component tests:** Test `forge_util_clk_divider.vhd` entity directly
- **Platform tests:** Test `CustomWrapper_bpd_forge.vhd` through Control0-15, OutputA-D

---

## Testing Best Practices

### 1. Use Progressive Test Levels

**P1 tests (platform integration):**
- 2-4 essential scenarios
- Small capture durations (10-50 μs, not 1 second)
- Verify state transitions, not absolute timing
- <20 line output (GHDL filter enabled)

**Example:**
```python
# P1 test - verify FSM reaches ARMED state
await scope.run(duration_ns=10000)  # Small duration
states = [v & 0x3F for v in scope.get_data('OutputC')['values']]
assert 0b000001 in states  # ARMED state present
```

### 2. Apply FORGE Control Scheme

**Always set CR0[31:29] correctly:**

```python
mcc = CloudCompileSimulator(dut, {
    'control_registers': {
        0: 0xE0000000,  # FORGE bits [31:29] all set
        # ... application registers ...
    }
})
```

**Verify FORGE state:**
```python
await mcc.apply_control_registers()
assert mcc.validate_forge_ready()  # All 4 conditions True
```

### 3. Small Sample Counts for P1

**Oscilloscope captures:**
- P1: 10-20 samples for validation
- P2: 100-500 samples for edge cases
- P3: 1000+ samples for stress tests

**Example:**
```python
# P1 - verify incrementing for 10 samples only
assert scope.verify_incrementing('OutputC', start_sample=0, count=10)
```

### 4. Reset Sequence

**Standard pattern:**
```python
clock = Clock(dut.Clk, 8, units="ns")
cocotb.start_soon(clock.start())

# Assert reset
dut.Reset.value = 1  # or 0 if active-low (check VHDL!)
await Timer(100, units='ns')

# Release reset
dut.Reset.value = 0  # or 1 if active-low
await Timer(100, units='ns')

# Apply control registers AFTER reset
await mcc.apply_control_registers()
```

### 5. Clear Data Between Runs

**For multi-scenario tests:**
```python
# Run scenario 1
await scope.run(duration_ns=5000)
data1 = scope.get_data('OutputC')

# Clear for scenario 2
scope.clear_data()
await scope.run(duration_ns=5000)
data2 = scope.get_data('OutputC')
```

---

## API Reference

### OscilloscopeSimulator API

**Constructor:**
```python
OscilloscopeSimulator(dut, settings: Dict[str, Any])
```

**Settings:**
- `sample_rate` (int): Samples/second (default 125e6)
- `channels` (List[str]): Signal names to capture (auto-discover if omitted)
- `decimation` (int): Sample rate reduction factor (default 1)
- `trigger_mode` (str): 'auto' | 'normal' | 'single' (future, default 'auto')
- `trigger_level` (int): Trigger threshold (future, default 0)

**Methods:**
- `async run(duration_ns: int) -> None` - Capture data
- `stop_capture() -> None` - Stop ongoing capture
- `get_data(channel: Optional[str] = None) -> Dict[str, Any]` - Retrieve data
- `get_value_at_sample(channel: str, sample_index: int) -> Optional[int]` - Get sample by index
- `verify_incrementing(channel: str, start_sample: int, count: int) -> bool` - Counter validation
- `get_latest_value(channel: str) -> Optional[int]` - Most recent sample
- `clear_data() -> None` - Reset buffers
- `get_statistics() -> Dict[str, Any]` - Capture stats
- `add_external_channel(channel_name: str, signal_handle: SimHandleBase) -> None` - Route signal

**Properties:**
- `data: Dict[str, List[tuple]]` - Raw data (time, value) tuples
- `channels: List[str]` - Configured channels
- `sample_rate: float` - Sampling rate
- `capture_active: bool` - Capture in progress

### CloudCompileSimulator API

**Constructor:**
```python
CloudCompileSimulator(dut, settings: Dict[str, Any])
```

**Settings:**
- `control_registers` (Dict[int, int]): Initial CR values (0-15)
- `bitstream` (str): Path to bitstream (informational)

**Methods:**
- `async apply_control_registers() -> None` - Apply all CRs to DUT
- `async set_control_register(register: int, value: int) -> None` - Set single CR
- `get_control_register(register: int) -> int` - Read CR value
- `async set_forge_ready() -> None` - Set CR0[31] = 1
- `async set_user_enable() -> None` - Set CR0[30] = 1
- `async set_clk_enable() -> None` - Set CR0[29] = 1
- `validate_forge_ready() -> bool` - Check FORGE state

**Properties:**
- `forge_state: Dict[str, bool]` - FORGE control bits
- `control_registers: Dict[int, int]` - CR bank
- `applied_crs: Dict[int, int]` - Applied CR values

---

## Common Pitfalls

### Pitfall 1: Capturing Too Long

**Problem:**
```python
await scope.run(duration_ns=1_000_000)  # 1 ms = 125,000 samples!
```

**Solution:**
```python
await scope.run(duration_ns=10_000)  # 10 μs = 1,250 samples
```

**Guideline:** P1 tests should capture 10-50 μs maximum

### Pitfall 2: Forgetting FORGE Control

**Problem:**
```python
mcc = CloudCompileSimulator(dut, {
    'control_registers': {
        1: 0x1234  # Missing CR0!
    }
})
```

**Solution:**
```python
mcc = CloudCompileSimulator(dut, {
    'control_registers': {
        0: 0xE0000000,  # FORGE bits [31:29]
        1: 0x1234
    }
})
```

### Pitfall 3: Wrong Reset Polarity

**Problem:**
```python
dut.Reset.value = 0  # Active-high assumed
await Timer(100, units='ns')
dut.Reset.value = 1  # Release
```

**Solution:** Check VHDL entity!
```vhdl
-- If rst_n (active-low):
dut.rst_n.value = 0  # Assert
dut.rst_n.value = 1  # Release

-- If Reset (active-high):
dut.Reset.value = 1  # Assert
dut.Reset.value = 0  # Release
```

### Pitfall 4: Not Clearing Data Between Runs

**Problem:**
```python
await scope.run(duration_ns=5000)
# ... change DUT state ...
await scope.run(duration_ns=5000)  # Appends to existing data!
```

**Solution:**
```python
await scope.run(duration_ns=5000)
scope.clear_data()  # Clear before next run
await scope.run(duration_ns=5000)
```

---

## Future Enhancements

### Phase 2: MokuConfig Integration

**Goal:** SimulationBackend reads MokuConfig YAML

**Benefits:**
- Unified configuration format (simulation + hardware)
- Multi-slot orchestration
- Inter-slot routing
- Network delay simulation

### Phase 3: Trigger Modes

**Goal:** OscilloscopeSimulator supports trigger modes

**Modes:**
- `auto` - Always triggers (current behavior)
- `normal` - Wait for trigger condition
- `single` - Capture once on trigger

### Phase 4: Status Register Monitoring

**Goal:** CloudCompileSimulator reads Status0-15

**Use Case:** Verify DUT status outputs (future MCC feature)

---

## Related Documentation

**Monorepo:**
- `../../CLAUDE.md` - FORGE architecture overview
- `../../llms.txt` - Monorepo quick reference

**Platform Specs:**
- `../moku-models/CLAUDE.md` - Moku platform specifications

**VHDL Components:**
- `../forge-vhdl/CLAUDE.md` - VHDL utilities + component tests

**Agent Workflow:**
- `../../.claude/shared/AGENT_WORKFLOW.md` - Agent invocation patterns

---

**Last Updated:** 2025-11-11
**Maintained By:** Moku Instrument FORGE Team
**Version:** 1.0.0
