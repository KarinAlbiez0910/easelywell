import os
from dotenv import load_dotenv

load_dotenv(override=False)

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'postgresql://easelyadmin:easely123@localhost/easelywell'
        
    # Handle both DATABASE_URL and SQLALCHEMY_DATABASE_URI
    db_url = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    # Fix for postgres:// vs postgresql:// (Railway uses postgres://)
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = db_url or 'postgresql://easelyadmin:easely123@localhost/easelywell'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



    


