from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime
from database import Base

class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    exercise_type = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    calories_burned = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Workout(exercise_type='{self.exercise_type}', date='{self.date}')>"

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    meal_type = Column(String, nullable=False)  # breakfast, lunch, dinner, snack
    food_name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    protein = Column(Float, nullable=True)  # in grams
    carbs = Column(Float, nullable=True)  # in grams
    fats = Column(Float, nullable=True)  # in grams
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Meal(food_name='{self.food_name}', date='{self.date}')>"

class BodyMeasurement(Base):
    __tablename__ = "body_measurements"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True)
    weight = Column(Float, nullable=False)  # in kg
    height = Column(Float, nullable=True)  # in cm
    bmi = Column(Float, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<BodyMeasurement(date='{self.date}', weight={self.weight})>"
