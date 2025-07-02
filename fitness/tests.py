
from django.test import TestCase
from ninja.testing import TestClient
from ninja import NinjaAPI
from django.utils import timezone
from datetime import timedelta

from .models import Instructor, FitnessClass , Booking

from .api import router

client = TestClient(router)
class FitnessClassAPITest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            name = "Test Instructor 1",
            email = "test@gmail.com"
        )

        FitnessClass.objects.create(
            name="Yoga class",
            type="yoga",
            datetime=timezone.now() + timedelta(days=1),
            instructor=self.instructor,
            total_slots=30,
            available_slots=30,

        )

    def test_get_classes_with_valid_timezone(self):
        print("valid timezone")
        response = client.get("/classes",query_params={"user_timezone": "Asia/Kolkata"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()),1)

    def test_get_classes_with_invalid_timezone(self):
        print("invalid timezone")
        response = client.get("/classes", query_params={"user_timezone": "Invalid/TimeZone"})
        self.assertEqual(response.status_code, 400)


class BookClassAPITest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            name="Test Instructor",
            email="test@example.com"
        )
        self.fitness_class = FitnessClass.objects.create(
            name="HIIT",
            type="hiit",
            datetime=timezone.now() + timedelta(days=1),
            instructor=self.instructor,
            total_slots=5,
            available_slots=5,
        )
        self.payload = {
            "fitness_class_id": self.fitness_class.id,
            "client_name": "Jagan",
            "client_email": "jagan@example.com"
        }

    def test_successful_booking(self):
        response = client.post("/book", json=self.payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["client_email"], "jagan@example.com")

    def test_duplicate_booking(self):
        client.post("/book", json=self.payload)
        response = client.post("/book", json=self.payload)
        self.assertEqual(response.status_code, 400)

    def test_booking_no_slots(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()
        response = client.post("/book", json=self.payload)
        self.assertEqual(response.status_code, 400)

    def test_invalid_class_id(self):
        self.payload["fitness_class_id"] = 9999
        response = client.post("/book", json=self.payload)
        self.assertEqual(response.status_code, 404)


class GetBookingsAPITest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(name="Test", email="test@x.com")
        self.fitness_class = FitnessClass.objects.create(
            name="Zumba",
            type="zumba",
            datetime=timezone.now() + timedelta(days=2),
            instructor=self.instructor,
            total_slots=10,
            available_slots=10,
        )
        self.booking = Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Jagan",
            client_email="jagan@example.com"
        )

    def test_fetch_bookings_success(self):
        response = client.get("/bookings", query_params={"client_email": "jagan@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_fetch_bookings_empty(self):
        response = client.get("/bookings", query_params={"client_email": "unknown@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


