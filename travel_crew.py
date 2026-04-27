"""
Exercise 1: Travel Assistant CrewAI Crew
=========================================
Agents:
  1. Flight Agent     – finds available flights (dummy function)
  2. Hotel Agent      – suggests hotels (AI-generated dummy data via Gemini)
  3. Tourism Agent    – builds a tourism itinerary
  4. Advisor Agent    – gives travel tips & advice

Run:
  python travel_crew.py
"""

import os
import random
from datetime import datetime, timedelta
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


#use your own LLM or a local one like Ollama, Gemini, etc. Make sure to set up the base_url in llm_config if needed.
LLM_MODEL = "ollama/qwen2.5:3b"


# ─── TOOL 1: Flight Search (Dummy) ────────────────────────────────────────────
class FlightSearchInput(BaseModel):
    origin: str = Field(description="Departure city or airport code")
    destination: str = Field(description="Destination city or airport code")
    date: str = Field(description="Travel date in YYYY-MM-DD format")


class FlightSearchTool(BaseTool):
    name: str = "flight_search"
    description: str = (
        "Search for available flights between two cities on a given date. "
        "Returns a list of flights with airline, departure time, arrival time, and price."
    )
    args_schema: type[BaseModel] = FlightSearchInput

    def _run(self, origin: str, destination: str, date: str) -> str:
        """Returns dummy flight data."""
        airlines = ["Air France", "Lufthansa", "Emirates", "Turkish Airlines", "KLM"]
        flights = []
        for i in range(4):
            dep_hour = random.randint(6, 20)
            duration = random.randint(2, 14)
            arr_hour = (dep_hour + duration) % 24
            price = random.randint(180, 950)
            airline = random.choice(airlines)
            flights.append(
                f"  ✈ {airline} | "
                f"Dep: {dep_hour:02d}:00 → Arr: {arr_hour:02d}:00 | "
                f"Duration: {duration}h | Price: ${price} | Stops: {'Non-stop' if duration < 6 else '1 stop'}"
            )
        result = (
            f"Available flights from {origin} to {destination} on {date}:\n"
            + "\n".join(flights)
        )
        return result


# ─── TOOL 2: Hotel Search (Dummy via description) ─────────────────────────────
class HotelSearchInput(BaseModel):
    city: str = Field(description="City to search hotels in")
    checkin: str = Field(description="Check-in date YYYY-MM-DD")
    checkout: str = Field(description="Check-out date YYYY-MM-DD")
    budget: str = Field(description="Budget level: budget / mid-range / luxury")


class HotelSearchTool(BaseTool):
    name: str = "hotel_search"
    description: str = (
        "Search for hotels in a city for given dates and budget level. "
        "Returns hotel suggestions with name, rating, price per night, and highlights."
    )
    args_schema: type[BaseModel] = HotelSearchInput

    def _run(self, city: str, checkin: str, checkout: str, budget: str) -> str:
        """Returns dummy hotel data based on budget level."""
        hotel_data = {
            "budget": [
                {"name": f"Cozy Inn {city}", "stars": 2, "price": 45, "highlight": "Free WiFi, central location"},
                {"name": f"Backpacker's Hub {city}", "stars": 2, "price": 35, "highlight": "Hostel-style, social vibe"},
                {"name": f"City Sleep {city}", "stars": 3, "price": 60, "highlight": "Clean rooms, good transport links"},
            ],
            "mid-range": [
                {"name": f"Grand Stay {city}", "stars": 3, "price": 110, "highlight": "Pool, breakfast included"},
                {"name": f"Urban Comfort {city}", "stars": 4, "price": 145, "highlight": "City view, gym, spa"},
                {"name": f"Business Premier {city}", "stars": 4, "price": 160, "highlight": "Conference facilities, bar"},
            ],
            "luxury": [
                {"name": f"Royal Palace Hotel {city}", "stars": 5, "price": 420, "highlight": "Butler service, rooftop bar"},
                {"name": f"The Grand {city}", "stars": 5, "price": 580, "highlight": "Michelin-star restaurant, pool"},
                {"name": f"Prestige Resort {city}", "stars": 5, "price": 750, "highlight": "Private beach, full spa, concierge"},
            ],
        }
        key = budget.lower() if budget.lower() in hotel_data else "mid-range"
        hotels = hotel_data[key]
        lines = [f"🏨 Hotel suggestions in {city} ({checkin} → {checkout}) | Budget: {budget}"]
        for h in hotels:
            lines.append(
                f"  ★{'★' * h['stars']}  {h['name']} — ${h['price']}/night | {h['highlight']}"
            )
        return "\n".join(lines)


# ─── AGENTS ───────────────────────────────────────────────────────────────────

def create_agents():
    flight_agent = Agent(
        role="Flight Search Specialist",
        goal="Find the best available flights for the traveler based on their travel dates and budget",
        backstory=(
            "You are an experienced travel agent with 15 years of expertise in finding "
            "optimal flight routes. You always compare multiple airlines and present "
            "the best options clearly. You are detail-oriented and price-conscious."
        ),
        tools=[FlightSearchTool()],
        llm=LLM_MODEL,
        llm_config={"base_url": "http://localhost:11434"},
        verbose=True,
        allow_delegation=False,
    )

    hotel_agent = Agent(
        role="Hotel Recommendations Expert",
        goal="Suggest the best hotels in the destination city that match the traveler's preferences and budget",
        backstory=(
            "You are a hospitality expert who has reviewed thousands of hotels worldwide. "
            "You understand that accommodation makes or breaks a trip. You always consider "
            "location, value for money, and unique features when making recommendations."
        ),
        tools=[HotelSearchTool()],
        llm=LLM_MODEL,
        llm_config={"base_url": "http://localhost:11434"},
        verbose=True,
        allow_delegation=False,
    )

    tourism_agent = Agent(
        role="Tourism & Itinerary Planner",
        goal="Build a detailed, day-by-day tourism itinerary for the destination country",
        backstory=(
            "You are a passionate traveler and certified tour guide who has visited over "
            "80 countries. You know every hidden gem, must-see landmark, and local experience "
            "worth having. You craft itineraries that balance culture, food, adventure, and rest."
        ),
        tools=[],
        llm=LLM_MODEL,
        llm_config={"base_url": "http://localhost:11434"},
        verbose=True,
        allow_delegation=False,
    )

    advisor_agent = Agent(
        role="Travel Advisor & Safety Expert",
        goal="Provide comprehensive travel advice including visa requirements, safety tips, culture, packing, and money",
        backstory=(
            "You are a seasoned travel advisor with expertise in international travel logistics. "
            "You have helped thousands of travelers navigate visa requirements, local customs, "
            "health precautions, and budget planning. Your advice is practical and up-to-date."
        ),
        tools=[],
        llm=LLM_MODEL,
        llm_config={"base_url": "http://localhost:11434"},
        verbose=True,
        allow_delegation=False,
    )

    return flight_agent, hotel_agent, tourism_agent, advisor_agent


# ─── TASKS ────────────────────────────────────────────────────────────────────

def create_tasks(agents, travel_request: dict):
    flight_agent, hotel_agent, tourism_agent, advisor_agent = agents

    origin = travel_request["origin"]
    destination = travel_request["destination"]
    country = travel_request["country"]
    departure_date = travel_request["departure_date"]
    return_date = travel_request["return_date"]
    budget = travel_request["budget"]
    travelers = travel_request["travelers"]
    interests = travel_request["interests"]

    task_flights = Task(
        description=(
            f"Search for flights from {origin} to {destination} departing on {departure_date}. "
            f"The traveler is {travelers} person(s) with a {budget} budget. "
            f"Use the flight_search tool with origin='{origin}', destination='{destination}', date='{departure_date}'. "
            "Present the 4 results clearly with a recommendation for the best option and explain why."
        ),
        expected_output=(
            "A formatted list of available flights with your top recommendation highlighted "
            "and a brief justification for the choice."
        ),
        agent=flight_agent,
    )

    task_hotels = Task(
        description=(
            f"Find hotel recommendations in {destination} for {travelers} traveler(s). "
            f"Check-in: {departure_date}, Check-out: {return_date}. Budget level: {budget}. "
            f"Use the hotel_search tool with city='{destination}', checkin='{departure_date}', "
            f"checkout='{return_date}', budget='{budget}'. "
            "Present the options and recommend the best one explaining why it suits this traveler."
        ),
        expected_output=(
            "A list of 3 hotel options with prices, ratings, and highlights, "
            "plus a clear recommendation with reasoning."
        ),
        agent=hotel_agent,
    )

    task_tourism = Task(
        description=(
            f"Create a detailed tourism itinerary for {country}. "
            f"The traveler stays from {departure_date} to {return_date}. "
            f"Their interests include: {interests}. Budget level: {budget}. "
            "Build a day-by-day plan that covers the best attractions, local food experiences, "
            "and hidden gems. Include morning, afternoon, and evening activities for each day."
        ),
        expected_output=(
            "A complete day-by-day itinerary with specific places, activities, restaurants, "
            "and estimated costs per day. Format it clearly with Day 1, Day 2, etc."
        ),
        agent=tourism_agent,
    )

    task_advice = Task(
        description=(
            f"Provide comprehensive travel advice for visiting {country} (specifically {destination}). "
            f"The traveler is going from {departure_date} to {return_date}. "
            f"Budget: {budget}. Number of travelers: {travelers}. "
            "Cover: visa requirements, best local currency/payment tips, safety advice, "
            "cultural etiquette, weather/packing tips, must-try local foods, transportation inside the country, "
            "and any health or vaccination considerations."
        ),
        expected_output=(
            "A well-organized travel advice guide covering all the key topics: "
            "visa, money, safety, culture, packing, food, transport, and health."
        ),
        agent=advisor_agent,
    )

    return [task_flights, task_hotels, task_tourism, task_advice]


# ─── CREW ─────────────────────────────────────────────────────────────────────

def run_travel_crew(travel_request: dict):
    print("\n" + "="*60)
    print("🌍  TRAVEL ASSISTANT CREW — Starting...")
    print("="*60 + "\n")

    agents = create_agents()
    tasks = create_tasks(agents, travel_request)

    crew = Crew(
        agents=list(agents),
        tasks=tasks,
        process=Process.sequential,   # Flight → Hotel → Tourism → Advice
        verbose=True,
    )

    result = crew.kickoff()
    return result


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🌍 Welcome to the AI Travel Assistant!")
    print("Please answer a few quick questions:\n")

    origin = input("Where are you flying FROM? (city or airport, e.g. 'Rotterdam'): ").strip() or "Rotterdam"
    destination = input("Where are you flying TO? (city, e.g. 'Tokyo'): ").strip() or "Tokyo"
    country = input("Which country is that in? (e.g. 'Japan'): ").strip() or "Japan"
    departure_date = input("Departure date (YYYY-MM-DD, e.g. 2026-06-01): ").strip() or "2026-06-01"
    return_date = input("Return date (YYYY-MM-DD, e.g. 2026-06-10): ").strip() or "2026-06-10"
    budget = input("Budget level (budget / mid-range / luxury): ").strip() or "mid-range"
    travelers = input("Number of travelers (e.g. 2): ").strip() or "2"
    interests = input("Your interests (e.g. 'history, food, nature, anime'): ").strip() or "history, food, culture"

    travel_request = {
        "origin": origin,
        "destination": destination,
        "country": country,
        "departure_date": departure_date,
        "return_date": return_date,
        "budget": budget,
        "travelers": travelers,
        "interests": interests,
    }

    result = run_travel_crew(travel_request)

    print("\n" + "="*60)
    print("✅  TRAVEL PLAN COMPLETE")
    print("="*60)
    print(result)
