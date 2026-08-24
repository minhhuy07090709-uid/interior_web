import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
load_dotenv()#read .env file, load environment variables

app= Flask(__name__)
db_user=os.getenv('DB_USER')
db_password=os.getenv('DB_PASSWORD')
db_host=os.getenv('DB_HOST')
db_name=os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
db=SQLAlchemy(app)

#---models---
class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(100),nullable=False)
    description=db.Column(db.Text, nullable=False)
    image_url= db.Column(db.String(200),nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
#---Route---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/')
def services():
    return render_template('services.html')

@app.route('/gallery')
def gallery():
    projects=Project.query.all()
    return render_template('gallery.html',projects=projects)
if __name__=='__main__':
    app.run(debug=True)

