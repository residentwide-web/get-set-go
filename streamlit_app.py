import streamlit as st
import pandas as pd
import os

# ---------------- Fueling Requirements Function ----------------
def fueling_requirements(sport_intensity: str, weight_kg: float, duration_hr: float):
    sport_carbs = {"light": (3, 5), "moderate": (5, 7), "endurance": (6, 10), "extreme": (8, 12)}
    carb_min, carb_max = sport_carbs.get(sport_intensity.lower(), (5, 7))
    carbs_min = weight_kg * carb_min
    carbs_max = weight_kg * carb_max

    if sport_intensity.lower() in ["endurance", "extreme"]:
        protein_min, protein_max = (1.4, 1.8)
    elif sport_intensity.lower() == "light":
        protein_min, protein_max = (1.2, 1.6)
    else:
        protein_min, protein_max = (1.6, 2.2)
    protein_min_g = weight_kg * protein_min
    protein_max_g = weight_kg * protein_max

    fat_min_g = weight_kg * 0.8
    fat_max_g = weight_kg * 1.0

    fluid_loss_ml = 600 * duration_hr
    fluid_replacement_ml = fluid_loss_ml * 1.5
    sodium_mg = 500 * duration_hr

    return {
        "carbs_g_range": (round(carbs_min), round(carbs_max)),
        "protein_g_range": (round(protein_min_g), round(protein_max_g)),
        "fat_g_range": (round(fat_min_g), round(fat_max_g)),
        "fluid_loss_ml": round(fluid_loss_ml),
        "fluid_replacement_ml": round(fluid_replacement_ml),
        "sodium_mg": round(sodium_mg)
    }

# ---------------- Example Food Database ----------------
example_foods = {
    "carbs": [("Oats (50g)", 30), ("Banana", 27), ("Rice (100g cooked)", 28)],
    "protein": [("Whey Protein Scoop", 20), ("Chicken Breast 100g", 31), ("Egg (1 large)", 6)],
    "fat": [("Almonds 30g", 15), ("Olive Oil 1 tbsp", 14), ("Avocado 100g", 15)]
}

# ---------------- Streamlit App ----------------
st.set_page_config(page_title="Fueling Tracker", layout="centered")

st.title("🏋️ Get Set, GO!!!")
st.write("Performance Driven Personalized Fuelling Requirements and Macro Tracker.")

st.markdown("---")

# --- User Inputs ---
st.subheader("Workout Details")

sport_type = st.selectbox("Select your sport:", ["Running", "Cycling", "Swimming", "Gym / Strength Training"])
sport_intensity = st.selectbox("Select intensity:", ["Light", "Moderate", "Endurance", "Extreme"])
weight = st.number_input("Weight (kg):", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
duration = st.number_input("Duration (hours):", min_value=0.5, max_value=8.0, value=2.0, step=0.5)

st.markdown("---")
st.subheader("Current Macro Intake")
carbs_intake = st.number_input("Carbs consumed (g):", min_value=0.0, value=0.0, step=5.0)
protein_intake = st.number_input("Protein consumed (g):", min_value=0.0, value=0.0, step=5.0)
fat_intake = st.number_input("Fat consumed (g):", min_value=0.0, value=0.0, step=5.0)

st.markdown("---")
if st.button("Calculate"):
    results = fueling_requirements(sport_intensity, weight, duration)
    
    # --- Collapsible Section: Requirements ---
    with st.expander("🔑 Daily Requirements", expanded=True):
        st.write(f"**Sport:** {sport_type}")
        st.write(f"**Carbs:** {results['carbs_g_range'][0]} – {results['carbs_g_range'][1]} g/day")
        st.write(f"**Protein:** {results['protein_g_range'][0]} – {results['protein_g_range'][1]} g/day")
        st.write(f"**Fat:** {results['fat_g_range'][0]} – {results['fat_g_range'][1]} g/day")
        st.write(f"**Fluid Loss:** ~{results['fluid_loss_ml']} ml")
        st.write(f"**Fluid Replacement (150%):** ~{results['fluid_replacement_ml']} ml")
        st.write(f"**Sodium:** ~{results['sodium_mg']} mg")

    # --- Macro Deficit ---
    carbs_needed = max(results['carbs_g_range'][0] - carbs_intake, 0)
    protein_needed = max(results['protein_g_range'][0] - protein_intake, 0)
    fat_needed = max(results['fat_g_range'][0] - fat_intake, 0)

    with st.expander("📊 Macro Deficit", expanded=True):
        st.write(f"**Carbs still needed:** {carbs_needed} g")
        st.write(f"**Protein still needed:** {protein_needed} g")
        st.write(f"**Fat still needed:** {fat_needed} g")

    # --- Food Suggestions ---
    def suggest_foods_practical(nutrient, deficit):
        suggestions = []
        remaining = deficit
        foods_sorted = sorted(example_foods[nutrient], key=lambda x: -x[1])
        for food, value in foods_sorted:
            if remaining <= 0:
                break
            count = int(remaining // value)
            if count > 0:
                suggestions.append(f"{count} x {food}")
                remaining -= value * count
        if remaining > 0:
            smallest_food, smallest_value = min(example_foods[nutrient], key=lambda x: x[1])
            suggestions.append(f"~1 x {smallest_food} to cover remaining {round(remaining)}g")
        return suggestions if suggestions else ["No suggestion needed"]

    with st.expander("🍌 Food Suggestions", expanded=True):
        st.write("**Carbs:**", ", ".join(suggest_foods_practical("carbs", carbs_needed)))
        st.write("**Protein:**", ", ".join(suggest_foods_practical("protein", protein_needed)))
        st.write("**Fat:**", ", ".join(suggest_foods_practical("fat", fat_needed)))

# ---------------- Feedback Form ----------------
st.markdown("---")
st.subheader("💬 Feedback Form")

with st.form("feedback_form"):
    q1 = st.radio("1. How useful do you find this fueling calculator?", 
                  ["Very useful", "Somewhat useful", "Neutral", "Not useful"])
    
    q2 = st.text_area("2. How are you currently tracking your fueling and nutrition needs?")
    
    q3 = st.radio("3. How often would you use a tool like this?", 
                  ["Daily", "Weekly", "Occasionally", "Rarely"])
    
    q4 = st.radio("4. Would you consider paying for a more advanced version (with features like barcode scanning, OCR, personalized plans)?", 
                  ["Yes definitely", "Maybe", "Not sure", "No"])
    
    q5 = st.text_area("5. What feature would make this most valuable for you?")
    
    submitted = st.form_submit_button("Submit Feedback")
    
    if submitted:
        st.success("✅ Thank you for your feedback!")
        st.write("Your responses:")
        st.write({"Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5})
        
        # Save locally (CSV for MVP)
        feedback_data = {"Q1": [q1], "Q2": [q2], "Q3": [q3], "Q4": [q4], "Q5": [q5]}
        df = pd.DataFrame(feedback_data)
        if not os.path.exists("feedback.csv"):
            df.to_csv("feedback.csv", index=False)
        else:
            df.to_csv("feedback.csv", mode="a", header=False, index=False)
