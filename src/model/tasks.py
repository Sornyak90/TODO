from pydantic import BaseModel, validator
from datetime import date


class Task(BaseModel):
    name_task: str
    description: str
    date: date
    status: bool = False

    @validator("date", pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError as e:
                raise ValueError(
                    f"Invalid date format {value}. Expected format is YYYY-MM-DD."
                )
        return value
