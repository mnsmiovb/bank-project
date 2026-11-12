import copy
import json
import os
from datetime import date
from decimal import Decimal, InvalidOperation

base_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(base_dir, "accounts.json")
tmp_file = os.path.join(base_dir, "accounts.tmp")
corrupt_file = os.path.join(base_dir, "accounts_corrupt.json")
initial_atm_cash = 500000
def to_cents(text):
    try:
        amount = Decimal(text.strip())
    except (InvalidOperation, AttributeError):
        return None
    if not amount.is_finite() or amount <= 0:
        return None
    if amount != amount.quantize(Decimal("0.01")):
        return None
    return int(amount * 100)
def fmt(cents):
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d}"
def today_str():
    return str(date.today())
def reset_daily_if_new_day(user):
    daily = user["daily"]
    if daily["date"] != today_str():
        daily["date"] = today_str()
        daily["deposited"] = 0
        daily["withdrawn"] = 0
        daily["transfer_count"] = 0
def find_username_by_account(data, account_number):
    for username, user in data["users"].items():
        if user["account_number"] == account_number:
            return username
    return None
def create_default_data():
    demo_accounts = [("user01", "Test@123", "10010001", 250000),
                     ("user02", "Test@456", "10010002", 150000),
                     ("user03", "Test@789", "10010003", 300000)]
    users = {}
    for username, password, account_number, balance in demo_accounts:
        users[username] = {
            "password": password,
            "failed_attempts": 0,
            "lock_until": 0,
            "blocked": False,
            "account_number": account_number,
            "balance": balance,
            "daily": {
                "date": today_str(),
                "deposited": 0,
                "withdrawn": 0,
                "transfer_count": 0,
            },
            "history": [],
            "last_login": None,
            "last_transaction": None,
        }
    return {"atm_cash": initial_atm_cash, "last_txn_number": 0, "users": users}
def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0
def is_valid_user(user):
    if not isinstance(user, dict):
        return False
    daily = user.get("daily")
    history = user.get("history")
    if not isinstance(daily, dict) or not isinstance(history, list):
        return False
    if not isinstance(user.get("password"), str):
        return False
    if not isinstance(user.get("account_number"), str):
        return False
    if not isinstance(user.get("blocked"), bool):
        return False
    numbers = [user.get("balance"), user.get("failed_attempts"),
               daily.get("deposited"), daily.get("withdrawn"),
               daily.get("transfer_count")]
    if not all(is_int(number) for number in numbers):
        return False
    lock_until = user.get("lock_until")
    if isinstance(lock_until, bool) or not isinstance(lock_until, (int, float)):
        return False
    if lock_until < 0:
        return False
    try:
        date.fromisoformat(daily.get("date"))
    except (TypeError, ValueError):
        return False
    return all(isinstance(record, dict) and "id" in record for record in history)
def is_valid_data(data):
    if not isinstance(data, dict) or not is_int(data.get("atm_cash")):
        return False
    if "last_txn_number" in data and not is_int(data["last_txn_number"]):
        return False
    users = data.get("users")
    if not isinstance(users, dict) or not users:
        return False
    if not all(is_valid_user(user) for user in users.values()):
        return False
    accounts = {user["account_number"] for user in users.values()}
    return len(accounts) == len(users)
def add_missing_fields(data):
    if "last_txn_number" not in data:
        data["last_txn_number"] = sum(
            len(user["history"]) for user in data["users"].values())
    for user in data["users"].values():
        user.setdefault("last_login", None)
        user.setdefault("last_transaction", None)
def save_data(data):
    try:
        with open(tmp_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            file.flush()
            os.fsync(file.fileno())
        os.replace(tmp_file, data_file)
        return True
    except (OSError, TypeError, ValueError):
        print("Xeta: melumat fayla yazila bilmedi.")
        try:
            os.remove(tmp_file)
        except OSError:
            pass
        return False
def load_data():
    if not os.path.exists(data_file):
        data = create_default_data()
        save_data(data)
        return data
    try:
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not is_valid_data(data):
            raise ValueError("Wrong structure")
    except (json.JSONDecodeError, ValueError, OSError):
        print("Fayl pozulub, yeni data yaradilir.")
        try:
            os.replace(data_file, corrupt_file)
        except OSError:
            pass
        data = create_default_data()
        save_data(data)
        return data
    add_missing_fields(data)
    return data
def take_snapshot(data):
    return copy.deepcopy(data)
def restore(target, source):
    if isinstance(target, dict):
        for key in list(target):
            if key not in source:
                del target[key]
        for key, value in source.items():
            if isinstance(value, (dict, list)) and type(target.get(key)) is type(value):
                restore(target[key], value)
            else:
                target[key] = copy.deepcopy(value)
    else:
        target[:] = copy.deepcopy(source)
def commit(data, snapshot):
    if save_data(data):
        return True
    restore(data, snapshot)
    return False
if __name__ == "__main__":
    data = load_data()
    print(fmt(data["atm_cash"]), list(data["users"].keys()))