from flask import Flask, request, flash, redirect, url_for, render_template

from forms import AddMedicalHistoryForm, LoginForm
from Blockchain import Blockchain
from zkp import gen_public_sig

from config import Config

import sqlite3 as sql
conn = sql.connect('loginauth.db')
print("connected to the database..")
conn.close()

# Instantiate or restore the Blockchain 
Blockchain.load_blockchains()

server = Flask(__name__)
server.config.from_object(Config)

status = False
username = ''
password = ''

@server.route('/', methods=['GET'])
def home():

    global status
    global username

    if(not status):
        return redirect('/login')

    return render_template('index.html', user=username)

@server.route('/addreport', methods=['POST', 'GET'])
def addreport():

    if(not status):
        return redirect('/login')

    form = AddMedicalHistoryForm(request.form)

    if (request.method == 'POST' and form.validate()):
        user = form.username.data
        print(type(user))
        visit_type = form.visit_type.data
        report = form.report.data
        medicine = form.medicine.data

        reportID = gen_public_sig(password, report)

        Blockchain.create_transaction(user, username, visit_type, report, medicine, reportID)
        Blockchain.mine(username)

        return redirect(url_for('home'))

    return render_template('addreport.html', form=form, user=username)


@server.route('/viewreport', methods=['POST', 'GET'])
def viewreport():

    if(not status):
        return redirect('/login')

    global username

    chain_data = []

    for block in Blockchain.chain_list:
        chain_data.append(block.__dict__)

    for i in chain_data:
        print(i, '\n')

    chain = Blockchain.get_blockchain(username).chain

    report = []
    if chain != None:
        for block in chain:
            report.append(block['transactions'])

    return render_template('viewreport.html', data=report, user=username)

@server.route('/logout', methods=['GET'])
def logout():
    global status
    global username

    status = False
    username = ''
    return redirect('/login')


@server.route('/login', methods=['GET', 'POST'])
def login():

    global status
    global username
    global password

    form = LoginForm()

    if (request.method == 'POST' and form.validate_on_submit()):

        username = form.username.data
        password = form.password.data

        con = sql.connect("loginauth.db")
        con.row_factory = sql.Row
        
        cur = con.cursor()
        
        cur.execute("select * from logintable where user=(?) AND pass=(?)", (username, password))
        userdata = cur.fetchall()
        if len(userdata) == 0:
            temp = 0
        else:
            temp = 1

        flash('Login requested for user {}]'.format(
            form.username.data))

        if(temp != 0):
            status = True
            username = username
            return redirect('/')

        else:
            flash('Invalid username or password')
            return redirect('/login')

    return render_template('login.html', title='Sign In', form=form)


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
    