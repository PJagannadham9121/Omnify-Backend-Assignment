
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


class BookingOut(BaseModel):
    id: int
    client_name: str
    client_email: str
    fitness_class_id: int
    booked_at: datetime

    class Config:
        from_attributes = True

class FitnessClassItem(BaseModel):
    id: int
    name: str
    type: str
    datetime: datetime
    instructor: InstructorOut

    class Config:
        from_attributes = True


class BookingItem(BaseModel):
    id: int  # Booking ID
    booked_at: datetime
    fitness_class: FitnessClassItem

    class Config:
        from_attributes = True

# class BookingSummaryItem(BaseModel):
#     fitness_class: BookingItem
#     booked_at: datetime

#     class Config:
#         from_attributes = True



class BookingSummary(BaseModel):
    client_email: str
    total_bookings: int
    bookings: List[BookingItem]

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    error: str

    class Config:
        from_attributes = True