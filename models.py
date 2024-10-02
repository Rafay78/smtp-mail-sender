from db import Base
from sqlalchemy import Column, String, create_engine , Integer


class Users(Base):  
    __tablename__ = 'users'  # the name of the table  

    # Define columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  
    email = Column(String, nullable=False, unique=True)  # unique email  
    image_url = Column(String)  

