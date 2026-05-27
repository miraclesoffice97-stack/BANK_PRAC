# BANK-PRAC

A terminal-based banking application built with Python and PostgreSQL. Users can sign up, log in, transfer funds, deposit money, view transaction history, and manage their profile — all from the command line.

---

## Features

- **Authentication** — Sign up with username validation, password requirements, and phone number verification. Log in with either your username or phone number.
- **Forgot Password** — Reset your password via a verification code sent to your registered phone number.
- **Dashboard** — View your account balance and navigate the app.
- **Transfer Funds** — Send money to another account by account number, with insufficient funds protection.
- **Add Funds (Deposit)** — Deposit money into any account using an account number.
- **Transaction History** — View a full record of money sent and received.
- **Profile Management** — View and edit your username and email after re-authenticating.
- **Logging** — All signup activity, login events, and errors are automatically written to log files.

---

## Project Structure

```
BANK PRAC/
│
├── AUTH/
│   ├── auth.py          # Signup, login, and auth menu
│   └── __init__.py
│
├── DB/
│   ├── db.py            # Database connection and table initialization
│   ├── db example.env   # Example environment variable file
│   └── __init__.py
│
├── MAIN/
│   ├── bankpayment.py   # Core banking logic — deposit, transfer, history, profile, dashboard, menu
│   └── __init__.py
│
├── LOG/
│   ├── loger.py         # Logging configuration for signup and login events
│   └── __init__.py
│
└── db.env               # Your local environment variables (never commit this)
```

---

## Requirements

- Python 3.10 or higher (required for `match/case` statements)
- PostgreSQL
- The following Python packages:
  - `psycopg2`
  - `python-dotenv`

Install dependencies with:

```bash
pip install psycopg2 python-dotenv
```

---

## Setup

**1. Clone or download the project**

```bash
git clone <your-repo-url>
cd "BANK PRAC"
```

**2. Set up your PostgreSQL database**

Make sure PostgreSQL is running and create a database for the project:

```sql
CREATE DATABASE your_database_name;
```

**3. Configure your environment variables**

Copy the example env file and fill in your own database credentials:

```bash
cp "DB/db example.env" db.env
```

Then open `db.env` and update the values:

```env
DB_HOST=localhost
DB_NAME=your_database_name
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_PORT=5432
```

> **Important:** Never commit `db.env` to version control. It contains sensitive credentials. The `envi.gitignore` file in the project is there to help with this — make sure it is renamed to `.gitignore`.

**4. Run the application**

```bash
python AUTH/auth.py
```

The app will automatically create all required database tables on first run.

---

## Database Tables

The app manages three tables in PostgreSQL:

| Table | Description |
|---|---|
| `auth_data` | Stores user accounts — username, email, password, phone number, account number, registration date |
| `payment_table` | Stores each user's balance and account number |
| `transaction_tab` | Records every transfer — sender, receiver, amount, and date |

---

## Log Files

The app writes four log files automatically in the project root:

| File | Contents |
|---|---|
| `signup_Info_record.log` | Successful new user registrations |
| `signup_error_record.log` | Errors during signup |
| `login_rec.log` | Successful login events |
| `login_errors.log` | Login errors and exceptions |

---

## How Account Numbers Work

When a user signs up, their account number is automatically generated from their phone number — the leading `0` is removed and the remaining 10 digits become the account number. For example, phone number `08012345678` becomes account number `8012345678`.

---

## Usage

When you run the app you will see:

```
____________________________________________________________
     BANK-PRAC LOGIN OR SIGNUP

     1. SIGN_UP to get started

     2. LOGIN if already have account

     3. EXIT
```

From the banking home menu after login:

```
-------- BANK-PRAC HOME ---------

     1. DASHBOARD
     2. TRANSFER
     3. ADD_FUNDS
     4. HISTORY
     5. PROFILE
     6. LOG_OUT
     7. EXIT APP
```

---

## Author

Built from scratch as a Python and PostgreSQL learning project, covering OOP inheritance, database design, error handling, and application architecture.
