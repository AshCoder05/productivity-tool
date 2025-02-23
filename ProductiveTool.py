import argparse
import json
import datetime

def parse_time_slot_duration(time_slot):
    """
    Parses a time slot string (e.g., "7:30 PM - 9 PM") and calculates the duration in hours.
    Handles AM/PM and cases where the time slot crosses midnight.
    """
    try:
        start_str, end_str = time_slot.split('-')
        start_time = datetime.datetime.strptime(start_str.strip(), "%I:%M %p").time()
        end_time = datetime.datetime.strptime(end_str.strip(), "%I:%M %p").time()
        
        # Handle time slots crossing midnight
        if end_time <= start_time:
            end_datetime = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), end_time)
        else:
            end_datetime = datetime.datetime.combine(datetime.date.today(), end_time)
        
        start_datetime = datetime.datetime.combine(datetime.date.today(), start_time)
        duration = (end_datetime - start_datetime).total_seconds() / 3600  # Convert seconds to hours
        return start_time, end_time, duration
    except ValueError:
        print(f"⚠️ Warning: Invalid time slot format -> {time_slot}. Expected format: 'X:XX AM/PM - Y:XX AM/PM'")
        return None, None, 0

def load_activities_from_json(file_path):
    """Loads activities from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: Activities file '{file_path}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in activities file '{file_path}'.")
        exit(1)

def load_availability_from_json(file_path):
    """Loads availability slots from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: Availability file '{file_path}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in availability file '{file_path}'.")
        exit(1)

def prioritize_activities(activities, availability):
    """
    Prioritizes activities based on available time slots, considering priority levels.
    Returns a suggested schedule mapping days to activities.
    """
    priority_order = {"High": 1, "Medium": 2, "Low": 3}  # Lower number = higher priority
    activities.sort(key=lambda x: priority_order.get(x.get("priority", "Low"), 3))
    
    suggested_schedule = {}
    for day, slots in availability.items():
        available_slots_for_day = list(slots)  # Copy to allow modifications
        suggested_schedule[day] = []
        
        for activity in activities:
            activity_name, duration = activity["name"], activity["duration"]
            
            for slot in available_slots_for_day[:]:  # Iterate over a copy to allow modifications
                start_time, end_time, slot_duration = parse_time_slot_duration(slot)
                if duration <= slot_duration:
                    suggested_schedule[day].append(f"✅ Suggestion: {activity_name} ({duration} hrs)")
                    available_slots_for_day.remove(slot)
                    break  # Move to the next activity

    return suggested_schedule

def main():
    """Main function to handle CLI input and generate the prioritized schedule."""
    parser = argparse.ArgumentParser(description="Prioritizes activities based on available time slots.")
    parser.add_argument('--activities-file', required=True, type=str, help="Path to a JSON file containing activity definitions.")
    parser.add_argument('--availability-file', required=True, type=str, help="Path to a JSON file containing weekly availability.")
    
    args = parser.parse_args()
    activities = load_activities_from_json(args.activities_file)
    availability = load_availability_from_json(args.availability_file)
    
    schedule = prioritize_activities(activities, availability)
    
    print("\n📅 Suggested Schedule:\n")
    for day, suggestions in schedule.items():
        print(f"{day}:")
        if suggestions:
            for suggestion in suggestions:
                print(f"  {suggestion}")
        else:
            print("  No activities suggested.")
        print("\n")
    
    if all(not suggestions for suggestions in schedule.values()):
        print("⚠️ Warning: No activities could be scheduled! Check your availability and durations.")

if __name__ == "__main__":
    main()
