from app import db
from app.admin import admin
from flask import render_template, url_for, redirect, request, flash
from app.models import Products, Category, Contact
from .forms import ProductForm, CategoryForm
from werkzeug.utils import secure_filename
from config import Config
import os, uuid

path = os.path.join(admin.static_folder, 'uploads/images')

@admin.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    products = db.session.query(Products.id, Products.filename_images, Products.content, Products.title, Category.category).join(Category).order_by(Products.timestamp.desc()).all()
    categorys = Category.query.all()
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(category=form.title.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('dashboard/index.html', title='Dashboard', products=products, categorys=categorys, form=form)

@admin.route('/create/product', methods=['POST','GET'])
def create():
    form = ProductForm()
    print('target folder: ' + path)

    if not os.path.exists(path):
        os.makedirs(path)

    if form.validate_on_submit():
        filename = secure_filename(form.filename_images.data.filename)
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4().hex, ext)
        destination_save = "/".join([path, filename])
        form.filename_images.data.save(destination_save)

        products = Products(title=form.title.data, price=form.price.data, filename_images=filename, content=form.content.data, kategori_id=form.category.data.id)
        db.session.add(products)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('create.html', title='Tambah Data', form=form)

@admin.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_product(id):
    products = Products.query.filter_by(id=id).first_or_404()
    old = products.filename_images
    destination_del = "/".join([path, old])
    os.remove(destination_del)
    db.session.delete(products)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin.route('/update/<int:id>/<title>', methods=['GET','POST'])
def edit_product(id, title):
    print("Target Folder : " + path)

    form = ProductForm()
    products = Products.query.filter_by(id=id).first_or_404()
    
    if form.validate_on_submit():
        old = products.filename_images
        destination_del = "/".join([path, old])
        os.remove(destination_del)

        filename = secure_filename(form.filename_images.data.filename)
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4().hex, ext)
        destination_save = "/".join([path, filename])
        form.filename_images.data.save(destination_save)
        
        products.price = form.price.data
        products.content = form.content.data
        products.kategori_id = form.category.data.id
        products.filename_images=filename
        products.title=form.title.data
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    elif request.method == 'GET':
        form.title.data = products.title
        form.price.data = products.price
        form.category.data = products.kategori_id
        form.content.data = products.content
        form.filename_images.data = products.filename_images
    return render_template('edit.html', form=form, product=products, title='Edit Data')

@admin.route('/contact')
def contact():
    contact = db.session.query(Contact.id, Contact.email, Contact.name, Contact.telp, Contact.messages, Category.category).join(Category).order_by(Contact.timestamp.desc()).all()
    return render_template('contact.html', title='Hubungi Kami', contact=contact)