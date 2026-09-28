# City AI Assistant

An AI-powered city assistant built with **LangChain, Groq, OpenWeather API, Tavily, and Streamlit**. Ask natural-language questions about Indian city weather or the latest city news, and a LangChain agent selects the right tool.

## Features

- Get current weather information for Indian cities
- Search the web for the latest city news
- Select tools automatically with a LangChain agent
- Use Groq-powered language models
- Interact through a Streamlit chat interface
- Clear the current chat
- Keep API keys in environment variables instead of source control

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python | Programming language |
| Streamlit | Web interface |
| LangChain | Agent and tool orchestration |
| Groq | Language model provider |
| OpenWeather API | Current weather data |
| Tavily | Web search for news |
| Requests | HTTP requests |
| python-dotenv | Load environment variables from `.env` |

## Architecture

```text
User
  -> Streamlit chat UI
  -> LangChain AI agent
		-> Weather tool -> OpenWeather API
		-> News tool -> Tavily
  -> Agent response
  -> Streamlit UI
```

## Project Structure

```text
city-ai-assistant/
|-- app.py
|-- Agents.py
|-- requirements.txt
|-- README.md
|-- .gitignore
\-- .env                 # Create locally; do not commit
```

`app.py` is the Streamlit application. `Agents.py` contains a terminal-based agent example. The `.env` file is excluded from Git because it contains private API keys.

## Installation

1. Clone the repository:

	```bash
	git clone https://github.com/arju3610/city-ai-assistant.git
	cd city-ai-assistant
	```

2. Create and activate a virtual environment:

	```bash
	python -m venv .venv
	```

	Windows PowerShell:

	```powershell
	.venv\Scripts\Activate.ps1
	```

	Windows Command Prompt:

	```bat
	.venv\Scripts\activate.bat
	```

3. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

## API Keys

Create a `.env` file in the project directory:

```dotenv
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never commit or upload `.env`; it contains private credentials.

## Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL to open in your browser.

## Example Queries

- What is the weather in Ludhiana?
- What's the weather in Delhi?
- Give me the latest news about Mumbai.
- What is the weather in Amritsar?
- Give me the latest news about Punjab.

## How It Works

The LangChain agent uses two tools:

- **Weather:** Retrieves current conditions and temperature in Celsius from OpenWeather. City lookups are configured for India.
- **News:** Searches Tavily for recent news and returns up to three results.

The Streamlit interface keeps displayed messages in the current session. The agent receives each submitted question independently; persistent conversation memory is not currently configured.

## Future Improvements

- Add weather forecasts and temperature conversion
- Support more countries and weather icons
- Display news results as cards with clickable links
- Add persistent conversation memory
- Add tool approval controls in Streamlit
- Improve API error and rate-limit handling
- Deploy the application

## Author

**Arzu**

If you find this project useful, consider giving the repository a star.
