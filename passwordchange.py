import json
import hashlib
from authentication import hash_password, load_accounts, save_data

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()


# def load_accounts():
#     with open("accounts.json", "r") as file:
#         return json.load(file)


# def save_data(accounts):
#     with open("accounts.json", "w") as file:
#         json.dump(accounts, file, indent=4)
        
        
def change_password(accounts, username):
    
    account = accounts[username]
    
    userpassword=input('Enter your old password: ')
        

    if hash_password(userpassword)==account["password"]:
        new_password=input('Enter new password: ')