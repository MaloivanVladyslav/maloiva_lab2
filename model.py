import time
import random
import datetime
from functools import wraps
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, DateTime, ForeignKey, func, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(20))
    date_registration = Column(DateTime(timezone=True))

    workouts = relationship("UserWorkout", back_populates="user")


class Workout(Base):
    __tablename__ = 'workout'
    workout_id = Column(Integer, primary_key=True)
    type_workout = Column(String(50))

    user_links = relationship("UserWorkout", back_populates="workout")


class UserWorkout(Base):
    __tablename__ = 'user_workout'
    user_workout_id = Column(Integer, primary_key=True)
    user_user_id = Column(Integer, ForeignKey('user.user_id'))
    workout_workout_id = Column(Integer, ForeignKey('workout.workout_id'))
    date = Column(Date)
    time = Column(Time(timezone=True))

    user = relationship("User", back_populates="workouts")
    workout = relationship("Workout", back_populates="user_links")
    health_metric = relationship("HealthMetric", uselist=False, back_populates="user_workout")


class HealthMetric(Base):
    __tablename__ = 'health metrics'
    metrics_id = Column(Integer, primary_key=True)
    user_workout_id = Column(Integer, ForeignKey('user_workout.user_workout_id'))
    steps = Column(Integer)
    pulse = Column(Integer)
    calories = Column(Integer)
    measurement_date = Column(DateTime(timezone=True))

    user_workout = relationship("UserWorkout", back_populates="health_metric")


class Friendship(Base):
    __tablename__ = 'friendship'
    id_composite = Column("user_id1,user_id2", Integer, primary_key=True)
    user_id1 = Column(Integer, ForeignKey('user.user_id'))
    user_id2 = Column(Integer, ForeignKey('user.user_id'))
    status = Column(String(20))
    date = Column(Date)


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        # print(f"\n[INFO] Function '{func.__name__}' executed in {elapsed_time:.4f} milliseconds\n")
        return result

    return wrapper


class Model:
    def __init__(self):
        try:
            self.engine = create_engine("postgresql://postgres:1234@localhost:4321/postgres")
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            print("Database connection successful (SQLAlchemy).")
        except Exception as e:
            print(f"FATAL: Database connection error: {e}")
            self.session = None

    def close_connection(self):
        if self.session:
            self.session.close()

    def _to_tuples(self, query_result):
        return query_result


    def get_all_users(self):
        try:
            result = self.session.query(
                User.user_id, User.first_name, User.last_name,
                User.email, User.phone, User.date_registration
            ).order_by(User.user_id).all()
            return result
        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return []

    def get_all_workouts(self):
        try:
            result = self.session.query(
                Workout.workout_id, Workout.type_workout
            ).order_by(Workout.workout_id).all()
            return result
        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return []

    def get_all_user_workouts(self):
        try:
            result = self.session.query(
                UserWorkout.user_workout_id, UserWorkout.user_user_id,
                UserWorkout.workout_workout_id, UserWorkout.date, UserWorkout.time
            ).order_by(UserWorkout.user_workout_id).all()
            return result
        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return []

    def get_all_health_metrics(self):
        try:
            result = self.session.query(
                HealthMetric.metrics_id, HealthMetric.user_workout_id,
                HealthMetric.steps, HealthMetric.pulse,
                HealthMetric.calories, HealthMetric.measurement_date
            ).order_by(HealthMetric.metrics_id).all()
            return result
        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return []

    def get_all_friendships(self):
        try:
            result = self.session.query(
                Friendship.id_composite, Friendship.user_id1,
                Friendship.user_id2, Friendship.status, Friendship.date
            ).order_by(Friendship.date).all()
            return result
        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return []

    @timeit
    def get_data_in_range(self, request):
        try:
            commands = request.split(' ')
            table_name = commands[0]
            field_name = commands[1]
            start_val = commands[2]
            end_val = commands[3]
            order_field = commands[4]

            model_map = {
                'user': User,
                'workout': Workout,
                'user_workout': UserWorkout,
                'health': HealthMetric,
                '"health metrics"': HealthMetric,
                'friendship': Friendship
            }

            ModelClass = model_map.get(table_name)
            if not ModelClass:
                print("Unknown table")
                return []

            field_attr = getattr(ModelClass, field_name)
            order_attr = getattr(ModelClass, order_field)

            query = self.session.query(ModelClass).filter(
                field_attr.between(start_val, end_val)
            ).order_by(order_attr)

            objs = query.all()
            print(f"\n{len(objs)} rows found.\n")

            result = []
            for obj in objs:
                row = [getattr(obj, col.name) for col in obj.__table__.columns]
                result.append(tuple(row))
            return result

        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return []

    @timeit
    def get_data_by_field_like(self, request):
        try:
            commands = request.split(' ')
            table_name = commands[0]
            req_field = commands[1]
            search_req = commands[2]
            order_field = commands[3]

            model_map = {
                'user': User, 'workout': Workout, 'user_workout': UserWorkout,
                'health': HealthMetric, 'friendship': Friendship
            }
            ModelClass = model_map.get(table_name)
            if not ModelClass: return []

            field_attr = getattr(ModelClass, req_field)
            order_attr = getattr(ModelClass, order_field)

            objs = self.session.query(ModelClass).filter(
                field_attr.like(f'%{search_req}%')
            ).order_by(order_attr).all()

            print(f"\n{len(objs)} rows found.\n")

            result = []
            for obj in objs:
                row = [getattr(obj, col.name) for col in obj.__table__.columns]
                result.append(tuple(row))
            return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @timeit
    def search_workouts_by_username(self, name_pattern):
        try:
            query = self.session.query(
                User.first_name, User.last_name, Workout.type_workout, UserWorkout.date, UserWorkout.time
            ).join(UserWorkout, User.user_id == UserWorkout.user_user_id) \
                .join(Workout, UserWorkout.workout_workout_id == Workout.workout_id) \
                .filter(User.first_name.like(f'%{name_pattern}%')) \
                .order_by(User.last_name, UserWorkout.date)

            result = query.all()
            print(f"\n{len(result)} rows found.\n")
            return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @timeit
    def search_users_by_pulse(self, min_pulse):
        try:
            query = self.session.query(
                User.user_id, User.first_name, User.last_name, HealthMetric.pulse
            ).select_from(User) \
                .join(UserWorkout, User.user_id == UserWorkout.user_user_id) \
                .join(HealthMetric, UserWorkout.user_workout_id == HealthMetric.user_workout_id) \
                .filter(HealthMetric.pulse > min_pulse) \
                .distinct() \
                .order_by(HealthMetric.pulse.desc())

            result = query.all()
            print(f"\n{len(result)} users found.\n")
            return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @timeit
    def get_workout_counts_by_user(self):
        try:
            query = self.session.query(
                User.user_id, User.first_name, User.last_name,
                func.count(UserWorkout.user_workout_id).label('workout_count')
            ).outerjoin(UserWorkout, User.user_id == UserWorkout.user_user_id) \
                .group_by(User.user_id, User.first_name, User.last_name) \
                .order_by(text('workout_count DESC'))  # text допомагає сортувати за аліасом

            result = query.all()
            print(f"\n{len(result)} users found.\n")
            return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    def add_user(self, first_name, last_name, email, phone, date_registration):
        try:
            max_id = self.session.query(func.max(User.user_id)).scalar() or 0
            new_id = max_id + 1

            new_obj = User(
                user_id=new_id, first_name=first_name, last_name=last_name,
                email=email, phone=phone, date_registration=date_registration
            )
            self.session.add(new_obj)
            self.session.commit()
            print(f"\n1 user added successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def add_workout(self, type_workout):
        try:
            max_id = self.session.query(func.max(Workout.workout_id)).scalar() or 0
            new_obj = Workout(workout_id=max_id + 1, type_workout=type_workout)
            self.session.add(new_obj)
            self.session.commit()
            print(f"\n1 workout added successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def add_user_workout(self, user_id, workout_id, date, time_val):
        try:
            max_id = self.session.query(func.max(UserWorkout.user_workout_id)).scalar() or 0
            new_obj = UserWorkout(
                user_workout_id=max_id + 1, user_user_id=user_id,
                workout_workout_id=workout_id, date=date, time=time_val
            )
            self.session.add(new_obj)
            self.session.commit()
            print(f"\n1 user_workout added successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def add_health_metric(self, user_workout_id, steps, pulse, calories, measurement_date):
        try:
            max_id = self.session.query(func.max(HealthMetric.metrics_id)).scalar() or 0
            new_obj = HealthMetric(
                metrics_id=max_id + 1, user_workout_id=user_workout_id,
                steps=steps, pulse=pulse, calories=calories, measurement_date=measurement_date
            )
            self.session.add(new_obj)
            self.session.commit()
            print(f"\n1 health_metric added successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def add_friendship(self, user_id1, user_id2, status, date):
        try:
            max_id = self.session.query(func.max(Friendship.id_composite)).scalar() or 0
            new_obj = Friendship(
                id_composite=max_id + 1, user_id1=user_id1, user_id2=user_id2,
                status=status, date=date
            )
            self.session.add(new_obj)
            self.session.commit()
            print(f"\n1 friendship added successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def update_user(self, user_id, first_name, last_name, email, phone):
        try:
            q = self.session.query(User).filter(User.user_id == user_id)
            if q.first():
                q.update({
                    User.first_name: first_name, User.last_name: last_name,
                    User.email: email, User.phone: phone
                })
                self.session.commit()
                print(f"\n1 row updated.\n")
            else:
                print("User not found")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def update_workout(self, workout_id, type_workout):
        try:
            q = self.session.query(Workout).filter(Workout.workout_id == workout_id)
            if q.first():
                q.update({Workout.type_workout: type_workout})
                self.session.commit()
                print(f"\n1 row updated.\n")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def update_user_workout(self, user_workout_id, user_id, workout_id, date, time_val):
        try:
            q = self.session.query(UserWorkout).filter(UserWorkout.user_workout_id == user_workout_id)
            if q.first():
                q.update({
                    UserWorkout.user_user_id: user_id, UserWorkout.workout_workout_id: workout_id,
                    UserWorkout.date: date, UserWorkout.time: time_val
                })
                self.session.commit()
                print(f"\n1 row updated.\n")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def update_health_metric(self, metrics_id, steps, pulse, calories, measurement_date):
        try:
            q = self.session.query(HealthMetric).filter(HealthMetric.metrics_id == metrics_id)
            if q.first():
                q.update({
                    HealthMetric.steps: steps, HealthMetric.pulse: pulse,
                    HealthMetric.calories: calories, HealthMetric.measurement_date: measurement_date
                })
                self.session.commit()
                print(f"\n1 row updated.\n")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def update_friendship(self, user_id1_key, user_id2_key, new_status):
        try:
            q = self.session.query(Friendship).filter(
                Friendship.user_id1 == user_id1_key,
                Friendship.user_id2 == user_id2_key
            )
            if q.first():
                q.update({Friendship.status: new_status})
                self.session.commit()
                print(f"\n1 row updated.\n")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def delete_data(self, table_name, field, value):
        try:
            model_map = {
                'user': User, 'workout': Workout, 'user_workout': UserWorkout,
                'health': HealthMetric, '"health metrics"': HealthMetric,
                'friendship': Friendship
            }
            ModelClass = model_map.get(table_name)
            if not ModelClass:
                print("Unknown table")
                return

            field_attr = getattr(ModelClass, field)

            rows_deleted = self.session.query(ModelClass).filter(field_attr == value).delete()
            self.session.commit()
            print(f"\n{rows_deleted} rows deleted successfully! ")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    @timeit
    def generate_users(self, num_users):
        try:
            max_id = self.session.query(func.max(User.user_id)).scalar() or 0
            new_users = []

            for i in range(1, int(num_users) + 1):
                uid = max_id + i
                u = User(
                    user_id=uid,
                    first_name=f'Name_{uid}',
                    last_name=f'Surname_{uid}',
                    email=f'user{uid}@gen.com',
                    phone=str(random.randint(100000000, 999999999)),
                    date_registration=datetime.date.today() - datetime.timedelta(days=random.randint(0, 365))
                )
                new_users.append(u)

            self.session.add_all(new_users)
            self.session.commit()
            print(f"\n{num_users} users generated successfully.\n")
        except Exception as e:
            self.session.rollback()
            print(f"Generation error: {e}")

    @timeit
    def generate_workouts(self, num_workouts):
        try:
            max_id = self.session.query(func.max(Workout.workout_id)).scalar() or 0
            types = ['Running', 'Weightlifting', 'Yoga', 'Cycling']
            new_data = []

            for i in range(1, int(num_workouts) + 1):
                new_data.append(Workout(
                    workout_id=max_id + i,
                    type_workout=random.choice(types)
                ))

            self.session.add_all(new_data)
            self.session.commit()
            print(f"\n{num_workouts} workouts generated successfully.\n")
        except Exception as e:
            self.session.rollback()
            print(f"Generation error: {e}")

    @timeit
    def generate_user_workouts(self, num_records):
        try:
            u_ids = [r[0] for r in self.session.query(User.user_id).all()]
            w_ids = [r[0] for r in self.session.query(Workout.workout_id).all()]

            if not u_ids or not w_ids:
                print("Need users and workouts first.")
                return

            max_id = self.session.query(func.max(UserWorkout.user_workout_id)).scalar() or 0
            new_data = []

            for i in range(1, int(num_records) + 1):
                new_data.append(UserWorkout(
                    user_workout_id=max_id + i,
                    user_user_id=random.choice(u_ids),
                    workout_workout_id=random.choice(w_ids),
                    date=datetime.date.today() - datetime.timedelta(days=random.randint(0, 30)),
                    time=datetime.time(random.randint(0, 23), random.randint(0, 59))
                ))

            self.session.add_all(new_data)
            self.session.commit()
            print(f"\n{num_records} user_workouts generated successfully.\n")
        except Exception as e:
            self.session.rollback()
            print(f"Generation error: {e}")

    @timeit
    def generate_health_metrics(self, num_records):
        try:
            uw_ids = [r[0] for r in self.session.query(UserWorkout.user_workout_id).limit(int(num_records)).all()]

            max_id = self.session.query(func.max(HealthMetric.metrics_id)).scalar() or 0
            new_data = []

            for i, uw_id in enumerate(uw_ids):
                new_data.append(HealthMetric(
                    metrics_id=max_id + i + 1,
                    user_workout_id=uw_id,
                    steps=random.randint(1000, 20000),
                    pulse=random.randint(60, 180),
                    calories=random.randint(100, 1000),
                    measurement_date=datetime.date.today()
                ))

            self.session.add_all(new_data)
            self.session.commit()
            print(f"\nMetrics generated (attempted).\n")
        except Exception as e:
            self.session.rollback()
            print(f"Generation error: {e}")

    @timeit
    def generate_friendships(self, num_records):
        try:
            u_ids = [r[0] for r in self.session.query(User.user_id).all()]
            if len(u_ids) < 2: return

            max_id = self.session.query(func.max(Friendship.id_composite)).scalar() or 0
            new_data = []

            for i in range(1, int(num_records) + 1):
                u1 = random.choice(u_ids)
                u2 = random.choice(u_ids)
                if u1 == u2: continue

                new_data.append(Friendship(
                    id_composite=max_id + i,
                    user_id1=u1,
                    user_id2=u2,
                    status=random.choice(['pending', 'accepted', 'blocked']),
                    date=datetime.date.today()
                ))

            self.session.add_all(new_data)
            self.session.commit()
            print(f"\nFriendships generated.\n")
        except Exception as e:
            self.session.rollback()
            print(f"Generation error: {e}")