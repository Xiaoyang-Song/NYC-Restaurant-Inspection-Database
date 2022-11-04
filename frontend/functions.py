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


@bp.route('/page/<rid>', methods=(['POST', 'GET']))
def page(rid):
    # uid is guaranteed to exist due to design
    info = []
    # Extract restaurant information
    cmd = "SELECT * FROM Restaurant AS R JOIN Locations as L on R.lid=L.lid WHERE R.rid = (:id)"
    # ic(cmd)
    info = g.conn.execute(text(cmd), id=rid).fetchone()
    # ic(info)
    userid = session.get('userid')
    # ic(userid)

    # Fetch current state of feeling
    cmd = "SELECT feel FROM FEEL WHERE userid=(:uid) AND rid=(:rid)"
    feel = g.conn.execute(text(cmd), uid=userid, rid=rid).fetchall()
    ic(feel)
    state = 0
    if len(feel) == 0:
        state = FL.IDLE
    elif feel[0][0] == 'Like':
        state = FL.LIKED
    else:
        assert feel[0][0] == 'Dislike'
        state = FL.DISLIKED

    # Handle request: like a state machine
    error = None
    if request.method == 'POST':
        if request.form.get('post') != None:
            reviews = request.form['comment']
            # ic(reviews)
            # TODO: add error handler here by modifying add_reviews function
            add_reviews(g.conn, userid, rid, reviews)
        elif request.form.get('likebutton') != None:
            if state == FL.IDLE:
                add_feel(g.conn, userid, [rid], ['Like'])
                state = FL.LIKED
            elif state == FL.LIKED:
                del_feel(g.conn, userid, rid)
                state = FL.IDLE
            else:
                assert state == FL.DISLIKED
                error = "Cancel your hate first before like!"
        else:
            assert request.form.get('dislikebutton') != None
            if state == FL.IDLE:
                # ic("dislike")
                add_feel(g.conn, userid, [rid], ['Dislike'])
                state = FL.DISLIKED
            elif state == FL.DISLIKED:
                del_feel(g.conn, userid, rid)
                state = FL.IDLE
            else:
                assert state == FL.LIKED
                error = "Cancel your like first before hate!"
    # Get Like & Dislike after update
    cmd = "SELECT feel FROM FEEL WHERE userid=(:uid) AND rid=(:rid)"
    feel = g.conn.execute(text(cmd), uid=userid, rid=rid).fetchall()
    ic(feel)
    # Get reviews
    rev = []
    cmd = "SELECT userid, content, post_time FROM Reviews_Post_Own WHERE rid = (:id)"
    rev = g.conn.execute(text(cmd), id=rid).fetchall()

    # Error handling
    if error is not None:
        flash(error)

    return render_template('functions/page.html', info=info, rev=rev, feel=feel, state=state)


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
