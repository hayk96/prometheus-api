from pydantic import BaseModel, Field
from typing import Optional


class ExemplarsConfig(BaseModel):
    max_exemplars: Optional[int] = Field(
        100000,
        description="Configures the maximum size of the circular buffer used to store exemplars for all series. "
                    "Resizable during runtime.")
