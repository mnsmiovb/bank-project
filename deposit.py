
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



