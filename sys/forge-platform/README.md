

# `sys/forge-platform/`



## L0: [[APP_forge_common_pkg.vhd]]
This is a small VHDL package file that contains FORGE app platform constants etc. 
## L1: [[APP_forge_mcc_top.vhd]]
This is the (static) template for compilation / synthesis with MCC. It has two simple jobs:
1) Pass off all of the [Control Registers provided by MCC](https://apis.liquidinstruments.com/mcc/controls.html) down into the shim (Layer 2)
## L2: [[APP_forge_shim.vhd]]
The default / template APP_forge_shim.vhd.

### Shim: register mapping 
Provides the 'integration' point for mapping the networks exposed Control registers to the (**intentionally** exposed) `Forge_App_network_reg_bundle`. 

This is basically the RTL for scraping individual bits out of the (networked) control registers and into the app specific domain.


### Shim: Clk-divider
Although not used by default, the shim layer includes a built in clk-divider module. The control bits of which are explicitly managed in the 'CR0' from **Layer one**


### Shim: Buffer loader



## L3: APP_main.vhd 
This is where the 'proper' FORGE app starts. 
All forge apps __shall__:
1) 