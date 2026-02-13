import os
from urllib import response
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("WEATHER_API_KEY")

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    recommendation: str
    feels_like: float = None 
    humidity: int = None  
    wind_speed: float = None  

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

@app.get("/", response_class=HTMLResponse)
async def root(request : Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/weather/{city}", response_model=WeatherResponse)
async def fetch_weather(city: str):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, 
            detail=f"WeatherAPI Error: {response.text}"
        )
    data = response.json()
    
    # Updated mapping for WeatherAPI.com structure
    temperature = data["current"]["temp_c"]
    description = data["current"]["condition"]["text"]
    recommendation = get_advice(temperature)
    feels_like = data["current"]["feelslike_c"]
    humidity = data["current"]["humidity"]
    wind_speed = data["current"]["wind_kph"]

    return WeatherResponse(
        city=data["location"]["name"],
        temperature=temperature,
        description=description,
        recommendation=recommendation,
        feels_like=feels_like,
        humidity=humidity,
        wind_speed=wind_speed
    )