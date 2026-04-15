import os
from anthropic import Anthropic
from dotenv import load_dotenv
from tools import book_consultation, generate_quote

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

sessions = {}
MAX_HISTORY = 20

SYSTEM_PROMPT = """You are Kaltum, a professional AI assistant for a consulting and web services business. You help users book consultations, get price quotes, and learn about services. Be warm, professional, and concise. Collect name and email before booking. Ask which service before quoting. Services: website, branding, seo, social_media."""

TOOLS = [
    {
        "name": "book_consultation",
        "description": "Books a consultation. Only call after collecting client name and email.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Client full name"},
                "email": {"type": "string", "description": "Client email address"}
            },
            "required": ["name", "email"]
        }
    },
    {
        "name": "generate_quote",
        "description": "Generates a price quote for a service.",
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string", "description": "Service: website, branding, seo, or social_media"}
            },
            "required": ["service"]
        }
    }
]


def process_tool_call(tool_name, tool_input):
    if tool_name == "book_consultation":
        return book_consultation(tool_input["name"], tool_input["email"])
    elif tool_name == "generate_quote":
        return generate_quote(tool_input["service"])
    return "Unknown tool."


def kaltum_agent(user_input, session_id="default"):
    if session_id not in sessions:
        sessions[session_id] = []

    history = sessions[session_id]
    history.append({"role": "user", "content": user_input})

    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    for _ in range(5):
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=history
        )

        history.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            text_blocks = [b.text for b in response.content if hasattr(b, "text")]
            return " ".join(text_blocks)

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = process_tool_call(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            history.append({"role": "user", "content": tool_results})
        else:
            break

    return "I am sorry, something went wrong. Please try again."


def clear_session(session_id="default"):
    if session_id in sessions:
        del sessions[session_id]