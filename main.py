from feature.file_storage import load_data
from authentication import login
from passwordchange import change_password
from account_information import account_information, check_balance
from deposit import deposit
from withdrawal import withdrawal, daily_limits
from feature.transfers import transfer_money
from feature.transaction_history import show_history
 
def show_menu(username):
    line = "=" * 36

    print(line)
    print("IT BANKING SYSTEM".center(36))
    print(line)
    print(f"Welcome, {username}!")
    print("1. View Account Information")
    print("2. Check Balance")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. Transaction History")
    print("7. Daily Limits")
    print("8. Change Password")
    print("9. Logout")
    print("0. Exit")
    print(line)
    
def choose_menu(data, username):
        show_menu(username)
        choice = input("Select an option: ").strip()
 
        if choice == "1":
                account_information(data, username)
                
        elif choice == "2":
                check_balance(data, username)
                 
        elif choice == "3":
                deposit(data, username)
        
        elif choice == "4":
                withdrawal(data, username)
                
        elif choice == "5":
                transfer_money(data, username)
                
        elif choice == "6":
                show_history(data, username)
                
        elif choice == "7":
                daily_limits(data, username)
                
        elif choice == "8":
                change_password(data, username)
        elif choice == "9":       # login ekranına qayıdır
                print("Logged out\n")
                return "logout"
        elif choice == "0":       #proqramı bağlayır
                print("Goodbye!")
                return "exit"
        else:
                print("Invalid option. Please choose a number from the menu")

        input("\nPress Enter to continue...")
         
 
def main():
    data = load_data()

    while True:
        username = login(data)

        if username is None:
            print("Login canceled")
            break

        while True: 
            result=choose_menu(data, username)
            if result in ("logout", "exit"):
                break

        if result=="exit":
            break
    

 
if __name__=="__main__":
    main()