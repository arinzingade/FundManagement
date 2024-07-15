
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from pymongo import MongoClient
from config import Config
import email_validator
from flask import Flask

# Flask App
appFlask = Flask(__name__, static_folder = 'static')
appFlask.config.from_object(Config)

# Mongo Client
client = MongoClient(appFlask.config['MONGO_URI'])

db = client['mydatabase']
users_collection = db['users']
office_collection = db['office']
fund_info = db['fund']
transaction_info = db['transactions']

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_confirm_password(self, field):
        if (self.password.data != self.confirm_password.data):
            raise ValidationError('Passwords must Match.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('LogIn')

class AdminForm(FlaskForm):
    adminName = StringField('Employee ID', validators=[DataRequired()])
    adminPass = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PanelForm(FlaskForm):
    totalAssets = FloatField('Total Assets', validators=[DataRequired()])
    totalLiabilities = FloatField('Total Liabilities', validators=[DataRequired()])
    nav = FloatField('NAV', validators=[DataRequired()])
    expenses = FloatField('Expenses', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class TransactionForm(FlaskForm):
    
    def __init__(self, client_choices, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.client.choices = client_choices
    
    date = DateField('Date')
    client = SelectField('Client', validators=[DataRequired()])
    particular = SelectField('Particular', choices = [('DEPOSIT', 'Deposit'), ('WITHDRAW', 'Withdraw')], validators=[DataRequired()])
    type = SelectField('Type', choices = [('NETBANKING', 'Net Banking'), ('UPI', 'Unified Payment'), ('FEES', 'Fees')], validators=[DataRequired()])
    debit = FloatField('Debit')
    credit = FloatField('Credit')
    submit = SubmitField('Submit')

class navForm(FlaskForm):
    def __init__(self, client_choices, *args, **kwargs):
        super(navForm, self).__init__(*args, **kwargs)
        self.client.choices = client_choices
    
    date = DateField('Date', validators=[DataRequired()])
    client = SelectField('Client', validators=[DataRequired()])
    type = SelectField('Type', choices = [('BUY', 'BUY'), ('SELL', 'SELL')], validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    amount = FloatField('amount', validators=[DataRequired()])
    submit = SubmitField('submit')    

class settleForm(FlaskForm):
    
    settle_confirm = StringField('Type "Settle All Accounts" ', validators=[DataRequired()])
    submit = SubmitField('Settle All Accounts')

class DailyPnL(FlaskForm):
    
    date = DateField('Date', validators = [DataRequired()])
    realised = FloatField('Realised', validators=[DataRequired()])

class BondForm(FlaskForm):
    def __init__(self, client_choices, *args, **kwargs):
        super(BondForm, self).__init__(*args, **kwargs)
        self.client.choices = client_choices
    
    date = DateField('Date', validators=[DataRequired()])
    client = SelectField('Client', validators=[DataRequired()])
    type = SelectField('Type', choices = [('ISSUE', 'ISSUE'), ('PAYMENT', 'PAYMENT')], validators=[DataRequired()])
    amount = FloatField('amount', validators=[DataRequired()])
    rate = FloatField('rate in %')
    tenure = FloatField('tenure in months')
    submit = SubmitField('submit')    
