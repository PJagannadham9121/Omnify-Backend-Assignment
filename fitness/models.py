from django.db import models
from django.utils import timezone


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class FitnessClass(models.Model):
    CLASS_TYPES = [
        ("yoga", "Yoga"),
        ("zumba", "Zumba"),
        ("hiit", "HIIT"),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CLASS_TYPES)
    datetime = models.DateTimeField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('fitness_class', 'client_email')

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"


