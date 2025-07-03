from ninja import Router
from .schema import FitnessClassOut, BookingIn, BookingOut, ErrorResponse, InstructorOut
from .models import FitnessClass, Booking
from typing import List  
from pytz import timezone as tz , all_timezones

from django.utils import timezone 
from django.db import transaction

router = Router()


import logging

logger = logging.getLogger(__name__)


@router.get("/classes", response={200: List[FitnessClassOut], 400: ErrorResponse})
def get_classes(request, user_timezone: str = "Asia/Kolkata"):
    try:
        user_tz = tz(user_timezone)
    except Exception:
        logger.warning("Invalid timezone: %s", user_timezone)
        return 400, {"error": "Invalid timezone"}


    classes = FitnessClass.objects.filter(datetime__gte=timezone.now()).select_related("instructor").all()

    response = []
    for cls in classes:
        response.append(
            FitnessClassOut(
                id=cls.id,
                name=cls.name,
                type=cls.type,
                datetime=cls.datetime.astimezone(user_tz),
                total_slots=cls.total_slots,
                available_slots=cls.available_slots,
                instructor=InstructorOut(
                    id=cls.instructor.id,
                    name=cls.instructor.name,
                    email=cls.instructor.email,
                )
            )
        )

    return 200, response


@router.post("/book", response={201: BookingOut, 400: ErrorResponse, 404: ErrorResponse})
def book_class(request, payload: BookingIn):
    try:
        with transaction.atomic():
            # handling overbooking condition 
            fitness_class = FitnessClass.objects.select_for_update().get(id=payload.fitness_class_id)
            if fitness_class.available_slots <= 0:
                logger.warning("Booking failed due to no slots for class ID: %d", payload.fitness_class_id)
                return 400, {"error": "No available slots for this class"}

            if payload.client_email and Booking.objects.filter(
                client_email=payload.client_email, 
                fitness_class=fitness_class
            ).exists():
                # handling single user can't book same class multiple times
                logger.warning("Booking a class is rejected/failed because of User (Email: %s) is already Enrolled the class ID: %d",payload.client_email,payload.fitness_class_id)
                return 400, {"error": "You have already booked this class"}

            fitness_class.available_slots -= 1
            fitness_class.save()

            booking = Booking.objects.create(
                fitness_class=fitness_class,
                client_name=payload.client_name,
                client_email=payload.client_email
            )
            logger.info("Booking created for user: %s", payload.client_email)
    except FitnessClass.DoesNotExist:
        logger.warning("Booking failed. Class not found for ID: %d", payload.fitness_class_id)
        return 404, {"error": "Fitness class not found"}


    return 201, BookingOut(
        id=booking.id,
        fitness_class=FitnessClassOut(
            id=booking.fitness_class.id,
            name=booking.fitness_class.name,
            type=booking.fitness_class.type,
            datetime=booking.fitness_class.datetime,
            total_slots=booking.fitness_class.total_slots,
            available_slots=booking.fitness_class.available_slots,
            instructor=InstructorOut(
                id=booking.fitness_class.instructor.id,
                name=booking.fitness_class.instructor.name,
                email=booking.fitness_class.instructor.email,
            )
        ),
        client_name=booking.client_name,
        client_email=booking.client_email,
        booking_time=booking.booking_time  
    )


@router.get("/bookings", response={200: List[BookingOut]})
def get_bookings_by_email(request, client_email: str):
    bookings = Booking.objects.filter(
        client_email=client_email
    ).select_related("fitness_class__instructor")

    if not bookings.exists():
        logger.info("No bookings found for email: %s", client_email)
        return 200, []
    
    return 200, bookings