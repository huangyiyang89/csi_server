from sqlmodel import SQLModel, Field


class NvrBase(SQLModel):
    mac: str
    ip: str
    brand: str | None = "hk"

class Nvr(NvrBase, table=True):
    id: int = Field(default=None, primary_key=True)
 
class NvrCreate(NvrBase):
    pass

class NvrUpdate(SQLModel):
    mac: str | None = None
    ip: str | None = None
    brand: str | None = None


