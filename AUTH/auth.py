import DB.db as db
import datetime
import LOG.loger as log
import MAIN.bankpayment as bp
import random

class signup:
    def __init__(self):

        self.details_saver = db.database_conn() 
        self.details_saver.auth_dataTable()

    def oauth(self):


        while True:

            print(f"{'_' * 60}\nInput lower (x) in any of the fields to request exit and quit signup\n{'_' * 60}")

            self.userreq = ''' USER NAME REQUIREMENT

            . must contain 8 or morethan 8 characters

            . must contain either uppercase, special characters or numbers

            '''

            print(self.userreq)

            name = input("Enter username dear: ")

            try:

                self.details_saver.cursor.execute(
                    '''SELECT username FROM auth_data WHERE username = %s''', (
                        name,
                    )
                )

                self.details_saver.psqlconn.commit()

                check = self.details_saver.cursor.fetchone()

                if check:
                    print("try another the name entered already exists")
                    print("restart")
                    break

            except Exception as e:
                log.loger.error(e, exc_info=True)
                pass

            self.usernameRequirement = [
                any(char.isupper() or char.isdigit() or not char.isalnum() for char in name),
            8 <= len(name)
            ]

            print('\n-----------Enter 11 digits Correct contact--------------')
            phone = input ("Enter Phone number: ")

            number_req = [
                all(char.isdigit() for char in phone),
                len(phone) == 11 
            ]
            
            print("\nEnter correct email following email format----------------")

            email = input("Enter email if (optional): ")

            emailcheck = [
                '.' in email and "@" in email,
                len(email) >= 8
            ]

            print ('''------- Password requirements -------
      
                    1. Must include uppercase 
                    
                    2. Must be 8 character or more
                    
                    3. must include number and special characters
                    
                    ''')

            password = input ("Enter unique password: ")

            pass_req = (
            any(char.isupper() for char in password),
            8 <= len(password),
            any(not char.isalnum() for char in password),
            any(char.isdigit() for char in password)
            )

            if email == "x" or name == "x" or password == "x" or phone == 'x':

                print("\n(x) request to exit was entered in one of the fields\n")
                break

            else:
                pass

            if email:

                if all(self.usernameRequirement) and all(emailcheck) and all(number_req) and all(pass_req):

                    if phone.startswith("0"):
                        accnum = phone[1:]

                    else:
                        print("Invalid phone number input!!")

                    regdate = datetime.datetime.now().strftime("%H, %M, %S _ %d-%m-%y")

                    self.email = email
                    self.username = name
                    self.password = password
                    self.regdate = regdate
                    self.phone = phone
                    self.accnum = accnum

                    try:

                        self.details_saver.cursor.execute('''INSERT INTO auth_data(username, email, password, date_of_registration, phone_number, accnum) VALUES(
                        %s, %s, %s, %s, %s, %s)
                        ''', (self.username, self.email, self.password, self.regdate, self.phone, self.accnum))
                        
                        self.details_saver.psqlconn.commit()

                        log.loger.info(f"New user registered {self.regdate}")

                    except Exception as e:
                        log.loger.error(e, exc_info=True)

                    break

                else:

                    print(" Unsuccessfull!! Please follow specific info when entering details!!!")

            else:

                if all(self.usernameRequirement) and all(number_req) and all(pass_req):

                    if phone.startswith("0"):
                        accnum = phone[1:]

                    else:
                        pass

                    regdate = datetime.datetime.now().strftime("%H, %M, %S _ %d-%m-%y")

                    self.email = email
                    self.username = name
                    self.password = password
                    self.regdate = regdate
                    self.phone = phone
                    self.accnum = accnum

                    try:

                        self.details_saver.cursor.execute('''INSERT INTO auth_data(username, email, password, date_of_registration, phone_number, accnum) VALUES(
                        %s, %s, %s, %s, %s, %s)
                        ''', (self.username, self.email, self.password, self.regdate, self.phone, self.accnum))

                        self.details_saver.psqlconn.commit()

                        log.loger.info(f"New user registered {self.regdate}")

                    except Exception as e:
                        log.loger.error(e, exc_info=True)
                        print("sorry error occured!! ")

                    break

                else:

                    print(" Unsuccessfull!! Please follow specific info when entering details!!!")

class login(signup):
    def __init__(self):

        super().__init__()

    def login_loj(self):

        while True:

            print(f'{"_" * 60}\nInput lower (q) in any of the fields to request exit and quit signup\n{"_" * 60}')

            optdet = input("\nEnter username or phone number: ")

            password = input("\nEnter password 'f' if forgotten password: ")

            if optdet == "q" or password == "q":
                break

            if password == "f":

                phone = input("Enter phone_number: ")

                self.details_saver.cursor.execute(
                    '''SELECT phone_number FROM auth_data WHERE phone_number = %s''', (phone,)
                )
                self.details_saver.psqlconn.commit()
                flag = self.details_saver.cursor.fetchone()

                if flag:
                    code = random.randint(1000, 9000)
                    print(code)

                    conf = float(input("Enter code alert or 0 to request new code: "))

                    if conf == code:
                        new_password = input("Enter new password: ")

                        self.details_saver.cursor.execute(
                            '''UPDATE auth_data SET password = %s WHERE phone_number = %s''', (
                                new_password, phone
                            )
                        )
                        self.details_saver.psqlconn.commit()

                    elif conf == 0:
                        code = random.randint(1000, 9000)
                        print("new code", code)

                    else:
                        print("Invalid verification code!! ")

                else:
                    print("Phone_number not found!! ")

            else:


                try:
                    
                    self.details_saver.cursor.execute(
                        '''SELECT username, password FROM auth_data WHERE username = %s AND password = %s''', (
                            optdet, password
                        )
                    )

                    check = self.details_saver.cursor.fetchone()

                    self.details_saver.cursor.execute(
                        '''SELECT phone_number, password FROM auth_data WHERE phone_number = %s AND password = %s''', (
                            optdet, password
                        )
                    )

                    check2 = self.details_saver.cursor.fetchone()

                    if check:

                        self.details_saver.cursor.execute('''SELECT accnum FROM auth_data WHERE username = %s''', (optdet,))

                        accnum = self.details_saver.cursor.fetchone()

                        bp.main(accnum[0], optdet)

                        print("user found successful login")

                        log.loginloger.info(f"Successful login {datetime.datetime.now().strftime("%H, %M, %S _ %d-%m-%y")}")

                        menu = bp.menu(accnum, optdet)

                        menu.menu()

                        return

                    else:
                        print("Invalid username or password!! user not found")

                    if check2:
                        print("user found successful login")
                        self.details_saver.cursor.execute('''SELECT accnum FROM auth_data WHERE phone_number = %s''', (optdet,))

                        accnumd = self.details_saver.cursor.fetchone()

                        bp.main(accnumd[0], optdet)

                        log.loginloger.info(f"Successful login {datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")}")

                        menu = bp.menu(accnumd, optdet)

                        menu.menu()
                        return

                    else:
                        print("Invalid username or password!! user not found")


                except Exception as e:
                    log.loginloger.error(e, exc_info=True)


class menu(login):

    def __init__(self):
        super().__init__()

        self.menu()

    def menu(self):
        while True:
            menu = f'''{'_' * 60}\n     BANK-PRAC LOGIN OR SIGNUP
            
            1. SIGN_UP to get started
            
            2. LOGIN if already have account
            
            3. EXIT
            
            _____________________________________________________'''

            print(menu)

            entry = input("\nentry: ")

            match entry:
                case "1":
                    self.oauth()

                case "2":
                    self.login_loj()

                case "3":
                    break

                case _:
                    print("Invalid input!!")
                    
m = menu()