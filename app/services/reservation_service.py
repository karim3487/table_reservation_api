import logging

from fastapi import Depends

from app.errors import exceptions
from app.models import Reservation
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.table_repository import TableRepository
from app.schemas import ReservationCreate

logger = logging.getLogger("app.services.reservations")


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
        logger.info(
            "Fetching reservation list: page_size=%s, start_index=%s",
            page_size,
            start_index,
        )
        return self.reservation_repository.list(page_size, start_index)

    def get(self, reservation_id: int) -> Reservation:
        reservation = self.reservation_repository.get(reservation_id)
        if not reservation:
            logger.warning("Reservation not found: id=%s", reservation_id)
            raise exceptions.ReservationNotFound()

        logger.info("Retrieved reservation id=%s", reservation_id)
        return reservation

    def create(self, data: ReservationCreate) -> Reservation:
        logger.info(
            "Creating reservation for table_id=%s at %s",
            data.table_id,
            data.reservation_time.isoformat(),
        )

        table = self.table_repo.get(data.table_id)
        if not table:
            logger.warning(
                "Table not found for reservation: table_id=%s", data.table_id
            )
            raise exceptions.TableNotFound(data.table_id)

        overlapping = self.reservation_repository.find_overlapping_reservations(
            table_id=data.table_id,
            start_time=data.reservation_time,
            duration_minutes=data.duration_minutes,
        )

        if overlapping:
            logger.warning(
                "Time conflict for table_id=%s at %s",
                data.table_id,
                data.reservation_time.isoformat(),
            )
            raise exceptions.ReservationTimeConflict(data.table_id)

        reservation = Reservation(**data.model_dump())
        logger.info(
            "Reservation created for table_id=%s by %s",
            data.table_id,
            data.customer_name,
        )
        return self.reservation_repository.create(reservation)

    def update(
        self, reservation_id: int, reservation_update: ReservationCreate
    ) -> Reservation:
        logger.info("Updating reservation id=%s", reservation_id)

        reservation = self.reservation_repository.get(reservation_id)
        if not reservation:
            logger.warning("Reservation not found for update: id=%s", reservation_id)
            raise exceptions.ReservationNotFound()

        updated_reservation = Reservation(
            id=reservation_id, **reservation_update.model_dump()
        )
        logger.info("Reservation id=%s updated", reservation_id)
        return self.reservation_repository.update(updated_reservation)

    def delete(self, reservation_id: int) -> None:
        reservation = self.reservation_repository.get(reservation_id)
        if not reservation:
            logger.warning(
                "Attempt to delete non-existent reservation: id=%s", reservation_id
            )
            raise exceptions.ReservationNotFound()

        logger.info("Deleting reservation id=%s", reservation_id)
        self.reservation_repository.delete(reservation)
