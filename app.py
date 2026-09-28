import streamlit as st
import os
import requests

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from tavily import TavilyClient
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call

# =========================================================
# CONFIG
# =========================================================

load_dotenv()

st.set_page_config(page_title="City AI Assistant", page_icon="🌆", layout="wide")

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* Header */
.hero {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 17px;
    opacity: 0.9;
}

/* Cards */
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

/* Tool badges */
.tool-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    background-color: #eef2ff;
    color: #4f46e5;
    font-size: 13px;
    margin-right: 5px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="hero">
    <h1>🌆 City AI Assistant</h1>
    <p>Your intelligent assistant for weather and latest city news.</p>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# WEATHER TOOL
# =========================================================


@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return "OpenWeather API key is missing."

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if str(data.get("cod")) != "200":
            return f"Error: {data.get('message', 'Could not fetch weather')}"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"Weather in {city}: {desc}, {temp}°C"

    except Exception as e:
        return f"Weather API error: {str(e)}"


# =========================================================
# NEWS TOOL
# =========================================================

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def get_news(city: str) -> str:
    """Get latest news about a city."""

    try:

        response = tavily_client.search(
            query=f"latest news in {city}", search_depth="basic", max_results=3
        )

        results = response.get("results", [])

        if not results:
            return f"No news found for {city}"

        news_list = []

        for r in results:

            title = r.get("title", "No title")
            url = r.get("url", "")
            snippet = r.get("content", "")

            news_list.append(f"- {title}\n" f"  🔗 {url}\n" f"  📝 {snippet[:150]}...")

        return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)

    except Exception as e:
        return f"News API error: {str(e)}"


# =========================================================
# LLM
# =========================================================


@st.cache_resource
def get_llm():

    return ChatGroq(model="openai/gpt-oss-20b")


llm = get_llm()


# =========================================================
# HUMAN APPROVAL
# =========================================================


@wrap_tool_call
def human_approval(request, handler):

    tool_name = request.tool_call["name"]

    # Streamlit cannot use input() like terminal apps.
    # For this UI version, tools are automatically approved.

    return handler(request)


# =========================================================
# AGENT
# =========================================================


@st.cache_resource
def create_city_agent():

    return create_agent(
        llm,
        tools=[get_weather, get_news],
        system_prompt="""
        You are a helpful city assistant.

        You can:
        1. Get current weather of Indian cities.
        2. Search for latest news about cities.

        Use the appropriate tool when the user asks
        about weather or latest news.
        """,
        middleware=[human_approval],
    )


agent = create_city_agent()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🌆 City AI")

    st.markdown("""
    ### Available Tools

    🌦️ **Weather**

    Get current weather information.

    📰 **News**

    Search latest city news.

    🤖 **AI Agent**

    LangChain agent decides which tool to use.
    """)

    st.divider()

    st.markdown("### 💡 Try asking")

    example_questions = [
        "What is the weather in Ludhiana?",
        "What's the weather in Delhi?",
        "Give me latest news about Mumbai",
        "What is the weather in Amritsar?",
        "Give me latest news about Punjab",
    ]

    for question in example_questions:
        st.markdown(f"• {question}")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []
        st.rerun()


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# DISPLAY OLD MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input("Ask me about weather or city news...")


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_input:

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_input)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            try:

                result = agent.invoke(
                    {"messages": [{"role": "user", "content": user_input}]}
                )

                response = result["messages"][-1].content

            except Exception as e:

                response = f"❌ Something went wrong:\n\n" f"`{str(e)}`"

        st.markdown(response)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": response})
