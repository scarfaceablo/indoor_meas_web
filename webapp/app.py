from flask import Flask
from flask import Flask, flash, redirect, render_template, session, abort, request
import os
import requests as api_requests
import pandas as pd

from flask_login import current_user, login_user

api_ip="http://35.195.64.234:5222/"

app = Flask(__name__)

@app.route('/')
def home(user_id=0, username=""):

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        r = api_requests.get(api_ip+"data/"+str(user_id))
        json_reponse_data=r.json()
        json_reponse_data_content=json_reponse_data["data"]
        try:
            df=pd.DataFrame(json_reponse_data_content)
            df['datetime'] = pd.to_datetime(df['datetime'],unit='s')
            df=df.sort_values(by="datetime", ascending=False).head(20)
        except:
            return render_template("login.html")
        
        return render_template('home.html',tables=[df.to_html(classes="data_table")],titles =['Data for user_id: '+str(user_id)], username= username)
 


@app.route('/login', methods=['POST'])
def do_admin_login():

    username_l = request.form['username']
    password_l =  request.form['password']

    r = api_requests.post(api_ip+"login", json={"username":username_l, "password":password_l})
    json_reponse_login=r.json()
    reponse_login=json_reponse_login["message"]
    reponse_user_id=json_reponse_login["user_id"]

    if reponse_login=="OK":
        session['logged_in'] = True
        return home(user_id=reponse_user_id, username=username_l)
    else:
        flash('wrong password!')

    
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4111)