from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField
from wtforms.validators import DataRequired, ValidationError, Email
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Category, choice_category


class ProductForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    price = FloatField('harga')
    filename_images = FileField('Gambar', validators=[FileRequired(u'Gambar tidak boleh kosong!'), FileAllowed(['jpeg', 'jpg', 'png'], u'Hanya upload file gambar!')])
    category = QuerySelectField(u'Category', validators=[DataRequired()], query_factory=choice_category, get_label='category', get_pk=lambda x: x.id)
    content = TextAreaField()
    submit = SubmitField('submit')


class CategoryForm(FlaskForm):
    title = StringField('Tambah Kategori')
    submit = SubmitField('submit')
