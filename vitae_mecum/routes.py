from vitae_mecum import app
from flask import render_template, request, flash, session, url_for, redirect
from flask_mail import Mail
from vitae_mecum.forms import ContactForm, SignupForm, SigninForm
from models import db, User

mail = Mail()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            #  msg = Message(form.subject.data, sender='', recipients=[''])
            #  msg.body = """
            #  From: %s <%s>
            #  %s
            #  """ % (form.name.data, form.email.data, form.message.data)
            #  mail.send(msg)
            return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if 'email' in session:
        return redirect(url_for('profile'))

    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email

            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/profile')
def profile():

    if 'email' not in session:
        return redirect(url_for('signin'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if 'email' in session:
        return redirect(url_for('profile'))

    form = SigninForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))

    session.pop('email', None)
    return redirect(url_for('home'))
