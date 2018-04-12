from webapp import app

from flask import render_template,flash, redirect, url_for, session

from webapp.forms import LoginForm

import requests as api_requests
import pandas as pd 
import json
from datetime import datetime

api_ip="http://35.195.64.234:5222/"

@app.template_filter('datetimeformat')
def datetimeformat(value, format="%d-%m-%Y %H:%M:%S"):
	return datetime.fromtimestamp(value).strftime(format)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)

        r = api_requests.post(api_ip+"login", json={"username":form.username.data, "password":form.password.data})
        json_reponse_login=r.json()

        reponse_login=json_reponse_login["message"]

        if reponse_login == "fail":
            print("wrong credentials") 
            return render_template('login.html', title='Sign In', form=form)

        reponse_user_id=json_reponse_login["user_id"]

        user_id_json = json.dumps({"user_id":reponse_user_id})


        if reponse_login=="OK":
        	return redirect(url_for('index',user_id_json=user_id_json))

        #flash('Login requested for user {}, remember_me={}'.format(
        #    form.username.data, form.remember_me.data))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/home')
def index():
	user = {'username': 'admin'}

	user_id=api_requests.args["user_id_json"]

	print(user_id)

	r = api_requests.get(api_ip+"data/"+str(user_id))
	json_reponse_data=r.json()

	json_reponse_data_content=json_reponse_data["data"]
	df=pd.DataFrame(json_reponse_data_content)

	df['datetime'] = pd.to_datetime(df['datetime'],unit='s')
	df=df.sort_values(by="datetime", ascending=False).head(100)

	data_rows=json.loads(df.to_json(orient="records", date_unit="s"))


	#print(json_reposnse_data_content)

	return render_template('index.html',title="home page", data_rows=data_rows)