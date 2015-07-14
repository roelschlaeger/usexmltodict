# vim:ts=4:sw=4:tw=0:wm=0:et
from flask import Flask, render_template, redirect, request, \
    url_for, session, flash, g

from functools import wraps
import sqlite3

app = Flask(__name__)

# TODO -- Security Problem
app.secret_key = "Shhh! Don't Tell!"
app.database = "ample.db"


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    posts = []
    try:
        g.db = connect_db()
        cur = g.db.execute("select * from posts")
        posts = [
            dict(title=row[0], description=row[1])
            for row in cur.fetchall()
        ]
    except sqlite3.OperationalError:
        flash("Your database needs to be installed")
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (
            request.form['username'] != 'admin'
            or
            request.form['password'] != 'admin'
        ):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


def connect_db():
    return sqlite3.connect(app.database)

if __name__ == '__main__':
    app.run(debug=True)

#### end of file ####
