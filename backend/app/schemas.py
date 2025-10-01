from typing import Optional
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


class CompositionSchema(BaseModel):
    name: str
    about: str


class MusicianSchema(BaseModel):
    name: str
    about: Optional[str]
    musician_type: MusicianType


class EnsembleSchema(BaseModel):
    name: str
    about: Optional[str]
    ensemble_type: EnsembleType


class PerformanceSchema(BaseModel):
    performance_date: date
    composition_id: int
    ensemble_id: int
