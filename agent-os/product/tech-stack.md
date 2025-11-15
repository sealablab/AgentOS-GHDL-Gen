# Tech Stack

## VHDL & HDL Tools

### Core HDL
- **Language Standard:** VHDL-2008 (IEEE 1076-2008)
- **Simulator:** GHDL (open-source VHDL simulator)
- **Synthesis Target:** Moku-GO FPGA platform (Xilinx-based)
- **Cloud Synthesis:** Moku cloud compile service

### Waveform Analysis
- **Format:** VCD (Value Change Dump)
- **Viewer:** GTKWave (recommended for manual inspection)
- **Automated Analysis:** Python-based waveform parsing libraries

## Testing & Verification

### Test Framework
- **Primary Framework:** CocoTB (Python-based hardware verification)
- **Testing Methodology:** Progressive Testing (incremental coverage approach)
- **Test Runner:** pytest integration with CocoTB
- **Coverage Tools:** CocoTB coverage plugins

### Verification Approach
- **Unit Testing:** Individual VHDL module verification
- **Integration Testing:** Multi-module system verification
- **Regression Testing:** Automated test suite execution on changes
- **Assertions:** PSL (Property Specification Language) assertions in VHDL where applicable

## Backend & Agent Framework

### Language & Runtime
- **Language:** Python 3.11+
- **Package Manager:** pip (with requirements.txt) or Poetry
- **Virtual Environment:** venv or Poetry environments

### Agent Framework
- **Framework:** Agent-OS (custom agent orchestration framework)
- **Data Validation:** Pydantic v2 (models for design specifications and validation)
- **Agent Communication:** Structured message passing between specialized agents
- **Workflow Orchestration:** Agent-based task decomposition and execution

### AI & LLM Integration
- **Primary Model:** Claude Sonnet 4 or 4.5 (Anthropic) for code generation and analysis
- **Alternative Models:** GPT-4 Turbo (OpenAI) as fallback or specialized tasks
- **Model Access:** API-based (anthropic-sdk, openai-sdk)
- **Prompt Management:** Structured prompts with few-shot examples for VHDL generation
- **Context Management:** Long-context models for analyzing full VHDL modules and testbenches

## API & Integration

### Web Framework
- **Framework:** FastAPI (async Python web framework)
- **API Design:** RESTful endpoints for design submission and status
- **Data Serialization:** JSON for API payloads
- **Request Validation:** Pydantic models for API request/response schemas

### Moku Platform Integration
- **Moku API:** HTTP-based API for control register writes
- **Platform:** Moku-GO FPGA device from Liquid Instruments
- **Deployment:** Bitstream upload via Moku cloud service
- **Hardware Control:** Network-accessible register interface

## Development Tools

### Code Quality
- **Linting:** Ruff (fast Python linter and formatter)
- **Type Checking:** mypy (static type analysis for Python)
- **VHDL Linting:** GHDL built-in syntax checking, vhdl-ls (VHDL Language Server)
- **Formatting:** black or ruff format for Python code

### Version Control
- **VCS:** Git
- **Platform:** GitHub (assumed primary hosting)
- **Branching Strategy:** Feature branches with PR-based review
- **Commit Standards:** Conventional Commits format

### CI/CD
- **Platform:** GitHub Actions
- **Test Execution:** Automated GHDL simulation + CocoTB test runs
- **Validation:** VHDL syntax checking on all commits
- **Artifact Management:** Waveform files and simulation logs as artifacts

## Development Environment

### Required Tools
- **GHDL:** Latest stable release (0.37+)
- **Python:** 3.11 or higher
- **CocoTB:** Latest stable (1.8+)
- **GTKWave:** For waveform viewing (optional, for debugging)

### Recommended IDE
- **VS Code** with extensions:
  - Python (Microsoft)
  - VHDL (vhdl-ls language server)
  - Pylance (Python type checking)
  - GitHub Copilot (optional, for AI assistance)

### System Requirements
- **OS:** Linux (primary), macOS (supported), Windows (WSL2)
- **Storage:** Minimal (no large vendor tools required)
- **RAM:** 8GB+ recommended for large designs
- **Network:** Required for cloud synthesis and Moku API access

## Third-Party Services

### AI/LLM Services
- **Anthropic Claude API:** Primary code generation service
- **OpenAI API:** Backup or specialized tasks
- **Rate Limiting:** Implement exponential backoff for API calls
- **Cost Management:** Token usage tracking and budget limits

### Cloud Services
- **Moku Cloud Compile:** FPGA synthesis service
- **Moku API:** Device control and configuration
- **Status Monitoring:** Polling-based compilation status checks

## Data Storage

### File-Based Storage
- **Design Files:** VHDL source files (.vhd, .vhdl)
- **Test Files:** Python CocoTB testbenches (.py)
- **Configuration:** YAML or TOML for design specifications
- **Output Files:** VCD waveforms, simulation logs, synthesis reports

### Structured Data
- **Design Specifications:** Pydantic models serialized to JSON
- **Test Results:** JSON test reports from CocoTB
- **Agent State:** In-memory or lightweight JSON-based state management
- **No Database Required:** File-based workflow for MVP

## Documentation

### Code Documentation
- **Python Docstrings:** Google or NumPy style docstrings
- **VHDL Comments:** Inline comments for complex logic blocks
- **API Documentation:** Auto-generated from FastAPI (Swagger/OpenAPI)

### Project Documentation
- **Format:** Markdown (.md files)
- **Location:** docs/ directory and agent-os/product/
- **Diagrams:** Mermaid.js for architecture and flow diagrams
- **Examples:** Sample VHDL modules and CocoTB testbenches

## Security & Secrets Management

### Environment Variables
- **API Keys:** Stored in .env files (never committed)
- **Moku Credentials:** Environment variables for cloud service access
- **Secret Management:** python-dotenv for local development

### Input Validation
- **API Inputs:** Pydantic validation on all FastAPI endpoints
- **VHDL Generation:** Sanitize specifications to prevent injection
- **File Operations:** Path validation to prevent directory traversal

## Performance Considerations

### Optimization
- **Parallel Simulation:** Run independent GHDL simulations concurrently
- **Async API:** FastAPI async handlers for non-blocking I/O
- **Caching:** Cache validated templates and common design patterns
- **Incremental Testing:** Progressive testing reduces redundant simulation time

### Resource Management
- **Process Management:** Proper cleanup of GHDL simulation processes
- **File Cleanup:** Remove temporary simulation files after completion
- **API Rate Limiting:** Respect Claude/OpenAI API rate limits
- **Memory Management:** Stream large waveform files rather than loading entirely
