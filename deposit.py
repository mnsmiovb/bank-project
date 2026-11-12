import datetime
import uuid
#from feature.file_storage import save_data
from authentication import save_data


def deposit(data, username):
    user = data["users"][username]

    # Reset daily limits if it is a new day
    today = str(datetime.date.today())
    if user["daily"]["date"] != today:
        user["daily"]["date"] = today
        user["daily"]["deposited"] = 0
        user["daily"]["withdrawn"] = 0
        

    try:
        amount = int(input("Enter deposit amount (AZN): "))
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return

    if amount <= 0:
        print("Invalid amount!")

    elif user["daily"]["deposited"] + amount * 100 <= 200000 and user["daily"]["limit"]<5:
        user["balance"] += amount * 100
        user["daily"]["deposited"] += amount * 100
        data["atm_cash"] += int(amount * 100)
        

                
        data["transactions"].append({
                "id": str(uuid.uuid4()),
                "username": username,
                "type": "deposit",
                "amount": amount*100,
                "date": today
        })
        save_data(data)

        print("Deposit successful!")
        print("New balance:", user["balance"] / 100, "AZN")

    else:
        remaining = 200000 - user["daily"]["deposited"]
        print("You can deposit", remaining / 100, "AZN today.")