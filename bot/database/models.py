from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

#Таблица точек
class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    cookies = relationship("CookieStorage", back_populates="location")
    teas = relationship("TeaStorage", back_populates="location")
    syrops = relationship("SyropStorage", back_populates="location")

# Типы запасов
class CookieType(Base):
    __tablename__ = 'cookie_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable=False)

    storages = relationship("CookieStorage", back_populates="cookie")


class TeaType(Base):
    __tablename__ = 'tea_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    storages = relationship("TeaStorage", back_populates="tea")


class Syrop(Base):
    __tablename__ = 'syrops'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    storages = relationship("SyropStorage", back_populates="syrop")


#Таблицы складов (связь продукт + точка)
class CookieStorage(Base):
    __tablename__ = 'cookie_storages'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    cookie_id = Column(Integer, ForeignKey('cookie_types.id'))
    quantity = Column(Integer, default=0)

    location = relationship("Location", back_populates="cookies")
    cookie = relationship("CookieType", back_populates="storages")


class TeaStorage(Base):
    __tablename__ = 'tea_storages'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    tea_id = Column(Integer, ForeignKey('tea_types.id'))
    quantity = Column(Integer, default=0)

    location = relationship("Location", back_populates="teas")
    tea = relationship("TeaType", back_populates="storages")


class SyropStorage(Base):
    __tablename__ = 'syrop_storages'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    syrop_id = Column(Integer, ForeignKey('syrops.id'))
    quantity = Column(Integer, default=0)

    location = relationship("Location", back_populates="syrops")
    syrop = relationship("Syrop", back_populates="storages")
