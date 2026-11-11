import datetime
from feature.file_storage import save_data


def withdrawal(accounts, username):
    user = accounts["users"][username]

    # Reset daily limits if it is a new day
    today = str(datetime.date.today())
    if user["daily"]["date"] != today:
        user["daily"]["date"] = today
        user["daily"]["deposited"] = 0
        user["daily"]["withdrawn"] = 0

    # Безопасный ввод: если пользователь введет буквы, программа не упадет
    try:
        amount = int(input("Enter withdrawal amount (AZN): "))
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return

    amount_qepik = amount * 100

    if amount <= 0:
        print("Invalid amount!")

    elif user["daily"]["withdrawn"] + amount_qepik > 100000:
        print("Daily withdrawal limit is 1000 AZN!")

    elif amount_qepik > accounts["atm_cash"]:
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
            accounts["atm_cash"] -= amount_qepik

            user["history"].append({
                "type": "withdrawal",
                "amount": amount_qepik,
                "fee": commission,
                "date": today
            })

            save_data(accounts)
            print("Withdrawal successful!")
            print("New balance:", user["balance"] / 100, "AZN")