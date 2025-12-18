import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from sqlalchemy import func
from database import init_db, get_db
from models import Workout, Meal, BodyMeasurement

st.set_page_config(
    page_title="Health & Fitness Tracker",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_db()

col_hero1, col_hero2, col_hero3 = st.columns(3)
with col_hero1:
    st.image("attached_assets/stock_images/fitness_gym_workout__79603433.jpg", use_container_width=True)
with col_hero2:
    st.image("attached_assets/stock_images/fitness_gym_workout__a2b68091.jpg", use_container_width=True)
with col_hero3:
    st.image("attached_assets/stock_images/fitness_gym_workout__6292474c.jpg", use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #FF4B4B; font-size: 3.5rem;'>💪 FITNESS TRACKER PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #FAFAFA; margin-bottom: 2rem;'>Transform Your Body, Track Your Progress, Achieve Your Goals</p>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", 
    "🏋️ Log Workout", 
    "🍎 Log Meal", 
    "📏 Body Measurements",
    "📈 Activity History"
])

def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (cm)"""
    if height > 0:
        height_m = height / 100
        return round(weight / (height_m ** 2), 2)
    return None

with tab1:
    st.header("Your Health Dashboard")
    
    db = get_db()
    
    col1, col2, col3, col4 = st.columns(4)
    
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    total_workouts = db.query(Workout).count()
    workouts_this_week = db.query(Workout).filter(Workout.date >= week_ago).count()
    
    total_calories_burned = db.query(func.sum(Workout.calories_burned)).scalar() or 0
    calories_this_week = db.query(func.sum(Workout.calories_burned)).filter(
        Workout.date >= week_ago
    ).scalar() or 0
    
    latest_weight = db.query(BodyMeasurement).order_by(
        BodyMeasurement.date.desc()
    ).first()
    
    calories_consumed_today = db.query(func.sum(Meal.calories)).filter(
        Meal.date == today
    ).scalar() or 0
    
    with col1:
        st.metric("Total Workouts", total_workouts, f"+{workouts_this_week} this week")
    
    with col2:
        st.metric("Calories Burned", f"{total_calories_burned:,}", f"+{calories_this_week} this week")
    
    with col3:
        if latest_weight:
            st.metric("Current Weight", f"{latest_weight.weight} kg", 
                     f"BMI: {latest_weight.bmi or 'N/A'}")
        else:
            st.metric("Current Weight", "No data", "")
    
    with col4:
        st.metric("Calories Today", f"{calories_consumed_today}", "consumed")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Workout Activity (Last 30 Days)")
        
        thirty_days_ago = today - timedelta(days=30)
        workouts_30d = db.query(Workout).filter(
            Workout.date >= thirty_days_ago
        ).order_by(Workout.date).all()
        
        if workouts_30d:
            workout_df = pd.DataFrame([{
                'Date': w.date,
                'Exercise': w.exercise_type,
                'Duration': w.duration,
                'Calories': w.calories_burned
            } for w in workouts_30d])
            
            workout_summary = workout_df.groupby('Date').agg({
                'Duration': 'sum',
                'Calories': 'sum'
            }).reset_index()
            
            fig = px.bar(workout_summary, x='Date', y='Calories',
                        title='Calories Burned per Day',
                        labels={'Calories': 'Calories Burned'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No workout data available. Start logging your workouts!")
    
    with col_chart2:
        st.subheader("Weight Trend")
        
        measurements = db.query(BodyMeasurement).order_by(
            BodyMeasurement.date
        ).all()
        
        if measurements:
            meas_df = pd.DataFrame([{
                'Date': m.date,
                'Weight': m.weight,
                'BMI': m.bmi
            } for m in measurements])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=meas_df['Date'], 
                y=meas_df['Weight'],
                mode='lines+markers',
                name='Weight (kg)',
                line=dict(color='#1f77b4', width=2)
            ))
            fig.update_layout(
                title='Weight Over Time',
                xaxis_title='Date',
                yaxis_title='Weight (kg)',
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No body measurement data available. Start tracking your measurements!")
    
    st.markdown("---")
    st.subheader("Daily Calorie Balance")
    
    calories_burned_today = db.query(func.sum(Workout.calories_burned)).filter(
        Workout.date == today
    ).scalar() or 0
    
    net_calories = calories_consumed_today - calories_burned_today
    
    col_cal1, col_cal2, col_cal3 = st.columns(3)
    with col_cal1:
        st.metric("Consumed", f"{calories_consumed_today} cal")
    with col_cal2:
        st.metric("Burned", f"{calories_burned_today} cal")
    with col_cal3:
        st.metric("Net", f"{net_calories} cal", 
                 "Surplus" if net_calories > 0 else "Deficit")
    
    db.close()

with tab2:
    st.header("🏋️ Log Your Workout")
    
    with st.form("workout_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            workout_date = st.date_input("Date", value=date.today())
            exercise_type = st.selectbox(
                "Exercise Type",
                ["Running", "Cycling", "Swimming", "Weightlifting", 
                 "Yoga", "Pilates", "Walking", "HIIT", "CrossFit", 
                 "Basketball", "Soccer", "Tennis", "Other"]
            )
        
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, value=30)
            calories_burned = st.number_input("Calories Burned", min_value=0, value=200)
        
        notes = st.text_area("Notes (optional)", placeholder="How did you feel? Any PRs?")
        
        submitted = st.form_submit_button("Log Workout", type="primary")
        
        if submitted:
            db = get_db()
            new_workout = Workout(
                date=workout_date,
                exercise_type=exercise_type,
                duration=duration,
                calories_burned=calories_burned,
                notes=notes if notes else None
            )
            db.add(new_workout)
            db.commit()
            db.close()
            st.success(f"✅ Logged {exercise_type} workout for {duration} minutes!")
            st.rerun()
    
    st.markdown("---")
    st.subheader("Recent Workouts")
    
    db = get_db()
    recent_workouts = db.query(Workout).order_by(
        Workout.date.desc()
    ).limit(5).all()
    
    if recent_workouts:
        for workout in recent_workouts:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    st.write(f"**{workout.date}**")
                with col2:
                    st.write(f"🏃 {workout.exercise_type}")
                with col3:
                    st.write(f"⏱️ {workout.duration} min | 🔥 {workout.calories_burned} cal")
                with col4:
                    if st.button("🗑️", key=f"del_workout_{workout.id}"):
                        db.delete(workout)
                        db.commit()
                        db.close()
                        st.rerun()
                if workout.notes:
                    st.caption(f"📝 {workout.notes}")
                st.markdown("---")
    else:
        st.info("No workouts logged yet. Start logging your first workout above!")
    
    db.close()

with tab3:
    st.header("🍎 Log Your Meals")
    
    with st.form("meal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            meal_date = st.date_input("Date", value=date.today(), key="meal_date")
            meal_type = st.selectbox(
                "Meal Type",
                ["Breakfast", "Lunch", "Dinner", "Snack"]
            )
            food_name = st.text_input("Food/Meal Name", placeholder="e.g., Grilled Chicken Salad")
        
        with col2:
            calories = st.number_input("Calories", min_value=0, value=300)
            protein = st.number_input("Protein (g)", min_value=0.0, value=0.0, step=0.1)
            carbs = st.number_input("Carbs (g)", min_value=0.0, value=0.0, step=0.1)
            fats = st.number_input("Fats (g)", min_value=0.0, value=0.0, step=0.1)
        
        submitted_meal = st.form_submit_button("Log Meal", type="primary")
        
        if submitted_meal:
            if food_name:
                db = get_db()
                new_meal = Meal(
                    date=meal_date,
                    meal_type=meal_type,
                    food_name=food_name,
                    calories=calories,
                    protein=protein if protein > 0 else None,
                    carbs=carbs if carbs > 0 else None,
                    fats=fats if fats > 0 else None
                )
                db.add(new_meal)
                db.commit()
                db.close()
                st.success(f"✅ Logged {food_name} ({calories} cal)")
                st.rerun()
            else:
                st.error("Please enter a food/meal name")
    
    st.markdown("---")
    st.subheader("Today's Meals")
    
    db = get_db()
    today_meals = db.query(Meal).filter(
        Meal.date == date.today()
    ).order_by(Meal.created_at).all()
    
    if today_meals:
        total_cal = sum(m.calories for m in today_meals)
        total_protein = sum(m.protein or 0 for m in today_meals)
        total_carbs = sum(m.carbs or 0 for m in today_meals)
        total_fats = sum(m.fats or 0 for m in today_meals)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Calories", f"{total_cal}")
        with col2:
            st.metric("Protein", f"{total_protein:.1f}g")
        with col3:
            st.metric("Carbs", f"{total_carbs:.1f}g")
        with col4:
            st.metric("Fats", f"{total_fats:.1f}g")
        
        st.markdown("---")
        
        for meal in today_meals:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 3, 3, 1])
                with col1:
                    st.write(f"**{meal.meal_type}**")
                with col2:
                    st.write(f"🍽️ {meal.food_name}")
                with col3:
                    macros = f"🔥 {meal.calories} cal"
                    if meal.protein or meal.carbs or meal.fats:
                        macros += f" | P:{meal.protein or 0}g C:{meal.carbs or 0}g F:{meal.fats or 0}g"
                    st.write(macros)
                with col4:
                    if st.button("🗑️", key=f"del_meal_{meal.id}"):
                        db.delete(meal)
                        db.commit()
                        db.close()
                        st.rerun()
                st.markdown("---")
    else:
        st.info("No meals logged today. Start tracking your nutrition!")
    
    db.close()

with tab4:
    st.header("📏 Track Body Measurements")
    
    with st.form("measurement_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            meas_date = st.date_input("Date", value=date.today(), key="meas_date")
            weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0, step=0.1)
            height = st.number_input("Height (cm)", min_value=0.0, value=170.0, step=0.1)
        
        with col2:
            body_fat = st.number_input("Body Fat % (optional)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
            notes_meas = st.text_area("Notes (optional)", key="meas_notes")
        
        submitted_meas = st.form_submit_button("Save Measurement", type="primary")
        
        if submitted_meas:
            bmi = calculate_bmi(weight, height)
            
            db = get_db()
            
            existing = db.query(BodyMeasurement).filter(
                BodyMeasurement.date == meas_date
            ).first()
            
            if existing:
                existing.weight = weight
                existing.height = height
                existing.bmi = bmi
                existing.body_fat_percentage = body_fat if body_fat > 0 else None
                existing.notes = notes_meas if notes_meas else None
                message = "✅ Updated measurement"
            else:
                new_measurement = BodyMeasurement(
                    date=meas_date,
                    weight=weight,
                    height=height,
                    bmi=bmi,
                    body_fat_percentage=body_fat if body_fat > 0 else None,
                    notes=notes_meas if notes_meas else None
                )
                db.add(new_measurement)
                message = f"✅ Saved measurement - BMI: {bmi}"
            
            db.commit()
            db.close()
            st.success(message)
            st.rerun()
    
    st.markdown("---")
    st.subheader("Measurement History")
    
    db = get_db()
    measurements = db.query(BodyMeasurement).order_by(
        BodyMeasurement.date.desc()
    ).limit(10).all()
    
    if measurements:
        meas_data = []
        for m in measurements:
            meas_data.append({
                'Date': m.date.strftime('%Y-%m-%d'),
                'Weight (kg)': m.weight,
                'Height (cm)': m.height or 'N/A',
                'BMI': m.bmi or 'N/A',
                'Body Fat %': m.body_fat_percentage or 'N/A'
            })
        
        df = pd.DataFrame(meas_data)
        st.dataframe(df, use_container_width=True)
        
        if len(measurements) >= 2:
            weight_change = measurements[0].weight - measurements[-1].weight
            if weight_change > 0:
                st.info(f"📉 You've lost {abs(weight_change):.1f} kg since {measurements[-1].date}")
            elif weight_change < 0:
                st.info(f"📈 You've gained {abs(weight_change):.1f} kg since {measurements[-1].date}")
            else:
                st.info("➡️ Your weight has remained stable")
    else:
        st.info("No measurements recorded yet. Add your first measurement above!")
    
    db.close()

with tab5:
    st.header("📈 Activity History & Analytics")
    
    db = get_db()
    
    date_range = st.date_input(
        "Select Date Range",
        value=(date.today() - timedelta(days=30), date.today()),
        key="history_date_range"
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        
        st.subheader("Workout Summary")
        
        workouts = db.query(Workout).filter(
            Workout.date >= start_date,
            Workout.date <= end_date
        ).order_by(Workout.date.desc()).all()
        
        if workouts:
            workout_df = pd.DataFrame([{
                'Date': w.date,
                'Exercise': w.exercise_type,
                'Duration (min)': w.duration,
                'Calories Burned': w.calories_burned,
                'Notes': w.notes or ''
            } for w in workouts])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Workouts", len(workouts))
            with col2:
                st.metric("Total Duration", f"{workout_df['Duration (min)'].sum()} min")
            with col3:
                st.metric("Total Calories", f"{workout_df['Calories Burned'].sum():,}")
            
            st.dataframe(workout_df, use_container_width=True)
            
            st.subheader("Exercise Type Breakdown")
            exercise_summary = workout_df.groupby('Exercise').agg({
                'Duration (min)': 'sum',
                'Calories Burned': 'sum'
            }).reset_index()
            
            fig = px.pie(exercise_summary, values='Duration (min)', names='Exercise',
                        title='Workout Duration by Exercise Type')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No workouts found in this date range.")
        
        st.markdown("---")
        st.subheader("Nutrition Summary")
        
        meals = db.query(Meal).filter(
            Meal.date >= start_date,
            Meal.date <= end_date
        ).order_by(Meal.date.desc()).all()
        
        if meals:
            meal_df = pd.DataFrame([{
                'Date': m.date,
                'Meal Type': m.meal_type,
                'Food': m.food_name,
                'Calories': m.calories,
                'Protein (g)': m.protein or 0,
                'Carbs (g)': m.carbs or 0,
                'Fats (g)': m.fats or 0
            } for m in meals])
            
            daily_cal = meal_df.groupby('Date')['Calories'].sum().reset_index()
            
            fig = px.line(daily_cal, x='Date', y='Calories',
                         title='Daily Calorie Intake',
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            avg_calories = meal_df['Calories'].sum() / len(daily_cal)
            st.metric("Average Daily Calories", f"{avg_calories:.0f}")
            
            st.dataframe(meal_df, use_container_width=True)
        else:
            st.info("No meals found in this date range.")
    
    db.close()

st.markdown("---")
st.caption("💪 Health & Fitness Tracker - Track your journey to a healthier you!")
