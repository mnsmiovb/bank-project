# 🏦 IT Banking System (CLI)

A comprehensive, console-based banking and ATM simulation application built entirely with Python's Standard Library. Designed around Azerbaijani currency (**AZN / Qəpik**), the system provides secure user authentication, brute-force lockout protection, real-time ATM cash reserve management, daily transaction limit enforcement, tiered withdrawal fee calculations, inter-account transfers, and persistent JSON-backed storage.

## 📋 Table of Contents

1. [Key Features](#-key-features)

2. [Business Rules & Financial Logic](#-business-rules--financial-logic)

3. [Security Architecture](#-security-architecture)

4. [Project Structure](#-project-structure)

5. [Data Schema (JSON)](#-data-schema-json)

6. [Installation & Setup](#-installation--setup)

7. [Usage & Walkthrough](#-usage--walkthrough)

8. [Module Reference](#-module-reference)

9. [Known Issues & Maintenance Notes](#-known-issues--maintenance-notes)

## 🚀 Key Features

* **Multi-Layer Authentication & Lockout System:**

  * Passwords are never stored in plain text; all credentials are hashed using **SHA-256**.

  * Implements progressive brute-force protection with temporary countdown lockouts and permanent administrative blocks.

* **Precision Currency Handling (Qəpik Engine):**

  * Eliminates IEEE 754 floating-point rounding bugs by storing and computing all balances, limits, and fees as integer **qəpik** ($1\text{ AZN} = 100\text{ qəpik}$), converting to formatted decimal AZN (`0.00 AZN`) only at the presentation layer.

* **ATM Cash Reserve Synchronization:**

  * Tracks physical cash available inside the ATM (`atm_cash`). Deposits replenish the ATM's cash supply, while withdrawals validate against both the user's account balance and the physical cash remaining in the machine.

* **Automated Daily Limit Reset:**

  * Tracks daily deposited and withdrawn totals per user and automatically resets counters at midnight when the system calendar date changes.

* **Tiered Fee & Commission Engine:**

  * Supports fee-free daily withdrawal allowances followed by automatic percentage-based commission calculations on excess amounts.

* **Audit-Ready Transaction Logs:**

  * Every financial operation generates a unique **UUIDv4** transaction identifier stamped with the user's username, operation type, amount in qəpik, and ISO date (`YYYY-MM-DD`).

* **Strict Password Policy Enforcement:**

  * Guided password-change workflow requiring complexity checks and confirmation matching.

## 💰 Business Rules & Financial Logic

The system enforces strict banking constraints across all operations:

| Operation / Rule | Threshold / Value | System Behavior | 
| ----- | ----- | ----- | 
| **Currency Unit** | $1\text{ AZN} = 100\text{ qəpik}$ | All internal math uses integers; displayed as `X.XX AZN`. | 
| **Daily Deposit Limit** | **2,000.00 AZN** (`200,000` qəpik) | Deposits exceeding remaining daily allowance are rejected, displaying the exact remaining quota. | 
| **Daily Withdrawal Limit** | **1,000.00 AZN** (`100,000` qəpik) | Hard cap on total cash withdrawn per calendar day. | 
| **Fee-Free Withdrawal Tier** | First **500.00 AZN** (`50,000` qəpik) / day | Zero commission charged up to 500 AZN withdrawn per day. | 
| **Withdrawal Commission** | **2%** on excess above 500 AZN | Calculated via `round(taxable_amount * 0.02)`. Deducted from user balance, not from `atm_cash`. | 
| **ATM Cash Reserve Check** | `amount_qepik <= data["atm_cash"]` | Blocks withdrawal if the ATM lacks physical banknotes to dispense the requested sum. | 

### Example Commission Calculation

If a user has withdrawn `400.00 AZN` today and requests an additional `300.00 AZN`:

1. **Remaining Fee-Free Allowance:** $500.00 - 400.00 = 100.00\text{ AZN}$

2. **Taxable Amount:** $300.00 - 100.00 = 200.00\text{ AZN}$

3. **2% Commission:** $200.00 \times 0.02 = 4.00\text{ AZN}$

4. **Total Deducted from User Account:** $300.00 + 4.00 = 304.00\text{ AZN}$

5. **Total Deducted from ATM Cash:** $300.00\text{ AZN}$

## 🔒 Security Architecture

### Login & Brute-Force Mitigation (`authentication.py`)

1. **Session Attempt Cap:** Users have up to **3 attempts** per login session before the session terminates.

2. **Temporary Lockout (3 Failed Attempts):** Reaching 3 cumulative failed password attempts triggers a **60-second lockout** (`lock_until = time.time() + 60`). A live `MM:SS` countdown timer blocks input until the cooldown expires.

3. **Permanent Block (6 Failed Attempts):** Reaching 6 cumulative failed attempts sets `"blocked": true` in persistent storage. The card/account is locked permanently until manually reset by a bank administrator.

4. **Counter Reset:** A successful login resets `failed_attempts` to `0` and `lock_until` to `0`.

### Password Complexity Rules (`passwordchange.py`)

When changing a password, users have **3 attempts** to verify their current password and **3 attempts** to set a valid new password. A new password must satisfy all of the following:

* Must **not** match the current password.

* Minimum length of **8 characters**.

* Cannot consist solely of numeric digits.

* Must contain at least **1 numeric digit** (`0-9`).

* Must contain at least **1 lowercase letter** (`a-z`).

* Must contain at least **1 uppercase letter** (`A-Z`).

## 📁 Project Structure

```
it-banking-system/
│
├── main.py                     # Entry point: login loop, main CLI menu, and navigation router
├── authentication.py           # User login, SHA-256 hashing, lockout timers, and block logic
├── account_information.py      # Account summary view and formatted balance checker
├── deposit.py                  # Cash deposit workflow, daily limit checks, and UUID logging
├── withdrawal.py               # Cash withdrawal workflow, 2% fee engine, and daily limit viewer
├── passwordchange.py           # Old password verification and new password strength validation
├── convert.py                  # Standalone migration utility to hash legacy plain-text passwords
├── .gitignore                  # Excludes local *.json database files from version control
│
└── feature/                    # Supporting package modules
    ├── file_storage.py         # JSON persistence layer (load_data / save_data)
    ├── transfers.py            # Peer-to-peer account money transfer logic
    └── transaction_history.py  # Formatted transaction history viewer

```

## 🗄️ Data Schema (JSON)

Because `*.json` files are ignored via `.gitignore` for security and privacy, you must ensure your JSON storage file (loaded by `feature/file_storage.py`, typically `accounts.json`) follows this structure:

```
{
  "atm_cash": 1000000,
  "users": {
    "ali_mammadov": {
      "account_number": "AZ21ITB0000000001234567",
      "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
      "balance": 250000,
      "blocked": false,
      "failed_attempts": 0,
      "lock_until": 0,
      "daily": {
        "date": "2026-11-13",
        "deposited": 0,
        "withdrawn": 0
      },
      "history": [
        {
          "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
          "username": "ali_mammadov",
          "type": "deposit",
          "amount": 50000,
          "date": "2026-11-13"
        }
      ]
    }
  }
}

```

### Field Definitions

* `atm_cash` *(int)*: Total physical cash inside the ATM in qəpik (`1000000` = `10,000.00 AZN`).

* `account_number` *(str)*: Unique IBAN-style account identifier.

* `password` *(str)*: 64-character hexadecimal SHA-256 digest of the user's password.

* `balance` *(int)*: Current account balance in qəpik (`250000` = `2,500.00 AZN`).

* `blocked` *(bool)*: Indicates whether the account is permanently locked due to excessive failed logins.

* `failed_attempts` *(int)*: Running counter of consecutive unsuccessful login attempts.

* `lock_until` *(float)*: Unix timestamp indicating when a temporary 60-second lockout expires (`0` if unlocked).

* `daily` *(dict)*: Tracks `"date"` (`YYYY-MM-DD`), `"deposited"` (qəpik), and `"withdrawn"` (qəpik).

* `history` *(list\[dict\])*: Chronological list of transaction records.

## 🛠️ Installation & Setup

1. **Clone or Download the Repository:**

   ```
   git clone <your-repository-url>
   cd it-banking-system
   
   ```

2. **Verify Python Environment:**
   Ensure Python **3.6 or higher** is installed:

   ```
   python --version
   
   ```

   *(No `pip install` step is required—the project relies exclusively on Python's built-in modules.)*

3. **Initialize Storage Data:**
   Create your JSON data file (e.g., `accounts.json`) using the schema shown above. If you initially populate passwords in plain text, you can adapt and run `convert.py` to batch-hash all unhashed passwords into 64-character SHA-256 digests.

4. **Launch the Application:**

   ```
   python main.py
   
   ```

## 🖥️ Usage & Walkthrough

### 1. Authentication

Upon launching `main.py`, enter a valid username and password:

```
Username: ali_mammadov
Password: ********
Login successful!

```

### 2. Main Banking Menu

Once authenticated, select an operation by entering its corresponding number (`0`–`9`):

```
====================================
         IT BANKING SYSTEM          
====================================
Welcome, ali_mammadov!
1. View Account Information
2. Check Balance
3. Deposit Money
4. Withdraw Money
5. Transfer Money
6. Transaction History
7. Daily Limits
8. Change Password
9. Logout
0. Exit
====================================
Select an option: 

```

### 3. Checking Daily Limits (`Option 7`)

Displays real-time usage and remaining allowances for the current calendar day:

```
===== DAILY LIMITS =====

Daily deposit limit:
Used: 200.0 AZN
Remaining: 1800.0 AZN

Daily withdrawal limit:
Used: 150.0 AZN
Remaining: 850.0 AZN

Fee-free withdrawal:
Remaining: 350.0 AZN

```

## 🧩 Module Reference

* **`main.py`**: Orchestrates the outer authentication loop and inner menu loop. Handles session state (`logout` vs. `exit`).

* **`authentication.py`**: Implements `hash_password()`, `countdown()`, `login()`, and `check_password()`.

* **`account_information.py`**: Implements `account_information()` (full profile summary) and `check_balance()` (formatted AZN balance supporting negative sign handling).

* **`deposit.py`**: Implements `deposit()`. Validates positive integer AZN inputs, enforces the 2,000 AZN daily cap, updates user balance and `atm_cash`, and appends a UUID transaction record.

* **`withdrawal.py`**: Implements `withdrawal()` and `daily_limits()`. Supports float AZN inputs, enforces the 1,000 AZN daily cap, checks ATM cash reserves, computes the 2% fee over 500 AZN, and records transactions.

* **`passwordchange.py`**: Implements `check_new_password()` and `change_password()` with multi-attempt verification and strength rules.

* **`convert.py`**: Administrative helper script to convert non-64-character plain-text passwords in storage into SHA-256 hashes.

## ⚠️ Known Issues & Maintenance Notes

1. **Transaction Type Label in `withdrawal.py`:**
   In `withdrawal.py` (lines 67–73), completed withdrawals are currently appended to `user["history"]` with `"type": "deposit"`. Changing this value to `"type": "withdrawal"` is recommended so transaction history reports accurately distinguish deposits from withdrawals.

2. **Integer vs. Float Input Consistency:**
   `deposit.py` parses user input using `int(...)` (whole Manats only), whereas `withdrawal.py` parses input using `float(...)` (allowing qəpik). Standardizing both to `float` (or `Decimal`) with 2-decimal validation will make the UX consistent.

3. **IDE Temporary File:**
   `tempCodeRunnerFile.py` is an auto-generated artifact from VS Code's *Code Runner* extension. It is not imported anywhere in the project and can safely be removed.

4. **Upgrade Path for Password Hashing:**
   `authentication.py` contains a commented-out `pbkdf2_hmac` implementation with random 16-byte salts. Migrating from plain SHA-256 to salted PBKDF2-HMAC-SHA256 is recommended for production-grade resistance against rainbow-table attacks.