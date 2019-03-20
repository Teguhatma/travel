from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email
from app.models import Category, choice_category, Country, choice_country


class ContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    telp = StringField('telp', validators=[DataRequired()])
    subject = StringField('subject', validators=[DataRequired()])
    category = QuerySelectField(u'Category', validators=[DataRequired()], query_factory=choice_category, allow_blank=True, get_label='category', get_pk=lambda x: x.id, blank_text=(u'Kategori'))
    country = QuerySelectField(u'Country', validators=[DataRequired()], query_factory=choice_country, get_pk=lambda x: x.id, get_label='name')
    messages = TextAreaField('Pesan', validators=[DataRequired()])
    submit = SubmitField('Kirim')
