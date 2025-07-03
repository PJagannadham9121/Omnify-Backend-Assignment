
from pydantic import BaseModel
from datetime import datetime
from typing import List



class InstructorOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class FitnessClassOut(BaseModel):
    id: int
    name: str
    type: str
    datetime: datetime
    total_slots: int
    available_slots: int
    instructor: InstructorOut

    class Config:
        from_attributes = True


class FitnessClassSummary(BaseModel):
    total_classes: int
    classes: List[FitnessClassOut]

    class Config:
        from_attributes = True
    




#  Booking payload
class BookingIn(BaseModel):
    fitness_class_id: int
    client_name: str
    client_email: str

    class Config:
        from_attributes = True

class BookingSummaryItem(BaseModel):
    id: int
    name: str
    type: str
    datetime: datetime
    instructor: InstructorOut
    booking_time: datetime

    class Config:
        from_attributes = True


class BookingOut(BaseModel):
    id: int
    client_name: str
    client_email: str
    fitness_class: BookingSummaryItem

    class Config:
        from_attributes = True


class BookingSummary(BaseModel):
    client_email: str
    total_bookings: int
    bookings: List[BookingSummaryItem]

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    error: str

    class Config:
        from_attributes = True