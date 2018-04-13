from webapp import app

from flask import render_template,flash, redirect, url_for, session

from webapp.forms import LoginForm, DatePicker_start_day

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

        r = api_requests.post(api_ip+"login", json={"username":form.username.data, "password":form.password.data})
        json_reponse_login=r.json()

        reponse_login=json_reponse_login["message"]

        if reponse_login == "fail":
            print("wrong credentials") 
            return render_template('login.html', title='Sign In', form=form)

        

        #user_id_json = json.dumps({"user_id":reponse_user_id})


        if reponse_login=="OK":

        	reponse_user_id=json_reponse_login["user_id"]
        	session['user_id'] = reponse_user_id

        	return redirect("/home")

        #flash('Login requested for user {}, remember_me={}'.format(
        #    form.username.data, form.remember_me.data))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/home', methods=["GET","POST"])
def index():

	form_start_day = DatePicker_start_day()

	if form_start_day.validate_on_submit():

		#date_from_picker=form.dt.data.strftime('%d-%m-%Y')
		date_from_picker_start=datetime.strptime(form_start_day.dt.data.strftime('%d-%m-%Y'),'%d-%m-%Y')
		date_from_picker_end=datetime.strptime(form_start_day.dt2.data.strftime('%d-%m-%Y'),'%d-%m-%Y')

		print(date_from_picker_start, date_from_picker_end)

		user_id=session.get("user_id", None)
		print(user_id)
		r = api_requests.get(api_ip+"data/"+str(user_id))
		json_reponse_data=r.json()

		json_reponse_data_content=json_reponse_data["data"]
		df=pd.DataFrame(json_reponse_data_content)

		df['datetime'] = pd.to_datetime(df['datetime'],unit='s')

		mask_date = ((df["datetime"] > date_from_picker_start)&(df["datetime"] < date_from_picker_end))

		df=df.loc[mask_date]

		df=df.sort_values(by="datetime", ascending=False).head(100)

		data_rows=json.loads(df.to_json(orient="records", date_unit="s"))

	#print(json_reposnse_data_content)

		return render_template('index.html',
								title="home page", 
								data_rows=data_rows,
								form_start_day=form_start_day)



	return render_template('index_empty.html',
								title="home page", 
								form_start_day=form_start_day)







