from database import Database
from user import User
from constants import *

db=Database()

class HomePage:

    def __init__(self,u):
        self.t=u

    def options(self):
        print("Welcome to your Groupzo account, "+self.t.full_name.upper())
        print("1.View your profile\n2.Search a user\n3.Settings\n4.Logout")
        choice=int(input())
        if (choice==1):
            self.view_profile()
        elif (choice==2):
            self.search_user()
        elif (choice==3):
            self.settings(self.t)
        elif (choice==4):
            self.logout()

    def view_profile(self):
        self.t.display_user_info()
        self.options()

    def search_user(self):
        name = input("Enter the name of the user\n")
        row = db.list_users(name)
        if (row):
            for index, val in enumerate(row):
                print(index + 1, ".", *val)
            ch = int(input("Enter the number to search for that user:\n"))
            name = row[ch - 1][0]
            v = User()
            v.display_user_info()
        else:
            print("No user found\n")
        self.options()

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
                        self.options()
                        break
            self.options()
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
                                    self.options()
                                    break
                            else:
                                db.update_email(u.email, new_email)
                                u.email = new_email
                                print("Email successfully updated\n")
                                break
                        self.options()
                else:
                    print("Wrong password\n 1. Verify again\n 2. Go back\n")
                    c=int(input())
                    if c==1:
                        continue
                    else:
                        self.options()

        elif (ch == 3):
            self.options()
            w.welcome()


    def logout(self):
        print("Successfully logged out\n")
        w=WelcomePage
        w.welcome()
