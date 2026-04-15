import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import book_consultation, generate_quote

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def kaltum_agent(user_input):

    user_input_lower = user_input.lower()

    # 👉 Booking Intent
    if "book" in user_input_lower:
        return book_consultation("Client", "client@email.com")

    # 👉 Pricing Intent
    if "price" in user_input_lower or "quote" in user_input_lower:
        return generate_quote("website")

    # 👉 Default AI response (FIXED)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Kaltum AI assistant. Help users professionally."},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content