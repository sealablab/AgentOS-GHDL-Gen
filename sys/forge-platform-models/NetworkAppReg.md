# [[NetworkAppReg]]
**NetworkAppReg** is essentially a vendor agnostic representation of the [Control Registers](https://apis.liquidinstruments.com/mcc/controls.html) that the moku platform exposes. 

It inherits from the [[StdLogicReg]] base-type, but adds the following:


## Properties

| name              | req? | descr                        | default |
| ----------------- | ---- | ---------------------------- | ------- |
| net_read_enabled  | Y    | FUTURE                       | `F`     |
| net_write_enabled | Y    | self-descr                   | 'Y'     |
| net_read_gated    | Y    | FUTURE                       | 'Y'     |
| net_write_gated   | Y    | L2-SHIM layer manages writes | 'Y'     |


# See Also

## [[StdLogicReg]]

## [LI:ControlRegisters](https://apis.liquidinstruments.com/mcc/controls.html)
