from authentication import save_data

from datetime import date

def withdrawal(accounts, username):
    reset_daily_limits(accounts, username)
    user = accounts[username]

    amountwithdraw = int(input("Enter withdrawal amount: "))

    if amountwithdraw <= 0:
        print("Invalid amount!")

    elif amountwithdraw + user["daily_withdrawal"] > 1000:
        print("Daily withdrawal limit exceeded!")

    elif amountwithdraw > accounts["atm"]["cash"]:
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
            accounts["atm"]["cash"] -= amountwithdraw

            save_data(accounts)

            print("Withdrawal successful!")
            print("Commission:", commission, "AZN")
            print("New balance:", user["balance"])