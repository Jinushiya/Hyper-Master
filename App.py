import streamlit as st
import pickle
import numpy as np

# Set page config
st.set_page_config(
    page_title="Hypertension Risk Prediction",
    page_icon="💓",
    layout="centered",
    initial_sidebar_state="auto"
)

# Load model safely
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    st.write("✅ Model loaded successfully.")
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# Title
st.title("💓 Hypertension Risk Prediction")

st.markdown("Enter your health details below:")

# Inputs
age = st.slider("👤 Age (years)", min_value=0, max_value=120, value=30, help="Select your age")

blood_pressure = st.slider(
    "🩸 Blood Pressure (mm Hg) (Normal: 90-120)", 
    min_value=0, max_value=200, value=120, 
    help="Systolic blood pressure"
)

cholesterol = st.slider(
    "🍔 Cholesterol Level (mg/dL) (Normal: <200)", 
    min_value=0, max_value=400, value=180, 
    help="Total cholesterol level"
)

bmi = st.slider(
    "⚖️ BMI (Normal: 18.5-24.9)", 
    min_value=0.0, max_value=60.0, value=22.5, step=0.1, 
    help="Body Mass Index"
)

smoking_status = st.selectbox("🚬 Smoking Status", ["Non-Smoker", "Smoker", "Former Smoker"])

physical_activity = st.selectbox("🏃 Physical Activity Level", ["Low", "Moderate", "High"])

# Encode categorical variables
smoking_map = {"Non-Smoker": 0, "Smoker": 1, "Former Smoker": 2}
activity_map = {"Low": 0, "Moderate": 1, "High": 2}

smoking_status_encoded = smoking_map[smoking_status]
physical_activity_encoded = activity_map[physical_activity]

# Function to check if any input is out of normal range
def is_out_of_range(bp, chol, bmi_val):
    return (bp < 90 or bp > 120) or (chol >= 200) or (bmi_val < 18.5 or bmi_val > 24.9)

if st.button("Predict"):
    if is_out_of_range(blood_pressure, cholesterol, bmi):
        # Automatically high risk if any input is out of normal range
        st.warning("⚠️ One or more values are outside normal range.")
        st.success("Predicted Hypertension Risk Level: 🔥 High Risk")
    else:
        # Inputs normal — use model prediction
        input_data = np.array([[age, blood_pressure, cholesterol, bmi, smoking_status_encoded, physical_activity_encoded]], dtype=float)
        try:
            prediction = model.predict(input_data)
            result = "🔥 High Risk" if prediction[0] == 1 else "✅ Low Risk"
            st.success(f"Predicted Hypertension Risk Level: {result}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
