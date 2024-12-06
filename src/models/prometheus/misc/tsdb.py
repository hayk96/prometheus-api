from pydantic import BaseModel, Field
from typing import Optional


class TSDBConfig(BaseModel):
    out_of_order_time_window: Optional[str] = Field(
        "0s", description="Configures how old an out-of-order/out-of-bounds "
        "sample can be w.r.t. the TSDB max time. "
        "An out-of-order/out-of-bounds sample is ingested "
        "into the TSDB as long as the timestamp of the "
        "sample is >= TSDB.MaxTime-out_of_order_time_window. "
        "When out_of_order_time_window is >0, the errors "
        "out-of-order and out-of-bounds are combined into "
        "a single error called 'too-old'; a sample is either "
        "(a) ingestible into the TSDB, i.e. it is an in-order "
        "sample or an out-of-order/out-of-bounds sample "
        "that is within the out-of-order window, or (b) "
        "too-old, i.e. not in-order and before the "
        "out-of-order window.")
