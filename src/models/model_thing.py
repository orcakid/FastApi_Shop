from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base


class Item(Base):
    __tablename__='items'
    
    id = Column(Integer(), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text(), nullable=True)
    price = Column(Float(), nullable=False)
    category_id = Column(Integer(), ForeignKey('categories.id'))
    category = relationship('Category', back_populates='item')


class Category(Base):
    __tablename__='categories'
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    item = relationship('Item', back_populates='category')
    