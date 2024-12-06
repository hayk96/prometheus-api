from ..misc.exemplar import ExemplarsConfig
from pydantic import BaseModel, Field
from ..misc.tsdb import TSDBConfig
from typing import Optional


class StorageConfig(BaseModel):
    tsdb: Optional[TSDBConfig] = Field(None)
    exemplars: Optional[ExemplarsConfig] = Field(None)
