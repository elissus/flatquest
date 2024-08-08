from fastapi import FastAPI
import pickle
from geo import find_nearby_places

app = FastAPI()

@app.get("/")
def root():
    return {'greeting':"hello"}

@app.get("/predict")
def predict(sepal_length,
            sepal_width,
            petal_length,
            petal_width):

    with open('../models/best_model.pkl', 'rb') as file:
        model = pickle.load(file)

    prediction = model.predict([[sepal_length,sepal_width,petal_length,petal_width]])

    pretty_prediction = from_number_to_flower(float(prediction[0]))

    print(f"Hello world!")

    return {"prediction": pretty_prediction}

@app.get("/search")
def flat_search(address,
                place_type,
                radius):

    radius= int(radius)

    return find_nearby_places(address, place_type, int(radius))
