from sqlmodel import SQLModel, Field


class NvrBase(SQLModel):
    mac: str
    ip: str
    brand: str | None = "hk"
    state: int | None = 0


class Nvr(NvrBase, table=True):
    id: int = Field(default=None, primary_key=True)


class NvrCreate(NvrBase):
    pass


class NvrUpdate(SQLModel):
    mac: str | None = None
    ip: str | None = None
    brand: str | None = None
    state: int | None = None
