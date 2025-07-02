from django.core.management.base import BaseCommand
from fitness.models import Instructor, FitnessClass
from django.utils import timezone
from datetime import timedelta
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with fake instructors and fitness classes'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear old data
        FitnessClass.objects.all().delete()
        Instructor.objects.all().delete()

        CLASS_TYPES = ["yoga", "zumba", "hiit"]

        # Create 3 instructors
        instructors = []
        for _ in range(3):
            instructor = Instructor.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                bio=fake.sentence(),
                specialization=random.choice(CLASS_TYPES)
            )
            instructors.append(instructor)

        now = timezone.now()

        # Create 5 classes
        for i in range(5):
            cls_type = random.choice(CLASS_TYPES)
            instructor = random.choice(instructors)
            start_time = now + timedelta(days=i+1, hours=random.randint(6, 18))

            FitnessClass.objects.create(
                name=f"{cls_type.capitalize()} Class {i+1}",
                type=cls_type,
                datetime=start_time,
                total_slots=20,
                available_slots=20,
                instructor=instructor
            )

        self.stdout.write(self.style.SUCCESS("✅ Fake seed data loaded successfully!"))