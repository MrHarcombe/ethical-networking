import functools, hashlib

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from ethical.db import get_db

bp = Blueprint('hauth', __name__, url_prefix='/hauth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM huser WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO huser (username, password) VALUES (?, ?)',
                (username, hashlib.sha1(bytearray(password, "utf8")).hexdigest())
            )
            db.commit()
            return redirect(url_for('hauth.login'))

        flash(error)

    return render_template('hauth/register.html')


###
# parameterized login - SQL-injection hardened
#
@bp.route('/login', methods=('GET', 'POST'))
def plogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM huser WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif user['password'] != hashlib.sha1(bytearray(password, "utf8")).hexdigest():
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['table'] = 'huser'
            return redirect(url_for('home'))

        flash(error)

    return render_template('hauth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('hauth.login'))

        return view(**kwargs)

    return wrapped_view


