"""StdLogicReg - A 'trivial' type included for the sake of completeness."""

from pydantic import BaseModel, Field


class StdLogicReg(BaseModel):
    """Standard logic register base type."""
    
    width: int = Field(
        default=7,
        description="bit-width",
        json_schema_extra={"req": "Y"}
    )
    
    type_hint: str = Field(
        default="std_logic_reg",
        description="string based type hinting (not enforced)",
        json_schema_extra={"req": "Y"}
    )
    
    descr: str = Field(
        default="APP_FILLMEIN",
        description="Brief description of the register",
        json_schema_extra={"req": "Y"}
    )
