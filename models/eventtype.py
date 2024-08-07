from sqlmodel import SQLModel, Field

class EventType(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    name: str | None = ""
    description: str | None = ""
    remark: str | None = ""
    level: int | None = 0
