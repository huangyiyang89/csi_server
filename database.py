from sqlmodel import SQLModel, create_engine, Session, select
from models.eventtype import EventType
from models.user import User
from typing import Generator


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


init_list = [
    EventType(id="1001", name="人员计数", description="", level=0),
    EventType(id="1002", name="安全帽检测", description="", level=0),
    EventType(id="1003", name="跌倒检测", description="", level=0),
    EventType(id="1004", name="积水检测", description="", level=0),
    EventType(id="1005", name="烟火检测", description="", level=0),
    # EventType(id="3101", name="设备状态检测", description="", level=1),
    # EventType(id="1402", name="反光衣检测", description="", level=2),
    # EventType(id="1502", name="打架检测", description="", level=2),
    # EventType(id="1311", name="抽烟检测", description="", level=2),
    # EventType(id="1202", name="电子围栏", description="", level=0),
]

init_user = User(id=1, name="admin", password="admin")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        evettype = session.exec(select(EventType)).first()
        if not evettype:
            for item in init_list:
                session.add(item)
        admin = session.exec(select(User)).first()
        if not admin:
            session.add(init_user)
        session.commit()

