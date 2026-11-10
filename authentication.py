# import os
import time
import json
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_accounts():
    with open("accounts.json", "r") as file:
        return json.load(file)


def save_data(accounts):
    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)
        
        
def login(accounts):

    for attempt in range(3):
        username = input("Username: ")

        if username in accounts:
            break

        print("Unsuccessful login")

    else:
        print("Too many attempts")
        return None

    account = accounts[username]

    if account["blocked"]:
        print("Maximum login attempts exceeded.\nYour card has been blocked.\nPlease contact the bank administrator.")
        return None
        

    while True:
        userpassword = input("Password: ")

        if hash_password(userpassword) == account["password"]:
            account["failed_attempts"] = 0
            account["lock_until"] = 0
            save_data(accounts)

            print("Login successful!")
            return username

        account["failed_attempts"] += 1
        print("Unsuccessful login")

        if account["failed_attempts"] >= 6:
            account["blocked"] = True
            save_data(accounts)

            print("Account permanently blocked")
            return None

        if account["failed_attempts"] == 3:
            account["lock_until"] = time.time() + 60
            save_data(accounts)
            
            print('Incorrect password. Attempt: 3/6')
            for i in range(60,0,-1):
            
               remaining = int(account["lock_until"] - time.time())
               time.sleep(1)
               print(f"Please wait {remaining} seconds")
        
            # print("Account locked for 60 seconds")
            # return None
            print('You may try again.')
        save_data(accounts)

