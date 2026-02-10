import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("WEATHER_API_KEY")

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    recommendation: str

def get_advice(temperature: float) -> str:
    if temperature < 0:
        return "It's freezing! Wear a heavy coat and stay warm."
    elif 0 <= temperature < 10:
        return "It's cold. Wear a jacket and consider layering."
    elif 10 <= temperature < 20:
        return "It's cool. A light jacket or sweater should be fine."
    elif 20 <= temperature < 30:
        return "It's warm. Dress comfortably, maybe in short sleeves."
    else:
        return "It's hot! Stay hydrated and wear light clothing."

@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    import requests

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")

    data = response.json()
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    recommendation = get_advice(temperature)

    return WeatherResponse(
        city=city.capitalize(),
        temperature=temperature,
        description=description,
        recommendation=recommendation
    )