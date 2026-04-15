def book_consultation(name, email):
    return f"Consultation booked for {name}. Confirmation sent to {email}."

def generate_quote(service):
    pricing = {
        "website": "$500 - $1,500 depending on complexity",
        "branding": "$300 - $800 for full brand identity",
        "seo": "$200 - $600 per month",
        "social_media": "$150 - $400 per month",
        "automation": "$800 - $2,000 depending on scope",
        "ai system": "$1,500 - $5,000 depending on requirements"
    }
    return pricing.get(service.lower(), "Custom pricing required — please book a consultation for a tailored quote.")