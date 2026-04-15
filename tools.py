def book_consultation(name, email):
    return f"✅ Consultation booked for {name}. Confirmation sent to {email}"

def generate_quote(service):
    pricing = {
        "website": "$500",
        "automation": "$800",
        "ai system": "$1500"
    }
    return pricing.get(service.lower(), "Custom pricing required")