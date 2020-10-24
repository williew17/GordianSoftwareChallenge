import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    GORDIAN_API_KEY = os.environ.get('GORDIAN_API_KEY') or 'you-will-never-guess'