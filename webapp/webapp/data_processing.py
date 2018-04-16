"""class to retrieve data from api and convert it to suitable formats for display"""

import requests as api_requests
import pandas as pd
import json 
from collections import OrderedDict

class GetDataApi():

	def __init__(self, api_url,user_id,rat_to_api,date_start_for_api,date_end_for_api):

		self.api_url=api_url
		self.user_id=user_id
		self.rat_to_api=rat_to_api
		self.date_start_for_api=date_start_for_api
		self.date_end_for_api=date_end_for_api

		self.df=pd.DataFrame([])

		self.get_data()

	def __str__():
		print("api connection:"+str(self.r))

	def get_data(self):
		self.r = api_requests.get(self.api_url
			+"data/"
			+str(self.user_id)
			+"/"
			+self.rat_to_api
			+"/"
			+self.date_start_for_api
			+"/"
			+self.date_end_for_api)
		

		json_reponse_data=self.r.json()
		self.json_reponse_data_content=json_reponse_data["data"]

		return self.json_reponse_data_content

	def pandas_dataframe(self):

		self.df=pd.DataFrame(self.json_reponse_data_content)

		self.df['datetime'] = pd.to_datetime(self.df['datetime'],unit='s')

		self.df=self.df.sort_values(by="datetime", ascending=False)

		del self.df["user_id"]

		return self.df

	def table_data(self):

		self.data_rows=json.loads(self.df.to_json(orient="records", date_unit="s"),object_pairs_hook=OrderedDict)

		return self.data_rows




