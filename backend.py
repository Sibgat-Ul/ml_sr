from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd

with open("./model/linear_regression_model.pkl", "rb") as f:
    linear_model = pickle.load(f)

with open("./model/xgb_regression_model.pkl", "rb") as f:
    xgb_model = pickle.load(f)

with open("./model/catboost_regression_model.pkl", "rb") as f:
    catboost_model = pickle.load(f)

with open('./encoders/label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

with open('./encoders/onehot_encoder.pkl', 'rb') as f:
    onehot_encoder = pickle.load(f)

with open('./encoders/cat_columns.pkl', 'rb') as f:
    cat_info = pickle.load(f)
    one_hot_cols = cat_info['one_hot_cols']
    label_cols = cat_info['label_cols']

app = FastAPI()

class FlightInput(BaseModel):
    airline: str
    flight: str
    source_city: str
    departure_time: str
    stops: str
    arrival_time: str
    destination_city: str
    flight_class: str  # renamed to avoid conflict with Python keyword
    duration: float
    days_left: int

def preprocess_input(df):
    df_encoded = df.copy()

    for col in label_cols:
        le = label_encoders[col]
        df_encoded[col] = le.transform(df_encoded[col].astype(str))

    if one_hot_cols:
        df_subset = df_encoded[one_hot_cols] if len(one_hot_cols) > 1 else df_encoded[[one_hot_cols[0]]]
        ohe_encoded = onehot_encoder.transform(df_subset)
        ohe_df = pd.DataFrame(ohe_encoded, 
                              columns=onehot_encoder.get_feature_names_out(one_hot_cols),
                              index=df.index)
        df_encoded = df_encoded.drop(columns=one_hot_cols)
        df_encoded = pd.concat([df_encoded, ohe_df], axis=1)

    return df_encoded


@app.post("/predict/")
def predict_price(flight: FlightInput):
    try:
        data = pd.DataFrame([{
            'airline': flight.airline,
            'flight': flight.flight,
            'source_city': flight.source_city,
            'departure_time': flight.departure_time,
            'stops': flight.stops,
            'arrival_time': flight.arrival_time,
            'destination_city': flight.destination_city,
            'class': flight.flight_class,
            'duration': flight.duration,
            'days_left': flight.days_left,
        }])

        data = preprocess_input(data)

        return {
            "linear_regression": float(linear_model.predict(data)[0]),
            "xgboost": float(xgb_model.predict(data)[0]),
            "catboost": float(catboost_model.predict(data)[0]),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
