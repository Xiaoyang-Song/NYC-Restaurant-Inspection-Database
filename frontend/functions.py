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

bp = Blueprint('functions', __name__, url_prefix='/functions')


@bp.route('/restaurants', methods=(['POST', 'GET']))
def restaurants():
    ic(g.user)
    data = []
    if request.method == 'POST':
        district = request.form['district']
        ic(district)
        cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R JOIN Locations as L on R.lid=L.lid  WHERE L.district=(:district)"
        data = g.conn.execute(text(cmd), district=district).fetchall()
        ic(data)
    return render_template('functions/restaurants.html', data=data)


@bp.route('/page/<uid>', methods=(['POST', 'GET']))
def page(uid):
    info = [uid]
    return render_template('functions/page.html', info=info)


@bp.before_app_request
def load_session():
    ic("Loading user session")
    g.conn = get_db_conn()
    userid = session.get('userid')
    ic(userid)
    if userid is None:
        g.user = None
    else:
        cmd = 'SELECT * FROM Users WHERE userid = (:id)'
        ic(cmd)
        g.user = g.conn.execute(text(cmd), id=userid).fetchone()
