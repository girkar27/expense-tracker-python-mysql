import MySQLdb
from datetime import datetime
import csv

db = MySQLdb.connect("localhost","root","","expenses" )
cur = db.cursor()

def users_table():
    sql = '''CREATE TABLE IF NOT EXISTS users(
        userid INT NOT NULL UNIQUE AUTO_INCREMENT,
        firstname VARCHAR(255) NOT NULL,
        lastname VARCHAR(255),
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255),
        PRIMARY KEY(userid)
        );'''   
    
    cur.execute(sql)


def insert_user(firstname, lastname, username, password):
    try:
        sql = "INSERT INTO users(firstname, lastname, username, password) VALUES('"+firstname+"','"+lastname+"','"+username+"','"+password+"');"
        cur.execute(sql)
        return "Done"
    except: 
        return 'error'



def login_user(username, password):
    try:
        sql = "SELECT username, password FROM users WHERE username = '"+username+"' AND password = '"+password+"' LIMIT 1;"  
        cur.execute(sql)
        result =  cur.fetchall()
        return result
    except:
        return 'error'  




def exp_table():
    sql = '''CREATE TABLE IF NOT EXISTS user_expense(
            id INT NOT NULL UNIQUE AUTO_INCREMENT,
            exp_date DATE,
            purpose VARCHAR(255),
            Cost INT NOT NULL,
            username VARCHAR(255),
            PRIMARY KEY(id),
            FOREIGN KEY (username) REFERENCES users(username)
            );'''
            
    cur.execute(sql)



def insert_exp(exp_date, purpose, Cost):
    if exp_date:
        exp_date = exp_date 
    else:
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d')
        exp_date = formatted_date
    try:
        sql = "INSERT INTO user_expense(exp_date, purpose, Cost) VALUES('"+exp_date+"', '"+purpose+"',"+str(Cost)+");"
        cur.execute(sql)
        return "Done"
    except:
        return "error"

def show_exp():
    sql = "SELECT * FROM user_expense;"  
    cur.execute(sql)
    result =  cur.fetchall()
    if result:
        return result
    else:
        return "None"

def sum_by_date(exp_date):
    sql = "SELECT exp_date, SUM(Cost) FROM user_expense WHERE exp_date = '"+exp_date+"';"
    cur.execute(sql)
    result =  cur.fetchall()
    if result:
        return result
    else:
        return "None"


def sum_by_monthtest(rawdate):
    sql = "SELECT MONTH(exp_date), YEAR(exp_date), SUM(Cost) FROM user_expense WHERE MONTH(exp_date) = MONTH('"+rawdate+"') AND YEAR(exp_date) = YEAR('"+rawdate+"');"
    cur.execute(sql)
    result =  cur.fetchall()
    if result:
        return result
    else:
        return "None"


def truncate():
    sql = "TRUNCATE TABLE user_expense;"
    cur.execute(sql)


def write_csv():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d') 
    filename = 'expense_' + formatted_date +".csv"
    if filename:
        result = show_exp()
        with open(filename, "w") as file:
            for row in result:
                csv.writer(file).writerow(row)
        return filename
    else:
        return "error"
