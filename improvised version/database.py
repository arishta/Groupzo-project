import mysql.connector
class Database:
    def __init__(self):
        self.mydb=mysql.connector.connect(  host="localhost",
                                            user="root",
                                            passwd="Arishta@123#",
                                            database="db")
        self.cur=self.mydb.cursor(buffered=True)
        self.cur.execute("CREATE TABLE IF NOT EXISTS members(first_name varchar(50) not null, last_name varchar(50) not null,full_name varchar(100), email varchar(100) not null primary key,password varchar(100) not null);")
        self.mydb.commit()

    def insert_into_members(self,user):
        self.cur.execute("insert into members(first_name,last_name,full_name,email,password) values(%s,%s,%s,%s,%s)",(user.first_name,user.last_name,user.full_name,user.email,user.password))
        self.mydb.commit()

    def user_info(self,atr,email):
        self.cur.execute("select " + atr + " from members where email=%s",(email,))
        row=self.cur.fetchall()
        return row[0][0]


    def email_verification(self,email):
        cmd="select email from members where email=%s"
        self.cur.execute(cmd,(email,))
        row=self.cur.fetchall()
        if row:
            return True #email exists
        else:
            return False #email does not exist

    def list_users(self,name):
        self.cur.execute("select full_name from members where full_name regexp %s",(name,))
        row=self.cur.fetchall()
        return row

    def email_from_name(self,name):
        self.cur.execute("select email from members where full_name=%s",(name,))
        row=self.cur.fetchone()
        return row[0]

    def update_password(self,email,new_password):
        self.cur.execute("update members set password=%s where email=%s",(new_password,email))
        self.mydb.commit()

    def update_email(self,email,new_email):
        self.cur.execute("update members set email=%s where email=%s",(email,new_email))
        self.mydb.commit()
