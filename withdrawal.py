import uuid
import datetime
from feature.file_storage import save_data
# from authentication import save_data


def withdrawal(data, username):
    user = data["users"][username]

    # Reset daily limits if it is a new day
    today = str(datetime.date.today())
    if user["daily"]["date"] != today:
        user["daily"]["date"] = today
        user["daily"]["deposited"] = 0
        user["daily"]["withdrawn"] = 0
        user["daily"]["transfer_count"] = 0

    # --- SAFE INPUT VALIDATION ---
    try:
        amount = float(input("Enter withdrawal amount (AZN): "))
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return

    # Convert entered amount to qepiks
    amount_qepik = amount * 100

    # --- PRE-WITHDRAWAL VALIDATION CHECKS ---
    if amount <= 0 or amount_qepik%1!=0:
        print("Invalid amount!")

    # Check daily withdrawal limit (max 1000 AZN = 100,000 qepiks)
    elif user["daily"]["withdrawn"] + amount_qepik > 100000:
        print("Daily withdrawal limit is 1000 AZN!")

    
    # Check if ATM has enough cash reserve
    elif amount_qepik > data["atm_cash"]:
        print("Not enough cash in ATM!")

    # --- COMMISSION CALCULATION ---
    # First 500 AZN (50,000 qepiks) per day are fee-free
    else:
        free_amount = max(0, 50000 - user["daily"]["withdrawn"])
        taxable_amount = max(0, amount_qepik - free_amount)
        commission = round(taxable_amount * 0.02) # 2% fee on the excess portion
        total_cost = amount_qepik + commission  # Total deduction (amount + fee)

        # Check if user has enough balance including commission
        if total_cost > user["balance"]:
            print("Not enough balance!")

        else:
            # --- UPDATE BALANCES AND ATM CASH ---
            user["balance"] -= total_cost
            user["daily"]["withdrawn"] += amount_qepik
            data["atm_cash"] -= amount_qepik  # Decrease ATM cash only by requested cash amount (excluding fee)

            # --- RECORD TRANSACTION HISTORY ---
            user["history"].append({
                "id": str(uuid.uuid4()),
                "username": username,
                "type": "withdraw",
                "amount": amount*100,
                "date": today
            })

            save_data(data)
            print("Withdrawal successful!")
            print("New balance:", user["balance"] / 100, "AZN")


def daily_limits(accounts, username):
    user = accounts["users"][username]


    # Check date change to keep limit statistics accurate
    today = str(datetime.date.today())

    if user["daily"]["date"] != today:
        user["daily"]["date"] = today
        user["daily"]["deposited"] = 0
        user["daily"]["withdrawn"] = 0

    # Calculate remaining limits
    deposit_remaining = 200000 - user["daily"]["deposited"]
    withdrawal_remaining = 100000 - user["daily"]["withdrawn"]
    fee_free_remaining = max(0, 50000 - user["daily"]["withdrawn"])

    # Display limit details to the user (divided by 100 to show in AZN)
    print("\n===== DAILY LIMITS =====")

    print("\nDaily deposit limit:")
    print("Used:", user["daily"]["deposited"] / 100, "AZN")
    print("Remaining:", deposit_remaining / 100, "AZN")

    print("\nDaily withdrawal limit:")
    print("Used:", user["daily"]["withdrawn"] / 100, "AZN")
    print("Remaining:", withdrawal_remaining / 100, "AZN")

    print("\nFee-free withdrawal:")
    print("Remaining:", fee_free_remaining / 100, "AZN")


