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
from utils import *

bp = Blueprint('userpage', __name__, url_prefix='/userpage')

@bp.route('/userinfo', methods=(['POST', 'GET']))
def userinfo():
    # uid is guaranteed to exist due to design
    userid = session.get('userid')
    user_info = []
    like = []
    dislike = []
    # Extract user information
    cmd = "SELECT userid, account_name, district FROM Users AS U WHERE U.userid = (:id)"
    user_info = g.conn.execute(text(cmd), id=userid).fetchone()
    # Extract current user's like list
    cmd = "SELECT U.userid, F.rid FROM Users AS U JOIN Feel AS F on U.userid=F.userid WHERE U.userid = (:id) AND feel='Like' "
    like = g.conn.execute(text(cmd), id=userid).fetchall()
    # Extract current user's dislike list
    cmd = "SELECT U.userid, F.rid FROM Users AS U JOIN Feel AS F on U.userid=F.userid WHERE U.userid = (:id) AND feel='Dislike' "
    dislike = g.conn.execute(text(cmd), id=userid).fetchall()
    # ic(info)
    return render_template('userpage/userinfo.html', like=like, dislike=dislike, user_info=user_info)


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