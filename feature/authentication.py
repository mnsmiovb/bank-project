import time
import json


def load_accounts():
    with open("users.json", "r") as file:
        return json.load(file)


def save_data(accounts):
    with open("users.json", "w") as file:
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
        print("Your account is permanently blocked")
        return None

    if account["lock_until"] > time.time():
        remaining = int(account["lock_until"] - time.time())
        print(f"Try again after {remaining} seconds.")
        return None

    while True:
        userpassword = input("Password: ")

        if userpassword == account["password"]:
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

            print("Account locked for 60 seconds")
            return None

        save_data(accounts)


accounts = load_accounts()
login(accounts)