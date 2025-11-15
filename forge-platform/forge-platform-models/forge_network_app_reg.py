"""NetworkAppReg - Vendor agnostic representation of Control Registers."""

from pydantic import BaseModel, Field
from forge_std_logic_reg import StdLogicReg

class NetworkAppReg(StdLogicReg):
    """
    NetworkAppReg is essentially a vendor agnostic representation of the 
    Control Registers that the moku platform exposes.
    
    Inherits from StdLogicReg and adds network-specific properties.
    """
    
    net_read_enabled: str = Field(
        default="F",
        description="FUTURE",
        json_schema_extra={"req": "Y"}
    )
    
    net_write_enabled: str = Field(
        default="Y",
        description="self-descr",
        json_schema_extra={"req": "Y"}
    )
    
    net_read_gated: str = Field(
        default="Y",
        description="FUTURE",
        json_schema_extra={"req": "Y"}
    )
    
    net_write_gated: str = Field(
        default="Y",
        description="L2-SHIM layer manages writes",
        json_schema_extra={"req": "Y"}
    )
