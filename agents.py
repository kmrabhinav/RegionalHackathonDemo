"""
Agent Manager Module
Manages all specialized AI agents with dummy APIs and mock data
"""

import random
import time
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.status = "idle"
        self.progress = 0
        self.result = None
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": self.agent_name,
            "status": self.status,
            "progress": self.progress,
            "result": self.result
        }

class WeatherAgent(BaseAgent):
    """Agent for weather analysis"""
    
    def __init__(self):
        super().__init__("weather_analysis")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch weather data using mock API"""
        destination = context.get('destination', 'Unknown')
        
        # Mock weather data
        weather_conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Clear']
        
        weather_data = {
            "current": {
                "condition": random.choice(weather_conditions),
                "temperature": random.randint(20, 35),
                "humidity": random.randint(40, 80),
                "wind_speed": random.randint(5, 25),
                "uv_index": random.randint(3, 10)
            },
            "forecast_7days": [
                {
                    "day": (datetime.now() + timedelta(days=i)).strftime("%A"),
                    "high": random.randint(25, 35),
                    "low": random.randint(18, 24),
                    "condition": random.choice(weather_conditions),
                    "rain_probability": random.randint(0, 60)
                }
                for i in range(7)
            ],
            "best_times": {
                "morning": "6:00 AM - 9:00 AM",
                "afternoon": "4:00 PM - 7:00 PM",
                "avoid": "11:00 AM - 3:00 PM (peak heat)"
            },
            "recommendations": [
                "Bring sunscreen (UV index is high)",
                "Light, breathable clothing recommended",
                "Stay hydrated throughout the day"
            ]
        }
        
        self.result = weather_data
        self.status = "completed"
        return weather_data

class SafetyAgent(BaseAgent):
    """Agent for safety and geopolitical analysis"""
    
    def __init__(self):
        super().__init__("safety_geopolitical")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze safety using mock API"""
        destination = context.get('destination', 'Unknown')
        
        safety_data = {
            "safety_rating": round(random.uniform(3.5, 5.0), 1),
            "travel_advisories": {
                "level": random.choice(["None", "Exercise Normal Precautions", "Exercise Increased Caution"]),
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "details": "No significant travel warnings for this destination"
            },
            "political_stability": {
                "rating": "Stable",
                "description": "Peaceful political climate with strong tourism infrastructure"
            },
            "health_requirements": {
                "vaccinations": ["Routine vaccinations", "Hepatitis A", "Typhoid"],
                "medical_facilities": "Good quality medical facilities available in major areas",
                "travel_insurance": "Strongly recommended"
            },
            "emergency_contacts": {
                "embassy": f"+{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "local_police": "112",
                "ambulance": "115",
                "tourist_police": f"+{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            },
            "safety_tips": [
                "Keep copies of important documents",
                "Use registered taxis or ride-sharing apps",
                "Avoid displaying expensive jewelry or electronics",
                "Be aware of your surroundings in crowded areas"
            ]
        }
        
        self.result = safety_data
        self.status = "completed"
        return safety_data

class FlightAgent(BaseAgent):
    """Agent for flight options"""
    
    def __init__(self):
        super().__init__("flight_options")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search flights using mock API"""
        destination = context.get('destination', 'Unknown')
        budget = float(context.get('budget', 2000))
        
        airlines = ['Emirates', 'Singapore Airlines', 'Qatar Airways', 'Cathay Pacific', 'Turkish Airlines']
        
        flights = []
        for i in range(3):
            price = random.randint(int(budget * 0.2), int(budget * 0.4))
            flights.append({
                "airline": random.choice(airlines),
                "price": price,
                "currency": "USD",
                "duration": f"{random.randint(10, 20)} hours",
                "stops": random.randint(0, 2),
                "departure_time": f"{random.randint(6, 23)}:{random.choice(['00', '30'])}",
                "arrival_time": f"{random.randint(6, 23)}:{random.choice(['00', '30'])}",
                "class": context.get('travel_style', 'Economy'),
                "baggage": "2 x 23kg checked + 7kg cabin",
                "booking_link": f"https://flights.example.com/book/{random.randint(10000, 99999)}"
            })
        
        # Sort by price
        flights.sort(key=lambda x: x['price'])
        
        flight_data = {
            "options": flights,
            "best_deal": flights[0],
            "recommendations": {
                "best_time_to_book": "Tuesday or Wednesday for better rates",
                "peak_season": "December - February",
                "off_peak": "June - August",
                "flexible_dates_savings": f"${random.randint(50, 200)}"
            },
            "airport_info": {
                "destination_airport": f"{destination} International Airport",
                "airport_code": "XXX",
                "transportation": "Taxi, bus, and rental cars available"
            }
        }
        
        self.result = flight_data
        self.status = "completed"
        return flight_data

class HotelAgent(BaseAgent):
    """Agent for hotel bookings"""
    
    def __init__(self):
        super().__init__("hotel_bookings")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search hotels using mock API"""
        destination = context.get('destination', 'Unknown')
        budget = float(context.get('budget', 2000))
        duration = int(context.get('duration', 7))
        travel_style = context.get('travel_style', 'Comfort')
        
        # Adjust price range based on travel style
        price_ranges = {
            'Budget': (30, 80),
            'Comfort': (80, 200),
            'Luxury': (200, 500),
            'Adventure': (40, 120),
            'Romantic': (150, 400)
        }
        
        min_price, max_price = price_ranges.get(travel_style, (80, 200))
        
        hotels = []
        for i in range(3):
            price_per_night = random.randint(min_price, max_price)
            hotels.append({
                "name": f"{random.choice(['Ocean', 'Sunset', 'Paradise', 'Garden', 'Beach'])} {random.choice(['Resort', 'Hotel', 'Villa', 'Lodge'])}",
                "rating": round(random.uniform(3.5, 5.0), 1),
                "price_per_night": price_per_night,
                "total_price": price_per_night * duration,
                "location": f"{destination} - {random.choice(['Beach Area', 'City Center', 'Mountain View', 'Old Town'])}",
                "amenities": random.sample([
                    "Swimming Pool", "Free WiFi", "Breakfast Included",
                    "Gym", "Spa", "Restaurant", "Bar", "Airport Shuttle",
                    "Room Service", "Concierge", "Beach Access"
                ], k=random.randint(4, 7)),
                "room_type": random.choice(['Standard Room', 'Deluxe Room', 'Suite', 'Ocean View Room']),
                "cancellation": random.choice(['Free cancellation', 'Non-refundable', 'Flexible']),
                "booking_link": f"https://hotels.example.com/book/{random.randint(10000, 99999)}"
            })
        
        # Sort by value (rating / price ratio)
        hotels.sort(key=lambda x: x['rating'] / (x['price_per_night'] / 100), reverse=True)
        
        hotel_data = {
            "options": hotels,
            "recommended": hotels[0],
            "neighborhoods": [
                {"name": "Beach District", "vibe": "Relaxed, touristy", "avg_price": f"${random.randint(100, 200)}"},
                {"name": "Old Town", "vibe": "Cultural, authentic", "avg_price": f"${random.randint(80, 150)}"},
                {"name": "City Center", "vibe": "Convenient, bustling", "avg_price": f"${random.randint(120, 250)}"}
            ],
            "booking_tips": [
                "Book at least 2 months in advance for better rates",
                "Check for package deals including breakfast",
                "Read recent reviews for accurate information"
            ]
        }
        
        self.result = hotel_data
        self.status = "completed"
        return hotel_data

class TransportAgent(BaseAgent):
    """Agent for local transport options"""
    
    def __init__(self):
        super().__init__("local_transport")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get transport options using mock API"""
        destination = context.get('destination', 'Unknown')
        
        transport_data = {
            "airport_transfer": {
                "taxi": {"price": f"${random.randint(20, 50)}", "duration": "30-45 min", "comfort": "High"},
                "shared_shuttle": {"price": f"${random.randint(10, 25)}", "duration": "45-60 min", "comfort": "Medium"},
                "public_bus": {"price": f"${random.randint(2, 8)}", "duration": "60-90 min", "comfort": "Basic"},
                "private_car": {"price": f"${random.randint(40, 80)}", "duration": "30 min", "comfort": "Premium"}
            },
            "daily_transport": {
                "scooter_rental": {"price_per_day": f"${random.randint(8, 15)}", "requirements": "International license"},
                "car_rental": {"price_per_day": f"${random.randint(30, 60)}", "requirements": "Valid driver's license"},
                "bicycle": {"price_per_day": f"${random.randint(5, 10)}", "requirements": "None"},
                "public_transport": {"price_per_ride": f"${random.randint(1, 3)}", "day_pass": f"${random.randint(5, 10)}"}
            },
            "ride_hailing_apps": [
                {"name": "Grab", "availability": "Excellent", "avg_cost": "$3-8 per ride"},
                {"name": "GoJek", "availability": "Good", "avg_cost": "$2-6 per ride"},
                {"name": "Local Taxi", "availability": "Good", "avg_cost": "$5-12 per ride"}
            ],
            "navigation_tips": [
                "Download offline maps before arrival",
                "Negotiate taxi fares before starting journey",
                "Peak traffic hours: 7-9 AM and 5-7 PM",
                "Scooters are most flexible for short distances"
            ]
        }
        
        self.result = transport_data
        self.status = "completed"
        return transport_data

class ShoppingAgent(BaseAgent):
    """Agent for shopping and markets"""
    
    def __init__(self):
        super().__init__("shopping_markets")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get shopping info using mock API"""
        destination = context.get('destination', 'Unknown')
        interests = context.get('interests', [])
        
        shopping_data = {
            "markets": [
                {
                    "name": "Central Traditional Market",
                    "type": "Traditional",
                    "open_hours": "6:00 AM - 6:00 PM",
                    "days": "Daily",
                    "specialties": ["Handicrafts", "Local Textiles", "Spices", "Fresh Produce"],
                    "bargaining": "Expected - start at 50% of asking price",
                    "best_time": "Early morning for freshest items"
                },
                {
                    "name": "Night Market",
                    "type": "Night Market",
                    "open_hours": "6:00 PM - 11:00 PM",
                    "days": "Friday - Sunday",
                    "specialties": ["Street Food", "Souvenirs", "Clothing", "Jewelry"],
                    "bargaining": "Yes, but less flexible",
                    "best_time": "7-9 PM for best atmosphere"
                },
                {
                    "name": "Modern Shopping District",
                    "type": "Mall/Shopping Center",
                    "open_hours": "10:00 AM - 10:00 PM",
                    "days": "Daily",
                    "specialties": ["International Brands", "Electronics", "Fashion", "Dining"],
                    "bargaining": "Fixed prices",
                    "best_time": "Weekdays to avoid crowds"
                }
            ],
            "must_buy_items": [
                {"item": "Handwoven Textiles", "price_range": "$20-100", "quality_tip": "Check for natural dyes"},
                {"item": "Local Spices", "price_range": "$5-30", "quality_tip": "Buy from reputable sellers"},
                {"item": "Handcrafted Jewelry", "price_range": "$10-200", "quality_tip": "Ask for certificate of authenticity"},
                {"item": "Traditional Artwork", "price_range": "$30-500", "quality_tip": "Visit artist studios for best selection"}
            ],
            "shopping_tips": [
                "Carry small bills for easier transactions",
                "Shop at government-approved stores for guaranteed quality",
                "Compare prices at multiple vendors before buying",
                "Save receipts for customs documentation"
            ],
            "payment_methods": {
                "cash": "Widely accepted, preferred at markets",
                "credit_card": "Accepted at malls and larger stores",
                "mobile_payment": "Growing acceptance in urban areas"
            }
        }
        
        self.result = shopping_data
        self.status = "completed"
        return shopping_data

class LanguageAgent(BaseAgent):
    """Agent for language support and translation"""
    
    def __init__(self):
        super().__init__("language_support")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get language support info using mock API"""
        destination = context.get('destination', 'Unknown')
        
        language_data = {
            "primary_language": "Local Language",
            "english_proficiency": {
                "level": "Moderate",
                "tourist_areas": "Good - most people speak basic English",
                "rural_areas": "Limited - translation tools helpful",
                "younger_generation": "Better English skills"
            },
            "essential_phrases": {
                "greetings": {
                    "hello": "Local Hello",
                    "goodbye": "Local Goodbye",
                    "thank_you": "Local Thank You",
                    "please": "Local Please",
                    "excuse_me": "Local Excuse Me"
                },
                "practical": {
                    "how_much": "Local: How much?",
                    "where_is": "Local: Where is...?",
                    "help": "Local: Help!",
                    "bathroom": "Local: Bathroom?",
                    "water": "Local: Water"
                },
                "numbers": {
                    "1-10": "One through ten in local language"
                }
            },
            "translation_tools": [
                {
                    "name": "Google Translate",
                    "offline": "Yes - download language pack",
                    "features": "Text, voice, camera translation"
                },
                {
                    "name": "iTranslate",
                    "offline": "Limited",
                    "features": "Voice translation, phrasebook"
                }
            ],
            "cultural_communication_tips": [
                "Smiling is universally appreciated",
                "Learn a few phrases - locals appreciate the effort",
                "Use translation apps respectfully, not lazily",
                "Be patient with language barriers",
                "Body language and gestures can help"
            ],
            "interpretation_services": {
                "available": True,
                "cost": "$30-60 per hour",
                "booking": "Through hotel concierge or tour operators"
            }
        }
        
        self.result = language_data
        self.status = "completed"
        return language_data

class AttractionsAgent(BaseAgent):
    """Agent for local attractions and activities"""
    
    def __init__(self):
        super().__init__("local_attractions")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get attractions info using mock API"""
        destination = context.get('destination', 'Unknown')
        interests = context.get('interests', [])
        
        # Generate attractions based on interests
        all_attractions = {
            "Adventure": [
                {"name": "Mountain Trekking", "rating": 4.7, "price": "$45", "duration": "Full day"},
                {"name": "Water Sports Center", "rating": 4.5, "price": "$60", "duration": "Half day"}
            ],
            "Culture": [
                {"name": "Ancient Temple Complex", "rating": 4.8, "price": "$15", "duration": "3 hours"},
                {"name": "Traditional Dance Show", "rating": 4.6, "price": "$25", "duration": "2 hours"}
            ],
            "Food": [
                {"name": "Cooking Class", "rating": 4.9, "price": "$50", "duration": "4 hours"},
                {"name": "Food Market Tour", "rating": 4.7, "price": "$35", "duration": "3 hours"}
            ],
            "Nature": [
                {"name": "Waterfall Trek", "rating": 4.6, "price": "$30", "duration": "5 hours"},
                {"name": "Botanical Gardens", "rating": 4.4, "price": "$10", "duration": "2 hours"}
            ],
            "Beaches": [
                {"name": "Snorkeling Excursion", "rating": 4.8, "price": "$55", "duration": "Half day"},
                {"name": "Beach Resort Day Pass", "rating": 4.5, "price": "$40", "duration": "Full day"}
            ]
        }
        
        relevant_attractions = []
        for interest in interests:
            if interest in all_attractions:
                relevant_attractions.extend(all_attractions[interest])
        
        # Add some general attractions
        general_attractions = [
            {"name": "City Walking Tour", "rating": 4.5, "price": "$20", "duration": "3 hours"},
            {"name": "Sunset Cruise", "rating": 4.7, "price": "$45", "duration": "2 hours"},
            {"name": "Local Museum", "rating": 4.3, "price": "$12", "duration": "2 hours"}
        ]
        
        attractions_data = {
            "top_rated": relevant_attractions[:5] if relevant_attractions else general_attractions,
            "general_attractions": general_attractions,
            "by_category": {
                "cultural": [
                    {"name": "Heritage Site", "rating": 4.7},
                    {"name": "Art Gallery", "rating": 4.4}
                ],
                "adventure": [
                    {"name": "Zip Lining", "rating": 4.8},
                    {"name": "Rock Climbing", "rating": 4.6}
                ],
                "relaxation": [
                    {"name": "Spa & Wellness Center", "rating": 4.9},
                    {"name": "Yoga Retreat", "rating": 4.7}
                ]
            },
            "day_trip_options": [
                {"destination": "Nearby Island", "distance": "2 hours", "cost": "$80", "highlights": "Pristine beaches, snorkeling"},
                {"destination": "Mountain Village", "distance": "3 hours", "cost": "$60", "highlights": "Traditional culture, hiking"}
            ],
            "booking_recommendations": [
                "Book popular attractions 1-2 weeks in advance",
                "Check for combo deals and multi-day passes",
                "Free walking tours available (tip-based)",
                "Skip-the-line tickets worth it for major sites"
            ],
            "seasonal_attractions": {
                "year_round": ["Temples", "Museums", "Markets"],
                "seasonal": ["Whale watching (Jun-Sep)", "Festival season (Mar-Apr)"]
            }
        }
        
        self.result = attractions_data
        self.status = "completed"
        return attractions_data


class AgentManager:
    """
    Manager class to coordinate all agents
    """
    
    def __init__(self):
        self.agents = {
            'weather_analysis': WeatherAgent(),
            'safety_geopolitical': SafetyAgent(),
            'flight_options': FlightAgent(),
            'hotel_bookings': HotelAgent(),
            'local_transport': TransportAgent(),
            'shopping_markets': ShoppingAgent(),
            'language_support': LanguageAgent(),
            'local_attractions': AttractionsAgent()
        }
        
        self.execution_results = {}
    
    def execute_agent(self, agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific agent"""
        if agent_name not in self.agents:
            return {"error": f"Agent {agent_name} not found"}
        
        agent = self.agents[agent_name]
        result = agent.execute(context)
        self.execution_results[agent_name] = result
        
        return result
    
    def execute_all_agents(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all agents in sequence"""
        results = {}
        
        for agent_name, agent in self.agents.items():
            results[agent_name] = agent.execute(context)
        
        self.execution_results = results
        return results
    
    def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        if agent_name not in self.agents:
            return {"error": f"Agent {agent_name} not found"}
        
        return self.agents[agent_name].get_status()
    
    def get_all_results(self) -> Dict[str, Any]:
        """Get results from all executed agents"""
        return self.execution_results
