from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta, datetime
from typing import List

from app.db import get_db_session
from app.models import Reservation


class ReservationRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_session)):
        self.db = db

    def list(self, limit: int | None, start: int | None) -> List[Reservation]:
        query = self.db.query(Reservation)
        return query.offset(start).limit(limit).all()

    def get(self, reservation_id: int) -> Reservation | None:
        return self.db.get(Reservation, reservation_id)

    def create(self, reservation: Reservation) -> Reservation:
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def update(self, reservation: Reservation) -> Reservation:
        self.db.merge(reservation)
        self.db.commit()
        return reservation

    def delete(self, reservation: Reservation) -> None:
        self.db.delete(reservation)
        self.db.commit()

    def find_overlapping_reservations(
        self, table_id: int, start_time: datetime, duration_minutes: int
    ) -> List[Reservation]:
        new_end_time = start_time + timedelta(minutes=duration_minutes)

        overlapping = (
            self.db.query(Reservation)
            .filter(
                Reservation.table_id == table_id,
                Reservation.reservation_time < new_end_time,
                (
                    Reservation.reservation_time
                    + func.make_interval(0, 0, 0, 0, 0, Reservation.duration_minutes, 0)
                )
                > start_time,
            )
            .all()
        )
        return overlapping
