from pydantic import BaseModel, Field
from typing import Optional


class RuntimeConfig(BaseModel):
    gogc: Optional[int] = Field(
        75,
        description="Configure the Go garbage collector GOGC parameter See: https://tip.golang.org/doc/gc-guide#GOGC "
                    "Lowering this number increases CPU usage.")
