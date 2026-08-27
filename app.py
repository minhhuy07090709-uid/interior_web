import os
from dotenv import load_dotenv
from flask import Flask
from extensions import db
load_dotenv()#read .env file, load environment variables

app= Flask(__name__)
db_user=os.getenv('DB_USER')
db_password=os.getenv('DB_PASSWORD')
db_host=os.getenv('DB_HOST')
db_name=os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

db.init_app(app)

from routes.public import public_bp
from routes.admin import admin_bp
app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

if __name__=='__main__':
    app.run(debug=True)

