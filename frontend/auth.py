import os
from os import abort
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.pool import NullPool
from flask import Blueprint, Flask, flash, request, session, render_template, g, redirect, Response, url_for
from icecream import ic
import functools
from werkzeug.security import check_password_hash, generate_password_hash
from db_utils import *
from users import *

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['roles']
        ic(role)
        error = None
        user = g.conn.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        account_name = request.form['account_name']
        password = request.form['password']
        dob = request.form['dob']
        district = request.form['district']
        error = None

        # Access database
        g.conn = get_db_conn()
        print(userid)
        print(dob)
        if not userid:
            error = 'Userid is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            dob_val = f"'{dob}'" if dob != 'NULL' else 'NULL'
            dis_val = f"'{district}'" if district != 'NULL' else 'NULL'
            if district != 'NULL':
                assert district in LOCATION_SET
            schema = f"Users(userid, account_name, passcode, dob, district)"
            try:
                cmd = f"INSERT INTO {schema} VALUES({userid}, '{account_name}', '{password}', {dob_val}, {dis_val})"
                cursor = g.conn.execute(cmd)
                g.conn.commit()
            except IntegrityError:
                error = f"User {userid} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


if __name__ == '__main__':
    ic("registration scripts")
