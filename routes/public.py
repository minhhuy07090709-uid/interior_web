#this is where routes are located
from flask import Blueprint, render_template, request, redirect, url_for
from models import Product, Project, Contact
from extensions import db

public_bp= Blueprint('public',__name__)

#---Route---
@public_bp.route('/')
def home():
    return render_template('home.html')

@public_bp.route('/about')
def about():
    return render_template('about.html')

@public_bp.route('/services')
def services():
    return render_template('services.html')

@public_bp.route('/gallery')
def gallery():
    products=Product.query.all()
    return render_template('gallery.html',products=products)

@public_bp.route('/projects')
def projects():
    projects=Project.query.all()
    return render_template('projects.html',projects=projects)

@public_bp.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name= request.form['name']
        email=request.form['email']
        message=request.form['message']

        new_message=Contact(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('public.contact'))
    return render_template('contact.html')

@public_bp.route('/search')
def search():
    query=request.args.get('q','')
    if query:
        products=Product.query.filter(Product.title.ilike(f'%{query}%')).all()
    else:
        products=[]
    return render_template('/gallery.html',products=products,search_query=query)

@public_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@public_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)