import streamlit as st
import requests

st.set_page_config(page_title="Flight Price Predictor")

st.title("✈️ Flight Price Prediction")

airlines = ['SpiceJet', 'AirAsia', 'Vistara', 'GO_FIRST', 'Indigo', 'Air_India']
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai']
times = ['Evening', 'Early_Morning', 'Morning', 'Afternoon', 'Night', 'Late_Night']
stops_options = ['zero', 'one', 'two_or_more']
classes = ['Economy', 'Business']

airline = st.selectbox("Airline", airlines)
flight = st.text_input("Flight Number", "SG-8157")
source_city = st.selectbox("Source City", cities)
departure_time = st.selectbox("Departure Time", times)
stops = st.radio("Number of Stops", stops_options)
arrival_time = st.selectbox("Arrival Time", times)
destination_city = st.selectbox("Destination City", cities)
flight_class = st.radio("Class", classes)
duration = st.slider("Duration (in minutes)", min_value=30, max_value=500, value=120)
days_left = st.slider("Days Left Until Departure", min_value=1, max_value=60, value=30)

if st.button("Predict Price"):
    with st.spinner("Contacting model API..."):
        input_data = {
            "airline": airline,
            "flight": flight,
            "source_city": source_city,
            "departure_time": departure_time,
            "stops": stops,
            "arrival_time": arrival_time,
            "destination_city": destination_city,
            "flight_class": flight_class,
            "duration": duration,
            "days_left": days_left
        }

        try:
            response = requests.post("http://localhost:8000/predict/", json=input_data)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Prediction Results")
                st.write(f"**Linear Regression:** ₹{result['linear_regression']:.2f}")
                st.write(f"**XGBoost:** ₹{result['xgboost']:.2f}")
                st.write(f"**CatBoost:** ₹{result['catboost']:.2f}")
            else:
                st.error(f"Error: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server. Is it running?")
