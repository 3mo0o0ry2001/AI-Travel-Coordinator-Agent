import os
import json
import requests
from dotenv import load_dotenv

# تحميل مفاتيح الـ API من ملف .env
load_dotenv()

# --- بيانات التقويم الوهمية (Mock Data) ---
# تستخدم لاختبار قدرة الـ Agent على اكتشاف التعارض في المواعيد
MY_CALENDAR = [
    {"date": "2026-01-23", "event": "Project Presentation", "time": "10:00 AM"},
]

# --- وظائف الأدوات (Actuators) ---

def search_flights_live(origin, dest, date):
    """
    Search for real-time flights on the internet via SerpApi (Google Flights).
    Requires airport codes (e.g., 'DXB') and date (YYYY-MM-DD).
    """
    # تعريف الرابط بشكل صحيح لتجنب NameError
    url = "https://serpapi.com/search.json" 
    
    print(f"🌐 Action: Fetching live flights from {origin} to {dest} on {date}...")
    
    # إعداد البارامترات مع تحديد النوع '2' لرحلات الذهاب فقط (One-way)
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": dest,
        "outbound_date": date,
        "type": "2",  # One-way flight
        "currency": "AED",
        "api_key": os.getenv("SERP_API_KEY")
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # تتبع الأخطاء المرجعة من الـ API
        if "error" in data:
            print(f"❌ API Error: {data['error']}")
            return json.dumps({"error": data["error"]})

        # جلب الرحلات الأفضل (Best Flights) أو الرحلات الأخرى المتاحة
        flights = data.get("best_flights") or data.get("other_flights") or []
        
        if not flights:
            return "No flights found on the internet for this date."

        # تبسيط البيانات لتقليل استهلاك الـ Tokens
        results = []
        for f in flights[:5]:
            results.append({
                "airline": f["flights"][0]["airline"],
                "price": f["price"],
                "duration": f["total_duration"],
                "link": data.get("search_metadata", {}).get("google_flights_url")
            })
            
        return json.dumps(results)
    
    except Exception as e:
        return json.dumps({"error": f"Connection failed: {str(e)}"})

def check_calendar(date):
    """
    Check the user's personal schedule for any event conflicts.
    """
    print(f"📅 Action: Checking calendar for {date}...")
    events = [e for e in MY_CALENDAR if e["date"] == date]
    return json.dumps({"status": "busy", "conflicts": events}) if events else json.dumps({"status": "free"})

def book_flight(flight_id):
    """
    Simulate the booking process once a flight and date are confirmed.
    """
    print(f"🎫 Action: Finalizing booking for ID: {flight_id}...")
    return json.dumps({"status": "confirmed", "booking_id": f"RES-{flight_id}-2026"})

# --- تعريف هيكل الأدوات للـ OpenAI (Tools Schema) ---
# هذا هو الكتالوج الذي يقرأه الـ LLM ليقرر أي أداة يستخدم

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_flights_live",
            "description": "Get real-time flight options and prices from the internet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "3-letter airport code"},
                    "dest": {"type": "string", "description": "3-letter airport code"},
                    "date": {"type": "string", "description": "YYYY-MM-DD format"},
                },
                "required": ["origin", "dest", "date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check if the user has scheduled events on a specific date.",
            "parameters": {
                "type": "object",
                "properties": {"date": {"type": "string"}},
                "required": ["date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_flight",
            "description": "Complete the flight booking. Call this only after checking the calendar.",
            "parameters": {
                "type": "object",
                "properties": {"flight_id": {"type": "string"}},
                "required": ["flight_id"],
            },
        },
    }
]