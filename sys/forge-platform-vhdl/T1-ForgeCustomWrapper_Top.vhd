library IEEE;
use IEEE.Std_Logic_1164.All;
use IEEE.Numeric_Std.all;

-- By convention we use 'Behavioural' to describe the CustomWrapper architecture
architecture Behavioural of CustomWrapper is
begin
  SHIM: entity WORK.APP_forge_shim
        port map (
            Clk => Clk,
            Reset => Reset,
            InputA => InputA,
            InputB => InputB,
            OutputA => OutputA,
            OutputB => OutputB
            -- ... etc etc

        );
end architecture;