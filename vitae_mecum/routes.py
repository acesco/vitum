from vitae_mecum import app
from flask import render_template, request, flash, session, url_for, redirect
from flask_mail import Mail
from vitae_mecum.forms import ContactForm, SignupForm, SigninForm, JournalForm
from vitae_mecum.models import db, User, JournalEntry
from datetime import date
from sqlalchemy import desc
from vitae_mecum.config import *

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

    if 'uid' in session:
        return redirect(url_for('profile'))

    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            new_user = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            session['uid'] = new_user.uid

            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/profile')
def profile():

    if 'uid' not in session:
        return redirect(url_for('signin'))

    user = User.query.filter_by(uid=session['uid']).first()
    journal = JournalEntry.query.order_by(desc(JournalEntry.date)).limit(5).all()

    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html', journal=journal)


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if 'uid' in session:
        return redirect(url_for('profile'))

    form = SigninForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['uid'] = User.query.filter_by(email=form.email.data).first().uid
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
    if 'uid' not in session:
        return redirect(url_for('signin'))

    session.pop('uid', None)
    return redirect(url_for('home'))


@app.route('/add_journal', methods=['GET', 'POST'])
def add_journal():
    if 'uid' not in session:
        return redirect(url_for('signin'))

    uid = session['uid']

    form = JournalForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('journal_entry.html', form=form, date=form.date.data)
        else:
            new_entry = JournalEntry(session['uid'], form.date.data, form.entry.data)
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('journal', date=str(form.date.data)))  # FIND OUT HOW TO GO TO PAGE

    elif request.method == 'GET':
        return render_template('journal_entry.html', form=form, date=form.date.data)


@app.route('/journal/<date>')
def journal(date):
    if 'uid' not in session:
        return redirect(url_for('signin'))

    uid = session['uid']
    journal_entry = JournalEntry.query.filter_by(uid=uid, date=date).first().entry
    if journal_entry is not None:
        return render_template('journal.html', entry=journal_entry, date=date)
    else:
        return redirect(url_for('add_journal'))


@app.route('/edit_journal/<date>', methods=['GET', 'POST'])
def edit_journal(date):
    if 'uid' not in session:
        return redirect(url_for('signin'))
    uid = session['uid']
    journal_entry = JournalEntry.query.filter_by(uid=uid, date=date).first()
    if journal_entry is not None:
        form = JournalForm(obj=journal_entry)
        if request.method == 'POST':
            if form.validate() == False:
                return render_template('journal_entry.html', form=form, date=date)
            else:
                print(form.date.data)
                print(date)
                if str(form.date.data) != str(date):
                    form.date.errors.append("Cannot change the date.")
                    return render_template('journal_entry.html', form=form, date=date)
                journal_entry.entry = form.entry.data
                db.session.commit()
                return redirect(url_for('journal', date=date))

        elif request.method == 'GET':
            return render_template('journal_entry.html', form=form, date=date)
    else:
        return redirect(url_for('add_journal'))


# NEED TO ADD USERNAME PROPERTY TO USER MODEL SO DON'T HAVE TO USE UID
# NEED TO ADD PRIVATE ATTRIBUTE TO JOURNAL_ENTRY AND FILTER THIS QUERY
@app.route('/<uid>/journal_log/<page>')
def user_journal(uid, page):
    uid, page = int(uid), int(page)
    entries = JournalEntry.query.filter_by(uid=uid).order_by(desc(JournalEntry.date)).paginate(page=page, per_page=POSTS_PER_PAGE)
    return render_template('journal_log.html', entries=entries, uid=uid)


@app.route('/test')
def test():
    return redirect(url_for('user_journal', uid=1, page=2))
