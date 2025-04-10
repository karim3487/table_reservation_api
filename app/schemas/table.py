from pydantic import BaseModel, Field


class TableBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Table name must be 2–50 characters",
    )
    seats: int = Field(
        ..., ge=1, le=1000, description="Count of seats can't be less than 1"
    )
    location: str = Field(..., min_length=3, max_length=100)


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int

    class Config:
        from_attributes = True
