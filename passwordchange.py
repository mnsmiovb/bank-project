 
from authentication import hash_password, save_data

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
    if new_password == new_password.upper():
            return 'Weak password: at least 1 lowercase letter should also be used'
            
        
    if new_password == new_password.lower():
            return 'Weak password: at least 1 uppercase letter should also be used'
            
        
    if new_password.isdigit():
            return 'Weak password: password should not contain only digits'
            
    
# Passwordun deyismesi 
def change_password(accounts, username):
    
    account = accounts[username]
    
    
        
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
    # Haslanma ve yadda saxlanmasi
    account['password'] = hash_password(new_password)
    save_data(accounts)
    print('Password changed successfully')