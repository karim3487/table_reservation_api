from fastapi import APIRouter, Depends, status

from app.schemas import ReservationRead, ReservationCreate
from app.services.reservation_service import ReservationService

ReservationRouter = APIRouter(prefix="/v1/reservations", tags=["reservations"])


@ReservationRouter.get("/", response_model=list[ReservationRead])
def index(
    page_size: int | None = 100,
    start_index: int | None = 0,
    reservation_service: ReservationService = Depends(),
):
    return [
        reservation for reservation in reservation_service.list(page_size, start_index)
    ]


@ReservationRouter.get("/{reservation_id}", response_model=ReservationRead)
def get(reservation_id: int, reservation_service: ReservationService = Depends()):
    return reservation_service.get(reservation_id)


@ReservationRouter.post(
    "/",
    response_model=ReservationRead,
    status_code=status.HTTP_201_CREATED,
)
def create(
    reservation: ReservationCreate,
    reservation_service: ReservationService = Depends(),
):
    return reservation_service.create(reservation)


@ReservationRouter.patch("/{reservation_id}", response_model=ReservationRead)
def update(
    reservation_id: int,
    author: ReservationCreate,
    reservation_service: ReservationService = Depends(),
):
    return reservation_service.update(reservation_id, author)


@ReservationRouter.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(reservation_id: int, reservation_service: ReservationService = Depends()):
    return reservation_service.delete(reservation_id)
