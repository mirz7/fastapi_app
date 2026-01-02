from collections.abc import AsyncGenerator
import uuid
from datetime import datetime
from sqlalchemy import Column,DateTime,String,Text,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
class Base(DeclarativeBase):
    pass
class Post(Base):
    __tablename__= "posts"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    #randomly generate unique id when we insert data to db
    caption = Column(Text)
    url = Column(String,nullable=False)
    file_type = Column(String,nullable=False)
    file_name = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)

engine = create_async_engine(DATABASE_URL)
async_sessionmaker = async_sessionmaker(engine,expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        #fill all the classes in declarative base and create the db

async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_sessionmaker() as session:
        yield session
    #session keywords uses yield for async sessions mandatory for async none uses until funcitn completes return none
    #creates a session allows to acces the db aynchronously