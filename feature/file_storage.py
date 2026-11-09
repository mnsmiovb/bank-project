import json
import os
from datetime import date
data_file="accounts.json"
initial_atm_cash = 500000#qepikle floatda xeta olmasin deye

def create_default_data():
    demo_accounts = [("user01","Test@123","10010001",250000),
                     ("user02","Test@456","10010002",150000),
                     ("user03","Test@789","10010003",300000),]
    users = {}
    for username, password, account_number, balance in demo_accounts:
        users[username] = {
            "password": password,
            "failed_attempts": 0,
            "lock_until": 0,
            "blocked": False,
            "account_number": account_number,
            "balance": balance,
            "daily": {
                "date": str(date.today()),
                "deposited": 0,
                "withdrawn": 0,
                "transfer_count": 0,
            },
            "history": [],}
           
    return {"atm_cash":initial_atm_cash, "users": users}
def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file)
    return True  
def load_data():
    if not os.path.exists(data_file): 
        data = create_default_data()
        save_data(data)
        return data
    with open(data_file, "r") as file:
        data = json.load(file)
    return data
if __name__=="__main__":
    data = load_data()
    print (data ["atm_cash"],list(data["users"].keys()))
