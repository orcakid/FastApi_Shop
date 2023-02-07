from sqlalchemy import Integer, String, Column
from ..db.database import Base


# user = Table(
#     'user',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('username', String, nullable=False),
#     Column('email', String, nullable=False),
#     Column('hashed_password', String, nullable=False)
# )

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String())
    email = Column(String())
    hashed_password = Column(String())