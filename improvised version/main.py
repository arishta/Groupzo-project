from database import Database
db=Database()

class temp: #temp is an empty class
    pass

class user:
    def __init__(self,email):
        self.first_name=db.user_info("first_name",email)
        self.last_name=db.user_info("last_name",email)
        self.full_name=db.user_info("full_name",email)
        self.password=db.user_info("password",email)
        self.email=email
    def display_user_info(self):
        print("FIRST NAME: ")
        print(self.first_name)
        print("LAST NAME: ")
        print(self.last_name)
        print("FULL NAME: ")
        print(self.full_name)
        print("EMAIL ADDRESS: "+self.email)

class welcome_page:

    def welcome(self):
        print("Welcome to Groupzo, a social networking site\n")
        print("1. Create a new account\n2. Login to existing account\n")
        choice=int(input())
        if (choice==1):
            self.create_new_account()
        elif (choice==2):
            self.login()

    def create_new_account(self):
        print("Fill in the following details\n ")

        first_name = input("Enter your first name\n")
        last_name = input("Enter your last name\n")
        full_name = first_name + ' ' + last_name
        while (1):
            email = input("Enter your email address\n")
            if (db.email_verification(email)):
                print("Email address already registered with some account\n")
                print("1. Enter a different email address\n2. Go back\n")
                choice = int(input())
                if (choice == 1):
                    continue
                elif (choice == 2):
                    self.welcome()
            else:
                t=temp()
                t.first_name=first_name
                t.last_name=last_name
                t.full_name=t.first_name+" "+t.last_name
                t.email=full_name
                t.email=email
                t.password = input("Enter your password\n")
                print("Account successfully created\n")
                db.insert_into_members(t)
                self.welcome()

    def login(self):
        while(1):
            email=input("Enter your email address:\n")
            if db.email_verification(email):
                u=user(email)
                while(1):
                    password=input("Enter your password\n")
                    if password==u.password:
                        print("Account verified\n Login successful\n")
                        hp=home_page()
                        hp.options(u)
                        break
                    else:
                        print("Password does not match\n 1. Enter another password\n 2. Go back")
                        choice=int(input())
                        if (choice==1):
                            continue
                        elif (choice==2):
                            self.welcome()
                break
            else:
                print("Email address does not match\n 1. Enter email again\n 2. Go back")
                choice=int(input())
                if (choice==1):
                    continue
                elif (choice==2):
                    self.welcome()



class home_page:
    def options(self,u):
        print("Welcome to your Groupzo account, "+u.full_name.upper())
        print("1.View your profile\n2.Search a user\n3.Settings\n4.Logout")
        choice=int(input())
        if (choice==1):
            self.view_profile(u)
        elif (choice==2):
            self.search_user(u)
        elif (choice==3):
            self.settings(u)
        elif (choice==4):
            self.logout()

    def view_profile(self,u):
        u.display_user_info()
        self.options(u)

    def search_user(self,u):
        name = input("Enter the name of the user\n")
        row = db.list_users(name)
        if (row):
            for index, val in enumerate(row):
                print(index + 1, ".", *val)
            ch = int(input("Enter the number to search for that user:\n"))
            name = row[ch - 1][0]
            v = user(db.email_from_name(name))
            v.display_user_info()
        else:
            print("No user found\n")
        self.options(u)

    def settings(self,u):
        print("1.Change password\n2.Update email address\n3.Go back")
        ch = int(input())
        if (ch == 1):
            while (1):
                pwd = input("Enter your old password\n")
                if u.password == pwd:
                    new_pwd = input("Enter new password\n")
                    if (new_pwd==pwd):
                        print("New password is the same as the old password\n")
                    else:
                        db.update_password(u.email, new_pwd)
                        u.password = new_pwd
                        print("Password successfully updated\n")
                        break
                else:
                    print("Wrong password\n1.Enter again\n2.Go back\n")
                    c = int(input())
                    if c == 1:
                        continue
                    elif c == 2:
                        self.options(u)
                        break
            self.options(u)
        elif (ch == 2):
            while (1):
                pwd=input("Verify your password\n")
                if (pwd==u.password):
                        while(1):
                            new_email = input("Enter new email address\n")
                            if (db.email_verification(new_email)):
                                if (new_email==u.email):
                                    print("Email address is already associated with your account\n")
                                else:
                                    print("Email is already registered with another user's account\n")
                                print("1. Enter again\n 2. Go back\n")
                                c = int(input())
                                if (c == 1):
                                    continue
                                elif (c == 2):
                                    self.options(u)
                                    break
                            else:
                                db.update_email(u.email, new_email)
                                u.email = new_email
                                print("Email successfully updated\n")
                                break
                        self.options(u)
                else:
                    print("Wrong password\n 1. Verify again\n 2. Go back\n")
                    c=int(input())
                    if c==1:
                        continue
                    else:
                        self.options(u)

        elif (ch == 3):
            self.options(u)
            w.welcome()

    def logout(self):
        print("Successfully logged out\n")
        w=welcome_page()
        w.welcome()



w=welcome_page()


















w.welcome()