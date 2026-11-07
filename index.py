
import json

file = open("data.json", "r")
data = json.load(file)
file.close()

username = input("Enter username: ")
user = data["users"][username]

def deposit(amountdep):
    amountdep = int(input("Enter deposit amount: "))

    if amountdep <= 0:
        print("Invalid amount!")

    elif user["daily_deposit"] + amountdep <= 2000:
        user["balance"] += amountdep
        user["daily_deposit"] += amountdep
        data["atm"]["cash"] += amountdep

        file = open("data.json", "w")
        json.dump(data, file, indent=4)
        file.close()

        print("Deposit successful!")
        print("New balance:", user["balance"])

    else:
        print("You can deposit", 2000 - user["daily_deposit"], "AZN")


def withdrawal(amountwithdraw):
    amountwithdraw = int(input("Enter withdrawal amount: "))

    if amountwithdraw <= 0:
        print("Invalid amount!")

    elif amountwithdraw + user["daily_withdrawal"] > 1000:
        print("Daily withdrawal limit exceeded!")

    elif amountwithdraw > data["atm"]["cash"]:
        print("Not enough cash in ATM!")

    else:
        remaining_free = max(0, 500 - user["daily_withdrawal"])
        taxable_amount = max(0, amountwithdraw - remaining_free)
        commission = taxable_amount * 0.02
        total_cost = amountwithdraw + commission

        if total_cost > user["balance"]:
            print("Not enough balance!")

        else:
            user["balance"] -= total_cost
            user["daily_withdrawal"] += amountwithdraw
            user["daily_fee_free_withdrawal"] += min(amountwithdraw, remaining_free)
            data["atm"]["cash"] -= amountwithdraw

            file = open("data.json", "w")
            json.dump(data, file, indent=4)
            file.close()

            print("Withdrawal successful!")
            print("Commission:", commission, "AZN")
            print("New balance:", user["balance"])
