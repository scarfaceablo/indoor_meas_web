import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = "mysql://root:ablo123@130.211.98.36/indoormeas"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLEMAPS_KEY = "AIzaSyBMdTKuddw9OqSfgAE_A0PnZcqGjjuwZqg"


    