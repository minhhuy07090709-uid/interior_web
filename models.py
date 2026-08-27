from extensions import db

#---models---
class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(100),nullable=False)
    description=db.Column(db.Text, nullable=False)
    image_url= db.Column(db.String(200),nullable=False)
    location=db.Column(db.String(200), nullable=True)
    client_name=db.Column(db.String(100),nullable=True)
    completed_date=db.Column(db.Date,nullable=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)  
class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)