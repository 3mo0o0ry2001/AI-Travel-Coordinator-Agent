# AI Travel Coordinator Agent ✈️🤖

An autonomous AI agent designed to streamline travel planning by orchestrating real-time flight searches and personal schedule verification. This project demonstrates an **Agentic Workflow** where the LLM acts as the decision-making "brain" and Python functions serve as "actuators" to interact with external data.

## 🌟 Key Features

* **Autonomous Reasoning**: Uses a ReAct (Reasoning + Acting) pattern to analyze user requests and determine the necessary steps for fulfillment.
* **Live Flight Search**: Integrated with **SerpApi (Google Flights)** to fetch real-time availability, pricing, and booking links from the internet.
* **Intelligent Schedule Verification**: Automatically cross-references travel dates with a local calendar to prevent booking conflicts.
* **Smart Recommendation**: Analyzes multiple flight options to suggest the most cost-effective choice for the user.

## 🏗️ Project Architecture

The system follows a decoupled architecture to ensure scalability and ease of tool integration:

1. **Orchestrator (`main.py`)**: Manages the conversation state and the reasoning loop.
2. **Actuators (`tools.py`)**: Contains the logic for external API calls and local database interactions, defined via JSON schemas for the LLM.
3. **Environment Configuration (`.env`)**: Safely stores API credentials for OpenAI and SerpApi.

## 🚀 Getting Started

### Prerequisites
* **Python 3.8+**
* **OpenAI API Key**
* **SerpApi Key** (for Google Flights)

### Installation
1. **Clone the repository**:
   ```bash
   git clone [https://github.com/3mo0o0ry2001/AI-Travel-Coordinator-Agent.git](https://github.com/3mo0o0ry2001/AI-Travel-Coordinator-Agent.git)
   cd AI-Travel-Coordinator-Agent

2. **Install dependencies**:
```bash
pip install -r requirements.txt

3. **Configure environment**:
'''bash
OPENAI_API_KEY=your_key_here
SERP_API_KEY=your_key_here
