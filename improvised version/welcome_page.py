from database import Database
from constants import *
from user import User
db = Database()

class WelcomePage:

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
        email_attempts_count=0
        while (email_attempts_count<email_attempts):
            email = input("Enter your email address\n")
            if (db.email_verification(email)):
                print("Email address already registered with some account\n")
                print("1. Enter a different email address\n2. Go back\n")
                choice = int(input())
                if (choice == 1):
                    pass
                elif (choice == 2):
                    self.welcome()
                    break
                email_attempts_count = email_attempts_count + 1
            else:
                u=User()
                u.first_name=first_name
                u.last_name=last_name
                u.full_name=u.first_name+" "+u.last_name
                u.email=full_name
                u.email=email
                u.password = input("Enter your password\n")
                print("Account successfully created\n")
                db.insert_into_members(u)
                self.welcome()
                break

        if (email_attempts_count>=email_attempts):
            print("Session timeout\n")
            self.welcome()

    def login(self):
        email_attempts_count=0
        while(email_attempts_count<email_attempts):
            email = input("Enter your email address:\n")
            name = db.email_verification(email)
            if name:
                print("Hello, "+ name.upper())
                pwd_attempts_count=0
                while(pwd_attempts_count<password_attempts):
                    password = input("Enter your password\n")
                    user_object = db.password_verification(email,password)
                    if user_object:
                        print("Account verified\n Login successful\n")
                        u = User()
                        u=user_object
                        return("login succesful")

                    else:
                        print("Password does not match\n 1. Enter another password\n 2. Go back")
                        choice = int(input())
                        if (choice == 1):
                            pass
                        elif (choice == 2):
                            self.welcome()
                            break
                        pwd_attempts_count+=1
                else:
                    print("Number of incorrect attempts exceeded\n")
                    self.welcome()
                    break
            else:
                print("Email address does not match\n 1. Enter email again\n 2. Go back")
                choice=int(input())
                if (choice == 1):
                    pass
                elif (choice == 2):
                    self.welcome()
            email_attempts_count += 1
        else:
            print("Number of attempts exceeded\n")
            self.welcome()




wp=WelcomePage()
wp.welcome()
