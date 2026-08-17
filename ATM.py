import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
import json
import os
import uuid


# =========================================================
# ATM SETTINGS
# =========================================================

DATA_FILE = "atm_data.json"

DAILY_WITHDRAWAL_LIMIT = 50000

DENOMINATIONS = [2000, 500, 200, 100]

ADMIN_PIN = "9999"


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
BUTTON_COLOR = "#2563EB"
BUTTON_HOVER = "#1D4ED8"
SUCCESS_COLOR = "#16A34A"
DANGER_COLOR = "#DC2626"
WARNING_COLOR = "#D97706"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#CBD5E1"


# =========================================================
# DEFAULT DATA
# =========================================================

default_data = {
    "balance": 10000000,
    "pin": "1234",
    "withdrawn_today": 0,
    "last_withdrawal_date": str(date.today()),

    "atm_cash": {
        "2000": 50,
        "500": 100,
        "200": 100,
        "100": 100
    },

    "transactions": []
}


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    if not os.path.exists(DATA_FILE):

        return default_data.copy()

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except:

        return default_data.copy()


data = load_data()


# =========================================================
# VARIABLES
# =========================================================

balance = data["balance"]

pin = data["pin"]

withdrawn_today = data["withdrawn_today"]

last_withdrawal_date = data["last_withdrawal_date"]

atm_cash = {
    int(key): value
    for key, value in data["atm_cash"].items()
}

transactions = data["transactions"]

active_entry = None


# =========================================================
# SAVE DATA
# =========================================================

def save_data():

    data = {
        "balance": balance,
        "pin": pin,
        "withdrawn_today": withdrawn_today,
        "last_withdrawal_date": last_withdrawal_date,

        "atm_cash": {
            str(key): value
            for key, value in atm_cash.items()
        },

        "transactions": transactions
    }

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# =========================================================
# RESET DAILY LIMIT
# =========================================================

def reset_daily_limit():

    global withdrawn_today
    global last_withdrawal_date

    today = str(date.today())

    if today != last_withdrawal_date:

        withdrawn_today = 0
        last_withdrawal_date = today

        save_data()


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title("ATM Machine")

window.geometry("500x750")

window.configure(
    bg=BG_COLOR
)

window.resizable(
    False,
    False
)


# =========================================================
# CLEAR SCREEN
# =========================================================

def clear_screen():

    for widget in window.winfo_children():

        widget.destroy()


# =========================================================
# KEYPAD
# =========================================================

def keypad_press(number):

    global active_entry

    if active_entry is None:

        return

    current = active_entry.get()

    if len(current) < 10:

        active_entry.insert(
            tk.END,
            str(number)
        )


def keypad_clear():

    global active_entry

    if active_entry:

        active_entry.delete(
            0,
            tk.END
        )


def keypad_backspace():

    global active_entry

    if active_entry:

        current = active_entry.get()

        if current:

            active_entry.delete(
                len(current) - 1,
                tk.END
            )


def set_active_entry(entry):

    global active_entry

    active_entry = entry


def create_keypad(parent):

    keypad_frame = tk.Frame(
        parent,
        bg=BG_COLOR
    )

    keypad_frame.pack(
        pady=15
    )

    keys = [
        ("1", 0, 0),
        ("2", 0, 1),
        ("3", 0, 2),

        ("4", 1, 0),
        ("5", 1, 1),
        ("6", 1, 2),

        ("7", 2, 0),
        ("8", 2, 1),
        ("9", 2, 2),

        ("C", 3, 0),
        ("0", 3, 1),
        ("⌫", 3, 2)
    ]

    for text, row, column in keys:

        if text == "C":

            command = keypad_clear

        elif text == "⌫":

            command = keypad_backspace

        else:

            command = (
                lambda value=text:
                keypad_press(value)
            )

        tk.Button(
            keypad_frame,
            text=text,
            command=command,
            width=7,
            height=2,
            font=("Arial", 13, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT_COLOR,
            relief="flat"
        ).grid(
            row=row,
            column=column,
            padx=5,
            pady=5
        )


# =========================================================
# LOGIN SCREEN
# =========================================================

def login_screen():

    global active_entry

    clear_screen()

    reset_daily_limit()

    main_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )

    main_frame.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        main_frame,
        text="🏧",
        font=("Arial", 50),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        main_frame,
        text="ATM MACHINE",
        font=("Arial", 27, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    tk.Label(
        main_frame,
        text="Secure Banking",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=SECONDARY_TEXT
    ).pack(
        pady=(5, 20)
    )

    card = tk.Frame(
        main_frame,
        bg=CARD_COLOR,
        padx=25,
        pady=20
    )

    card.pack(
        padx=40,
        fill="x"
    )

    tk.Label(
        card,
        text="ENTER YOUR PIN",
        font=("Arial", 13, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=5
    )

    pin_entry = tk.Entry(
        card,
        show="●",
        font=("Arial", 20),
        justify="center",
        width=15
    )

    pin_entry.pack(
        pady=10
    )

    set_active_entry(pin_entry)

    attempts = [0]

    def login():

        entered_pin = pin_entry.get()

        if entered_pin == pin:

            attempts[0] = 0

            messagebox.showinfo(
                "Login",
                "Login Successful!"
            )

            dashboard()

        else:

            attempts[0] += 1

            pin_entry.delete(
                0,
                tk.END
            )

            remaining = 3 - attempts[0]

            if attempts[0] >= 3:

                messagebox.showerror(
                    "Account Locked",
                    "Too many incorrect PIN attempts."
                )

                login_button.config(
                    state="disabled"
                )

                return

            messagebox.showerror(
                "Login Failed",
                f"Incorrect PIN!\n\n"
                f"Attempts remaining: {remaining}"
            )

    login_button = tk.Button(
        card,
        text="LOGIN",
        command=login,
        width=18,
        height=2,
        font=("Arial", 12, "bold"),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground=BUTTON_HOVER,
        activeforeground=TEXT_COLOR,
        relief="flat"
    )

    login_button.pack(
        pady=10
    )

    create_keypad(main_frame)

    tk.Label(
        main_frame,
        text="Admin: Use Admin button from dashboard",
        font=("Arial", 9),
        bg=BG_COLOR,
        fg=SECONDARY_TEXT
    ).pack(
        pady=5
    )


# =========================================================
# FIND ATM NOTE COMBINATION
# =========================================================

def calculate_notes(amount):

    denominations = [2000, 500, 200, 100]

    def find_combination(
        index,
        remaining,
        result
    ):

        if remaining == 0:

            return result.copy()

        if index == len(denominations):

            return None

        denomination = denominations[index]

        available = atm_cash[denomination]

        maximum = min(
            remaining // denomination,
            available
        )

        for count in range(
            maximum,
            -1,
            -1
        ):

            result[denomination] = count

            answer = find_combination(
                index + 1,
                remaining -
                (denomination * count),
                result
            )

            if answer is not None:

                return answer

        return None

    result = {}

    answer = find_combination(
        0,
        amount,
        result
    )

    if answer is None:

        return None

    return {
        denomination: count
        for denomination, count
        in answer.items()
        if count > 0
    }


# =========================================================
# TOTAL ATM CASH
# =========================================================

def get_total_atm_cash():

    total = 0

    for denomination, count in atm_cash.items():

        total += denomination * count

    return total


# =========================================================
# RECEIPT
# =========================================================

def show_receipt(
    transaction_type,
    amount,
    balance_after,
    notes=None
):

    receipt_window = tk.Toplevel(
        window
    )

    receipt_window.title(
        "ATM Receipt"
    )

    receipt_window.geometry(
        "400x560"
    )

    receipt_window.configure(
        bg="white"
    )

    transaction_id = (
        "TXN"
        + uuid.uuid4().hex[:8].upper()
    )

    receipt = ""

    receipt += (
        "================================\n"
    )

    receipt += (
        "          ATM MACHINE\n"
    )

    receipt += (
        "================================\n\n"
    )

    receipt += (
        f"Transaction ID : {transaction_id}\n"
    )

    receipt += (
        f"Date & Time    : "
        f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
    )

    receipt += (
        "--------------------------------\n"
    )

    receipt += (
        f"Transaction    : {transaction_type}\n"
    )

    receipt += (
        f"Amount         : ₹{amount:,}\n"
    )

    if notes:

        receipt += (
            "\nCash Dispensed:\n"
        )

        for denomination, count in notes.items():

            receipt += (
                f"₹{denomination:,} × {count}\n"
            )

    receipt += (
        "--------------------------------\n"
    )

    receipt += (
        f"Balance        : ₹{balance_after:,}\n"
    )

    receipt += (
        "\n================================\n"
    )

    receipt += (
        "       THANK YOU FOR BANKING\n"
    )

    receipt += (
        "================================\n"
    )

    text_box = tk.Text(
        receipt_window,
        font=("Courier New", 10),
        width=43,
        height=23
    )

    text_box.pack(
        padx=15,
        pady=15
    )

    text_box.insert(
        tk.END,
        receipt
    )

    text_box.config(
        state="disabled"
    )

    def save_receipt():

        filename = (
            "ATM_Receipt_"
            + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".txt"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(receipt)

        messagebox.showinfo(
            "Receipt Saved",
            f"Receipt saved as:\n{filename}"
        )

    tk.Button(
        receipt_window,
        text="💾 Save Receipt",
        command=save_receipt,
        width=20,
        height=2,
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(
        pady=5
    )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    clear_screen()

    reset_daily_limit()

    main_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )

    main_frame.pack(
        fill="both",
        expand=True
    )

    # -----------------------------
    # HEADER
    # -----------------------------

    header = tk.Frame(
        main_frame,
        bg=CARD_COLOR
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="🏧 ATM",
        font=("Arial", 23, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        side="left",
        padx=25,
        pady=18
    )

    tk.Label(
        header,
        text="Welcome",
        font=("Arial", 11),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT
    ).pack(
        side="right",
        padx=25
    )

    # -----------------------------
    # BALANCE
    # -----------------------------

    balance_card = tk.Frame(
        main_frame,
        bg=BUTTON_COLOR,
        padx=20,
        pady=15
    )

    balance_card.pack(
        padx=25,
        pady=15,
        fill="x"
    )

    tk.Label(
        balance_card,
        text="AVAILABLE BALANCE",
        font=("Arial", 10, "bold"),
        bg=BUTTON_COLOR,
        fg=SECONDARY_TEXT
    ).pack()

    balance_label = tk.Label(
        balance_card,
        text=f"₹ {balance:,}",
        font=("Arial", 23, "bold"),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR
    )

    balance_label.pack(
        pady=3
    )

    # -----------------------------
    # UPDATE BALANCE
    # -----------------------------

    def update_balance():

        balance_label.config(
            text=f"₹ {balance:,}"
        )

    # -----------------------------
    # AMOUNT
    # -----------------------------

    tk.Label(
        main_frame,
        text="Enter Amount",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    amount_entry = tk.Entry(
        main_frame,
        font=("Arial", 18),
        justify="center"
    )

    amount_entry.pack(
        pady=5,
        ipady=4
    )

    set_active_entry(
        amount_entry
    )

    # =====================================================
    # CHECK BALANCE
    # =====================================================

    def check_balance():

        messagebox.showinfo(
            "Balance",
            f"Available Balance\n\n"
            f"₹ {balance:,}"
        )

    # =====================================================
    # DEPOSIT
    # =====================================================

    def deposit():

        global balance

        try:

            amount = int(
                amount_entry.get()
            )

            if amount <= 0:

                raise ValueError

            balance += amount

            transaction = {
                "type": "Deposit",
                "amount": amount,
                "time": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "balance": balance
            }

            transactions.append(
                transaction
            )

            save_data()

            update_balance()

            amount_entry.delete(
                0,
                tk.END
            )

            messagebox.showinfo(
                "Deposit",
                f"₹{amount:,} deposited successfully."
            )

            show_receipt(
                "DEPOSIT",
                amount,
                balance
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid amount."
            )

    # =====================================================
    # WITHDRAW
    # =====================================================

    def withdraw():

        global balance
        global withdrawn_today
        global last_withdrawal_date

        reset_daily_limit()

        try:

            amount = int(
                amount_entry.get()
            )

            if amount <= 0:

                raise ValueError

            # Multiple of ₹100

            if amount % 100 != 0:

                messagebox.showerror(
                    "Invalid Amount",
                    "Amount must be a multiple of ₹100."
                )

                return

            # Account balance

            if amount > balance:

                messagebox.showerror(
                    "Insufficient Balance",
                    "You don't have enough account balance."
                )

                return

            # Daily limit

            remaining_limit = (
                DAILY_WITHDRAWAL_LIMIT
                - withdrawn_today
            )

            if amount > remaining_limit:

                messagebox.showerror(
                    "Daily Limit Exceeded",
                    f"You can withdraw only "
                    f"₹{remaining_limit:,} more today."
                )

                return

            # Total ATM cash

            if amount > get_total_atm_cash():

                messagebox.showerror(
                    "ATM Cash Unavailable",
                    "The ATM does not have enough "
                    "cash at the moment."
                )

                return

            # Find notes

            notes = calculate_notes(
                amount
            )

            if notes is None:

                messagebox.showerror(
                    "ATM Cash Unavailable",
                    "The ATM cannot dispense this amount "
                    "using the available ₹2,000, ₹500, "
                    "₹200 and ₹100 notes.\n\n"
                    "Please try another amount."
                )

                return

            # Remove notes

            for denomination, count in notes.items():

                atm_cash[denomination] -= count

            # Update account

            balance -= amount

            withdrawn_today += amount

            # Save transaction

            transaction = {
                "type": "Withdrawal",
                "amount": amount,
                "time": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "balance": balance
            }

            transactions.append(
                transaction
            )

            save_data()

            update_balance()

            amount_entry.delete(
                0,
                tk.END
            )

            show_receipt(
                "WITHDRAWAL",
                amount,
                balance,
                notes
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter numbers only."
            )

    # =====================================================
    # MINI STATEMENT
    # =====================================================

    def mini_statement():

        statement_window = tk.Toplevel(
            window
        )

        statement_window.title(
            "Mini Statement"
        )

        statement_window.geometry(
            "520x600"
        )

        statement_window.configure(
            bg=BG_COLOR
        )

        tk.Label(
            statement_window,
            text="📜 MINI STATEMENT",
            font=("Arial", 21, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            pady=20
        )

        if not transactions:

            tk.Label(
                statement_window,
                text="No transactions yet.",
                font=("Arial", 13),
                bg=BG_COLOR,
                fg=SECONDARY_TEXT
            ).pack(
                pady=30
            )

            return

        recent = transactions[-5:]

        text = ""

        for transaction in reversed(recent):

            text += (
                f"{transaction['time']}\n"
            )

            text += (
                f"{transaction['type']}   "
                f"₹{transaction['amount']:,}\n"
            )

            text += (
                f"Balance: "
                f"₹{transaction['balance']:,}\n"
            )

            text += (
                "-" * 42
                + "\n"
            )

        text += (
            f"\nCurrent Balance: ₹{balance:,}"
        )

        text_box = tk.Text(
            statement_window,
            font=("Courier New", 10),
            width=52,
            height=23
        )

        text_box.pack(
            padx=15,
            pady=10
        )

        text_box.insert(
            tk.END,
            text
        )

        text_box.config(
            state="disabled"
        )

    # =====================================================
    # DAILY LIMIT
    # =====================================================

    def show_daily_limit():

        reset_daily_limit()

        remaining = (
            DAILY_WITHDRAWAL_LIMIT
            - withdrawn_today
        )

        messagebox.showinfo(
            "Daily Withdrawal Limit",
            f"Daily Limit: ₹{DAILY_WITHDRAWAL_LIMIT:,}\n\n"
            f"Withdrawn Today: ₹{withdrawn_today:,}\n\n"
            f"Remaining: ₹{remaining:,}"
        )

    # =====================================================
    # ATM CASH STATUS
    # =====================================================

    def show_atm_cash():

        total = get_total_atm_cash()

        details = (
            "🏧 ATM CASH STATUS\n\n"
        )

        for denomination in DENOMINATIONS:

            details += (
                f"₹{denomination:,} : "
                f"{atm_cash[denomination]} notes\n"
            )

        details += (
            f"\nTotal ATM Cash: ₹{total:,}"
        )

        messagebox.showinfo(
            "ATM Cash Status",
            details
        )

    # =====================================================
    # CHANGE PIN
    # =====================================================

    def change_pin_window():

        global pin

        change_window = tk.Toplevel(
            window
        )

        change_window.title(
            "Change PIN"
        )

        change_window.geometry(
            "360x430"
        )

        change_window.configure(
            bg=BG_COLOR
        )

        tk.Label(
            change_window,
            text="🔐 CHANGE PIN",
            font=("Arial", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            pady=20
        )

        tk.Label(
            change_window,
            text="Current PIN",
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack()

        old_entry = tk.Entry(
            change_window,
            show="●",
            font=("Arial", 14),
            justify="center"
        )

        old_entry.pack(
            pady=8
        )

        tk.Label(
            change_window,
            text="New PIN",
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack()

        new_entry = tk.Entry(
            change_window,
            show="●",
            font=("Arial", 14),
            justify="center"
        )

        new_entry.pack(
            pady=8
        )

        tk.Label(
            change_window,
            text="Confirm New PIN",
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack()

        confirm_entry = tk.Entry(
            change_window,
            show="●",
            font=("Arial", 14),
            justify="center"
        )

        confirm_entry.pack(
            pady=8
        )

        def save_pin():

            global pin

            old = old_entry.get()

            new = new_entry.get()

            confirm = confirm_entry.get()

            if old != pin:

                messagebox.showerror(
                    "Error",
                    "Current PIN is incorrect."
                )

                return

            if len(new) != 4 or not new.isdigit():

                messagebox.showerror(
                    "Error",
                    "PIN must contain exactly 4 digits."
                )

                return

            if new != confirm:

                messagebox.showerror(
                    "Error",
                    "New PINs do not match."
                )

                return

            pin = new

            save_data()

            messagebox.showinfo(
                "Success",
                "PIN changed successfully."
            )

            change_window.destroy()

        tk.Button(
            change_window,
            text="SAVE PIN",
            command=save_pin,
            width=18,
            height=2,
            bg=SUCCESS_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 11, "bold"),
            relief="flat"
        ).pack(
            pady=20
        )

    # =====================================================
    # ADMIN MODE
    # =====================================================

    def admin_mode():

        admin_window = tk.Toplevel(
            window
        )

        admin_window.title(
            "ATM Admin"
        )

        admin_window.geometry(
            "420x650"
        )

        admin_window.configure(
            bg=BG_COLOR
        )

        tk.Label(
            admin_window,
            text="👨‍💼 ATM ADMIN",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            pady=20
        )

        tk.Label(
            admin_window,
            text="Admin PIN",
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack()

        admin_entry = tk.Entry(
            admin_window,
            show="●",
            font=("Arial", 15),
            justify="center"
        )

        admin_entry.pack(
            pady=10
        )

        refill_frame = tk.Frame(
            admin_window,
            bg=CARD_COLOR,
            padx=20,
            pady=15
        )

        refill_frame.pack(
            padx=25,
            pady=10,
            fill="x"
        )

        tk.Label(
            refill_frame,
            text="Cash Refill",
            font=("Arial", 15, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            pady=5
        )

        entries = {}

        for denomination in DENOMINATIONS:

            row = tk.Frame(
                refill_frame,
                bg=CARD_COLOR
            )

            row.pack(
                pady=5
            )

            tk.Label(
                row,
                text=f"₹{denomination:,} notes:",
                width=15,
                anchor="w",
                bg=CARD_COLOR,
                fg=TEXT_COLOR
            ).pack(
                side="left"
            )

            entry = tk.Entry(
                row,
                width=10,
                justify="center"
            )

            entry.pack(
                side="left"
            )

            entries[denomination] = entry

        def refill():

            entered_pin = admin_entry.get()

            if entered_pin != ADMIN_PIN:

                messagebox.showerror(
                    "Access Denied",
                    "Incorrect admin PIN."
                )

                return

            added = False

            for denomination, entry in entries.items():

                value = entry.get().strip()

                if value == "":

                    continue

                if not value.isdigit():

                    messagebox.showerror(
                        "Error",
                        "Enter numbers only."
                    )

                    return

                count = int(value)

                if count < 0:

                    messagebox.showerror(
                        "Error",
                        "Invalid note count."
                    )

                    return

                atm_cash[denomination] += count

                added = True

            if not added:

                messagebox.showerror(
                    "Error",
                    "Enter at least one note quantity."
                )

                return

            save_data()

            messagebox.showinfo(
                "Success",
                "ATM cash refilled successfully."
            )

            admin_window.destroy()

        tk.Button(
            admin_window,
            text="REFILL ATM",
            command=refill,
            width=20,
            height=2,
            bg=SUCCESS_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 11, "bold"),
            relief="flat"
        ).pack(
            pady=15
        )

        def show_admin_cash():

            if admin_entry.get() != ADMIN_PIN:

                messagebox.showerror(
                    "Access Denied",
                    "Enter the correct admin PIN first."
                )

                return

            details = "ATM NOTE INVENTORY\n\n"

            for denomination in DENOMINATIONS:

                details += (
                    f"₹{denomination:,} : "
                    f"{atm_cash[denomination]} notes\n"
                )

            details += (
                f"\nTotal Cash: "
                f"₹{get_total_atm_cash():,}"
            )

            messagebox.showinfo(
                "ATM Inventory",
                details
            )

        tk.Button(
            admin_window,
            text="📊 VIEW ATM INVENTORY",
            command=show_admin_cash,
            width=22,
            height=2,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 10, "bold"),
            relief="flat"
        ).pack(
            pady=5
        )

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout():

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if answer:

            save_data()

            login_screen()

    # =====================================================
    # DASHBOARD BUTTONS
    # =====================================================

    button_frame = tk.Frame(
        main_frame,
        bg=BG_COLOR
    )

    button_frame.pack(
        pady=8
    )

    buttons = [
        ("💰 Check Balance", check_balance),
        ("💵 Deposit", deposit),
        ("💸 Withdraw", withdraw),
        ("📜 Mini Statement", mini_statement),
        ("📊 Daily Withdrawal Limit", show_daily_limit),
        ("🏧 ATM Cash Status", show_atm_cash),
        ("🔐 Change PIN", change_pin_window),
        ("👨‍💼 Admin Mode", admin_mode)
    ]

    for text, command in buttons:

        tk.Button(
            button_frame,
            text=text,
            command=command,
            width=27,
            height=1,
            font=("Arial", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT_COLOR,
            relief="flat"
        ).pack(
            pady=2
        )

    # =====================================================
    # LOGOUT / EXIT
    # =====================================================

    bottom_frame = tk.Frame(
        main_frame,
        bg=BG_COLOR
    )

    bottom_frame.pack(
        pady=7
    )

    tk.Button(
        bottom_frame,
        text="🚪 Logout",
        command=logout,
        width=12,
        height=2,
        bg=DANGER_COLOR,
        fg=TEXT_COLOR,
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        bottom_frame,
        text="❌ Exit",
        command=window.destroy,
        width=12,
        height=2,
        bg=DANGER_COLOR,
        fg=TEXT_COLOR,
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(
        side="left",
        padx=5
    )


# =========================================================
# START ATM
# =========================================================

login_screen()

window.mainloop()