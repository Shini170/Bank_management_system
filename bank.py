from db import get_connection

class Bank:
    bank_name = "SBI"

    # ---------- VALIDATIONS ----------
    @staticmethod
    def is_valid_acc_no(acc_no):
        acc_no = str(acc_no)
        return acc_no.isdigit() and 6 <= len(acc_no) <= 12

    @staticmethod
    def is_valid_name(name):
        name = name.strip()
        return name.replace(" ", "").isalpha() and len(name.split()) >= 2

    @staticmethod
    def is_valid_transfer_acc_num(acc_no):
        return Bank.is_valid_acc_no(acc_no)

    @staticmethod
    def is_valid_pin(pin):
        pin=str(pin)
        return pin.isdigit() and len(pin)==4

    # ---------- CREATE ACCOUNT ----------
    @staticmethod
    def create_account(name, acc_no,pin):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT acc_no FROM accounts WHERE acc_no=%s",
            (acc_no,)
        )
        if cursor.fetchone():
            conn.close()
            return None

        cursor.execute(
            "INSERT INTO accounts (acc_no, name,pin) VALUES (%s, %s, %s)",
            (acc_no, name, pin)
        )

        conn.commit()
        conn.close()
        return True

    # ---------- LOGIN ----------
    @staticmethod
    def login(acc_no,pin):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM accounts WHERE acc_no=%s AND pin=%s",
            (acc_no,pin)
        )
        acc = cursor.fetchone()
        conn.close()
        return acc

    # ---------- DEPOSIT ----------
    @staticmethod
    def deposit(acc_no, amount):
        if amount <= 0:
            print("Invalid amount")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE acc_no=%s",
            (amount, acc_no)
        )

        cursor.execute(
            "INSERT INTO transactions (acc_no, type, amount) VALUES (%s,%s,%s)",
            (acc_no, "DEPOSIT", amount)
        )

        conn.commit()
        conn.close()
        print("Deposit successful")

    # ---------- WITHDRAW ----------
    @staticmethod
    def withdrawal(acc_no, amount):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT balance FROM accounts WHERE acc_no=%s",
            (acc_no,)
        )
        acc = cursor.fetchone()

        if not acc or acc["balance"] - amount < 500:
            print("Insufficient balance or minimum balance issue")
            conn.close()
            return

        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE acc_no=%s",
            (amount, acc_no)
        )

        cursor.execute(
            "INSERT INTO transactions (acc_no, type, amount) VALUES (%s,%s,%s)",
            (acc_no, "WITHDRAW", amount)
        )

        conn.commit()
        conn.close()
        print("Withdrawal successful")

    # ---------- BALANCE ----------
    @staticmethod
    def balance_check(acc_no):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT balance FROM accounts WHERE acc_no=%s',
                       (acc_no,))
        balance=cursor.fetchone()[0]
        conn.close()
        print('Balance:',balance)

    # ---------- TRANSFER ----------
    @staticmethod
    def transfer(from_acc, to_acc, amount):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT balance FROM accounts WHERE acc_no=%s",
            (from_acc,)
        )
        sender = cursor.fetchone()

        if not sender or sender["balance"] - amount < 500:
            print("Transfer failed")
            conn.close()
            return

        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE acc_no=%s",
            (amount, from_acc)
        )
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE acc_no=%s",
            (amount, to_acc)
        )

        cursor.execute(
            "INSERT INTO transactions (acc_no, type, amount) VALUES (%s,%s,%s)",
            (from_acc, "TRANSFER", amount)
        )

        conn.commit()
        conn.close()
        print("Transfer successful")

    # ---------- TRANSACTION HISTORY ----------
    @staticmethod
    def transaction_history(acc_no):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM transactions WHERE acc_no=%s",
            (acc_no,)
        )

        for row in cursor.fetchall():
            print(row)

        conn.close()

    # ---------- DELETE ACCOUNT ----------
    @staticmethod
    def delete_account(acc_no,pin):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('DELETE FROM transactions WHERE acc_no=%s',
                       (acc_no,))

        cursor.execute('DELETE FROM accounts WHERE acc_no=%s AND pin=%s',
                       (acc_no,pin))


        conn.commit()
        conn.close()
        print('Account Deleted Successfully')
        return True

