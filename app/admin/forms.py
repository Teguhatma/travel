from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    FloatField,
    IntegerField,
)
from wtforms.validators import DataRequired, ValidationError, Email
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Category, choice_category
from flask_ckeditor import CKEditorField
from app.models import Products, Category, Layanan, Contact, Description


class ProductForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    price = FloatField("harga")
    filename_images = FileField(
        "Choose a file",
        validators=[
            FileRequired(u"Gambar tidak boleh kosong!"),
            FileAllowed(["jpeg", "jpg", "png"], u"Hanya upload file gambar!"),
        ],
    )
    category = QuerySelectField(
        u"Category",
        validators=[DataRequired()],
        query_factory=choice_category,
        get_label="category",
        get_pk=lambda x: x.id,
    )
    content = CKEditorField()
    file = FileField("Upload File", validators=[FileAllowed(["pdf"]), FileRequired()])
    submit = SubmitField("Tambah Data")

    def __init__(self, original_title, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_title(self, title):
        if title.data != self.original_title:
            product = Products.query.filter_by(title=self.title.data).first()
            if product is not None:
                raise ValidationError("Please use a different username.")


class EditProductForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    price = FloatField("harga")
    filename_images = FileField(
        "Choose a file",
        validators=[
            FileRequired(u"Gambar tidak boleh kosong!"),
            FileAllowed(["jpeg", "jpg", "png"], u"Hanya upload file gambar!"),
        ],
    )
    category = QuerySelectField(
        u"Category",
        validators=[DataRequired()],
        query_factory=choice_category,
        get_label="category",
        get_pk=lambda x: x.id,
    )
    file = FileField("Upload File", validators=[FileAllowed("pdf"), FileRequired()])
    content = CKEditorField()
    submit = SubmitField("Tambah Data")


class CategoryForm(FlaskForm):
    title = StringField("Tambah Kategori", validators=[DataRequired()])
    submit = SubmitField("Tambah Kategori")

    def validate_title(self, title):
        category = Category.query.filter_by(category=title.data).first()
        if category is not None:
            raise ValidationError("Gunakan nama yang lain")


class DescriptionForm(FlaskForm):
    deskripsi = TextAreaField("deskripsi", validators=[DataRequired()])
    telp = StringField("Nomor", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    sm_fb = StringField("Facebook")
    sm_wa = StringField("Whatapp")
    sm_ig = StringField("Instagram")
    address = StringField("Alamat")
    submit = SubmitField("submit")


class LayananForm(FlaskForm):
    title = StringField("Layanan", validators=[DataRequired()])
    filename_images = FileField(
        "Choose a file",
        validators=[
            FileRequired(u"Gambar tidak boleh kosong!"),
            FileAllowed(["jpeg", "jpg", "png"], u"Hanya upload file gambar!"),
        ],
    )
    content = CKEditorField()
    submit = SubmitField("Tambah Layanan")

    def __init__(self, original_title, *args, **kwargs):
        super(LayananForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_title(self, title):
        if title.data != self.original_title:
            layanan = Layanan.query.filter_by(title=self.title.data).first()
            if layanan is not None:
                raise ValidationError("Please use a different username.")


class EditLayananForm(FlaskForm):
    title = StringField("Layanan", validators=[DataRequired()])
    filename_images = FileField(
        "Choose a file",
        validators=[
            FileRequired(u"Gambar tidak boleh kosong!"),
            FileAllowed(["jpeg", "jpg", "png"], u"Hanya upload file gambar!"),
        ],
    )
    content = CKEditorField()
    submit = SubmitField("Tambah Layanan")
