from sqlalchemy import String, Integer, create_engine, Column
from sqlalchemy.orm import sessionmaker,declarative_base
from urllib.parse import quote_plus
db_admin_password = quote_plus("Mamaguai123.@")
Database_url = f'mysql+mysqlconnector://root:{db_admin_password}@localhost/LoginSysDB'

engine = create_engine(Database_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(20),nullable=False)
    password = Column(String(100),nullable=False)
    email = Column(String(20),nullable=True)

Base.metadata.create_all(bind=engine)