from app import db, login
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy import orm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import event


class Category(db.Model):
    __tablename__ = "kategori"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), unique=True)
    jasa = db.relationship("Products", backref="kategori", lazy="dynamic")


def choice_category():
    return Category.query


class Products(db.Model):
    __tablename__ = "Products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    price = db.Column(db.Float)
    slug = db.Column(db.String(100), unique=True)
    content = db.Column(db.String)
    filename_images = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    kategori_id = db.Column(db.Integer, db.ForeignKey("kategori.id"))

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


event.listen(Products.title, "set", Products.generate_slug, retval=False)


class Layanan(db.Model):
    __tablename__ = "Layanan"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(100), unique=True)
    content = db.Column(db.String)
    filename_images = db.Column(db.String(64), unique=True)

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


event.listen(Layanan.title, "set", Layanan.generate_slug, retval=False)


class Contact(db.Model):
    __tablename__ = "kontak"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    messages = db.Column(db.String(120))
    telp = db.Column(db.String(15))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    kategori_id = db.Column(db.Integer, db.ForeignKey("kategori.id"))
    kategori = db.relationship("Category")
    country = db.Column(db.Integer, db.ForeignKey("country.id"))


class Description(db.Model):
    __tablename__ = "Deskripsi"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(64))
    telp = db.Column(db.String(15))
    deskripsi = db.Column(db.String())
    sm_fb = db.Column(db.String(64))
    sm_ig = db.Column(db.String(64))
    sm_wa = db.Column(db.String(64))


class Country(db.Model):
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name = db.Column(db.String, unique=True)
    contact = db.relationship("Contact")


def choice_country():
    return Country.query.order_by(Country.code.asc())


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    filename_images = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
