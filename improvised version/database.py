import mysql.connector
from user import User

class Database:
    def __init__(self):
        self.mydb=mysql.connector.connect(  host="localhost",
                                            user="root",
                                            passwd="Arishta@123#",
                                            database="db")
        self.cur=self.mydb.cursor(buffered=True,dictionary=True)
        self.cur.execute("CREATE TABLE IF NOT EXISTS members(first_name varchar(50) not null, last_name varchar(50) not null,full_name varchar(100), email varchar(100) not null primary key,password varchar(100) not null);")
        self.mydb.commit()

    def insert_into_members(self,user):
        self.cur.execute("insert into members(first_name,last_name,full_name,email,password) values(%s,%s,%s,%s,%s)",(user.first_name,user.last_name,user.full_name,user.email,user.password))
        self.mydb.commit()

    def user_info(self,atr,email):
        self.cur.execute("select " + atr + " from members where email=%s",(email,))
        row=self.cur.fetchone()
        return row[atr]

    def email_verification(self,email):
        cmd = "select full_name from members where email=%s"
        self.cur.execute(cmd,(email,))
        row = self.cur.fetchone()
        if row:
            return row["full_name"] #email verified
        else:
            return None #email not verified

    def password_verification(self,email,pwd):
        cmd = "select first_name,last_name,full_name,email,password from members where email=%s and password=%s"
        self.cur.execute(cmd, (email,pwd))
        row = self.cur.fetchall()

        if row:
            t=User()
            t.first_name=row[0]["first_name"]
            t.last_name=row[0]["last_name"]
            t.full_name=row[0]["full_name"]
            t.email=email
            t.password=pwd
            return t  # password matches
        else:
            return None  # password does not match

    def list_users(self,name):
        self.cur.execute("select full_name from members where full_name regexp %s",(name,))
        row=self.cur.fetchall()
        l=[]
        for i in row:
            l.append(i["full_name"])
        return l

    def email_from_name(self,name):
        self.cur.execute("select email from members where full_name=%s",(name,))
        row=self.cur.fetchone()
        return row["email"]

    def update_password(self,email,new_password):
        self.cur.execute("update members set password=%s where email=%s",(new_password,email))
        self.mydb.commit()

    def update_email(self,email,new_email):
        self.cur.execute("update members set email=%s where email=%s",(new_email,email))
        self.mydb.commit()

