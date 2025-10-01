from typing import Optional, List
from datetime import date
from pydantic import BaseModel
from .models import MusicianType, EnsembleType


class RecordSchema(BaseModel):
    company: str
    wholesale_company_address: str
    retail_price: float
    wholesale_price: float
    release_date: date

    # Статистика
    current_year_sold: int
    last_year_sold: int
    remaining_stock: int

    performances_id: List[int]


class RecordResponse(BaseModel):
    company: str
    wholesale_company_address: str
    retail_price: float
    wholesale_price: float
    release_date: date

    # Статистика
    current_year_sold: int
    last_year_sold: int
    remaining_stock: int

    performances: List['PerformanceResponse']


class CompositionSchema(BaseModel):
    name: str
    about: str


class CompositionResponse(BaseModel):
    id: int
    name: str
    about: str


class MusicianSchema(BaseModel):
    name: str
    about: Optional[str]
    musician_type: MusicianType


class MusicianResponse(BaseModel):
    id: int
    name: str
    about: Optional[str]
    musician_type: MusicianType


class EnsembleSchema(BaseModel):
    name: str
    about: Optional[str]
    ensemble_type: EnsembleType

    musicians_id: List[int]


class EnsembleResponse(BaseModel):
    id: int
    name: str
    about: Optional[str]
    ensemble_type: EnsembleType

    musicians: List[MusicianResponse]


class PerformanceSchema(BaseModel):
    performance_date: date
    composition_id: int
    ensemble_id: int


class PerformanceResponse(BaseModel):
    id: int
    performance_date: date
    composition_id: int
    ensemble_id: int
