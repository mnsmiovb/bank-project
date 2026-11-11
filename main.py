from authentication import login, load_accounts
from passwordchange import change_password
# from accounts import view_account_info, check_balance, daily_limits
# from deposit import deposit
# from withdraw import withdraw

# from transfer import transfer
# from history import transaction_history
# from storage import save_accounts
 
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
    
def choose_menu(accounts, username):
        show_menu(username)
        choice = input("Select an option: ").strip()
 
        if choice == "1":
                # view_account_info(accounts, username)
                pass
        elif choice == "2":
                # check_balance(accounts, username)
                pass
        elif choice == "3":
                # deposit(accounts, username)
                pass
        elif choice == "4":
                # withdraw(accounts, username)\
                pass
        elif choice == "5":
                # transfer(accounts, username)
                pass
        elif choice == "6":
                # transaction_history(accounts, username)
                pass
        elif choice == "7":
                # daily_limits(accounts, username)
                pass
        elif choice == "8":
                change_password(accounts, username)
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
    accounts = load_accounts()

    while True:
        username=login(accounts)

        if username is None:
            print("Login canceled")
            break

        while True: 
            result=choose_menu(accounts, username)
            if result in ("logout", "exit"):
                break

        if result=="exit":
            break
    

 
if __name__=="__main__":
    main()