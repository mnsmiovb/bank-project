
import time
import json
import hashlib

# Fayl ucun
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_accounts():
    with open("accounts.json", "r") as file:
        return json.load(file)


def save_data(accounts):
    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)

# Vaxt saygaci
def countdown(account):
     
    remaining = int(account["lock_until"] - time.time()) + 1

    for seconds in range(remaining, 0, -1):
         
        print(f"Please wait {seconds//60:02d}:{seconds%60:02d}")
        # 02d niye yazdim?
        # d--> decimal kimi yazilsin
        # 2--> en azi 2 simvol yer tutsun
        # 0 --> bos qalan yerler 0la dolsun
        time.sleep(1)
    print('You may try again.')
    
        

def login(accounts):
    # Username yoxlanilmasi
    
    for attempt in range(3):
        username = input("Username: ")

        if username in accounts:
            break

        print("Unsuccessful login")

    else:
        print("Too many attempts")
        # return None
        

    account = accounts[username]
    # Accountun veziyyeti ucun
    if account["blocked"]:
        print("Maximum login attempts exceeded.\nYour card has been blocked.\nPlease contact the bank administrator.")
        return None
    
    # Vaxtin giris cixis etdikden sonra silinmemesi ucun
    if account["lock_until"] > time.time():
        print("Your account is temporarily locked")
        countdown(account)

    while True:
        # Password yoxlanilmasi
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
            print(f"Incorrect password. Attempt: {account['failed_attempts']}/6")
            save_data(accounts)
            
            countdown(account)
           
        save_data(accounts)

