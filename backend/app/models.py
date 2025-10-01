from datetime import date
from typing import Optional, List
from enum import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, Date, Table, Column, MetaData
from sqlalchemy.dialects.postgresql import ENUM as pgEnum

class Base(DeclarativeBase):
    __abstract__ = True
    
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


# Таблицы многие-ко-многим
musician_ensemble = Table(
    'musician_ensemble',
    Base.metadata,
    Column('musician_id', ForeignKey('musicians.id')),
    Column('ensemble_id', ForeignKey('ensembles.id')),
)


performance_record = Table(
    'performance_record',
    Base.metadata,
    Column('performance_id', ForeignKey('performances.id')),
    Column('record_id', ForeignKey('records.id')),
)


# Модели SQLAlchemy и enum'ы
class MusicianType(Enum):
    performer = 1
    composer = 2
    conductor = 3
    director = 4


class Musician(Base):
    '''Модель музыканта'''
    __tablename__ = 'musicians'

    name: Mapped[str] = mapped_column(String(100))
    about: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    musician_type: Mapped[MusicianType] = mapped_column(pgEnum(MusicianType))


class EnsembleType(Enum):
    orchestra = 1
    quartet = 2
    quintet = 3


class Ensemble(Base):
    '''Модель ансамбля'''
    __tablename__ = 'ensembles'

    name: Mapped[str] = mapped_column(String(100))
    about: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    ensemble_type: Mapped[EnsembleType] = mapped_column(pgEnum(EnsembleType))

    musicians: Mapped[List[Musician]] = relationship(secondary=musician_ensemble)


class Composition(Base):
    '''Модель музыкального произведения'''
    __tablename__ = 'compositions'

    name: Mapped[str] = mapped_column(String(100))
    about: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)


class Performance(Base):
    '''Модель исполнения'''
    __tablename__ = 'performances'

    performance_date: Mapped[date] = mapped_column(Date)
    
    composition_id: Mapped[int] = mapped_column(ForeignKey('compositions.id'))
    composition: Mapped[Composition] = relationship()
    ensemble_id: Mapped[int] = mapped_column(ForeignKey('ensembles.id'))
    ensemble: Mapped[Ensemble] = relationship()


class Record(Base):
    '''Модель пластинки'''
    __tablename__ = 'records'

    company: Mapped[str] = mapped_column(String(100))
    wholesale_company_address: Mapped[str] = mapped_column(String(100))
    retail_price: Mapped[float] = mapped_column(Float)
    wholesale_price: Mapped[float] = mapped_column(Float)
    release_date: Mapped[date] = mapped_column(Date)

    # Статистика
    current_year_sold: Mapped[int] = mapped_column(Integer, default=0)
    last_year_sold: Mapped[int] = mapped_column(Integer, default=0)
    remaining_stock: Mapped[int] = mapped_column(Integer, default=0)

    performances: Mapped[List[Performance]] = relationship(secondary=performance_record)


# Модели для авторизации
class User(Base):
    '''Пользователь системы'''
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String, unique=True)
