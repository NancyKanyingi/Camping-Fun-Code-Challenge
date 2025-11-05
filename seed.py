from app import app, db
from models import Camper, Activity, Signup




def seed():
with app.app_context():
db.create_all()


# Clear existing
Signup.query.delete()
Camper.query.delete()
Activity.query.delete()
db.session.commit()


c1 = Camper(name='Caitlin', age=8)
c2 = Camper(name='Lizzie', age=9)


a1 = Activity(name='Archery', difficulty=2)
a2 = Activity(name='Swimming', difficulty=3)


db.session.add_all([c1, c2, a1, a2])
db.session.commit()


s1 = Signup(camper_id=c1.id, activity_id=a1.id, time=9)
s2 = Signup(camper_id=c2.id, activity_id=a2.id, time=10)


db.session.add_all([s1, s2])
db.session.commit()
print('Seeded DB with sample campers, activities, and signups')




if __name__ == '__main__':
seed()