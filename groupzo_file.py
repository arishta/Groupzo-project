import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Arishta@123#",
    database="grp"
)

mycursor = mydb.cursor(buffered=True)

def update_member_count():
    sql="update mygroups set member_count=(select count(*) from groups_and_members where groups_and_members.group_id=mygroups.group_id)"
    mycursor.execute(sql)
    mydb.commit()

def check_group(group):
    sql="select group_name from mygroups where group_name=%s"
    mycursor.execute(sql,(group,))
    mycursor.fetchone()
    if (mycursor.rowcount==0):
        return 0 #no group exists
    else:
        return 1 #group exists


def add_member(group_name,name):
    full_name=getfull_nameFromName(name)
    sql="insert into groups_and_members(user_id,group_id) values((select user_id from members where full_name=%s),(select group_id from mygroups where group_name=%s))"
    val=(full_name,group_name)
    mycursor.execute(sql,val)
    mydb.commit()
    update_member_count()

def remove_member(group_name,name):
    full_name=getfull_nameFromName(name)
    sql="delete from groups_and_members where group_id=(select group_id from mygroups where group_name=%s) and user_id=(select user_id from members where full_name=%s)"
    val=(group_name,full_name)
    mycursor.execute(sql,val)
    mydb.commit()
    update_member_count()

def insert_into_members(first_name,last_name,email,password):
    sql="insert into members(first_name,last_name,email,password) values(%s,%s,%s,%s)"
    val=(first_name,last_name,email,password)
    mycursor.execute(sql,val)
    sql="update members set full_name=concat(first_name,' ',last_name)"
    mycursor.execute(sql)
    mydb.commit()

def insert_into_groups_and_members(user_id,group_id):
    sql="insert into groups_and_members(user_id,group_id) values(%s,%s)"
    val=(user_id,group_id)
    mycursor.execute(sql,val)
    mydb.commit()
    update_member_count()

def insert_into_mygroups(group_name,description):
    sql="insert into mygroups(group_name,description) values(%s,%s)"
    val=(group_name,description)
    mycursor.execute(sql,val)
    mydb.commit()


def truncate_tables(table_name):
    sql="truncate table %s" % table_name
    mycursor.execute(sql)
    mydb.commit()

def display_table(table_name):
    sql = " select * from %s "% table_name
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for row in myresult:
        print(row)

def delete_from_mygroups(group_name):
    sql="delete from groups_and_members where group_id in (select group_id from mygroups where group_name=%s)"
    val=(group_name,)
    mycursor.execute(sql,val)
    mydb.commit()
    sql="delete from mygroups where group_name=%s"
    val=(group_name,)
    mycursor.execute(sql,val)
    mydb.commit()
    update_member_count()

def delete_from_members(name):
    full_name=getfull_nameFromName(name)
    sql="delete from groups_and_members where user_id in (select user_id from members where full_name=%s)"
    val=(full_name,)
    mycursor.execute(sql,val)
    mydb.commit()
    sql="delete from members where full_name=%s"
    val=(full_name,)
    mycursor.execute(sql,val)
    mydb.commit()
    update_member_count()

def welcome():
    print("Welcome to Groupzo: a social networking site :\n")
    print("1. Create a new account \n2. Login to your existing account\n")
    choice=(int(input()))
    while(1):
        if (choice==1):
            create_new_account()
            break
        elif (choice==2):
            login()
            break
        else:
            print("Enter a valid choice:\n")

def create_new_account():
    print("Fill in the following details\n")
    first_name=input("Enter your first name\n")
    last_name=input("Enter your last name\n")
    while(1):
        email=input("Enter your email address\n")
        sql="select email from members where email=%s"
        mycursor.execute(sql,(email,))
        mycursor.fetchone()
        if (mycursor.rowcount==0):
            break
        else:
            print("Email address is already registered: 1. Press 1 to login \n 2. Press 2 to enter a different email address\n 3. Press 3 to exit\n")
            choice=int(input())
            if (choice==1):
                login()
                return
            elif (choice==2):
                continue
            elif (choice==3):
                welcome()
                return
            else:
                print("Enter a valid choice\n")
    password=input("Enter a password\n")
    insert_into_members(first_name,last_name,email,password)
    print("Account successfully created\n Press 1 to login \n Press 2 to exit")
    while(1):
        choice=int(input())
        if (choice==1):
            login()
            return
        elif (choice==2):
            welcome()
            return
        else:
            print("Enter a valid choice\n")

def login():
    while(1):
        email=input("Enter your email address:\n")
        sql="select email from members where email=%s"
        mycursor.execute(sql,(email,))
        mycursor.fetchone()
        if (mycursor.rowcount!=0):
            break
        else:
            print("Email address not found \n 1. Press 1 to create a new account\n 2. Press 2 to enter again \n 3. Press 3 to exit\n")
            choice=int(input())
            if (choice==1):
                create_new_account()
                return
            elif (choice==2):
                login()
            else:
                welcome()
                return
    while(1):
        password=input("Enter your password\n")
        sql="select password from members where password=%s"
        mycursor.execute(sql,(password,))
        mycursor.fetchone()
        if (mycursor.rowcount!=0):
            print("Login successful\n")
            home_page(email)
            return
        else:
            print("Wrong password\n 1. Press 1 to enter again \n 2. Press 2 to exit\n")
            choice=int(input())
            if (choice==1):
                continue
            elif (choice==2):
                welcome()
                return

def insert_into_friends(user,friend):
    sql="insert into friends(user,friends) values(%s,%s)"
    val=(user,friend)
    mycursor.execute(sql,val)
    mydb.commit()

def delete_from_friends(user,friends):
    sql="delete from friends where user=%s and friends=%s"
    val=(user,friends)
    mycursor.execute(sql,val)
    mydb.commit()

def insert_into_pending_requests(user,pending):
    sql="insert into pending_requests values(%s,%s)"
    val=(user,pending)
    mycursor.execute(sql,val)
    mydb.commit()

def delete_from_pending_requests(user,pending):
    sql="delete from pending_requests where user=%s and pending=%s"
    val=(user,pending)
    mycursor.execute(sql,val)
    mydb.commit()

def view_groups(email):
    sql = '''select group_name,description
        FROM groups_and_members gm
        JOIN members m ON m.user_id=gm.user_id
        JOIN mygroups mg ON mg.group_id=gm.group_id where email=%s'''
    mycursor.execute(sql, (email,))
    myresult=mycursor.fetchall()
    if (mycursor.rowcount!=0):
        for row in myresult:
            print(row)
    else:
        print("No groups\n")


def view_profile(email):
    print("FIRST NAME:")
    sql="select first_name from members where email=%s"
    mycursor.execute(sql,(email,))
    for row in mycursor.fetchone():
        print(row)
    print("\nLAST NAME:")
    sql="select last_name from members where email=%s"
    mycursor.execute(sql,(email,))
    for row in mycursor.fetchone():
        print(row)
    print("\nEMAIL ADDRESS:\n"+email)
    print("\nFRIEND LIST:")
    view_friend_list(email)
    print("GROUPS :")
    view_groups(email)




def search_user(name,email_user):
    sql="select email from members where first_name=%s or last_name=%s"
    val=(name,name)
    mycursor.execute(sql,val)
    for row in mycursor.fetchone():
        email=row
    view_profile(email)



def change_password(email):
    old=input("Enter your old password\n")
    sql="select password from members where email=%s"
    mycursor.execute(sql,(email,))
    for row in mycursor.fetchone():
        x=row

    while(1):
        if (x==old):
            new=input("Enter your new password\n")
            sql="update members set password=%s where email=%s"
            val=(new,email)
            mycursor.execute(sql,val)
            print("Password successfully updated\n")
            mydb.commit()
            return
        else:
            print("Wrong password\n press 1 to try again\n press 2 to exit\n")
            choice=int(input())
            if (choice==1):
                change_password(email)
            elif (choice==2):
                home_page(email)
            else:
                print("Enter a valid choice\n")


def log_out():
    print("Successfully logged out\n")
    welcome()


def getfull_nameFromEmail(email):
    sql="select full_name from members where email=%s"
    mycursor.execute(sql,(email,))
    myresult=mycursor.fetchone()
    for row in myresult:
        return row

def check_pending_requests_of_user(email):
    full_name=getfull_nameFromEmail(email)
    sql="select pending from pending_requests where user=%s"
    val=(full_name,)
    mycursor.execute(sql,val)
    mycursor.fetchone()
    if (mycursor.rowcount==0):
        return 0 #there are no pending requests
    else:
        return 1 #there are pending requests

def check_unaccepted_requests_of_user(email):
    full_name = getfull_nameFromEmail(email)
    sql = "select pending from pending_requests where pending=%s"
    val = (full_name,)
    mycursor.execute(sql, val)
    mycursor.fetchone()
    if (mycursor.rowcount == 0):
        return 0  # all requests sent by the user are accepted
    else:
        return 1  # there are requests sent by user which are not accepted



def view_pending_requests(email):
    full_name=getfull_nameFromEmail(email)
    if (check_pending_requests_of_user(email)==1):
        sql="select pending from pending_requests where user=%s"
        mycursor.execute(sql,(full_name,))
        for row in mycursor:
            print(row)
    else:
        print("There are no pending requests\n")

def getfull_nameFromName(name):
    sql="select full_name from members where first_name=%s or last_name=%s or full_name=%s"
    val=(name,name,name)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    for row in myresult:
        return row

def member_exist(name):
    sql="select * from members where full_name regexp %s"
    mycursor.execute(sql,(name,))
    mycursor.fetchone()
    if mycursor.rowcount!=0:
        return 1 #exists
    else:
        return 0



def accept_pending_requests(email):
    full_name_of_user=getfull_nameFromEmail(email)
    if check_pending_requests_of_user(email)==1:
        name=input("Enter the name of user whose request you want to accept\n")
        full_name=getfull_nameFromName(name)
        insert_into_friends(full_name_of_user,full_name)
        insert_into_friends(full_name,full_name_of_user)
        delete_from_pending_requests(full_name_of_user,full_name)
        print(full_name_of_user+" and " +full_name+" are now friends\n")
    else:
        print("You don't have any pending requests\n")


def view_sent_requests(email):
    full_name=getfull_nameFromEmail(email)
    sql="select user from pending_requests where pending=%s"
    mycursor.execute(sql,(full_name,))
    myresult=mycursor.fetchall()
    if (mycursor.rowcount==0):
        print("You don't have any sent requests\n")
    else:
        for row in myresult:
            print(row)

def check_friend_of_user(email):
    full_name=getfull_nameFromEmail(email)
    sql="select friends from friends where user=%s"
    mycursor.execute(sql,(email,))
    mycursor.fetchone()
    if mycursor.rowcount==0:
        return 1 #this user has friends
    else:
        return 0 #the user does not have any friends

def remove_friend(email):
    full_name=getfull_nameFromEmail(email)
    if (check_friend_of_user(email) == 1):
        name = input("Enter name of person who you want to remove as friend\n")
        if (member_exist(name) == 1):
            name_friend = getfull_nameFromName(name)
            ch = check_friend(full_name, name_friend)
            if ch == 1:
                delete_from_friends(full_name, name_friend)
                delete_from_friends(name_friend, full_name)
                print(name_friend + " has been removed from your friend list\n")
            else:
                print(name_friend + " is not found in your friend list\n")
        else:
            print("User does not exist\n")
    else:
        print("You don't have any friends in your friend list\n")


def check_friend(user1,user2):
    sql="select friends from friends where user=%s and friends=%s"
    val=(user1,user2)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    if (myresult):
        return 1 #they are friends
    else:
        return 0 #they are not friends

def send_friend_request(email):
    name=input("Enter name of user who you want to send request to:\n ")
    if (member_exist(name)==1):
        full_name=getfull_nameFromEmail(email)
        full_name_of_person=getfull_nameFromName(name)
        ch=check_friend(full_name_of_person,full_name)
        if (ch==0):
            p=check_pending_request(full_name,full_name_of_person)
            if (p==0):
                insert_into_pending_requests(full_name_of_person,full_name)
                print("Friend request sent to "+full_name_of_person)
            else:
                print("You have already sent friend request to "+name)
        else:
            print("You and "+full_name_of_person+" are already friends\n")
    else:
        print("User not found\n")

def view_friend_list(email):
    full_name=getfull_nameFromEmail(email)
    sql="select friends from friends where user=%s"
    mycursor.execute(sql,(full_name,))
    myresult=mycursor.fetchall()
    if mycursor.rowcount!=0:
        print("Here is your friend list\n")
        for row in myresult:
            print(row)
    else:
        print("Empty friend list\n")

def check_pending_request(user_from,user_to):
    sql="select pending from pending_requests where user=%s and pending=%s"
    val=(user_to,user_from)
    mycursor.execute(sql,val)
    mycursor.fetchone()
    if (mycursor.rowcount==0):
        return 0 #no pending request
    else:
        return 1 #pending request exists


def cancel_requests(email):
    full_name=getfull_nameFromEmail(email)
    if (check_unaccepted_requests_of_user(email)==1):
        name=input("Enter name of person whose request you want to cancel\n")
        if (member_exist(name)==1):
            name_friend=getfull_nameFromName(name)
            if check_pending_request(full_name,name_friend)==0:
                print("You have not sent request to "+name_friend)
            else:
                print("Friend request cancelled\n")
                delete_from_pending_requests(name_friend,full_name)
        else:
            print("User does not exist\n")
    else:
        print("You haven't sent requests to any  user yet\n")


def home_page(email):
    full_name=getfull_nameFromEmail(email)
    print("WELCOME TO YOUR GROUPZO ACCOUNT, "+full_name.upper())
    print("What do you want to do? Choose from the following:\n")
    print(" 1. MY PROFILE\n 2. SEARCH A USER\n 3. FRIENDS SECTION\n 4. GROUPS SECTION\n 5. SETTINGS\n 6. LOGOUT\n ")
    choice=int(input())
    while(1):
        if (choice==1):
            view_profile(email)
            redirect_to_home_page(email)
            break
        elif (choice==2):
            name=input("Enter the name of user :\n")
            search_user(name,email)
            redirect_to_home_page(email)
            break
        elif (choice==3):
            friends_section(email)
            break
        elif (choice==4):
            groups_section(email)
            break
        elif (choice==5):
            settings(email)
            break
        elif (choice==6):
            log_out()
            welcome()
        else:
            print("Enter a valid choice\n")





def friends_section(email):
    print("What do you want to do?")
    print("1. VIEW FRIEND LIST\n2. SEND REQUESTS\n3. ACCEPT REQUESTS\n4. REMOVE FROM FRIENDS\n5. GO BACK TO HOME PAGE\n")
    choice=int(input())
    if (choice == 1):
        view_friend_list(email)
        redirect_to_friends_section(email)

    elif (choice == 2):
        ch = int(input("1. View sent requests\n2. Cancel sent requests\n3. Send request\n"))
        if (ch == 1):
            view_sent_requests(email)
            redirect_to_friends_section(email)

        elif (ch == 2):
            cancel_requests(email)
            redirect_to_friends_section(email)

        elif (ch == 3):
            send_friend_request(email)
            redirect_to_friends_section(email)
    elif (choice == 3):
        ch = int(input("1.View pending requests\n 2. Accept pending requests\n"))
        while (1):
            if (ch == 1):
                view_pending_requests(email)
                redirect_to_friends_section(email)
            elif (ch == 2):
                accept_pending_requests(email)
                redirect_to_friends_section(email)
            else:
                print("Enter a valid choice:\n")
    elif (choice == 4):
        remove_friend(email)
        redirect_to_friends_section(email)
    elif (choice == 5):
        home_page(email)

def settings(email):
    print("1.Press 1 to change password \n2.Press to update email address \n3.Press 3 to go to home page ")
    choice=int(input())
    if choice==1:
        change_password(email)
        redirect_to_settings(email)
    elif (choice==2):
        while(1):
            newEmail=input("Enter the new email address\n")
            sql="select email from members where email=%s"
            mycursor.execute(sql,(email,))
            mycursor.fetchone()
            if mycursor.rowcount==0:
                break
            else:
                print("Email address is already registered with some account\n 1. Enter 1 to enter a different email\n 2. Enter 2 to go back\n")
                ch=int(input())
                if (ch==1):
                    continue
                else:
                    settings(email)
                    break
        sql="update members set email=%s where email=%s"
        val=(newEmail,email)
        mycursor.execute(sql,val)
        mydb.commit()
        print("Email successfully updated\n")
        redirect_to_settings(email)
    elif (choice==3):
        home_page(email)

def display_groups():
    sql="select group_name,description from mygroups"
    mycursor.execute(sql)
    myresult=mycursor.fetchall()
    if (mycursor.rowcount==0):
        print("No groups found")
    else:
        print("Here is the list of groups\n")
        for index,row in enumerate(myresult,start=1):
            print(index,row)


def groups_section(email):
    print("choose from the following\n")
    print(" 1. View groups \n 2. Create a new group\n 3. Remove an existing group\n 4. Add member to a group\n 5. Remove member from a group\n 6. Go back to the home page")
    choice=int(input())
    if (choice==1):
        print("1. View groups that you are a part of ")
        print("2. View all groups")
        ch=int(input())
        if (ch==1):
            view_groups(email)
        else:
            display_groups()
        redirect_to_groups_section(email)
    elif (choice==2):
        group_name=input("Enter the name of the group\n")
        group_des=input("Enter the description of the group\n")
        insert_into_mygroups(group_name,group_des)
        print("Group sucessfully created\n")
        redirect_to_groups_section(email)
    elif (choice==3):
        group_name=input("Enter the name of the group you want to remove\n")
        if (check_group(group_name)==1):
            delete_from_mygroups(group_name)
            print("Group successfully deleted\n")
        else:
            print("No such group exists\n")
        redirect_to_groups_section(email)
    elif (choice==4):
        name=input("Enter the name of the person you want to add to the group\n")
        if (member_exist(name) == 1):
            group_name = input("Enter the group name\n")
            if (check_group(group_name) == 1):
                add_member(group_name, name)
                print(name + " has been added to " + group_name)
            else:
                print("No such group exists\n")
        else:
            print("No such user exists\n")

        redirect_to_groups_section(email)
    elif (choice==5):
        name = input("Enter the name of the person you want to remove from the group\n")
        if (member_exist(name)==1):
            group_name = input("Enter the group name\n")
            if (check_group(group_name)==1):
                remove_member(group_name,name)
                print(name+" has been removed from "+group_name)
            else:
                print("Group does not exist\n")
        else:
            print("User not found\n")
        redirect_to_groups_section(email)
    elif (choice==6):
        home_page(email)

def redirect_to_home_page(email):
    choice=int(input("press 1 to go back to home page\n"))
    if (choice==1):
        home_page(email)
    else:
        print("invalid choice\n enter again\n")
        redirect_to_home_page(email)


def redirect_to_friends_section(email):
    choice=int(input("press 1 to go back to friends section\n"))
    if (choice==1):
        friends_section(email)
    else:
        print("invalid choice\n enter again\n")
        redirect_to_friends_section(email)


def redirect_to_groups_section(email):
    choice=int(input("press 1 to go back to groups section\n"))
    if (choice==1):
        groups_section(email)
    else:
        print("invalid choice\n enter again\n")
        redirect_to_groups_section(email)

def redirect_to_settings(email):
    choice=int(input("press 1 to go back to settings\n"))
    if (choice==1):
        settings(email)
    else:
        print("invalid choice\n enter again\n")
        redirect_to_settings(email)

def main():
    welcome()

if __name__=="__main__":
    main()