from fastapi import Depends

from app.models import Reservation
from app.schemas import ReservationCreate
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.table_repository import TableRepository
from app.errors import exceptions


class ReservationService:
    reservation_repository: ReservationRepository
    table_repository: TableRepository

    def __init__(
        self,
        reservation_repository: ReservationRepository = Depends(),
        table_repository: TableRepository = Depends(),
    ):
        self.reservation_repository = reservation_repository
        self.table_repo = table_repository

    def list(
        self, page_size: int | None = 10, start_index: int | None = 0
    ) -> list[Reservation]:
        return self.reservation_repository.list(page_size, start_index)

    def get(self, reservation_id: int) -> Reservation:
        reservation = self.reservation_repository.get(reservation_id)
        if not reservation:
            raise exceptions.ReservationNotFound()
        return reservation

    def create(self, data: ReservationCreate) -> Reservation:
        # Проверяем, что столик существует
        table = self.table_repo.get(data.table_id)
        if not table:
            raise exceptions.TableNotFound(data.table_id)

        # Проверяем на пересечения с существующими бронированиями
        overlapping = self.reservation_repository.find_overlapping_reservations(
            table_id=data.table_id,
            start_time=data.reservation_time,
            duration_minutes=data.duration_minutes,
        )

        if overlapping:
            raise exceptions.ReservationTimeConflict(data.table_id)

        reservation = Reservation(**data.model_dump())

        return self.reservation_repository.create(reservation)

    def update(
        self, reservation_id: int, reservation_update: ReservationCreate
    ) -> Reservation:
        reservation = self.reservation_repository.get(reservation_id)
        if not reservation:
            raise exceptions.ReservationNotFound()

        updated_reservation = Reservation(
            id=reservation_id, **reservation_update.model_dump()
        )
        return self.reservation_repository.update(updated_reservation)

    def delete(self, reservation_id: int) -> None:
        reservation = self.reservation_repository.get(reservation_id)
        if not reservation:
            raise exceptions.ReservationNotFound()
        self.reservation_repository.delete(reservation)
