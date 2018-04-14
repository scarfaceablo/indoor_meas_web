from webapp import db
from flask_login import UserMixin
from webapp import login
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True)
	password = db.Column(db.String(500))
	admin = db.Column(db.Boolean)
	
	def set_password(self, password_web):
		self.password = generate_password_hash(password_web, method="sha256")

	def check_password(self, password_web):
		return check_password_hash(self.password, password_web)

	def get_id(self): 
		return (self.user_id)

	def __repr__(self):
		return '<username {}><password {}><user_id {}>'.format(self.username,self.password, self.user_id)



@login.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))