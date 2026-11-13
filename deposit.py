import datetime
import uuid
from feature.file_storage import save_data
# from authentication import save_data


def deposit(data, username):
    # Retrieve the specific user dictionary from the global data structure
    user=data["users"][username]

    # Reset daily limits if it is a new day
    today = str(datetime.date.today())
    if user["daily"]["date"] != today:
        user["daily"]["date"] = today
        user["daily"]["deposited"] = 0
        user["daily"]["withdrawn"] = 0
        

    # --- INPUT VALIDATION ---
    # Try-except block prevents program crash if the user enters letters instead of numbers
    try:
        amount = int(input("Enter deposit amount (AZN): "))
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return

    # --- CHECKS AND BUSINESS LOGIC ---
    if amount <= 0:
        print("Invalid amount!")

    # Check daily deposit limit (max 2000 AZN = 200,000 qepiks) 
    # and additional condition for transaction limit count
    elif user["daily"]["deposited"] + amount * 100 <= 200000:

        # Convert Manats to qepiks (* 100) for precise financial calculations (avoiding float errors)
        user["balance"] += amount * 100
        user["daily"]["deposited"] += amount * 100
        data["atm_cash"] += int(amount * 100)
        

        # --- TRANSACTION HISTORY ---
        # Generate a unique transaction ID (uuid) and record the operation in history
        user["history"].append({
                "id": str(uuid.uuid4()),
                "username": username,
                "type": "deposit",
                "amount": amount*100,
                "date": today
        })

        # Save updated data to the file
        save_data(data)

        print("Deposit successful!")
        print("New balance:", user["balance"] / 100, "AZN")

    else:
        # If limit is exceeded, show how much more can be deposited today
        remaining = 200000 - user["daily"]["deposited"]
        if remaining==0:
            print("You have reached the deposit limit")
        else:
            print("You can deposit", remaining / 100, "AZN today.")