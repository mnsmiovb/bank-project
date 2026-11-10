
from authentication import save_data

from datetime import date

def reset_daily_limits(accounts, username):
    user = accounts[username]
    today = str(date.today())

    if user["deposit_date"] != today:
        user["daily_deposit"] = 0
        user["deposit_date"] = today

    if user["withdrawal_date"] != today:
        user["daily_withdrawal"] = 0
        user["daily_fee_free_withdrawal"] = 0
        user["withdrawal_date"] = today

    save_data(accounts)

def deposit(accounts, username):
    reset_daily_limits(accounts, username)
    user = accounts[username]


    amountdep = int(input("Enter deposit amount: "))

    if amountdep <= 0:
        print("Invalid amount!")

    elif user["daily_deposit"] + amountdep <= 2000:
        user["balance"] += amountdep
        user["daily_deposit"] += amountdep
        accounts["atm"]["cash"] += amountdep

        save_data(accounts)

        print("Deposit successful!")
        print("New balance:", user["balance"])

    else:
        print("You can deposit", 2000 - user["daily_deposit"], "AZN")



