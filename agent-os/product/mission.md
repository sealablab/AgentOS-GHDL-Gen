# Product Mission

## Pitch
AgentOS-GHDL-Gen is an AI-powered VHDL development framework that helps software engineers new to hardware design create, test, and deploy FPGA designs by providing automated code generation, intelligent testbench creation, and cloud-based synthesis without requiring heavyweight vendor toolchains.

## Users

### Primary Customers
- **Software Engineers Learning VHDL**: Developers with strong software engineering backgrounds who need to work with FPGAs but lack deep hardware design experience
- **Moku-GO Platform Developers**: Engineers targeting the Moku-GO FPGA platform from Liquid Instruments who want to streamline their development workflow

### User Personas

**Alex** (28-35 years old)
- **Role:** Full-stack Software Engineer / Embedded Systems Developer
- **Context:** Working on a project requiring FPGA integration for signal processing or custom hardware acceleration on Moku-GO platform
- **Pain Points:**
  - Overwhelmed by traditional VHDL toolchains (Vivado, Quartus) that require gigabytes of storage and complex licensing
  - Struggles with VHDL syntax and idioms coming from Python/JavaScript background
  - Finds manual testbench creation tedious and error-prone
  - Long iteration cycles when setting up traditional FPGA development environments
- **Goals:**
  - Quickly prototype and iterate on simple VHDL designs locally
  - Leverage existing software engineering skills (Python, testing frameworks)
  - Deploy to Moku-GO without installing massive vendor tools
  - Automate repetitive aspects of hardware testing

**Jordan** (24-30 years old)
- **Role:** Research Engineer / Hardware Prototyper
- **Context:** Building custom signal processing or control systems using Moku-GO for academic or industrial research
- **Pain Points:**
  - Limited by institutional licenses or IT restrictions preventing installation of large toolchains
  - Needs to iterate quickly on multiple design variants
  - Wants to apply modern software development practices (CI/CD, version control, automated testing) to hardware design
  - Manually writing CocoTB testbenches is time-consuming
- **Goals:**
  - Develop VHDL modules with software-like agility
  - Automate verification and validation workflows
  - Collaborate with software-focused team members on hardware components
  - Reduce time from design concept to hardware validation

## The Problem

### Traditional VHDL Development is Heavyweight and Inaccessible
Software engineers entering the FPGA domain face a steep learning curve compounded by toolchain complexity. Vendor-specific tools like Xilinx Vivado or Intel Quartus require multi-gigabyte installations, complex licensing, and significant system resources just to compile and simulate basic designs. This creates a massive barrier to entry for developers who simply want to iterate on small designs or learn VHDL incrementals.

**Our Solution:** AgentOS-GHDL-Gen leverages open-source GHDL for local simulation and the Moku cloud compile service for synthesis, eliminating the need for heavyweight vendor toolchains entirely. Developers can work in their familiar environments using lightweight tools.

### Manual Testbench Creation is Repetitive and Error-Prone
Writing VHDL testbenches manually is tedious, especially for software engineers accustomed to modern testing frameworks. The gap between software testing practices (pytest, Jest) and VHDL simulation creates friction and slows down development cycles. Many developers spend more time debugging their testbenches than their actual design.

**Our Solution:** AI-powered testbench generation using CocoTB allows developers to write tests in Python, their familiar language. Progressive Testing methodology ensures comprehensive coverage while automated generation handles the repetitive boilerplate, letting engineers focus on design logic rather than test infrastructure.

### Long Iteration Cycles Slow Development
Traditional FPGA workflows require full synthesis runs even for simple logic changes, leading to 30+ minute iteration cycles. This is incompatible with modern rapid development practices and discourages experimentation and learning.

**Our Solution:** Local GHDL simulation provides instant feedback on functionality and timing before synthesis. Only final validated designs need cloud compilation, reducing iteration time from hours to minutes and enabling true test-driven hardware development.

### Lack of Modern Development Workflow Integration
Hardware design tools often exist in isolated ecosystems without good integration into modern development workflows (Git, CI/CD, code review, automated testing). This makes collaboration difficult and prevents teams from applying proven software engineering practices to hardware.

**Our Solution:** Agent-based automation orchestrates the entire VHDL development workflow as code. Everything from design generation to verification runs in scripts, enabling version control, code review, automated testing, and CI/CD integration just like software projects.

## Differentiators

### Agent-Driven Development Workflow
Unlike traditional point-and-click FPGA tools, AgentOS-GHDL-Gen uses AI agents to automate the entire development cycle from specification to verification. This enables reproducible, scriptable workflows that integrate naturally with modern DevOps practices and version control systems.

### Python-First Testing Philosophy
Unlike traditional VHDL testbenches that require learning another HDL (VHDL/Verilog), we use CocoTB to enable testing in Python. Software engineers can leverage their existing Python knowledge and testing patterns, dramatically reducing the learning curve and increasing productivity.

### No Vendor Lock-in or Heavyweight Tools
Unlike Vivado or Quartus-based workflows that require multi-GB installations and complex licensing, we use open-source GHDL for local development and Moku cloud services for synthesis. This results in a lightweight, portable development environment that runs anywhere Python runs.

### Progressive Testing Methodology
Unlike manual ad-hoc testing approaches common in VHDL development, we implement Progressive Testing that automatically generates comprehensive test scenarios incrementally. This ensures thorough verification while minimizing developer effort and catching edge cases early.

### Template-Based HDL Generation
Unlike writing VHDL from scratch or copy-pasting code snippets, we use AI-powered template generation that follows VHDL-2008 best practices. This results in consistent, maintainable code that follows industry standards while accelerating initial development.

### Moku-GO Platform Optimization
Unlike generic FPGA tools, we are specifically optimized for the Moku-GO platform with direct integration to Moku API for register control and cloud compile services. This results in a streamlined workflow from design to deployment on actual hardware.

## Key Features

### Core Features
- **AI-Powered VHDL Code Generation:** Automatically generate VHDL-2008 compliant code from high-level specifications, reducing manual coding time and ensuring adherence to best practices
- **GHDL Simulation Orchestration:** Run lightweight local simulations using open-source GHDL without requiring vendor toolchains, enabling rapid iteration and immediate feedback
- **Template-Based HDL Generation:** Use proven design templates for common patterns (state machines, interfaces, signal processing blocks) to accelerate development and maintain consistency

### Collaboration Features
- **Agent-Based Design Verification:** AI agents automatically validate designs against specifications, check for common errors, and suggest improvements throughout the development cycle
- **Automated Testbench Creation with CocoTB:** Generate Python-based testbenches automatically, allowing software engineers to write hardware tests using familiar Python syntax and testing patterns
- **Progressive Testing Methodology:** Systematically build test coverage through automated incremental testing, starting from basic functionality and progressing to edge cases and corner conditions

### Advanced Features
- **Moku API Integration:** Direct integration with Moku-GO platform via FastAPI server for writing to network-accessible control registers and managing hardware configuration
- **Cloud Synthesis Offloading:** Automatically submit validated designs to Moku cloud compile service for synthesis, eliminating local resource requirements for place-and-route
- **Version-Controlled Hardware Development:** Full integration with Git workflows enabling code review, CI/CD, and collaborative hardware development using software engineering best practices
