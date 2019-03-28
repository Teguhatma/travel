from app import db, login
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy import orm
from flask import current_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from slugify import slugify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import event


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = False

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permission += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permission = perm

    def reset_permission(self):
        self.permission = False

    def has_permission(self, perm):
        return self.permission & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            "User": [Permission.WRITE, Permission.MODERATE],
            "Administrator": [Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }
        default_role = "User"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = role.name == default_role
            db.session.add(role)
        db.session.commit()


class Category(db.Model):
    __tablename__ = "kategori"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), unique=True)
    jasa = db.relationship("Products", backref="kategori", lazy="dynamic")


def choice_category():
    return Category.query


class Products(db.Model):
    __tablename__ = "Products"
    __maxsize__ = 16000000

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    price = db.Column(db.Float)
    slug = db.Column(db.String(100), unique=True)
    content = db.Column(db.String)
    filename_images = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    kategori_id = db.Column(db.Integer, db.ForeignKey("kategori.id"))
    file_filename = db.Column(db.String(500))
    file = db.Column(db.LargeBinary(__maxsize__))

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
    password_hash = db.Column(db.String(120))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribut')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["ADMIN"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permisssions):
        return False

    def is_administrator(self):
        return False


login.anonymous_user = AnonymousUser


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
