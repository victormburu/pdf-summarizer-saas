def to_seconds(hours, minutes, seconds):
    """Convert hours, minutes, and seconds to total seconds."""
    return hours * 3600 + minutes * 60 + seconds

print("Welcome to the time converter!")

cont = "y"
while(cont.lower() == "y"):
    try:
        hours = int(input("Enter hours: "))
        minutes = int(input("Enter minutes: "))
        seconds = int(input("Enter seconds: "))
        
        total_seconds = to_seconds(hours, minutes, seconds)
        print(f"Total seconds: {total_seconds}")
    except ValueError:
        print("Invalid input. Please enter numeric values for hours, minutes, and seconds.")
    
    cont = input("Do you want to convert another time? (y/n): ")