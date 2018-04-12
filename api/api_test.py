from flask import Flask
from flask_restful import Resource, Api, reqparse
import sqlalchemy
import pandas as pd


app = Flask(__name__)
api = Api(app)

class ApiInfo(Resource):
	def post(self):
		return "API info: "

class Login(Resource):
	def post(self):

		parser = reqparse.RequestParser()
		parser.add_argument('username', type=str)
		parser.add_argument('password', type=str)

		username_from_a=parser.parse_args()["username"]
		password_from_a=parser.parse_args()["password"]

		engine_gcloud=sqlalchemy.create_engine("mysql+pymysql://root:ablo123@130.211.98.36/indoormeas")
		connection_gcloud=engine_gcloud.connect()
		result = connection_gcloud.execute("""select password from users where username = '"""+username_from_a+"""'""")
		for row in result:
			password=row[0]

		if password_from_a == password:
			return True
		else:
			return False
        
class GetData(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('user_id', type=int)

		user_id=parser.parse_args()["user_id"]

		engine_gcloud=sqlalchemy.create_engine("mysql+pymysql://root:ablo123@130.211.98.36/indoormeas")
		connection_gcloud=engine_gcloud.connect()
		query_get_data="""select * 
			from data where user_id = """+str(user_id)+"""
			order by datetime desc
			"""

		df_get_data=pd.read_sql(sql=query_get_data ,con=connection_gcloud)

		return df_get_data.to_json(orient="index")

class PostData(Resource):
	def post(self):

		parser = reqparse.RequestParser()
		parser.add_argument('datetime', type=str)
		parser.add_argument('user_id', type=int)
		parser.add_argument('cell_id', type=int)
		parser.add_argument('rat', type=str)
		parser.add_argument('signal_strength', type=int)
		parser.add_argument('signal_quality', type=int)

		datetime=parser.parse_args()["datetime"]
		user_id=parser.parse_args()["user_id"]
		cell_id=parser.parse_args()["cell_id"]
		rat=parser.parse_args()["rat"]
		signal_strength=parser.parse_args()["signal_strength"]
		signal_quality=parser.parse_args()["signal_quality"]

		engine_gcloud=sqlalchemy.create_engine("mysql+pymysql://root:ablo123@130.211.98.36/indoormeas")
		connection_gcloud=engine_gcloud.connect()

		print(datetime)
		print(user_id)

		query_post_data="""select * 
			from data where user_id = """+str(user_id)+"""
			order by datetime desc
			"""

		df_get_data=pd.read_sql(sql=query_get_data ,con=connection_gcloud)

		return df_get_data.to_json(orient="index")


api.add_resource(Login, '/login', endpoint='login')

api.add_resource(ApiInfo, "/info", endpoint="info")

api.add_resource(GetData, "/data/get", endpoint="data/get")

api.add_resource(PostData, "/data/post", endpoint="data/post")


if __name__ == '__main__':
    app.run(debug=True, port=5111, host="0.0.0.0")



