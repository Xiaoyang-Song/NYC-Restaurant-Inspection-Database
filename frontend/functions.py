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


@bp.route('/restaurants')
def restaurants():
    ic(g.user)
    return render_template('functions/restaurants.html')


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
