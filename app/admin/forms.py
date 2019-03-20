from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField
from wtforms.validators import DataRequired, ValidationError, Email
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Category, choice_category
from flask_ckeditor import CKEditorField


class ProductForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    price = FloatField('harga')
    filename_images = FileField('Choose a file', validators=[FileRequired(u'Gambar tidak boleh kosong!'), FileAllowed(['jpeg', 'jpg', 'png'], u'Hanya upload file gambar!')])
    category = QuerySelectField(u'Category', validators=[DataRequired()], query_factory=choice_category, get_label='category', get_pk=lambda x: x.id)
    content = CKEditorField()
    submit = SubmitField('Tambah Data')


class CategoryForm(FlaskForm):
    title = StringField('Tambah Kategori', validators=[DataRequired()])
    submit = SubmitField('submit')

class DescriptionForm(FlaskForm):
    deskripsi = TextAreaField('deskripsi', validators=[DataRequired()])
    telp = StringField('Nomor', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    sm_fb = StringField('Sosial Media')
    address = StringField('Alamat')
    submit = SubmitField('submit')

class LayananForm(FlaskForm):
    title = StringField('Layanan', validators=[DataRequired()])
    filename_images = FileField('Choose a file', validators=[FileRequired(u'Gambar tidak boleh kosong!'), FileAllowed(['jpeg', 'jpg', 'png'], u'Hanya upload file gambar!')])
    content = CKEditorField()
    submit = SubmitField('Tambah Layanan')
