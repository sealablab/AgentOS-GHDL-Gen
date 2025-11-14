
# 2025-11-14-Layout

Johnnys proposed AgentOS-GHDL-Gen layout and seperation of concerns / lessons learned


## Lessons learned

## L1: Absolute voltages == tricky
Previous attempts to 'expose' absolute voltage settings to python layers resulted in __lots__ more complexity than anticipated. These fell into two distinct camps:
- Different run-time selectable analog front ends makes it difficult for client apps to be absolutely confident in device configuration
- Marshalling / representing these voltages (over the wire, in memory, etc etc) is cumbersome. 

In at attempt to radically simplify FORGE infrastructure the following model is suggested:
## A1: Apps only expose / express voltages as a 7-bit index into an (app-supplied) LUT) 

This has the advantage that it 
a) Maps logically and clearly to a human-friendly display unit (percentage)
b) can easily be represented in 7-bits
c) Is inherently platform / voltage / unit agnostic. 


## L2:  Absolute time units == tricky
Previous iterations attempted to 'pass' units of time over the wire into bitstreams (nanoseconds, usecs, etc).

This worked, but suffered from similar problems as absolute voltages: serialization, representation, etc.

The __upside__ of this arrangement was that the mapping of clock rates -> time units could be done on the bitstream / platform side of things. While elegant, i propose the following solution (for now)

## A2: Clients are responsible for time->clk math
Motivated for similar reasons as the change to 'percent' based voltage (avoid serialization ambiguity), python clients shall:
1) convert all time units into platform specific clk cycles at run time. 



