# riscure-models

Pydantic models for Riscure FI/SCA probe specifications and Moku integration.

---

## Quick Start

```bash
# Installation (development mode)
cd riscure-models/
uv pip install -e .
```

```python
from riscure_models import DS1120A_PLATFORM

# Load probe specification
probe = DS1120A_PLATFORM

# Check port specs
trigger = probe.get_port_by_id('digital_glitch')
print(f"Trigger: {trigger.get_voltage_range_str()}")  # "0.0V to 3.3V"
```

---

## Documentation

This library uses **tiered documentation** for efficient information access:

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[llms.txt](llms.txt)** | Quick reference: API, probe specs, common tasks | Always start here |
| **[DETAILS.md](DETAILS.md)** | Complete technical details: Design patterns, integration | Design/integration work |
| **Source code** | Implementation details | Debugging/implementation |

**For AI agents:** See [.ai/context-strategy.md](.ai/context-strategy.md) for token-efficient loading strategy.

---

## Repository Structure

```
riscure-models/
├── .ai/                   # AI agent guidance
│   └── context-strategy.md
├── riscure_models/        # Python package
│   ├── __init__.py
│   └── probes/
│       ├── ds1120a.py     # DS1120A probe model
│       └── __init__.py
├── llms.txt               # Quick reference
├── DETAILS.md             # Complete technical details
├── README.md              # This file
├── pyproject.toml
└── LICENSE
```

---

## Supported Probes

- **DS1120A**: High-power unidirectional EM-FI probe (450V, 64A, fixed 50ns pulse) - ✅ Implemented
- **DS1121A**: Bidirectional EM-FI probe with sensing capability - 🚧 Planned

---

## Integration

**Works with:**
- [moku-models-v4](https://github.com/sealablab/moku-models-v4) - Platform specifications for voltage compatibility

---

## License

MIT

---

**Version:** 1.0.0 | **Last Updated:** 2025-11-10
