from datetime import date
from pydantic import BaseModel


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
