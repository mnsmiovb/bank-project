from authentication import hash_password
from feature.file_storage import save_data
import time

# Kohne passwordun yoxlanilmasi ucun verilen cehd sayi
passwordattempts=3

# Yeni passwordun tehlukesizliyinin artirilmasi ucun qoyulan sertler
def check_new_password(old_password, new_password):
    if old_password==new_password:
            return 'New password cannot be the same as your current password'
              
        
    if len(new_password)<8:
            return 'Weak password: password should be minimum 8 characters '
             
    # .isupper() ve islower() evezine bele yazdimki istifadeci parol olaraq sadece bosluq,!,@,# kimi 
    # simvollar istifade etmesin
    
    if new_password.isdigit():
                return 'Weak password: password should not contain only digits'
            
    if not any(digit.isdigit() for digit in new_password):
            return 'Weak password: at least 1 digit should be used'    
        # any zamani en azi 1 sert odenilirse true olur
        # digit.isdigit() passwordda reqem olub olmadiqin yoxlayir
        # eger reqem varsa anyden true cixir not onu false edir , yoxdursa returna dusur
        
    if new_password == new_password.upper():
            return 'Weak password: at least 1 lowercase letter should also be used'
            
        
    if new_password == new_password.lower():
            return 'Weak password: at least 1 uppercase letter should also be used'
            
        
    
            
    
# Passwordun deyismesi 
def change_password(data, username):
    
    account = data["users"][username]
    
    
        
    for attempt in range(passwordattempts):
        old_password=input('Enter your old password: ')
        
        if hash_password(old_password)==account["password"]:
            break
        
        print('Wrong password')
    else:
        print("Too many wrong attempts. Returning to menu")
        return
    # Yeni parolun tesdiqlenmesi
    while True:  
        for attempt in range(passwordattempts):
              new_password=input('Enter new password: ')

        
              error=check_new_password(old_password,new_password)
              if error:
                 print(error)
                 continue
    
    
              new_password_again=input('Enter new password again to confirm: ')
              if new_password!=new_password_again:
                print("Passwords do not match.Please try again")
                continue
        
              break
        else:
            print("Too many wrong attempts. Returning to menu")
            return
# Haslanma ve yadda saxlanmasi
        account['password'] = hash_password(new_password)
        save_data(data)
        print('Password changed successfully')