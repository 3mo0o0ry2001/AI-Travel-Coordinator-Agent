import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import search_flights_live, check_calendar, book_flight, tools_schema
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Map tool names to actual functions for execution
available_actions = {
    "search_flights_live": search_flights_live, # New name
    "check_calendar": check_calendar,
    "book_flight": book_flight,
}

def run_agent(user_query):
    # System Prompt defines identity and operational rules
    messages = [
        {"role": "system", "content": """
        You are a proactive Travel Assistant.
        Operational Protocol:
        1. Always search for flights first.
        2. ALWAYS check the user's calendar for the flight date before booking.
        3. If a conflict exists, do not book; instead, report the conflict.
        4. If free, book the cheapest available flight.
        Current Date: 2026-01-20.
        """},
        {"role": "user", "content": user_query}
    ]

    print("🤖 Thinking...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools_schema,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)
        
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            # Execute tool and get JSON result
            action_result = available_actions[func_name](**func_args)
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": func_name,
                "content": action_result,
            })
        
        # Second call to provide the final reasoned response
        print("🤖 Analyzing results...")
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return final_response.choices[0].message.content
    
    return response_message.content

if __name__ == "__main__":
    query = "Find a flight from DXB to CAI on 2026-01-27 and book the cheapest one."
    print(f"Request: {query}\n" + "-"*50)
    print(f"Final Agent Output:\n{run_agent(query)}")