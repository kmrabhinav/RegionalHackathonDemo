"""
Mock API Module
Provides dummy APIs for testing without external dependencies
"""

import random
from typing import Dict, Any, List
from datetime import datetime, timedelta

class MockWeatherAPI:
    """Mock Weather API"""
    
    @staticmethod
    def get_current_weather(location: str) -> Dict[str, Any]:
        """Get current weather data"""
        conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Clear']
        
        return {
            "location": location,
            "temperature": random.randint(20, 35),
            "condition": random.choice(conditions),
            "humidity": random.randint(40, 80),
            "wind_speed": random.randint(5, 25),
            "uv_index": random.randint(3, 10),
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def get_forecast(location: str, days: int = 7) -> List[Dict[str, Any]]:
        """Get weather forecast"""
        conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Clear']
        forecast = []
        
        for i in range(days):
            forecast.append({
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "day": (datetime.now() + timedelta(days=i)).strftime("%A"),
                "high": random.randint(25, 35),
                "low": random.randint(18, 24),
                "condition": random.choice(conditions),
                "rain_probability": random.randint(0, 60)
            })
        
        return forecast

class MockFlightAPI:
    """Mock Flight Search API"""
    
    @staticmethod
    def search_flights(origin: str, destination: str, date: str, passengers: int = 1) -> List[Dict[str, Any]]:
        """Search for flights"""
        airlines = ['Emirates', 'Singapore Airlines', 'Qatar Airways', 'Cathay Pacific', 'Turkish Airlines']
        flights = []
        
        for i in range(5):
            flights.append({
                "flight_id": f"FL{random.randint(1000, 9999)}",
                "airline": random.choice(airlines),
                "price": random.randint(400, 1500),
                "currency": "USD",
                "duration": f"{random.randint(8, 20)} hours",
                "stops": random.randint(0, 2),
                "departure": {
                    "airport": origin,
                    "time": f"{random.randint(6, 23)}:{random.choice(['00', '30'])}"
                },
                "arrival": {
                    "airport": destination,
                    "time": f"{random.randint(6, 23)}:{random.choice(['00', '30'])}"
                },
                "available_seats": random.randint(5, 50)
            })
        
        return sorted(flights, key=lambda x: x['price'])

class MockHotelAPI:
    """Mock Hotel Booking API"""
    
    @staticmethod
    def search_hotels(location: str, checkin: str, checkout: str, guests: int = 2) -> List[Dict[str, Any]]:
        """Search for hotels"""
        prefixes = ['Ocean', 'Sunset', 'Paradise', 'Garden', 'Beach', 'Mountain', 'City']
        suffixes = ['Resort', 'Hotel', 'Villa', 'Lodge', 'Inn', 'Suites']
        
        hotels = []
        
        for i in range(8):
            hotels.append({
                "hotel_id": f"HT{random.randint(1000, 9999)}",
                "name": f"{random.choice(prefixes)} {random.choice(suffixes)}",
                "rating": round(random.uniform(3.5, 5.0), 1),
                "price_per_night": random.randint(50, 400),
                "location": f"{location} - {random.choice(['Beach', 'Downtown', 'Old Town', 'Airport Area'])}",
                "amenities": random.sample([
                    "WiFi", "Pool", "Gym", "Spa", "Restaurant", "Bar",
                    "Room Service", "Parking", "Airport Shuttle", "Beach Access"
                ], k=random.randint(4, 7)),
                "available_rooms": random.randint(1, 20),
                "cancellation": random.choice(['Free cancellation', 'Non-refundable', 'Flexible'])
            })
        
        return sorted(hotels, key=lambda x: x['rating'], reverse=True)

class MockSafetyAPI:
    """Mock Safety Information API"""
    
    @staticmethod
    def get_safety_info(location: str) -> Dict[str, Any]:
        """Get safety information for location"""
        return {
            "location": location,
            "safety_rating": round(random.uniform(3.0, 5.0), 1),
            "travel_advisory": {
                "level": random.choice(["Level 1: Exercise Normal Precautions", 
                                       "Level 2: Exercise Increased Caution"]),
                "updated": datetime.now().strftime("%Y-%m-%d")
            },
            "common_risks": random.sample([
                "Petty theft", "Traffic accidents", "Natural disasters",
                "Food safety", "Air pollution"
            ], k=random.randint(2, 3)),
            "emergency_numbers": {
                "police": "112",
                "ambulance": "115",
                "fire": "113",
                "tourist_police": f"+{random.randint(100, 999)}-{random.randint(1000000, 9999999)}"
            },
            "health_requirements": {
                "vaccinations": ["Routine", "Hepatitis A", "Typhoid"],
                "malaria_risk": random.choice(["None", "Low", "Moderate"])
            }
        }

class MockTranslationAPI:
    """Mock Translation API"""
    
    @staticmethod
    def translate(text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """Translate text"""
        return {
            "original": text,
            "translation": f"[Translated: {text}]",
            "source_language": source_lang,
            "target_language": target_lang,
            "confidence": round(random.uniform(0.85, 0.99), 2)
        }
    
    @staticmethod
    def get_common_phrases(language: str) -> Dict[str, str]:
        """Get common phrases in target language"""
        return {
            "hello": f"Hello in {language}",
            "goodbye": f"Goodbye in {language}",
            "thank_you": f"Thank you in {language}",
            "please": f"Please in {language}",
            "yes": f"Yes in {language}",
            "no": f"No in {language}",
            "help": f"Help in {language}",
            "how_much": f"How much? in {language}"
        }

class MockGeoAPI:
    """Mock Geolocation and Maps API"""
    
    @staticmethod
    def geocode(address: str) -> Dict[str, Any]:
        """Convert address to coordinates"""
        return {
            "address": address,
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6),
            "country": "Country Name",
            "city": address
        }
    
    @staticmethod
    def get_nearby_places(lat: float, lon: float, place_type: str, radius: int = 5000) -> List[Dict[str, Any]]:
        """Get nearby places"""
        places = []
        
        for i in range(random.randint(5, 15)):
            places.append({
                "name": f"{place_type.title()} {i+1}",
                "type": place_type,
                "rating": round(random.uniform(3.5, 5.0), 1),
                "distance": random.randint(100, radius),
                "price_level": random.randint(1, 4)
            })
        
        return places

class MockStockAPI:
    """Mock Stock Market API (for airline stocks, tourism companies)"""
    
    @staticmethod
    def get_stock_price(symbol: str) -> Dict[str, Any]:
        """Get stock price"""
        return {
            "symbol": symbol,
            "price": round(random.uniform(50, 500), 2),
            "change": round(random.uniform(-5, 5), 2),
            "change_percent": round(random.uniform(-2, 2), 2),
            "volume": random.randint(1000000, 10000000),
            "timestamp": datetime.now().isoformat()
        }

class MockCurrencyAPI:
    """Mock Currency Exchange API"""
    
    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Get exchange rate"""
        return {
            "from": from_currency,
            "to": to_currency,
            "rate": round(random.uniform(0.5, 2.0), 4),
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Convert currency"""
        rate = round(random.uniform(0.5, 2.0), 4)
        
        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "rate": rate,
            "result": round(amount * rate, 2)
        }

class MockEmailAPI:
    """Mock Email API"""
    
    @staticmethod
    def send_email(to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send email"""
        return {
            "status": "sent",
            "message_id": f"MSG{random.randint(100000, 999999)}",
            "to": to,
            "subject": subject,
            "timestamp": datetime.now().isoformat()
        }

# Mock API Registry
MOCK_APIS = {
    'weather': MockWeatherAPI(),
    'flights': MockFlightAPI(),
    'hotels': MockHotelAPI(),
    'safety': MockSafetyAPI(),
    'translation': MockTranslationAPI(),
    'geo': MockGeoAPI(),
    'stock': MockStockAPI(),
    'currency': MockCurrencyAPI(),
    'email': MockEmailAPI()
}

def get_mock_api(api_name: str):
    """Get mock API instance"""
    return MOCK_APIS.get(api_name)
