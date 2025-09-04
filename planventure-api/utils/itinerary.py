from datetime import datetime, timedelta
from typing import Dict, List, Optional

def generate_default_itinerary(destination: str, start_date: str, end_date: str, trip_type: str = "leisure") -> str:
    """
    Generate a default itinerary template based on destination and trip duration.
    
    Args:
        destination: The trip destination
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        trip_type: Type of trip (leisure, business, adventure, family)
    
    Returns:
        Generated itinerary string
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        duration = (end - start).days + 1
        
        # Get destination-specific activities
        activities = get_destination_activities(destination.lower())
        
        # Generate itinerary based on trip type and duration
        if trip_type.lower() == "business":
            return generate_business_itinerary(destination, start, duration, activities)
        elif trip_type.lower() == "adventure":
            return generate_adventure_itinerary(destination, start, duration, activities)
        elif trip_type.lower() == "family":
            return generate_family_itinerary(destination, start, duration, activities)
        else:  # Default leisure trip
            return generate_leisure_itinerary(destination, start, duration, activities)
            
    except ValueError:
        return generate_generic_itinerary(destination, 3)

def get_destination_activities(destination: str) -> Dict[str, List[str]]:
    """
    Get destination-specific activities and attractions.
    
    Args:
        destination: Destination name (lowercase)
    
    Returns:
        Dictionary with categorized activities
    """
    destination_data = {
        "paris": {
            "landmarks": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Arc de Triomphe", "Sacré-Cœur"],
            "districts": ["Montmartre", "Marais", "Latin Quarter", "Champs-Élysées", "Saint-Germain"],
            "activities": ["Seine River cruise", "Wine tasting", "Café hopping", "Shopping at Galeries Lafayette"],
            "day_trips": ["Palace of Versailles", "Giverny (Monet's Garden)", "Fontainebleau"]
        },
        "tokyo": {
            "landmarks": ["Tokyo Tower", "Senso-ji Temple", "Meiji Shrine", "Imperial Palace", "Skytree"],
            "districts": ["Shibuya", "Harajuku", "Shinjuku", "Asakusa", "Ginza"],
            "activities": ["Sushi making class", "Karaoke", "Traditional tea ceremony", "Robot Restaurant"],
            "day_trips": ["Mount Fuji", "Nikko", "Kamakura", "Hakone"]
        },
        "new york": {
            "landmarks": ["Statue of Liberty", "Central Park", "Times Square", "Brooklyn Bridge", "Empire State Building"],
            "districts": ["Manhattan", "Brooklyn", "SoHo", "Greenwich Village", "Upper East Side"],
            "activities": ["Broadway show", "Museum visits", "Food tours", "High Line walk"],
            "day_trips": ["Statue of Liberty & Ellis Island", "Coney Island", "The Hamptons"]
        },
        "london": {
            "landmarks": ["Big Ben", "Tower Bridge", "Buckingham Palace", "Westminster Abbey", "London Eye"],
            "districts": ["Covent Garden", "Camden", "Notting Hill", "Shoreditch", "Kensington"],
            "activities": ["Afternoon tea", "Pub crawl", "Thames cruise", "West End show"],
            "day_trips": ["Windsor Castle", "Stonehenge", "Bath", "Canterbury"]
        }
    }
    
    # Check if destination matches any known destinations
    for city, data in destination_data.items():
        if city in destination.lower():
            return data
    
    # Return generic activities if destination not found
    return {
        "landmarks": ["Local landmarks", "Historic sites", "Main attractions"],
        "districts": ["City center", "Old town", "Cultural district"],
        "activities": ["Local cuisine tasting", "Walking tours", "Shopping", "Cultural experiences"],
        "day_trips": ["Nearby attractions", "Natural sites", "Historical locations"]
    }

def generate_leisure_itinerary(destination: str, start_date, duration: int, activities: Dict) -> str:
    """Generate a leisure-focused itinerary."""
    itinerary_lines = [f"🌍 {destination} Leisure Trip ({duration} days)\n"]
    
    current_date = start_date
    
    for day in range(1, duration + 1):
        day_date = current_date + timedelta(days=day-1)
        itinerary_lines.append(f"📅 Day {day} ({day_date.strftime('%A, %B %d')})")
        
        if day == 1:
            itinerary_lines.append("• Arrival and check-in")
            itinerary_lines.append("• Orientation walk around the area")
            if activities["landmarks"]:
                itinerary_lines.append(f"• Visit {activities['landmarks'][0]}")
        elif day == duration and duration > 1:
            itinerary_lines.append("• Final shopping and souvenir hunting")
            itinerary_lines.append("• Check-out and departure")
        else:
            # Assign different activities for middle days
            if day <= len(activities["landmarks"]) + 1:
                landmark_idx = (day - 2) % len(activities["landmarks"])
                itinerary_lines.append(f"• Explore {activities['landmarks'][landmark_idx]}")
            
            if day <= len(activities["districts"]) + 1:
                district_idx = (day - 2) % len(activities["districts"])
                itinerary_lines.append(f"• Wander through {activities['districts'][district_idx]}")
            
            if activities["activities"] and day % 2 == 0:
                activity_idx = ((day - 2) // 2) % len(activities["activities"])
                itinerary_lines.append(f"• {activities['activities'][activity_idx]}")
        
        itinerary_lines.append("")  # Empty line between days
    
    return "\n".join(itinerary_lines)

def generate_business_itinerary(destination: str, start_date, duration: int, activities: Dict) -> str:
    """Generate a business-focused itinerary."""
    itinerary_lines = [f"💼 {destination} Business Trip ({duration} days)\n"]
    
    current_date = start_date
    
    for day in range(1, duration + 1):
        day_date = current_date + timedelta(days=day-1)
        day_name = day_date.strftime('%A')
        itinerary_lines.append(f"📅 Day {day} ({day_date.strftime('%A, %B %d')})")
        
        if day == 1:
            itinerary_lines.append("• Arrival and hotel check-in")
            itinerary_lines.append("• Conference/meeting registration")
            itinerary_lines.append("• Welcome reception or networking dinner")
        elif day == duration and duration > 1:
            itinerary_lines.append("• Final meetings and wrap-up")
            itinerary_lines.append("• Check-out and departure")
        else:
            if day_name in ['Saturday', 'Sunday']:
                itinerary_lines.append("• Free time / Optional sightseeing")
                if activities["landmarks"]:
                    itinerary_lines.append(f"• Optional visit to {activities['landmarks'][0]}")
            else:
                itinerary_lines.append("• Morning: Conference sessions/meetings")
                itinerary_lines.append("• Lunch: Business networking")
                itinerary_lines.append("• Afternoon: Workshops/client meetings")
                itinerary_lines.append("• Evening: Business dinner")
        
        itinerary_lines.append("")
    
    return "\n".join(itinerary_lines)

def generate_adventure_itinerary(destination: str, start_date, duration: int, activities: Dict) -> str:
    """Generate an adventure-focused itinerary."""
    itinerary_lines = [f"🏔️ {destination} Adventure Trip ({duration} days)\n"]
    
    current_date = start_date
    
    for day in range(1, duration + 1):
        day_date = current_date + timedelta(days=day-1)
        itinerary_lines.append(f"📅 Day {day} ({day_date.strftime('%A, %B %d')})")
        
        if day == 1:
            itinerary_lines.append("• Arrival and gear check")
            itinerary_lines.append("• Adventure briefing and safety orientation")
            itinerary_lines.append("• Light exploration of local area")
        elif day == duration and duration > 1:
            itinerary_lines.append("• Final adventure activity")
            itinerary_lines.append("• Equipment return and departure")
        else:
            # Add adventure activities
            if activities["day_trips"] and day % 2 == 0:
                trip_idx = ((day - 2) // 2) % len(activities["day_trips"])
                itinerary_lines.append(f"• Full day trip to {activities['day_trips'][trip_idx]}")
            else:
                itinerary_lines.append("• Morning: Outdoor adventure activity")
                itinerary_lines.append("• Afternoon: Exploration and nature walks")
                itinerary_lines.append("• Evening: Local cultural experience")
        
        itinerary_lines.append("")
    
    return "\n".join(itinerary_lines)

def generate_family_itinerary(destination: str, start_date, duration: int, activities: Dict) -> str:
    """Generate a family-friendly itinerary."""
    itinerary_lines = [f"👨‍👩‍👧‍👦 {destination} Family Trip ({duration} days)\n"]
    
    current_date = start_date
    
    for day in range(1, duration + 1):
        day_date = current_date + timedelta(days=day-1)
        itinerary_lines.append(f"📅 Day {day} ({day_date.strftime('%A, %B %d')})")
        
        if day == 1:
            itinerary_lines.append("• Family check-in and room setup")
            itinerary_lines.append("• Nearby park or family-friendly area exploration")
            itinerary_lines.append("• Early dinner at family restaurant")
        elif day == duration and duration > 1:
            itinerary_lines.append("• Final family activity")
            itinerary_lines.append("• Souvenir shopping")
            itinerary_lines.append("• Check-out and departure")
        else:
            itinerary_lines.append("• Morning: Family-friendly attraction")
            if activities["landmarks"]:
                landmark_idx = (day - 2) % len(activities["landmarks"])
                itinerary_lines.append(f"• Visit {activities['landmarks'][landmark_idx]} (family-friendly areas)")
            itinerary_lines.append("• Afternoon: Rest time / Kid-friendly activities")
            itinerary_lines.append("• Evening: Family dinner and relaxation")
        
        itinerary_lines.append("")
    
    return "\n".join(itinerary_lines)

def generate_generic_itinerary(destination: str, duration: int) -> str:
    """Generate a generic itinerary template."""
    itinerary_lines = [f"✈️ {destination} Trip ({duration} days)\n"]
    
    for day in range(1, duration + 1):
        itinerary_lines.append(f"📅 Day {day}")
        
        if day == 1:
            itinerary_lines.append("• Arrival and check-in")
            itinerary_lines.append("• Explore nearby area")
            itinerary_lines.append("• Welcome dinner")
        elif day == duration and duration > 1:
            itinerary_lines.append("• Final sightseeing")
            itinerary_lines.append("• Shopping for souvenirs")
            itinerary_lines.append("• Check-out and departure")
        else:
            itinerary_lines.append("• Morning: Main attraction visit")
            itinerary_lines.append("• Afternoon: Local experience")
            itinerary_lines.append("• Evening: Dining and relaxation")
        
        itinerary_lines.append("")
    
    return "\n".join(itinerary_lines)

def get_itinerary_suggestions(destination: str) -> Dict[str, str]:
    """
    Get multiple itinerary suggestions for a destination.
    
    Args:
        destination: Trip destination
    
    Returns:
        Dictionary with different itinerary types
    """
    sample_dates = "2024-10-15"
    end_dates = "2024-10-20"
    
    return {
        "leisure": generate_default_itinerary(destination, sample_dates, end_dates, "leisure"),
        "business": generate_default_itinerary(destination, sample_dates, end_dates, "business"),
        "adventure": generate_default_itinerary(destination, sample_dates, end_dates, "adventure"),
        "family": generate_default_itinerary(destination, sample_dates, end_dates, "family")
    }
