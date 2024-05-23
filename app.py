from flask import Flask, render_template, url_for, redirect, session, flash, request, make_response
from pymongo import MongoClient, DESCENDING
import bcrypt
from datetime import datetime
import numpy as np
import json
import plotly
import plotly.express as px
import plotly.io as pio
from urllib.parse import quote_plus
import os


from forms import SignupForm, LoginForm, AdminForm, PanelForm, TransactionForm, navForm, settleForm
from functions import AveragePrice, UpdateNAVdata, NumberConv, TotalInvested
from charts import LineCharts
from docker import clientLinkClass

# Flask App
appFlask = Flask(__name__, static_folder = 'static')
appFlask.config['SECRET_KEY'] = "mysecretkey"

# Mongo Client
ck = clientLinkClass()
client = ck.clientLink(True)

db = client['mydatabase']
users_collection = db['users']
office_collection = db['office']
fund_info = db['fund']
transaction_info = db['transactions']
nav_info = db['nav']
settle_info = db['settle']

existing_doc = office_collection.find_one({'username': 'eagles007'})
if existing_doc is None:
    office_collection.insert_one({
        'username': 'eagles007',
        'password': bcrypt.hashpw(b'TheRouge@01', bcrypt.gensalt())
    })


# Flask Routes
@appFlask.route('/')
def landing():
    return render_template('landing.html')

@appFlask.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = users_collection.find_one({'username': username})
        existing_email = users_collection.find_one({'email': email})

        if existing_user:
            flash('Username is already taken', 'danger')
            return render_template('signup.html', form=form)

        if existing_email:
            flash('Email is already registered', 'danger')
            return render_template('signup.html', form=form)

        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'hashed_pass': hashed_pass
        }
        users_collection.insert_one(user_data)
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@appFlask.route('/login', methods=['POST', 'GET'])
def login():
    loginForm = LoginForm()
    
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data

        user = users_collection.find_one({'username': username})
        

        if user and bcrypt.checkpw(password.encode('utf-8'), user['hashed_pass']):
            
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('username', username)
            return resp
            
        else:
            flash('Invalid Username and Password', 'danger')

    return render_template('login.html', form=loginForm)

@appFlask.route('/logout')
def logout():
    request.cookies.clear
    return render_template('landing.html')

@appFlask.route('/admin', methods = ['GET', 'POST'])
def admin():
    adminForm = AdminForm()
    
    if adminForm.validate_on_submit():
        adminUser = adminForm.adminName.data
        adminPass = adminForm.adminPass.data
        
        admin = office_collection.find_one({'username' : adminUser})
        if admin and bcrypt.checkpw(adminPass.encode('utf-8'), admin['password']):
            session['username'] = adminUser
            return redirect(url_for('panel'))
        else:
            flash('You are not registered with the Company BackOffice Database.', 'danger')
            
    return render_template('admin.html', form = adminForm)   

@appFlask.route('/panel', methods = ['GET', 'POST'])
def panel():
    return render_template('panel.html')

@appFlask.route('/panel/fundUpdate', methods = ['GET', 'POST'])
def fund_update():
    form = PanelForm()
    if form.validate_on_submit():
        
        totalAssets = form.totalAssets.data
        totalLiabilities = form.totalLiabilities.data
        nav = form.nav.data
        expenses = form.expenses.data
        
        current_date = datetime.now()
        fund_data = {
            'date': current_date,
            'total_assets': totalAssets,
            'total_liabilities': totalLiabilities,
            'nav': nav,
            'expenses':expenses
        }

        fund_info.insert_one(fund_data)
        flash('Data submitted successfully!', 'success')
    
    
    return render_template('fundUpdate.html', form = form)

# Admin Panel
@appFlask.route('/panel/clientUpdate', methods = ['GET', 'POST'])
def client_update():   
    
    users = users_collection.find({}, {'username': 1})
    client_choices = [(user['username'], user['username']) for user in users]
    
    transForm = TransactionForm(client_choices)
    
    navform = navForm()
    setForm = settleForm()
    latest_doc = db.fund.find_one(sort = [('date', -1)])
    latest_nav = latest_doc['nav']
  
    if transForm.validate_on_submit():
        
        client = transForm.client.data
        particular = transForm.particular.data
        type = transForm.type.data
        debit = transForm.debit.data
        credit = transForm.credit.data
        date = transForm.date.data
        date_to_insert = datetime(date.year, date.month, date.day)
        date = date_to_insert.strftime("%Y-%m-%d")
        
        try:
            transaction_info.insert_one({
                'date': date,
                'client': client,
                'particular': particular,
                'type': type,
                'debit': debit,
                'credit': credit
            })
            flash("Transaction Information added successfully!", 'success')
        except Exception as e:
            flash(f"Error inserting data into MongoDB: {e}", 'error')
    else:
        print("Form validation failed:", transForm.errors) 

    if navform.validate_on_submit():
        date = navform.date.data
        date_to_insert = datetime(date.year, date.month, date.day)
        date = date_to_insert.strftime("%Y-%m-%d")
        client = navform.client.data
        type = navform.type.data
        price = navform.price.data
        amount = navform.amount.data
        shares = round(amount / price, 2) 
   
        try:
            nav_info.insert_one({
                'client': client,
                'date': date,
                'type': type,
                'price': price,
                'qty': shares,
                'remaining_qty': round(shares,2),
                'amount': round(amount,2),
                'realised': 0,
                'unrealised': 0,
                'checked': 0,
                'sold_at': 0
            })
            
            flash("Transaction Information added successfully!", 'success')
        except Exception as e:
            flash(f"Error inserting data into MongoDB: {e}", 'error')
    
    if setForm.validate_on_submit():
        total_settled_amount = 0
        

    return render_template('clientUpdate.html', transForm=transForm, navform = navform, settleForm = setForm)

# Dashboard
@appFlask.route('/dashboard')
def dashboard():
    username_dash = request.cookies.get('username')
    return render_template('dashboard.html', username_dash = username_dash)

@appFlask.route('/dashboard/InvestorRelations')
def investorR():
    username_dash = request.cookies.get('username')
    return render_template('iR.html', username_dash = username_dash)

@appFlask.route('/dashboard/transactions')
def transactions():
    username_trans = request.cookies.get('username')
    transactions = transaction_info.find({'client': username_trans}, {'_id': 0})
    transactions = list(transactions)[::-1]
    
    totalInvestedConst = TotalInvested(transaction_info, username_trans)
    net_balance = totalInvestedConst.total_invested()
    
    numbConv = NumberConv()
    net_balance_format = numbConv.numConv(net_balance,1)
    
    return render_template("transactions.html", transactions = transactions, username_trans = username_trans,
                                                net_balance = net_balance_format)

@appFlask.route('/dashboard/portfolio')
def portfolio():
    user_account = request.cookies.get('username')
    
    totalInvestedConst = TotalInvested(transaction_info, user_account)
    total_invested = totalInvestedConst.total_invested()
    
    ## Total Profit = Unrealised + Realised
    ## Remember to make it interactive so they can bifurcate
    total_profit = 781245612
    
    ## Total Returns = Latest NAV/Average NAV - 1
    latest_doc = db.fund.find_one(sort = [('date', -1)])
    if latest_doc:
        latest_nav = latest_doc['nav']
    else:
        latest_nav = 0

    arr = []
    for docs in nav_info.find({'client' : user_account}):
        arr.append((docs['type'], docs['qty'], docs['price']))

    ap = AveragePrice()
    avg_nav_price = ap.average_price(arr)[0]
    
    if avg_nav_price != 0:
        total_return = latest_nav/avg_nav_price - 1
    else:
        total_return = 0
    
    numbConv = NumberConv()
    total_invested_formatted = numbConv.numConv(total_invested,0)
    total_profit_formatted = numbConv.numConv(abs(total_profit),0)
    total_return_formatted = round(total_return,2)*100
    
    return render_template("portfolio.html", user_account=user_account, total_profit = total_profit, 
                           total_invested_formatted = total_invested_formatted, total_return_formatted=total_return_formatted, 
                           profit_integer_part = total_profit, total_profit_formatted = total_profit_formatted)

@appFlask.route('/dashboard/HedgeFund')
def hedgeFund():
    user_account = request.cookies.get('username')
    
    nav_chart = LineCharts.NavChart()
    nav_chartJSON = json.dumps(nav_chart, cls = plotly.utils.PlotlyJSONEncoder)
    
    return render_template("hedgeFund.html", user_account = user_account, nav_chart = nav_chartJSON)

@appFlask.route('/dashboard/settings')
def settings():
    
    fig = LineCharts.NavChart()
    graph1Json = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    
    return render_template("settings.html", graph1JSON = graph1Json)
    
@appFlask.route('/dashboard/Account')
def account():
    user_account = request.cookies.get('username')
    total_shares = 0
    weighted_price = 0
    withdraw = 0
    unsettel = 0
    settel = 0
    
    latest_doc = db.fund.find_one(sort = [('date', -1)])
    if latest_doc:
        latest_nav = latest_doc['nav']
    else:
        latest_nav = 0
        
    if (nav_info.count_documents({'client': user_account}) == 0):
        print(nav_info.count_documents({'username': user_account}))
        print('fail')
        return render_template('account.html', user_account = user_account, total_shares = round(total_shares,2),
                                            weighted_price = round(weighted_price,2), unsettel = round(unsettel,2),
                                            withdraw = round(withdraw, 2), setteled = round(settel, 2))
    
    else: 
        arr = []
        for docs in nav_info.find({'client' : user_account}):
            arr.append((docs['type'], docs['qty'], docs['price']))

        
        ap = AveragePrice()
        info_price = ap.average_price(arr)
        
        up = UpdateNAVdata()
        newVar = 0
        weighted_price = round(info_price[0],2)
        total_shares = info_price[1]
        info_list = up.update_nav(user_account, latest_nav)
        unsettel = info_list[0]
        settel = info_list[1]
        
        unrealised_formatted = '{:,.0f}'.format(round(unsettel))
        realised_formatted = '{:,.0f}'.format(round(settel))
        
    data = nav_info.find({'client' : user_account})
    
    return render_template('account.html', user_account = user_account, total_shares = round(total_shares,2),
                                            weighted_price = weighted_price, unsettel = unrealised_formatted,
                                            withdraw = round(withdraw, 2), setteled = realised_formatted, data = data)


