import uuid
import datetime
#from feature.file_storage import save_data
from authentication import save_data


def withdrawal(data, username):
    user = data["users"][username]

    # Reset daily limits if it is a new day
    today = str(datetime.date.today())
    if user["daily"]["date"] != today:
        user["daily"]["date"] = today
        user["daily"]["deposited"] = 0
        user["daily"]["withdrawn"] = 0

    # Безопасный ввод: если пользователь введет буквы, программа не упадет
    try:
        amount = float(input("Enter withdrawal amount (AZN): "))
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return

    amount_qepik = amount * 100

    if amount <= 0:
        print("Invalid amount!")

    elif user["daily"]["withdrawn"] + amount_qepik > 100000:
        print("Daily withdrawal limit is 1000 AZN!")

    elif amount_qepik > data["atm_cash"]:
        print("Not enough cash in ATM!")

    else:
        free_amount = max(0, 50000 - user["daily"]["withdrawn"])
        taxable_amount = max(0, amount_qepik - free_amount)
        commission = round(taxable_amount * 0.02)
        total_cost = amount_qepik + commission

        if total_cost > user["balance"]:
            print("Not enough balance!")

        else:
            user["balance"] -= total_cost
            user["daily"]["withdrawn"] += amount_qepik
            data["atm_cash"] -= amount_qepik

            data["transactions"].append({
                "id": str(uuid.uuid4()),
                "username": username,
                "type": "deposit",
                "amount": amount*100,
                "date": today
            })

            save_data(data)
            print("Withdrawal successful!")
            print("New balance:", user["balance"] / 100, "AZN")


def daily_limits(accounts, username):
    user = accounts["users"][username]

    # Reset daily limits if it is a new day
    today = str(datetime.date.today())

    if user["daily"]["date"] != today:
        user["daily"]["date"] = today
        user["daily"]["deposited"] = 0
        user["daily"]["withdrawn"] = 0

    deposit_remaining = 200000 - user["daily"]["deposited"]
    withdrawal_remaining = 100000 - user["daily"]["withdrawn"]
    fee_free_remaining = max(0, 50000 - user["daily"]["withdrawn"])

    print("\n===== DAILY LIMITS =====")

    print("\nDaily deposit limit:")
    print("Used:", user["daily"]["deposited"] / 100, "AZN")
    print("Remaining:", deposit_remaining / 100, "AZN")

    print("\nDaily withdrawal limit:")
    print("Used:", user["daily"]["withdrawn"] / 100, "AZN")
    print("Remaining:", withdrawal_remaining / 100, "AZN")

    print("\nFee-free withdrawal:")
    print("Remaining:", fee_free_remaining / 100, "AZN")


