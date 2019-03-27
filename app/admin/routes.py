from app import db
from app.admin import admin
from flask import render_template, url_for, redirect, request, flash
from app.models import Products, Category, Contact, Country, Description, Layanan
from .forms import ProductForm, CategoryForm, DescriptionForm, LayananForm, EditProductForm, EditLayananForm
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from config import Config
from app.models import User, Role
from app.decorators import admin_required
import os, uuid

path = os.path.join(admin.static_folder, "uploads/images")


@admin.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    products = (
        db.session.query(
            Products.id,
            Products.filename_images,
            Products.content,
            Products.title,
            Category.category,
        )
        .join(Category)
        .order_by(Products.timestamp.desc())
        .all()
    )
    categorys = Category.query.all()
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(category=form.title.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    return render_template(
        "index.html",
        title="Dashboard",
        products=products,
        categorys=categorys,
        form=form,
    )


@admin.route("/category/<int:id>/delete")
@login_required
def category_delete(id):
    category = Category.query.filter_by(id=id).first_or_404()
    product = Products.query.filter_by(kategori_id=id).first()
    contact = Contact.query.filter_by(kategori_id=id).first()
    if category.id != product.kategori_id:
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    else:
        flash("Kategori digunakan!","error")
        return redirect(url_for('admin.dashboard'))


@admin.route("product/lihat")
@login_required
def product_lihat():
    products = (
        db.session.query(
            Products.id,
            Products.filename_images,
            Products.content,
            Products.title,
            Products.slug,
            Category.category,
        )
        .join(Category)
        .order_by(Products.timestamp.desc())
        .all()
    )
    return render_template("product_lihat.html", products=products)


@admin.route("/product/create", methods=["POST", "GET"])
@admin_required
@login_required
def product_create():
    form = ProductForm(current_user.username)

    if not os.path.exists(path):
        os.makedirs(path)

    if form.validate_on_submit():
        filename = secure_filename(form.filename_images.data.filename)
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4().hex, ext)
        destination_save = "/".join([path, filename])
        form.filename_images.data.save(destination_save)

        products = Products(
            title=form.title.data,
            price=form.price.data,
            filename_images=filename,
            content=form.content.data,
            kategori_id=form.category.data.id,
        )
        db.session.add(products)
        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    return render_template("product_create.html", title="Tambah Data", form=form)


@admin.route("/product/<int:id>/delete", methods=["POST", "GET"])
@login_required
def delete_product(id):
    products = Products.query.filter_by(id=id).first_or_404()
    old = products.filename_images
    destination_del = "/".join([path, old])
    os.remove(destination_del)
    db.session.delete(products)
    db.session.commit()
    return redirect(url_for("admin.dashboard"))


@admin.route("/product/<int:id>/<slug>/update", methods=["GET", "POST"])
@login_required
def product_update(slug,id):
    products = Products.query.filter_by(id=id, slug=slug).first()
    form = EditProductForm()

    if form.validate_on_submit():
        old = products.filename_images
        destination_del = "/".join([path, old])
        os.remove(destination_del)

        filename = secure_filename(form.filename_images.data.filename)
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4().hex, ext)
        destination_save = "/".join([path, filename])
        form.filename_images.data.save(destination_save)

        products.price = form.price.data
        products.content = form.content.data
        products.kategori_id = form.category.data.id
        products.filename_images = filename
        products.title = form.title.data
        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    elif request.method == "GET":
        form.title.data = products.title
        form.price.data = products.price
        form.category.data = products.kategori_id
        form.content.data = products.content
        form.filename_images.data = products.filename_images
    return render_template(
        "product_create.html", form=form, title="Edit Data"
    )


@admin.route("/contact/lihat")
@login_required
def contact():
    contact = (
        db.session.query(
            Contact.id,
            Contact.email,
            Contact.name,
            Country.code,
            Contact.telp,
            Contact.messages,
            Category.category,
        )
        .join(Category, Country)
        .order_by(Contact.timestamp.desc())
        .all()
    )
    return render_template("contact.html", title="Hubungi Kami", contact=contact)

@admin.route('/deskripsi/lihat')
@login_required
def deskripsi():
    deskripsi = Description.query.all()
    return render_template('deskripsi_lihat.html', deskripsi=deskripsi)

@admin.route("/deskripsi/<int:id>", methods=["GET", "POST"])
@login_required
def deskripsi_edit(id):
    deskripsi = Description.query.filter_by(id=id).first_or_404()
    form = DescriptionForm()
    if form.validate_on_submit():
        deskripsi.email = form.email.data
        deskripsi.telp = form.telp.data
        deskripsi.address = form.address.data
        deskripsi.deskripsi = form.deskripsi.data
        deskripsi.sm_fb = form.sm_fb.data
        deskripsi.sm_ig = form.sm_ig.data
        deskripsi.sm_wa = form.sm_wa.data
        db.session.commit()
        return redirect(url_for("admin.deskripsi"))
    elif request.method == "GET":
        form.email.data = deskripsi.email
        form.telp.data = deskripsi.telp
        form.address.data = deskripsi.address
        form.deskripsi.data = deskripsi.deskripsi
        form.sm_fb.data = deskripsi.sm_fb
        form.sm_ig.data = deskripsi.sm_ig
        form.sm_wa.data= deskripsi.sm_wa
    return render_template("deskripsi_edit.html", form=form)


@admin.route("/layanan/lihat")
@login_required
def layanan_lihat():
    layanan = Layanan.query.all()
    return render_template("layanan_lihat.html", layanan=layanan)


@admin.route("/layanan/tambah", methods=["GET", "POST"])
@login_required
def layanan_create():
    form = LayananForm(current_user.username)
    print("target folder: " + path)

    if not os.path.exists(path):
        os.makedirs(path)

    if form.validate_on_submit():
        filename = secure_filename(form.filename_images.data.filename)
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4().hex, ext)
        destination_save = "/".join([path, filename])
        form.filename_images.data.save(destination_save)

        layanan = Layanan(
            title=form.title.data, filename_images=filename, content=form.content.data
        )
        db.session.add(layanan)
        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    return render_template("layanan_create.html", title="Tambah Data", form=form)


@admin.route("/layanan/<int:id>/<string:slug>/update", methods=["GET", "POST"])
@login_required
def layanan_edit(slug, id):
    layanan = Layanan.query.filter_by(id=id, slug=slug).first_or_404()
    form = EditLayananForm()
    if form.validate_on_submit():
        old = layanan.filename_images
        destination_del = "/".join([path, old])
        os.remove(destination_del)

        filename = secure_filename(form.filename_images.data.filename)
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4().hex, ext)
        destination_save = "/".join([path, filename])
        form.filename_images.data.save(destination_save)

        layanan.title = form.title.data
        layanan.filename_images = filename
        layanan.content = form.content.data
        db.session.commit()
        return redirect(url_for("admin.layanan_lihat"))
    elif request.method == "GET":
        form.title.data = layanan.title
        form.content.data = layanan.content
        form.filename_images.data = layanan.filename_images
    return render_template("layanan_edit.html", form=form)


@admin.route("/layanan/<int:id>/delete", methods=["POST", "GET"])
@login_required
def layanan_delete(id):
    layanan = Layanan.query.filter_by(id=id).first_or_404()
    old = layanan.filename_images
    destination_del = "/".join([path, old])
    os.remove(destination_del)
    db.session.delete(layanan)
    db.session.commit()
    return redirect(url_for("admin.layanan_lihat"))

@admin.route('/contact/<int:id>/delete')
@login_required
def contact_delete(id):
    contact = Contact.query.filter_by(id=id).first_or_404()
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('admin.contact'))



@admin.route("/home")
@login_required
def lihatuser():
    user = (
        db.session.query(
            User.id,
            User.username,
            User.email,
            Role.name.label("namarole"),
            Role.permission
        )
        .join(Role, Role.id == User.id)
        .all()
    )
    return render_template('lihatuser.html', user=user)

@admin.app_errorhandler(404)
def not_found_error(e):
    return render_template("errors/404.html"), 404


@admin.app_errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template("500.html"), 500