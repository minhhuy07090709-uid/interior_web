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
    image_url = db.Column(db.String(500), nullable=False)  
    price=db.Column(db.Integer,nullable=True)
    category=db.Column(db.String(50),nullable=True)
    stock_quantity=db.Column(db.Integer,nullable=False,default=0)

    @property
    def stock_status(self):
        if self.stock_quantity<=0:
            return {'label':"Hết hàng",'class':'status-out'}
        elif self.stock_quantity<=5:
            return {'label':f'Còn {self.stock_quantity} sản phẩm','class':"status-low"}
        else:
            return {'label':'Còn hàng','class':"status-in"}
class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)