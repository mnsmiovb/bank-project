from authentication import login, load_accounts
from passwordchange import change_password
 
 
def show_menu():
    print("\n--- Bank Menu ---")
    print("1. Change password")
    print("2. Logout")
 
 
def main():
    accounts = load_accounts()
    username = login(accounts)
 
    if username is None:
        print("Login canceled")
        return
 
    print(f"\nWelcome, {username}!")
 
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
 
        if choice == "1":
            change_password(accounts, username)
        elif choice == "2":
            print("Logged out. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1 or 2.")
 
 
if __name__ == "__main__":
    main()
 