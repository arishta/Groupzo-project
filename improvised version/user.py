class User:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.password = None
        self.email = None

    def display_user_info(self):
        print("FIRST NAME: ")
        print(self.first_name)
        print("LAST NAME: ")
        print(self.last_name)
        print("FULL NAME: ")
        print(self.full_name)
        print("EMAIL ADDRESS: "+self.email)



