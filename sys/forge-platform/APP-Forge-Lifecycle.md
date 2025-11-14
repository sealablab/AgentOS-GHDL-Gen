
# App-Forge-Lifecycle

This note describes the lifecycle of an 'App-Forge' created instrument


## Bitstream loading
The actual loading of the bitstream is accomplished using first party tools and libraries. It is outside the scope of the lifecycle.
##  S0) Platform initialization
On bringup the Moku-Platform will: 
1) set the TOP level Reset
2) initialize all Control-Registers to 0x00


> [!NOTE] FORGE-Control-scheme
> FORGE-apps use a special calling convention deocumented in XXX that prevents the 'main' app from running



## S1) Forge-Shim receives control
By design the FORGE shim layer gates execution of the 'main' application. The shim does this for a few reasons:

### 'Safe' network register updates
The shim layer protects the 'main' application logic from spurious updates to network enabled control registers. 

All 'main' applications are required to expose an
##### `Ready_for_Updates` (out)
the **ready_for_updates** signal is how the main (L3) application signals to the shim layer that it can safely handle updates to its  `NetworkRegisters` bundle. 

By default this is allowed in the following two states:
- STATE_S1_READY (aka 'Idle') 
- STATE_S60_Done: (optional 'done' state)


### Divided clk management
The **Forge-shim** layer is also responsible for routing a (potentially) divided clock into the main application layer. This allows for consistent (remote) control of the main clk rate without the 'main' application having to manage it.

