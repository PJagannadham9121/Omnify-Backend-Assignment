# Omnify-Backend-Assignment


Starting the Project(steps) :

Clone this repo:
    - git clone git@github.com:PJagannadham9121/Omnify-Backend-Assignment.git
    - cd Ominify-Backend-Assignment

1.Create Virtual Environment:
    - run python -m venv venv # 'venv' is the virtual environment name

2.Activate Virtual Environment:
    - source venv/bin/activate   # Use 'venv\Scripts\activate' on Windows

3.Install required Modules:
    - pip install -r requirement.txt
 
4.Add Dummy data for classes:
    - python manage.py seed_data

5.Run migrations to create tables in database:
    - python manage.py migrate

6.Run Backend Server
    - python manage.py runserver # Default: http://localhost:8000

7.Run TestCases:
    - python manage.py test fitness


Feature wise implemetation:

1.Dummy Data Generation:
    -Used Faker library for Generating fake classes data.

2.Handling OverBooking Issue(Race Condition + same user booking class multiple times issue):
    - Used transaction.atomic() and selected_for_update() to solve over booking issue.
    - Used unique fitness_class + client_email as contrain to avoid multiple bookings of same class by same user issue.

3.Handling Timezone:
    - Used pytz to convert classes time to respected timezone of a user.

4.Test cases:
    - Implemented Testcases to cover all cases.


Curl for Endpoints:

1.Getting all Classes:
    curl --location 'http://localhost:8000/api/classes'

2.Booking a class:
        curl --location 'http://localhost:8000/api/book' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "fitness_class_id": 4,
    "client_name": "User1",
    "client_email": "user1@gmail.com"

    }'

3.Get all bookings by specific email:
    curl --location 'http://localhost:8000/api/bookings?client_email=user1%40gmail.com'






        


