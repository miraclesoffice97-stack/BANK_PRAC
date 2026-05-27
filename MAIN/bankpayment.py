import DB.db as db
import datetime
import sys

class main:
    def __init__(self, account_number, username):

        self.account_number = account_number

        self.username = username
        self.curcon = db.database_conn()
        self.paydb = db.payment()

        self.paydb.payment_table_init()

        total = 0
        self.curcon.cursor.execute(
            '''INSERT INTO payment_table (username, total_bal, accountnum) VALUES(%s, %s, %s)
            ON CONFLICT (username) DO NOTHING''',
            (self.username, total, self.account_number)
        )

        self.curcon.psqlconn.commit()

    #ADD FUNDS LINE
    def deposit(self):

        while True:

            try:

                print("---------ADD FUNDS TO ACCOUNT----------")

                entry = input("\nEnter account Number or x to quit: ")


                if entry == "x".lower():
                    break

                self.curcon.cursor.execute(
                    '''SELECT accountnum FROM payment_table WHERE accountnum = %s''', (entry,)
                )

                check = self.curcon.cursor.fetchone()

                if check:

                    self.curcon.cursor.execute(
                    '''SELECT total_bal FROM payment_table WHERE accountnum = %s''', (check[0],)
                    )

                    ttl = self.curcon.cursor.fetchone()[0]

                    amt = float(input("\nEnter amount to deposit: N"))
                    new_bal = ttl + amt


                    self.curcon.cursor.execute(
                    '''UPDATE payment_table SET total_bal = %s WHERE accountnum = %s''', (new_bal, entry)
                    )

                    self.curcon.psqlconn.commit()

                    print("\n deposit successfull")

                else:
                    print("Invalid account number!!")

            except Exception as e:

                print("Error occured: ", e)

        
class payment(main):

    def __init__(self, account_number, username):
        super().__init__(account_number, username)

        db.transaction().history_table_init()

        
    def transfer(self):

        while True:

            try:

                print("--------- TRANSFER FUNDS ----------")

                entry = input("\nEnter account Number or x to quit: ")


                if entry == "x".lower():
                    break

                self.curcon.cursor.execute(
                    '''SELECT total_bal, username FROM payment_table WHERE accountnum = %s''', (entry,)
                    )

                ttl = self.curcon.cursor.fetchone()


                if ttl:

                    try:

                        amt = float(input("Enter amount to deposit: N"))

                        self.curcon.cursor.execute(
                        '''SELECT total_bal FROM payment_table WHERE username = %s''', (self.username,)
                        )

                        senderttl = self.curcon.cursor.fetchone()[0]

                        if senderttl < amt:

                            print("Insufficient Funds Check balance")
                            break

                        sbal = senderttl - amt

                        newbal = ttl[0] + amt


                        self.curcon.cursor.execute(
                        '''UPDATE payment_table SET total_bal = %s WHERE accountnum = %s''', (newbal, entry)
                        )

                        self.curcon.psqlconn.commit()

                        self.curcon.cursor.execute(
                        '''UPDATE payment_table SET total_bal = %s where username = %s''', (sbal, self.username)
                        )

                        self.curcon.psqlconn.commit()

                        receivers_name = ttl[1]

                        sendername = self.username

                        self.date = datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")



                        self.curcon.cursor.execute(
                            '''INSERT INTO transaction_tab (username, sender, amount, date, receiver) VALUES(%s, %s, %s, %s, %s)''',
                            (
                                self.username, sendername, amt, self.date, receivers_name 
                            )
                        )

                        self.curcon.psqlconn.commit()

                        self.curcon.cursor.execute(
                            '''INSERT INTO transaction_tab (username, sender, amount, date, receiver) VALUES(%s, %s, %s, %s, %s)''',
                            (
                                receivers_name, sendername, amt, self.date, receivers_name 
                            )
                        )

                        self.curcon.psqlconn.commit()


                        print(f"Transfer to {receivers_name} Successful!!")

                    except Exception as e:
                        print("Error occured: ", e)
                    

                else:
                    print("Invalid account number!!")

            except Exception as e:

                print("Error occured: ", e)


class history(payment):
    def __init__(self, account_number, username):
        super().__init__(account_number, username)

    def history_menu(self):

        while True:

            self.history = []

            self.receive_history = []

            try:

                        self.curcon.cursor.execute(
                        '''SELECT sender, amount, date, receiver FROM transaction_tab WHERE sender = %s GROUP BY sender, amount, date, receiver''', 
                        (
                            self.username,
                        )
                        )

                        datas = self.curcon.cursor.fetchall()

                        if datas:

                            for rows in datas:

                                sender = rows[0]

                                amount = rows[1]

                                date = rows[2]

                                receiver = rows[3] 

                                format = f"N{amount:.2f} sent to {receiver} on {date} "

                                self.history.append(format)

                        else:
                            pass

                        self.curcon.cursor.execute(
                            '''SELECT sender, amount, date, receiver FROM transaction_tab WHERE receiver = %s GROUP BY sender, amount, date, receiver''', 
                            (
                                self.username,
                            )
                        )

                        

                        datas = self.curcon.cursor.fetchall()

                        if datas:

                            for rows in datas:

                                sender = rows[0]

                                amount = rows[1]

                                date = rows[2]

                                receiver = rows[3] 

                                format = f"N{amount:.2f} received from {sender} on {date} "

                                self.receive_history.append(format)

                        else:
                            pass


            except Exception as e:
                print(e)
                pass


            print('''TRANSACTION HISTORY''')

            if self.history:

                print("Sent history")

                sep = "\n".join(self.history)
                print()
                print (sep)

            else:
                print("\n No transaction history record")


            #receivers history

            if self.receive_history:

                print("\ndeposit report")

                res = "\n".join(self.receive_history)
                print()
                print (res)

            else:
                print("\n No transaction history record")

            entry = input("Enter q to exit to menu: ").lower()
            
            if entry == 'q':
                break
            else:
                print("Invalid input!! ")


class profile(history):
    def __init__(self, account_number, username):
        super().__init__(account_number, username)

    def profile(self):

        while True:

            self.curcon.cursor.execute(''' SELECT * FROM auth_data WHERE username = %s''', (self.username,))

            data = self.curcon.cursor.fetchone()

            self.username = data[1]

            self.email = data[2]

            self.password = data[3]

            self.date_of_registration = data[4]

            self.phone_number = data[5]

            self.account_number = data[6]

            print(f'''USER PROFILE
                    
                    username: {self.username}
                    
                    email: {self.email}''')
            
            entry = input("Enter 'q' to exit or 'e' to edit profile details: ").lower()

            if entry == "q":
                break

            elif entry == "e":
                self.edit_profile()

            else:
                print("Inavlid input!! ")
            
    def edit_profile(self):

        print("Enter login details to edit profile")

        username = input("\nEnter Username: ")

        password = input("Enter Password: ")

        self.curcon.cursor.execute(
                    '''SELECT username, password FROM auth_data WHERE username = %s AND password = %s ''', (
                       username, password
                    )
                )

        check = self.curcon.cursor.fetchone()

        if check:

            while True:
                print("\n-------- EDIT PROFILE DETAILS ---------")


                print("\nenter q in any of the fields to exit And leave blank any field you are not editing")

                new_username = input("\nEnter new username:") or self.username

                new_email = input('\nEnter new email: ') or self.email

                if new_username == "q" or new_email == "q":
                    break

                self.curcon.cursor.execute(
                    '''UPDATE auth_data SET username = %s, email = %s WHERE username = %s''', (new_username, new_email, self.username)
                )

                self.curcon.psqlconn.commit()

        else:
            print("Access denied! invalid inputs")

class dashboard(profile):
    def __init__(self, account_number, username):
        super().__init__(account_number, username)

    def board(self):

        date = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")


        while True:

            self.curcon.cursor.execute(
                        '''SELECT total_bal FROM payment_table WHERE username = %s''', (self.username,)
                    )

            total = self.curcon.cursor.fetchone()[0]

            dashboard_home = f''' DASHBOARD 
            WELCOME -> {self.username}       {date}

            ____________________________________________ 

            TOTAL BALANCE  N{total:.2f}
            ____________________________________________
            
            - h to view transaction history
            
            - p to transfer funds

            - e to view profile
            
            - q to exit to menu'''

            print(dashboard_home)


            entry = input("Entry: ")

            match entry:
                case "h":
                    self.history_menu()

                case "p":
                    self.transfer()

                case 'e':
                    self.profile()

                case 'q':
                    break

class menu(dashboard):
    def __init__(self, account_number, username):
        super().__init__(account_number, username)

        db.transaction().history_table_init()

    def menu(self):

        while True:
            home = '''\n-------- BANK-PRAC HOME ---------
            
            1. DASHBOARD
            
            2. TRANSFER
            
            3. ADD_FUNDS
            
            4. HISTORY
            
            5. PROFILE
            
            6. LOG_OUT
            
            7. EXIT APP'''

            print(home)

            entry = input("Entry: ")

            match entry:
                case "1":
                    self.board()

                case "2":
                    self.transfer()

                case "3":
                    self.deposit()

                case "4":
                    self.history_menu()

                case "5":
                    self.profile()

                case "6":
                    break

                case "7":
                    sys.exit()