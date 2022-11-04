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

# Define global variables for efficiency
page_stats = {}


@bp.route('/restaurants', methods=(['POST', 'GET']))
def restaurants():
    # ic(g.user)
    data = []
    if request.method == 'POST':
        district = request.form['district']
        # ic(district)
        cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R JOIN Locations as L on R.lid=L.lid  WHERE L.district=(:district)"
        data = g.conn.execute(text(cmd), district=district).fetchall()
        # ic(data)
    return render_template('functions/restaurants.html', data=data)

# TODO: separate this to make it more efficient


@bp.route('/page/<rid>', methods=(['POST', 'GET']))
def page(rid):
    userid = session.get('userid')
    if request.method == 'GET':
        page_stats.clear()
        # ic(request.method)
        # uid is guaranteed to exist due to design
        info = []
        # Extract restaurant information
        cmd = "SELECT * FROM Restaurant AS R JOIN Locations as L on R.lid=L.lid WHERE R.rid = (:id)"
        # ic(cmd)
        info = g.conn.execute(text(cmd), id=rid).fetchone()
        # ic(info)
        # userid = session.get('userid')
        page_stats['info'] = info

        # Fetch current state of feeling
        cmd = "SELECT feel FROM FEEL WHERE userid=(:uid) AND rid=(:rid)"
        feel = g.conn.execute(text(cmd), uid=userid, rid=rid).fetchall()
        # ic(feel)
        state = None
        if len(feel) == 0:
            state = FL.IDLE
        elif feel[0][0] == 'Like':
            state = FL.LIKED
        else:
            assert feel[0][0] == 'Dislike'
            state = FL.DISLIKED
        page_stats['state'] = state

    state = page_stats['state']
    # Handle like/dislike request using state machine
    error = None
    if request.method == 'POST':
        if request.form.get('post') != None:
            reviews = request.form['comment']
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
    page_stats['state'] = state

    if request.method == 'GET' or \
            (request.method == 'POST' and request.form.get('post') is not None):
        # Get reviews
        rev = []
        cmd = "SELECT userid, content, post_time FROM Reviews_Post_Own WHERE rid = (:id)"
        rev = g.conn.execute(text(cmd), id=rid).fetchall()
        page_stats['rev'] = rev

    if request.method == 'GET' or \
            (request.method == 'POST' and request.form.get('post') is None):
        # Get Like & Dislike after update
        cmd = "SELECT feel FROM FEEL WHERE userid=(:uid) AND rid=(:rid)"
        feel = g.conn.execute(text(cmd), uid=userid, rid=rid).fetchall()
        # Update cache
        page_stats['feel'] = feel
        # Display stats
        stats = {}
        # like & dislike stats
        # like
        cmd = "SELECT COUNT(*) FROM FEEL WHERE userid=(:uid) AND rid=(:rid) AND feel='Like'"
        num_like = g.conn.execute(
            text(cmd), uid=userid, rid=rid).fetchall()
        # ic(num_like)
        # dislike
        cmd = "SELECT COUNT(*) FROM FEEL WHERE userid=(:uid) AND rid=(:rid) AND feel='Dislike'"
        num_hate = g.conn.execute(
            text(cmd), uid=userid, rid=rid).fetchall()
        # ic(num_hate)
        stats['num_like'] = num_like[0][0]
        stats['num_hate'] = num_hate[0][0]
        # Update cache
        page_stats['stats'] = stats
    # Error handling
    if error is not None:
        flash(error)

    return render_template('functions/page.html', info=page_stats['info'], rev=page_stats['rev'],
                           feel=page_stats['feel'], state=page_stats['state'],
                           stats=page_stats['stats'])


@bp.before_app_request
def load_session():
    # ic("Loading user session")
    g.conn = get_db_conn()
    userid = session.get('userid')
    # ic(userid)
    if userid is None:
        g.user = None
    else:
        cmd = 'SELECT * FROM Users WHERE userid = (:id)'
        # ic(cmd)
        g.user = g.conn.execute(text(cmd), id=userid).fetchone()
