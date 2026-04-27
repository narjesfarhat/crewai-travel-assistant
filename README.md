✈️ Travel CrewAI — Multi-Agent Travel Planner (Local Qwen Model)
A fully local AI-powered travel planning assistant built with CrewAI 1.9, Python, and Ollama. This project uses a team of specialized AI agents to collaboratively create complete travel plans — including flights, hotels, itineraries, and travel advice — all without relying on cloud APIs or paid services.
Designed for developers, AI enthusiasts, and learners exploring multi-agent systems, this project demonstrates how autonomous agents can coordinate to solve real-world planning tasks entirely offline.

🚀 Key Features
✅ 100% Local AI Execution
Run everything on your own machine using Ollama with local language models such as:


Qwen2.5 (recommended)


Llama 3.1


Other Ollama-supported models


✅ No API Keys Required
No OpenAI keys, no external subscriptions, no cloud dependency.
✅ Multi-Agent Collaboration with CrewAI
Four specialized agents work together:
AgentRole🛫 Flight AgentFinds the best available flight options (demo dataset / mock search)🏨 Hotel AgentRecommends hotels based on budget and preferences🗺️ Tourism AgentBuilds a personalized day-by-day travel itinerary💡 Advisor AgentProvides visa tips, safety advice, local customs, and packing guidance
✅ Interactive CLI Experience
Simple command-line interface for entering travel details and receiving a complete plan.
✅ Modular & Extendable
Clean Python structure that can easily be upgraded with APIs, UI frontends, exports, and more.

🧠 Tech Stack


Python 3.10 – 3.12


CrewAI 1.9.x


crewai-tools


Ollama


Qwen2.5 / Llama 3.1



📦 Installation
1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/crewai-travel-assistant.gitcd crewai-travel-assistant

2️⃣ Create a Virtual Environment
Windows
python -m venv venvvenv\Scripts\activate
macOS / Linux
python3 -m venv venvsource venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

🤖 Install & Run Local Model (Ollama)
1️⃣ Install Ollama
Download and install:
👉 https://ollama.com/download

2️⃣ Pull a Model
Recommended:
ollama pull qwen2.5
Alternative:
ollama pull llama3.1

3️⃣ Start Ollama
ollama serve

⚙️ Configure the Model
Open travel_crew.py and set:
LLM_MODEL = "ollama/qwen2.5"
Use the exact model name shown by:
ollama list

▶️ Run the Application
python travel_crew.py

💬 User Input Flow
The assistant will ask for:


Departure city


Destination city


Departure date


Return date


Budget level


Number of travelers


Travel interests


Example:
From: AmsterdamTo: TokyoDates: June 10 - June 20Budget: MediumTravelers: 2Interests: Food, culture, nature

📌 Example Output
The AI agents collaborate to generate:
✈️ Best Flight Option
Recommended route with estimated pricing.
🏨 Best Hotel Recommendation
Hotel matched to budget and location.
🗺️ Personalized Itinerary
Day-by-day travel schedule with activities.
💡 Smart Travel Advice


Visa requirements


Safety notes


Currency tips


Packing checklist


Cultural etiquette



📁 Project Structure
crewai-travel-assistant/│── travel_crew.py│── requirements.txt│── README.md└── optional_assets/

📝 Notes


Runs fully offline after model download


No API keys required


Qwen2.5 recommended for stronger reasoning


Works on Windows, macOS, and Linux


Easily customizable for your own travel use cases



🔮 Future Enhancements
Planned improvements:


Real-time flight API integration


Real hotel booking APIs


Interactive map support


Gradio / Streamlit web interface


PDF itinerary export


Multi-language support


Voice assistant mode



🤝 Contributing
Contributions are welcome.
If you'd like to improve this project:


Fork the repository


Create a feature branch


Submit a pull request



💛 Author
Narjes
AI Enthusiast • SEO Analyst • Multi-Agent Systems Learner

⭐ Support
If you found this project useful:


Star the repository ⭐


Share it with others


Build your own version



📜 License
This project is open-source and available under the MIT License.
