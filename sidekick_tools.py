from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
import os
import requests
from langchain_core.tools import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper



load_dotenv(override=True)
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"
serper = GoogleSerperAPIWrapper()


def safe_serper_search(query: str) -> str:
    """Run Serper search; return a string instead of raising on API errors."""
    try:
        return serper.run(query)
    except Exception as e:
        return (
            f"Web search failed ({type(e).__name__}: {e}). "
            "Check SERPER_API_KEY in .env (get a key at https://serper.dev). "
            "Use the browser tools or Wikipedia instead."
        )


_wikipedia = WikipediaAPIWrapper()


def safe_wikipedia_search(query: str) -> str:
    """Run Wikipedia lookup; return a string instead of raising on API/network errors."""
    try:
        return _wikipedia.run(query)
    except Exception as e:
        return (
            f"Wikipedia lookup failed ({type(e).__name__}: {e}). "
            "Try the web search tool or browser tools instead."
        )

async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


def push(text: str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})
    return "success"


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()


async def other_tools():
    push_tool = Tool(name="send_push_notification", func=push, description="Use this tool when you want to send a push notification")
    file_tools = get_file_tools()

    tool_search = Tool(
        name="search",
        func=safe_serper_search,
        description="Use this tool when you want to get the results of an online web search",
    )

    wiki_tool = Tool(
        name="wikipedia",
        func=safe_wikipedia_search,
        description="Look up factual summaries on Wikipedia. Input should be a search query or topic name.",
    )

    python_repl = PythonREPLTool()

    return file_tools + [push_tool, tool_search, python_repl, wiki_tool]

