from webapp import app

from flask import render_template,flash, redirect, url_for, session

from webapp.forms import LoginForm, DatePicker_start_day, MakeCallButton, RegistrationForm

import requests as api_requests
import pandas as pd 
import json
from datetime import datetime

from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly
import numpy as np

import pusher

from webapp import db
from flask_login import current_user, login_user, logout_user, login_required
from webapp.models import User

from flask import send_from_directory
import os

api_ip="http://35.195.64.234:5222/"

@app.template_filter('datetimeformat')
def datetimeformat(value, format="%d-%m-%Y %H:%M:%S"):
	return datetime.fromtimestamp(value).strftime(format)


@app.route('/favicon.ico', methods=["GET"])
def favicon():
	return send_from_directory(directory=os.path.join(app.root_path, 'webbapp/templates'),
                               filename='favicon.ico', 
                               mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect("/home")

	form = LoginForm()

	if form.validate_on_submit():

		user=User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password")
			return redirect("/index")
		print(user)
		login_user(user, remember=form.remember_me.data)

		return redirect("/home")

	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/index")


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect("/home")

	form = RegistrationForm()

	if form.validate_on_submit():

		user = User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("New user created")
		return redirect("/index")

	return render_template("register.html", form=form)


@app.route('/home', methods=["GET","POST"])
@login_required
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

		mask_date = ((df["datetime"] >= date_from_picker_start)&(df["datetime"] <= date_from_picker_end))

		df=df.loc[mask_date]

		df=df.sort_values(by="datetime", ascending=False).head(100)
		del df["user_id"]
		data_rows=json.loads(df.to_json(orient="records", date_unit="s"))


		#rng = pd.date_range('1/1/2011', periods=7500, freq='H')
		#ts = pd.Series(np.random.randn(len(rng)), index=rng)

		graphs = [
		        dict(
		            data=[
		                dict(
		                    x=list(df["datetime"]),
		                    y=list(df["signal_strength"]),
		                    type='scatter',
		                    name="Signal strength[dBm]"
		                ),
		                	dict(
		                    x=list(df["datetime"]),
		                    y=list(df["signal_quality"]),
		                    type='scatter',
		                    name="Signal quality[dB]"
		                )
		            ],
		            layout=dict(
		                title='Signal Strength and Quality',
		                height=400,
		                width=800
		            )
		        )

		    ]

	    # Add "ids" to each of the graphs to pass up to the client
	    # for templating
		ids = ['graph_{}'.format(i) for i, _ in enumerate(graphs)]

		graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

		#print(json_reposnse_data_content)

		return render_template('index.html',
								title="home page", 
								data_rows=data_rows,
								form_start_day=form_start_day,
								ids=ids,
								graphJSON=graphJSON)



	return render_template('index_empty.html',
								title="home page", 
								form_start_day=form_start_day)



@app.route('/remoteapp', methods=['GET', 'POST'])
@login_required
def remoteapp():
	
	pusher_client = pusher.Pusher(
	  app_id='509027',
	  key='bff446cfed9e4cfc6570',
	  secret='c150b2aaf785cbb0df16',
	  cluster='eu',
	  ssl=True
	)

	form_make_call = MakeCallButton()

	if form_make_call.validate_on_submit():
		print(form_make_call.pin.data)
		if form_make_call.pin.data == "33714195":
			pusher_client.trigger('my-channel', 'my-event', {'message': 'push to make a call'})


	return render_template('remoteapp.html', form_make_call=form_make_call)





