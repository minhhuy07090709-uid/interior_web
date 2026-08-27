import os 
from functools import wraps
from flask import Blueprint, render_template, request, redirect,url_for,session
from models import Product, Project,Contact
from extensions import db
admin_bp= Blueprint('admin',__name__,url_prefix='/admin')
ADMIN_USERNAME=os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD=os.getenv('ADMIN_PASSWORD')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username==ADMIN_USERNAME and password==ADMIN_PASSWORD:
            session['logged_in']=True
            return redirect(url_for('admin.home'))
        else:
            error='Sai tên đăng nhập hoặc mật khẩu'
    return render_template('admin/login.html',error=error)

@admin_bp.route('/')
@login_required
def home():
    return render_template('admin/home.html')

@admin_bp.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('admin.login'))

#ADMIN CRUD
@admin_bp.route('/products')
@login_required
def products():
    all_products= Product.query.all()
    return render_template('admin/products.html',products=all_products)

@admin_bp.route('/products/add',methods=['GET','POST'])
@login_required
def add_product():
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        image_url=request.form['image_url']

        new_product=Product(title=title, description=description, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html',product=None)

@admin_bp.route('/products/edit/<int:product_id>',methods=['GET','POST'])
@login_required
def edit_product(product_id):
    product=Product.query.get_or_404(product_id)

    if request.method=='POST':
        product.title=request.form['title']
        product.description=request.form['description']
        product.image_url=request.form['image_url']
        db.session.commit()
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html',product=product)

@admin_bp.route('/products/delete/<int:product_id>',methods=['POST'])
@login_required
def delete_product(product_id):   
    product=Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin.products'))