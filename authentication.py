
import time
import hashlib
from feature.file_storage import save_data

# Fayl ucun
def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()

# def hash_password(password):
#     salt = os.urandom(16)
#     hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
#     return salt.hex() + "$" + hashed.hex()


# Vaxt saygaci
def countdown(account):
     
    remaining=int(account["lock_until"]-time.time())+1

    for seconds in range(remaining, 0, -1):
         
        print(f"Please wait {seconds//60:02d}:{seconds%60:02d}")
        # 02d niye yazdim?
        # d--> decimal kimi yazilsin
        # 2--> en azi 2 simvol yer tutsun
        # 0 --> bos qalan yerler 0la dolsun
        time.sleep(1)
    print('You may try again ')
    
        

def login(data):
    # Username yoxlanilmasi
    
    for attempt in range(3):
        username=input("Username: ")

        if username in data["users"]:
            break

        print("Unsuccessful login")

    else:
        print("Too many attempts")
        return None
        
    account=data["users"][username]
    # Accountun veziyyeti ucun
    if account["blocked"]:
        print("Maximum login attempts exceeded.\nYour card has been blocked.\nPlease contact the bank administrator.")
        return None
    
    # Vaxtin giris cixis etdikden sonra silinmemesi ucun
    if account["lock_until"]>time.time():
        print("Your account is temporarily locked")
        countdown(account)

    while True:
        # Password yoxlanilmasi
        userpassword=input("Password: ")

        if hash_password(userpassword)==account["password"]:
            account["failed_attempts"]=0
            account["lock_until"]=0
            save_data(data)

            print("Login successful!")
            return username

        account["failed_attempts"]+=1
        print("Unsuccessful login")

        if account["failed_attempts"]>=6:
            account["blocked"]=True
            save_data(data)

            print("Account permanently blocked")
            return None

        if account["failed_attempts"]==3:
            account["lock_until"]=time.time() + 60
            print(f"Incorrect password. Attempt: {account['failed_attempts']}/6")
            save_data(data)
            
            countdown(account)
           
        save_data(data)

