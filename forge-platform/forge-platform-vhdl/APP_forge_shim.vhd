--------------------------------------------------------------------------------
-- File: forge_shim.vhd
-- Created: 2025-11-15
-- Generator: Manual (johnny)
--
-- Layer 2 of 3-Layer Forge Architecture:
--   Layer 1: APP_forge_mcc_top.vhd (static, shared)
--   Layer 2: APP_forge_shim.vhd (THIS FILE - register mappin template)
--   Layer 3: APP_forge_main.vhd (hand-written app logic)
--
-- References:
--   - forge_common_pkg.vhd (FORGE_READY control scheme)
--   - external_Example/DS1140_polo_shim.vhd (pattern reference)
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

library WORK;
use WORK.forge_common_pkg.all;

entity APP_forge_shim is
    port (
        ------------------------------------------------------------------------
        -- Clock and Reset
        ------------------------------------------------------------------------
        Clk         : in  std_logic;
        Reset       : in  std_logic;  -- Active-high reset

        ------------------------------------------------------------------------
        -- FORGE Control Signals (from MCC_TOP_forge_loader or CustomWrapper)
        ------------------------------------------------------------------------
        forge_ready  : in  std_logic;  -- CR0[31] - Set by loader
        user_enable  : in  std_logic;  -- CR0[30] - User control
        clk_enable   : in  std_logic;  -- CR0[29] - Clock gating
        loader_done  : in  std_logic;  -- BRAM loader FSM done signal

        ------------------------------------------------------------------------
        -- Application Registers (from MCC_TOP_forge_loader)
        -- Raw Control Registers CR1-CR11 (MCC provides CR0-CR15)
        ------------------------------------------------------------------------
        app_reg_1 : in  std_logic_vector(31 downto 0);
        app_reg_2 : in  std_logic_vector(31 downto 0);
        app_reg_3 : in  std_logic_vector(31 downto 0);
        app_reg_4 : in  std_logic_vector(31 downto 0);
        app_reg_5 : in  std_logic_vector(31 downto 0);
        app_reg_6 : in  std_logic_vector(31 downto 0);
        app_reg_7 : in  std_logic_vector(31 downto 0);
        app_reg_8 : in  std_logic_vector(31 downto 0);
        app_reg_9 : in  std_logic_vector(31 downto 0);
        app_reg_10 : in  std_logic_vector(31 downto 0);
        app_reg_11 : in  std_logic_vector(31 downto 0);

        ------------------------------------------------------------------------
        -- BRAM Interface (from forge_bram_loader FSM)
        ------------------------------------------------------------------------
        bram_addr   : in  std_logic_vector(11 downto 0);  -- 4KB address space
        bram_data   : in  std_logic_vector(31 downto 0);  -- 32-bit data
        bram_we     : in  std_logic;                      -- Write enable

        ------------------------------------------------------------------------
        -- MCC I/O (from CustomWrapper)
        -- Native MCC types: signed(15 downto 0) for all ADC/DAC channels
        ------------------------------------------------------------------------
        InputA      : in  signed(15 downto 0);
        InputB      : in  signed(15 downto 0);
        OutputA     : out signed(15 downto 0);
        OutputB     : out signed(15 downto 0);
        OutputC     : out signed(15 downto 0)
    );
end entity BPD_forge_shim;

