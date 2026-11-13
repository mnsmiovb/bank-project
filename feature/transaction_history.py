from datetime import datetime
from feature.file_storage import fmt

deposit = "Deposit"
withdrawal = "Withdrawal"
transfer_sent = "Transfer Sent"
transfer_received = "Transfer Received"
withdrawal_commission = "Withdrawal Commission"
other_account_labels = {
    transfer_sent: "Recipient account",
    transfer_received: "Sender account",
}

def add_transaction(data, username, tx_type, amount, before, after,
                    fee=0, other_account=None):#pul gonderilmezse komisyani sifri ve qarsi hesabio yox edfeciyik 
    data["last_txn_number"] = data.get("last_txn_number", 0) + 1#sa7ygaci artiririq ve yoxdurasa sifirdan baslayiriq
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")#strftime ayrica datetime metodudur busayede melumat metne cevrilir year month day hout minute second
    user = data["users"][username]
    record = {
        "id": f"TXN{int(data['last_txn_number']):04d}",
        "time": now,
        "type": tx_type,
        "amount": amount,
        "before": before,
        "after": after,
        "fee": fee,
        "other_account": other_account,
    }#file storage.py daki record burda yaradilir ve idare edilir
    user["history"].append(record)#history hissesine qeyd gerin qaytariklrui
    user["last_transaction"] = now#Wemeliyyet vaxti saheasi9 indice elave olunur
    return record
def get_history(data, username, limit=10):
    if limit <= 0:
        return []#bos siyahi qaytarirki hecne gosterilmesin prob yaranmasin
    history = data["users"][username]["history"]
    return list(reversed(history[-limit:]))
def show_history(data, username, limit=10):
    records = get_history(data, username, limit)
    if not records:
        print("No transactions found.")
        return
    print("==$$=== TRANSACTION HISTORY ==$$==")
    for i in records:
        tx_type = i.get("type", "")
        print(f"ID: {i.get('id', '')}")
        print(f"Date: {i.get('time', '')}")
        print(f"Type: {tx_type}")
        if i.get("other_account"):
            label = other_account_labels.get(tx_type, "Other account")
            print(f"{label}: {i['other_account']}")
        print(f"Amount: {fmt(i.get('amount', 0))} AZN")
        if i.get("fee"):
            print(f"Fee: {fmt(i['fee'])} AZN")
        print(f"Balance before: {fmt(i.get('before', 0))} AZN")
        print(f"Balance after: {fmt(i.get('after', 0))} AZN")
        print("-" * 41)