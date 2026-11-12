from file_storage import (
    to_cents,
    fmt,
    find_username_by_account,
    reset_daily_if_new_day,
    take_snapshot,
    restore,
    commit
)
from transaction_history import (
    add_transaction,
    transfer_sent,
    transfer_received
)
def transfer_money(data, username):
    if username not in data["users"]:
        print("User not found.")
        return False

    sender = data["users"][username]
    if sender.get("blocked", False):
        print("Your account is blocked.")
        return False
    reset_daily_if_new_day(sender)
    recipient_account = input("Enter recipient account number: ").strip()
    recipient_username = find_username_by_account(
        data, recipient_account
    )
    if recipient_username is None:
        print("Recipient account not found.")
        return False
    if recipient_username == username:
        print("You cannot transfer money to your own account.")
        return False
    recipient = data["users"][recipient_username]
    if recipient.get("blocked", False):
        print("Recipient account is blocked.")
        return False
    amount_text = input("Enter transfer amount: ")
    amount = to_cents(amount_text)
    if amount is None:
        print("Invalid amount.")
        return False
    sender_balance = sender["balance"]
    recipient_balance = recipient["balance"]
    if sender_balance < amount:
        print("Insufficient balance.")
        return False
    snapshot = take_snapshot(data)
    try:
        sender["balance"] -= amount
        recipient["balance"] += amount
        sender["daily"]["transfer_count"] = (
            sender["daily"].get("transfer_count", 0) + 1
        )
        add_transaction(
            data,
            username,
            transfer_sent,
            amount,
            sender_balance,
            sender["balance"],
            fee=0,
            other_account=recipient_account
        )
        add_transaction(
            data,
            recipient_username,
            transfer_received,
            amount,
            recipient_balance,
            recipient["balance"],
            fee=0,
            other_account=sender["account_number"]
        )
        if not commit(data, snapshot):
            print("Transfer failed. Data restored.")
            return False
        print("\nTransfer successful!")
        print(f"Amount: {fmt(amount)} AZN")
        print(f"Recipient: {recipient_account}")
        print(f"Remaining balance: {fmt(sender['balance'])} AZN")
        return True
    except Exception as error:
        restore(data, snapshot)
        print(f"Transfer failed: {error}")
        return False