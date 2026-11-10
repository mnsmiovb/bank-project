from authentication import login, load_accounts


def main():
    accounts = load_accounts()
    username = login(accounts)

    if username is None:
        print("Login canceled")
        return

    # Bank menyusu burada davam edir


if __name__ == "__main__":
    main()