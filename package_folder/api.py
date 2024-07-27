from fastapi import FastAPI
from package_folder.geo import find_nearby_places


app = FastApi()

@app.get("/")

def root():
    return {'greeting': 'hello'}

@app.get("/predict")
def predict(address:str, type:str, radius:int):
    try:
        nearby_places = find_nearby_places(address, type, radius)
        return {
            "address": address,
            "type": type,
            "radius": radius,
            "places": nearby_places
        }
    except ValueError as e:
        return {"error": str(e)}
