from datetime import date, timedelta
from database import get_db, init_db
from models import Workout, Meal, BodyMeasurement

init_db()

db = get_db()

today = date.today()

print("Clearing existing data...")
db.query(Workout).delete()
db.query(Meal).delete()
db.query(BodyMeasurement).delete()
db.commit()

print("Adding sample workouts...")
sample_workouts = [
    Workout(date=today - timedelta(days=0), exercise_type="HIIT", duration=30, calories_burned=320, notes="Intense session!"),
    Workout(date=today - timedelta(days=1), exercise_type="Running", duration=45, calories_burned=450, notes="5km morning run"),
    Workout(date=today - timedelta(days=2), exercise_type="Weightlifting", duration=60, calories_burned=280, notes="Leg day - squats and deadlifts"),
    Workout(date=today - timedelta(days=3), exercise_type="Yoga", duration=50, calories_burned=150, notes="Relaxing flow"),
    Workout(date=today - timedelta(days=4), exercise_type="Cycling", duration=90, calories_burned=550, notes="Long ride in the park"),
    Workout(date=today - timedelta(days=5), exercise_type="Swimming", duration=40, calories_burned=380, notes="Great pool session"),
    Workout(date=today - timedelta(days=6), exercise_type="CrossFit", duration=45, calories_burned=400, notes="Box jumps and burpees"),
    Workout(date=today - timedelta(days=7), exercise_type="Running", duration=35, calories_burned=350, notes="Easy recovery run"),
    Workout(date=today - timedelta(days=8), exercise_type="Weightlifting", duration=65, calories_burned=300, notes="Upper body focus"),
    Workout(date=today - timedelta(days=10), exercise_type="HIIT", duration=25, calories_burned=280, notes="Quick morning burn"),
    Workout(date=today - timedelta(days=12), exercise_type="Basketball", duration=60, calories_burned=420, notes="Pickup game with friends"),
    Workout(date=today - timedelta(days=14), exercise_type="Pilates", duration=45, calories_burned=180, notes="Core strength"),
    Workout(date=today - timedelta(days=16), exercise_type="Running", duration=50, calories_burned=500, notes="10km personal record!"),
    Workout(date=today - timedelta(days=18), exercise_type="Weightlifting", duration=70, calories_burned=320, notes="Full body workout"),
    Workout(date=today - timedelta(days=20), exercise_type="Cycling", duration=60, calories_burned=450, notes="Spin class"),
    Workout(date=today - timedelta(days=22), exercise_type="Swimming", duration=45, calories_burned=400, notes="Interval training"),
    Workout(date=today - timedelta(days=25), exercise_type="HIIT", duration=30, calories_burned=310, notes="Tabata style"),
    Workout(date=today - timedelta(days=28), exercise_type="Running", duration=40, calories_burned=380, notes="Trail run"),
]

for workout in sample_workouts:
    db.add(workout)

print("Adding sample meals...")
sample_meals = [
    Meal(date=today, meal_type="Breakfast", food_name="Oatmeal with berries", calories=320, protein=12.0, carbs=58.0, fats=6.0),
    Meal(date=today, meal_type="Lunch", food_name="Grilled chicken salad", calories=450, protein=38.0, carbs=35.0, fats=18.0),
    Meal(date=today, meal_type="Snack", food_name="Protein shake", calories=180, protein=25.0, carbs=15.0, fats=3.0),
    Meal(date=today, meal_type="Dinner", food_name="Salmon with vegetables", calories=520, protein=42.0, carbs=28.0, fats=26.0),
    
    Meal(date=today - timedelta(days=1), meal_type="Breakfast", food_name="Greek yogurt with granola", calories=280, protein=18.0, carbs=42.0, fats=8.0),
    Meal(date=today - timedelta(days=1), meal_type="Lunch", food_name="Turkey sandwich", calories=380, protein=28.0, carbs=48.0, fats=12.0),
    Meal(date=today - timedelta(days=1), meal_type="Snack", food_name="Apple with almond butter", calories=220, protein=6.0, carbs=28.0, fats=11.0),
    Meal(date=today - timedelta(days=1), meal_type="Dinner", food_name="Pasta with chicken", calories=620, protein=35.0, carbs=72.0, fats=18.0),
    
    Meal(date=today - timedelta(days=2), meal_type="Breakfast", food_name="Scrambled eggs with toast", calories=340, protein=22.0, carbs=32.0, fats=14.0),
    Meal(date=today - timedelta(days=2), meal_type="Lunch", food_name="Quinoa bowl", calories=480, protein=18.0, carbs=62.0, fats=16.0),
    Meal(date=today - timedelta(days=2), meal_type="Dinner", food_name="Steak with sweet potato", calories=680, protein=48.0, carbs=52.0, fats=28.0),
    
    Meal(date=today - timedelta(days=3), meal_type="Breakfast", food_name="Smoothie bowl", calories=350, protein=15.0, carbs=58.0, fats=9.0),
    Meal(date=today - timedelta(days=3), meal_type="Lunch", food_name="Tuna wrap", calories=420, protein=32.0, carbs=44.0, fats=14.0),
    Meal(date=today - timedelta(days=3), meal_type="Dinner", food_name="Chicken stir fry", calories=540, protein=40.0, carbs=48.0, fats=20.0),
    
    Meal(date=today - timedelta(days=4), meal_type="Breakfast", food_name="Protein pancakes", calories=380, protein=28.0, carbs=48.0, fats=10.0),
    Meal(date=today - timedelta(days=4), meal_type="Lunch", food_name="Caesar salad with shrimp", calories=460, protein=35.0, carbs=22.0, fats=24.0),
    Meal(date=today - timedelta(days=4), meal_type="Dinner", food_name="Beef tacos", calories=580, protein=38.0, carbs=56.0, fats=22.0),
    
    Meal(date=today - timedelta(days=5), meal_type="Breakfast", food_name="Avocado toast", calories=320, protein=12.0, carbs=38.0, fats=16.0),
    Meal(date=today - timedelta(days=5), meal_type="Lunch", food_name="Chicken burrito bowl", calories=620, protein=42.0, carbs=68.0, fats=20.0),
    Meal(date=today - timedelta(days=5), meal_type="Dinner", food_name="Grilled fish with rice", calories=480, protein=38.0, carbs=54.0, fats=12.0),
]

for meal in sample_meals:
    db.add(meal)

print("Adding sample body measurements...")
sample_measurements = [
    BodyMeasurement(date=today, weight=75.2, height=175, bmi=24.55, body_fat_percentage=15.5, notes="Feeling strong"),
    BodyMeasurement(date=today - timedelta(days=7), weight=75.8, height=175, bmi=24.75, body_fat_percentage=16.0, notes="Good progress"),
    BodyMeasurement(date=today - timedelta(days=14), weight=76.5, height=175, bmi=24.98, body_fat_percentage=16.5),
    BodyMeasurement(date=today - timedelta(days=21), weight=77.0, height=175, bmi=25.14, body_fat_percentage=17.0),
    BodyMeasurement(date=today - timedelta(days=28), weight=77.5, height=175, bmi=25.31, body_fat_percentage=17.2, notes="Starting weight"),
]

for measurement in sample_measurements:
    db.add(measurement)

db.commit()
db.close()

print("✅ Sample data successfully added!")
print(f"Added {len(sample_workouts)} workouts")
print(f"Added {len(sample_meals)} meals")
print(f"Added {len(sample_measurements)} body measurements")
