
from pydantic import BaseModel
from datetime import datetime



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


#  Booking payload
class BookingIn(BaseModel):
    fitness_class_id: int
    client_name: str
    client_email: str

    class Config:
        from_attributes = True

class BookingOut(BaseModel):
    id: int
    fitness_class: FitnessClassOut
    client_name: str
    client_email: str
    booking_time: datetime

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    error: str

    class Config:
        from_attributes = True