#this is where routes are located
from flask import Blueprint, render_template, request, redirect, url_for
from models import Product, Project, Contact
from extensions import db
from sqlalchemy import or_
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
    return search()

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
PRICE_RANGES={
    'duoi-1tr': (0, 1000000),
    '1-3tr': (1000000, 3000000),
    '3-5tr': (3000000, 5000000),
    '5-10tr': (5000000, 10000000),
    'tren-10tr': (10000000, None),
}
@public_bp.route('/search')
def search():
    query=request.args.get('q','')
    category=request.args.get('category','')
    price_ranges=request.args.getlist('price_range')

    products_query=Product.query
    if query:
        products_query=products_query.filter(Product.title.ilike(f'%{query}%'))
    if category:
        products_query=products_query.filter(Product.category==category)
    if price_ranges:
        conditions=[]
        for r in price_ranges:
            if r in PRICE_RANGES:
                min_p,max_p=PRICE_RANGES[r]
                if max_p is None:
                    conditions.append(Product.price>=min_p)
                else:
                    conditions.append(Product.price.between(min_p,max_p))
        if conditions:
            products_query=products_query.filter(or_(*conditions))

    products=products_query.all()
    return render_template(
        'gallery.html',
        products=products,
        search_query=query,
        selected_category=category,
        selected_price_ranges=price_ranges
    )
@public_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@public_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)