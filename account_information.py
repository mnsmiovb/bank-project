
def account_information(data, username):
    user = data['users'][username]

    account_number = user["account_number"]

    # Convert balance from qepik to AZN
    balance = user["balance"]
    whole_azn = balance // 100
    qepik = balance % 100

    # Temporary account status
    status = "Active"

    print("\n========== ACCOUNT INFORMATION ==========")
    print("Account Holder:", username)
    print("Account Number:", account_number)
    print(f"Available Balance: {whole_azn}.{qepik:02d} AZN")
    print("Account Status:", status)
    print("=========================================")
    
def check_balance(data, username):
    user = data['users'][username]
 
    # Convert balance from qepik to AZN
    balance = user["balance"]
    sign = "-" if balance < 0 else ""
    balance = abs(balance)
    whole_azn = balance // 100
    qepik = balance % 100
 
    print("\n========== BALANCE ==========")
    print(f"Available Balance: {sign}{whole_azn}.{qepik:02d} AZN")
    print("=============================")
 