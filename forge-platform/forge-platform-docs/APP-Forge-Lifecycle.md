
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


### L2-Shim: Divided clk management
The **Forge-shim** layer is also responsible for routing a (potentially) divided clock into the main application layer. This allows for consistent (remote) control of the main clk rate without the 'main' application having to manage it.


### L2-Shim: 'main-app' reset
The **Forge-shim** layer is responsible for exposing an 'application' level reset across the network. 


> [!NOTE] Application-main allows remote python clients to quickly and uniformly perform an 'application' level reset without reloading the bitstream or otherwise repeating platform initialization.


###  L2-Shim:  network register updates
The shim layer protects the 'main' application logic from spurious updates to network enabled control registers. 

##### **`Ready_for_Updates` (out)**
the **ready_for_updates** signal is how the main (L3) application signals to the shim layer that it can safely handle updates to its  `NetworkRegisters` bundle. 




## S2) 'main' app receives reset
Once the L2-shim has configured the (optional) clk-divider, it will
- set Clk, Reset, Enable, clk_enable
- perform an initial reset (first and once)
-