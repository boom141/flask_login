import smtplib, random
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, redirect,url_for,render_template,session, request, flash
from datetime import datetime
from DataBaseTable import *
from settings import app,db
session_register = {}

@app.route("/", methods = ['POST','GET'])
def test():
    session_register = {}
    if request.method == 'POST':
        try:
            if request.form['L_Email']:
                login_email = request.form['L_Email']
                login_password = request.form['L_Pword']
            
                session_username = UserInfo.query.filter_by(username=login_email).first()
                session_password = UserInfo.query.filter_by(password=login_password).first()
                
                if session_username and session_password:
                    return redirect(url_for('user'))
        except:
            if request.form['R_Email']:
                user_email = request.form['R_Email']
                password = request.form['Pword']
                password_auth = request.form['ConfirmPword']
                if not UserInfo.query.filter_by(username=user_email).first():
                
                    if password == password_auth:
                        return redirect(url_for('send_mail', user_email = user_email, password = password))
                else: 
                    return redirect(url_for("test"))
    return render_template("base.html")

@app.route("/register", methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        session_register['name'] = request.form['name']
        session_register['email'] = request.form['email'] 
        session_register['password'] = request.form['password']
        session_register['repeat-password'] = request.form['repeat-password']
        if ( session_register['name'] and
            session_register['email'] and 
            session_register['password'] and 
            session_register['repeat-password'] ):
            return redirect(url_for('otp'))
        else:
            flash(' You should check in on some of those fields above.')
            return render_template("register.html")

    return render_template("register.html")


@app.route("/user")
def user():
    return f'welcome madapaker'

@app.route('/verify_otp', methods=['POST','GET'])
def verify_otp():
    data = request.get_json()
    
    if session_register['otp'] == data['pin_data']:
        Add_User = UserInfo(session_register['name'],session_register['email'],session_register['password'])
        db.session.add(Add_User)
        db.session.commit()
        return redirect(url_for('test'))
    else:
        return redirect(url_for('register')) 

@app.route("/otp", methods = ['POST','GET'])
def otp():

    generated_otp = ''
    for i in range(4):
        generated_otp += str(random.randint(0,9))

    session_register['otp'] = generated_otp
    mail_content = f"YOU'RE OTP PIN IS: {generated_otp}"
    #The mail addresses and password
    sender_address = 'roxas.emerson10dummy@gmail.com'
    sender_pass = 'lnoqdrmszgwibmyz'
    receiver_address = session_register['email']
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'ONE TIME PIN REGISTRATION.'   #The subject line
    
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
   
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

    return render_template('verification.html', email=session_register['email'])

if __name__ == "__main__":
    app.run(debug=True)