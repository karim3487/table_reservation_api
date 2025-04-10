from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    table_id: int
    reservation_time: datetime = Field(
        ..., examples=["2025-04-10T21:30:00+03:00"]
    )
    duration_minutes: int = Field(
        ..., ge=1, le=240, description="Duration must be between 1 and 240 minutes"
    )


class ReservationCreate(ReservationBase):
    @field_validator("reservation_time")
    def validate_datetime(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            raise ValueError("reservation_time must be timezone-aware")
        now = datetime.now(timezone.utc)
        if v < now:
            raise ValueError("reservation_time must be in the future")
        return v


class ReservationRead(ReservationBase):
    id: int

    @field_validator("reservation_time", mode="before")
    def ensure_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    class Config:
        from_attributes = True
