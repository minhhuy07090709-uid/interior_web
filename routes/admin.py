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

@admin_bp.route('/projects')
@login_required
def projects():
    all_projects=Project.query.all()
    return render_template('admin/projects.html',projects=all_projects)

@admin_bp.route('/projects/add',  methods=['GET','POST'])
@login_required
def add_project():

    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        image_url=request.form['image_url']
        location=request.form['location']
        client_name=request.form['client_name']
        new_project=Project(
            title=title,
            description=description,
            image_url=image_url,
            location=location,
            client_name=client_name
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html',project=None)

@admin_bp.route('/projects/edit/<int:project_id>',methods=['GET','POST'])
@login_required
def edit_project(project_id):
    project=Project.query.get_or_404(project_id)
    if request.method=='POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.image_url = request.form['image_url']
        project.location = request.form['location']
        project.client_name = request.form['client_name']
        db.session.commit()
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', project=project)

@admin_bp.route('projects/delete/<int:project_id>',methods=['POST'])
@login_required
def delete_project(project_id):
    project=Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('admin.projects'))

@admin_bp.route('/messages')
@login_required
def messages():
    all_messages=Contact.query.order_by(Contact.id.desc()).all()
    return render_template('admin/messages.html',messages=all_messages)

@admin_bp.route('/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Contact.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('admin.messages'))

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
