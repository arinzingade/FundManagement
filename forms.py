
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from pymongo import MongoClient
from docker import clientLinkClass
import email_validator

ck = clientLinkClass()
client = ck.clientLink(True)

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
    
    client_choices = [(user['username'], user['username']) for user in users_collection.find({}, {'username' : 1})]
    
    date = DateField('Date')
    client = SelectField('Client', choices = client_choices, validators=[DataRequired()])
    particular = SelectField('Particular', choices = [('DEPOSIT', 'Deposit'), ('WITHDRAW', 'Withdraw')], validators=[DataRequired()])
    type = SelectField('Type', choices = [('NETBANKING', 'Net Banking'), ('UPI', 'Unified Payment')], validators=[DataRequired()])
    debit = FloatField('Debit')
    credit = FloatField('Credit')
    submit = SubmitField('Submit')

class navForm(FlaskForm):
    client_choices = [(user['username'], user['username']) for user in users_collection.find({}, {'username' : 1})]
    
    date = DateField('Date', validators=[DataRequired()])
    client = SelectField('Client', choices = client_choices, validators=[DataRequired()])
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
