from ninja import NinjaAPI
from .schema import FitnessClassOut, BookingIn, BookingOut , ErrorResponse
from .models import FitnessClass, Booking
from typing import List  
from pytz import timezone as tz

api = NinjaAPI()

@api.get("/classes", response={200: List[FitnessClassOut], 400: ErrorResponse})
def list_classes(request, timezone: str = "Asia/Kolkata"):
    try:
        user_tz = tz(timezone)
    except Exception:
        return 400, {"error": "Invalid timezone"}

    classes = FitnessClass.objects.select_related("instructor").all()

    response =[]
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

    for cls in classes:
        cls.datetime = cls.datetime.astimezone(user_tz)

    return classes


@api.post("/book", response={201: BookingOut, 400 : ErrorResponse})
def book_class(request, payload: BookingIn):
    try:
        fitness_class = FitnessClass.objects.get(id=payload.fitness_class_id)
    except FitnessClass.DoesNotExist:
        return 404, {"error": "Fitness class not found"}

    if fitness_class.available_slots <= 0:
        return 400, {"error": "No available slots for this class"}

    if payload.client_email and Booking.objects.filter(client_email=payload.client_email, fitness_class=fitness_class).exists():
        return 400, {"error": "You have already booked this class"}

    fitness_class.available_slots -= 1
    fitness_class.save()

    booking = Booking.objects.create(
        fitness_class=fitness_class,
        client_name=payload.client_name,
        client_email=payload.client_email
    )

    return 201,booking



@api.get("/bookings", response={200: List[BookingOut], 404: ErrorResponse})
def list_bookings(request, client_email: str):
    bookings = Booking.objects.filter(client_email=client_email).select_related("fitness_class__instructor")
    return bookings  

