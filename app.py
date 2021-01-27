from flask import Flask
from flask import request, jsonify
from flask import render_template
from flask import redirect

import model
from data import month_func

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
    

@app.route('/login',methods=["GET", 'POST'])
def login():
    if request.method =="POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        user = model.login_user(username, pwd)
        try:
            if username == user[0][0] and pwd ==user[0][1]:
                return redirect('/dashboard')
            else:
                return redirect("/loginfailure")  
        except:
            return redirect("/loginfailure")


@app.route('/loginfailure',methods=['GET'])
def loginfailure():
    return render_template('loginfailure.html')


# dashboard
@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')
    

@app.route('/dashboard_2',methods=['POST'])
def dashboard_2():
        date = request.form.get("date")
        purpose = request.form.get("purpose")
        amount = request.form.get("amount")
        amount_array = amount.split('.')
        final_amt = int(amount_array[0])
        model.exp_table() 
        exp = model.insert_exp(date, purpose, final_amt)
        if exp == 'Done':
            return jsonify({'success': 'Data Entry Added'})
        else:
            return jsonify({'error': 'SQL error'})




# register user
@app.route('/register',methods=['GET'])
def register():
    return render_template('register.html')



@app.route('/action', methods=['POST'])
def register_user():
    if request.method =="POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        model.users_table()
        inserted_user = model.insert_user(firstname, lastname, username, pwd)
        if inserted_user == 'Done':
            return "User registered"  
        else:
            return "error"  


# display tables
@app.route('/dashboard/expenses', methods=['GET'])
def expenses():
    data = model.show_exp()
    exp_list = []
    for row in data:
        dict1 = {
            'expenseid': row[0],
            'date': row[1],     
            'purpose': row[2],     
            'amount': row[3]     
        }
        exp_list.append(dict1)
    
    return render_template('expenses.html', result=exp_list)

@app.route('/dashboard/date_exp', methods=['POST'])
def date_exp():
    if request.method =="POST":
        rawdate = request.form.get("date_day")
        date1 = rawdate.split('-')
        DTE = date1[1]
        month = month_func(DTE)
        sqldataraw = model.sum_by_date(rawdate)
        sqldata = sqldataraw[0]

        dict1 = {
            'date': rawdate,
            'amount': sqldata[1]          
        }

    return render_template('dateexpense.html', result=dict1)
        
@app.route('/dashboard/month_exp', methods=['POST'])
def month_exp():
    if request.method =="POST":
        rawdate = request.form.get("date_month")
        date1 = rawdate.split('-')
        DTE = date1[1]
        month = month_func(DTE)
        sqldataraw = model.sum_by_monthtest(rawdate)
        sqldata = sqldataraw[0]

        dict1 = {
            'month': month,          
            'year': sqldata[1],           
            'amount': sqldata[2],           
        }
    return render_template('monthexpense.html', result=dict1)


@app.route('/delete_data', methods=['GET'])
def delete_data():
    model.truncate()
    return "DELETED ALL DATA"

@app.route('/dataexported', methods=['GET'])
def dataexported():
    filename = model.write_csv()
    return "DATA written in "+ filename + ".... Thanks."

if __name__ == "__main__":
    app.run(debug=True)