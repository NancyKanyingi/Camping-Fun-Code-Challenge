# Server/seed.py
from Server.extensions import db
from Server.models import Camper, Activity, Signup
from faker import Faker
import random
from Server.app import create_app

fake = Faker()

app = create_app()

with app.app_context():
    print("Clearing existing data...")
    db.session.query(Signup).delete()
    db.session.query(Activity).delete()
    db.session.query(Camper).delete()

    print("Seeding campers...")
    campers = []
    for _ in range(10):
        camper = Camper(
            name=fake.first_name(),
            age=random.randint(8, 18)
        )
        db.session.add(camper)
        campers.append(camper)

    print("Seeding activities...")
    activities = []
    activity_names = [
        "Archery", "Swimming", "Hiking by the Stream",
        "Canoeing", "Fishing", "Arts & Crafts",
        "Rock Climbing", "Campfire Songs", "Nature Walks"
    ]
    for name in activity_names:
        activity = Activity(
            name=name,
            difficulty=random.randint(1, 5)
        )
        db.session.add(activity)
        activities.append(activity)

    db.session.commit()

    print("Seeding signups...")
    for _ in range(20):
        signup = Signup(
            camper_id=random.choice(campers).id,
            activity_id=random.choice(activities).id,
            time=random.randint(0, 23)
        )
        db.session.add(signup)

    db.session.commit()
    print(" Done seeding!")
