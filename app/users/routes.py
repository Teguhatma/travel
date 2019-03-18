from app import db, mail
from .forms import ContactForm
from app.models import Contact
from flask import redirect, request, render_template, current_app, url_for, flash
from app.users import users
from flask_mail import Message
from config import Config


@users.route('/hubungi', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            contact = Contact(name=form.name.data, email=form.email.data, messages=form.messages.data, kategori_id=form.category.data.id, telp=form.telp.data, country=form.country.data.id)
            db.session.add(contact)
            db.session.commit()
            
            msg = Message(form.subject.data, sender=current_app.config['MAIL_SENDER'], recipients=['teguhatmayudha@gmail.com'])
            msg.body = form.messages.data
            mail.send(msg)
            flash('Terimakasih telah menghubungi kami.')
            return redirect(url_for('users.contact'))
    return render_template('hubungi.html', form=form, title='Hubungi Kami')