from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import time
from datetime import timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:ablo123@130.211.98.36/indoormeas"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="secret"

db = SQLAlchemy(app)


class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True)
	password = db.Column(db.String(500))
	admin = db.Column(db.Boolean)

class Data(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	datetime=db.Column(db.String(50))
	user_id=db.Column(db.Integer)
	cell_id=db.Column(db.Integer)
	rat=db.Column(db.String(5))
	signal_strength=db.Column(db.Integer)
	signal_quality=db.Column(db.Integer)
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)


@app.route("/user", methods=["GET"])
def get_all_users():

	users = User.query.all()
	output=[]
	for user in users:
		user_data={}
		user_data["user_id"]=user.user_id
		user_data["username"]=user.username
		user_data["password"]=user.password
		user_data["admin"]=user.admin
		output.append(user_data)

	return jsonify({"users":output})

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
	user = User.query.filter_by(user_id=user_id).first()

	if not user:
		return jsonify({"message": "no user found"})

	user_data={}
	user_data["user_id"]=user.user_id
	user_data["username"]=user.username
	user_data["password"]=user.password
	user_data["admin"]=user.admin

	return jsonify({"user":user_data})

@app.route("/user", methods=["POST"])
def create_user():
	data  = request.get_json()

	hashed_password=generate_password_hash(data["password"], method="sha256")

	new_user = User(username = data["username"], password=hashed_password, admin=False)
	db.session.add(new_user)
	db.session.commit()
	return jsonify({"message":"new user created"})

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user():
	return ""


@app.route("/login", methods=["POST"])
def login():

	data = request.get_json()

	print(data)

	user = User.query.filter_by(username=data["username"]).first()
	
	if check_password_hash(user.password, str(data["password"])):

		return jsonify({"message":"OK","user_id":user.user_id})

	else:
		return jsonify({"message":"fail"})


@app.route("/data", methods=["POST"])
def send_data():
	data = request.get_json()

	new_data = Data(datetime = data["datetime"], 
					user_id=data["user_id"], 
					cell_id=data["cell_id"],
					rat=data["rat"],
					signal_strength=data["signal_strength"],
					signal_quality=data["signal_quality"],
					latitude=data["latitude"],
					longitude=data["longitude"])

	db.session.add(new_data)
	db.session.commit()
	return jsonify({"message":"new data inserted"})


@app.route("/data", methods=["GET"])
def read_data_all_users():

	data = Data.query.all()
	output=[]
	for data_point in data:

		data_meas={}
		data_meas["datetime"]=data_point.datetime
		data_meas["user_id"]=data_point.user_id
		data_meas["cell_id"]=data_point.cell_id
		data_meas["rat"]=data_point.rat
		data_meas["signal_strength"]=data_point.signal_strength
		data_meas["signal_quality"]=data_point.signal_quality
		data_meas["latitude"]=data_point.latitude
		data_meas["longitude"]=data_point.longitude

		output.append(data_meas)

	return jsonify({"data":output})


@app.route("/data/<user_id>/", methods=["GET"])
def read_data_one_user(user_id):

	data = Data.query.filter_by(user_id=user_id).order_by(Data.datetime).all()
	print(data)

	output=[]
	for data_point in data:

		data_meas={}
		data_meas["datetime"]=data_point.datetime
		data_meas["user_id"]=data_point.user_id
		data_meas["cell_id"]=data_point.cell_id
		data_meas["rat"]=data_point.rat
		data_meas["signal_strength"]=data_point.signal_strength
		data_meas["signal_quality"]=data_point.signal_quality
		data_meas["longitude"]=data_point.longitude
		data_meas["latitude"]=data_point.latitude

		output.append(data_meas)

	return jsonify({"data":output})

@app.route("/data/<user_id>/<start_date>/<end_date>", methods=["GET"])
def read_data_one_user_filter_date(user_id, start_date, end_date):

	#example get by date: http://localhost:5222/data/7/08_04_2018_06_00_00/09_04_2018_12_00_00

	start_date_dt = datetime.datetime.strptime(start_date, '%d_%m_%Y_%H_%M_%S')
	start_date_unix = int(time.mktime(start_date_dt.timetuple()))

	end_date_dt = datetime.datetime.strptime(end_date, '%d_%m_%Y_%H_%M_%S')
	end_date_dt=end_date_dt+timedelta(days=1)
	end_date_unix = int(time.mktime(end_date_dt.timetuple()))

	if start_date_unix==end_date_unix:

		data = Data.query.filter_by(user_id=user_id).filter(datetime=start_date_unix)
	else:
		data = Data.query.filter_by(user_id=user_id).filter(Data.datetime.between(start_date_unix, end_date_unix))


	output=[]
	for data_point in data:

		data_meas={}
		data_meas["datetime"]=data_point.datetime
		data_meas["user_id"]=data_point.user_id
		data_meas["cell_id"]=data_point.cell_id
		data_meas["rat"]=data_point.rat
		data_meas["signal_strength"]=data_point.signal_strength
		data_meas["signal_quality"]=data_point.signal_quality
		data_meas["longitude"]=data_point.longitude
		data_meas["latitude"]=data_point.latitude

		output.append(data_meas)

	return jsonify({"data":output})

if __name__ == "__main__":
	app.run(debug=True, port=5222, host="0.0.0.0")











