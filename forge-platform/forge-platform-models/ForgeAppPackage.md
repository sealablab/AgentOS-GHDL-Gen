# ForgeAppPackage

**ForgeAppPackage** model contains metadata about a 'forge application'
## Properties

| name                          | req? | descr                           | default   |
| ----------------------------- | ---- | ------------------------------- | --------- |
| forge_app_name                | Y    | FUTURE                          | `F`       |
| forge_app_ver                 | Y    | self-descr                      | 'Y'       |
| forge_app_descr               | Y    | FUTURE                          | 'Y'       |
| num_bram_bufs                 | Y    | number of 4K bram buffers (0-1) | 'Y'       |
| forge_app_platforms_supported | Y    | MOKU_GO, MOKU_LAB, etc          | `MOKU-GO` |


### ForgeAppPackagePaths
Paths to bitreams and zero or more 4KB bram buffers
## Properties

| name               | req? | descr                                            | default |
| ------------------ | ---- | ------------------------------------------------ | ------- |
| bitstream_path     | Y    | `/path/to/your_bits.tar`                         |         |
| bram_buff_paths[N] | Y    | array of paths to `num_bram_bufs` distinct files | 'Y'     |
|                    |      |                                                  |         |



# See Also

## [[StdLogicReg]]

## [LI:ControlRegisters](https://apis.liquidinstruments.com/mcc/controls.html)
