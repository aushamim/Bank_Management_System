from datetime import datetime


class Bank:
    def __init__(self):
        self.__total_balance = 0
        self.__total_loan = 0
        self.__loan_active = True
        self.__users = {}

    def check_total_balance(self):
        print(f"\n-> TOTAL BALANCE: {self.__total_balance} TK\n")

    def check_total_loan(self):
        print(f"\n-> TOTAL LOANED AMOUNT: {self.__total_loan} TK\n")

    def check_user(self, account_no):
        if account_no in self.__users:
            return self.__users[account_no]
        else:
            return False

    def users_len(self):
        return len(self.__users)

    def add_user(self, account_no, user):
        self.__users[account_no] = user

    def delete_user(self, account_no):
        if account_no in self.__users:
            self.__users.pop(account_no)
            print("\n-> USER DELETED SUCCESSFULLY\n")
        else:
            print("\n-> ACCOUNT DOES NOT EXISTS\n")

    def show_all_users(self):
        print("\n---------- ALL USERS ----------")
        for account_no, user in self.__users.items():
            print(user)
        print("-------------------------------\n")

    def deposit_money(self, amount):
        self.__total_balance += amount

    def is_bankrupt(self, amount):
        if self.__total_balance >= amount:
            return False
        else:
            print("\n-> THE BANK IS BANKRUPT\n")
            return True

    def withdraw_money(self, amount):
        self.__total_balance -= amount

    def add_loan(self, amount):
        self.__total_loan += amount
        self.__total_balance -= amount

    def toggle_loan(self):
        print(f"\nLOAN STATUS: {'ACTIVE' if self.__loan_active else 'INACTIVE'}")
        loan_op = input("DO YOU WANT TO TOGGLE LOAN STATUS (Y/N)?: ")
        if loan_op.lower() == "y":
            self.__loan_active = False if self.__loan_active else True
            print("\n-> LOAN STATUS TOGGLED SUCCESSFULLY\n")
        elif loan_op.lower() == "n":
            print("\n-> OPERATION CANCELLED\n")
        else:
            print("\n-> INVALID SELECTION\n")

    def is_loan_active(self):
        return self.__loan_active


class User:
    def __init__(self, name, email, password, address, acc_type, acc_no_prefix):
        self.__account_no = (
            acc_type[0].upper()
            + name[0].upper()
            + address[0].upper()
            + email[0].upper()
            + str(acc_no_prefix + 101)
        )
        self.__name = name
        self.__email = email
        self.__password = password
        self.__address = address
        self.__acc_type = acc_type
        self.__balance = 0
        self.__transaction_history = []
        self.__available_loan = 2

        print("\n-> ACCOUNT CREATED SUCCESSFULLY")
        print(f"-> THIS IS YOUR ACCOUNT NO.: {self.__account_no}")
        print("-> YOU WILL NEED THIS TO LOGIN TO YOUR ACCOUNT\n")

    def check_password(self, password):
        if self.__password == password:
            return True
        else:
            return False

    def get_account_no(self):
        return self.__account_no

    def deposit_money(self, amount):
        self.__balance += amount
        self.__transaction_history.append(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + ": DEPOSITED - "
            + str(amount)
        )

    def withdraw_money(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            self.__transaction_history.append(
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                + ": WITHDRAWN - "
                + str(amount)
            )
            return True
        else:
            return False

    def take_loan(self, amount):
        if self.__available_loan > 0:
            self.__balance += amount
            self.__transaction_history.append(
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                + ": LOANED - "
                + str(amount)
            )
            return True
        else:
            print("\n-> YOU CANNOT TAKE LOAN ANYMORE")
            print("-> LOAN COUNT EXCEEDED\n")
            return False

    def check_balance(self):
        return self.__balance

    def transaction_history(self):
        print("\n---------- TRANSACTION HISTORY ----------")
        for hist in self.__transaction_history:
            print(hist)
        print("-----------------------------------------\n")

    def transfer_out(self, amount, account_no):
        if self.__balance >= amount:
            self.__balance -= amount
            self.__transaction_history.append(
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                + ": TRANSFERED - "
                + str(amount)
                + " TK TO ACC - "
                + account_no
            )
            print("\n-> TRANSFERRED SUCCESSFULLY\n")
            return True
        else:
            print("\n-> TRANSFER FAILED. LOW BALANCE\n")
            return False

    def transfer_in(self, amount, account_no):
        self.__balance += amount
        self.__transaction_history.append(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + ": RECEIVED - "
            + str(amount)
            + " TK FROM ACC - "
            + account_no
        )

    def __repr__(self) -> str:
        return f"ACCOUNT NO: {self.__account_no}   NAME: {self.__name}   EMAIL: {self.__email}   ADDRESS: {self.__address}"


bank = Bank()

loggedIn = False
isAdmin = False
user = ""
while True:
    if loggedIn:
        if isAdmin:
            print("\n---------- ADMIN MENU ----------")
            print("1. CREATE ACCOUNT")
            print("2. DELETE ACCOUNT")
            print("3. ALL USERS")
            print("4. TOTAL BALANCE")
            print("5. TOTAL LOAN")
            print("6. TOGGLE LOAN STATUS")
            print("0. LOGOUT")
            op = input("SELECT AN OPTION: ")

            if op == "1":
                print("\nPlease Enter the Following Informations")
                name = input("Name: ")
                email = input("Email: ")
                password = input("Password: ")
                address = input("Address: ")
                acc_type = input("Account Type [ Savings(S) - Current(C) ]: ")
                acc_no_prefix = bank.users_len()
                new_user = User(name, email, password, address, acc_type, acc_no_prefix)
                bank.add_user(new_user.get_account_no(), new_user)
                print("\n-> SUCCESSFULLY ADDED NEW USER\n")
            elif op == "2":
                acc_no = input("\nENTER ACCOUNT NO.: ")
                bank.delete_user(acc_no)
            elif op == "3":
                bank.show_all_users()
            elif op == "4":
                bank.check_total_balance()
            elif op == "5":
                bank.check_total_loan()
            elif op == "6":
                bank.toggle_loan()
            elif op == "0":
                loggedIn = False
                isAdmin = False
            else:
                print("\n-> INVALID OPTION. PLEASE TRY AGAIN")
        else:
            print("\n1. CHECK BALANCE")
            print("2. DEPOSIT MONEY")
            print("3. WITHDRAW MONEY")
            print("4. TAKE LOAN")
            print("5. TRANSFER MONEY")
            print("6. CHECK TRANSACTION HISTORY")
            print("0. LOGOUT")
            op = input("SELECT AN OPTION: ")

            if op == "1":
                print(f"\n-> AVAILABLE BALANCE: {user.check_balance()} TK\n")
            elif op == "2":
                amount = int(input("\nENTER AMOUNT: "))
                user.deposit_money(amount)
                bank.deposit_money(amount)
            elif op == "3":
                amount = int(input("\nENTER AMOUNT: "))
                if user.check_balance() >= amount:
                    if not bank.is_bankrupt(amount):
                        if user.withdraw_money(amount):
                            bank.withdraw_money(amount)
                else:
                    print("\n-> WITHDRWAL AMOUNT EXCEEDED\n")
            elif op == "4":
                if bank.is_loan_active():
                    amount = int(input("\nENTER AMOUNT: "))
                    if user.take_loan(amount):
                        bank.add_loan(amount)
                else:
                    print("\n-> THE BANK IS NOT PROVIDING ANY LOAN AT THE MOMENT\n")
            elif op == "5":
                acc_no = input("\nENTER RECEIVER'S ACCOUNT NO: ")
                amount = int(input("ENTER AMOUNT: "))
                receiver = bank.check_user(acc_no)
                if receiver:
                    chk = user.transfer_out(amount, acc_no)
                    if chk:
                        receiver.transfer_in(amount, user.get_account_no())
                else:
                    print("\n-> ACCOUNT DOES NOT EXIST\n")
            elif op == "6":
                user.transaction_history()
            elif op == "0":
                loggedIn = False
            else:
                print("\n-> INVALID OPTION. PLEASE TRY AGAIN")
    else:
        print("\n1. LOGIN")
        print("2. REGISTER")
        print("0. EXIT")
        op = input("SELECT AN OPTION: ")

        if op == "1":
            acc_no = input("ENTER ACCOUNT NO.: ")
            password = input("ENTER PASSWORD: ")
            if acc_no.lower() == "admin":
                if password == "123":
                    loggedIn = True
                    isAdmin = True
                else:
                    print("\n-> WRONG ADMIN PASSWORD\n")
            else:
                tmp_user = bank.check_user(acc_no.upper())
                if not tmp_user:
                    print("\n-> USER NOT FOUND\n")
                else:
                    if tmp_user.check_password(password):
                        user = tmp_user
                        loggedIn = True
                    else:
                        print("\n-> WRONG PASSWORD\n")
        elif op == "2":
            print("\nPlease Enter the Following Informations")
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            address = input("Address: ")
            acc_type = input("Account Type [ Savings(S) - Current(C) ]: ")
            acc_no_prefix = bank.users_len()
            new_user = User(name, email, password, address, acc_type, acc_no_prefix)
            user = new_user
            bank.add_user(new_user.get_account_no(), new_user)
            loggedIn = True
        elif op == "0":
            break
        else:
            print("\n-> INVALID OPTION. PLEASE TRY AGAIN")
