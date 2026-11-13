from datetime import datetime
from file_storage import fmt

deposit="Deposit"
withdrawal="Withdrawal"
transfer_sent="Transfer Sent"
transfer_received="Transfer Received"
withdrawal_commission="Withdrawal Commission"

other_account_labels={
    transfer_sent: "Recipient account",
    transfer_received: "Sender account",
}


def add_transaction(data, username, tx_type, amount, before, after,
                    fee=0, other_account=None):
    data["last_txn_number"] = data.get("last_txn_number", 0) + 1
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user=data["users"][username]
    record={
        "id": f"TXN{data['last_txn_number']:04d}",
        "time": now,
        "type": tx_type,
        "amount": amount,
        "before": before,
        "after": after,
        "fee": fee,
        "other_account": other_account,
    }
    user["history"].append(record)
    user["last_transaction"]=now
    return record


def get_history(data, username, limit=10):
    if limit<=0:
        return []
    history=data["users"][username]["history"]
    return list(reversed(history[-limit:]))


def show_history(data, username, limit=10):
    records=get_history(data, username, limit)
    if not records:
        print("No transactions found.")
        return
    print("========== TRANSACTION HISTORY ==========")
    for record in records:
        tx_type = record.get("type", "")
        print(f"ID: {record.get('id', '')}")
        print(f"Date: {record.get('time', '')}")
        print(f"Type: {tx_type}")
        if record.get("other_account"):
            label = other_account_labels.get(tx_type, "Other account")
            print(f"{label}: {record['other_account']}")
        print(f"Amount: {fmt(record.get('amount', 0))} AZN")
        if record.get("fee"):
            print(f"Fee: {fmt(record['fee'])} AZN")
        print(f"Balance before: {fmt(record.get('before', 0))} AZN")
        print(f"Balance after: {fmt(record.get('after', 0))} AZN")
        print("-" * 41)