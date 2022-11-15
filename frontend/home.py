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

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/homepage', methods=(['POST', 'GET']))
def homepage():
    userid = session.get('userid')
    userdis = session.get('district')
    result,cols = [],0
    if request.method == 'POST':
        if request.form.get('btn_mostLiked') == 'Most Liked':
            cols=3
            cmd = "SELECT R.rid, R.dba, COUNT(*)\
                 FROM Restaurant AS R, Feel AS FL\
                 WHERE R.rid=FL.rid AND FL.feel='Like'\
                 GROUP BY R.rid, R.dba\
                 ORDER BY COUNT(*) DESC\
                 LIMIT 10"
            result = g.conn.execute(text(cmd)).fetchall()
        if request.form.get('btn_mostHated') == 'Most Hated':
            cols=3
            cmd = "SELECT R.rid, R.dba, COUNT(*)\
                        FROM Restaurant AS R, Feel AS FL\
                        WHERE R.rid=FL.rid AND FL.feel='Dislßike'\
                        GROUP BY R.rid, R.dba\
                        ORDER BY COUNT(*) DESC\
                        LIMIT 10"
            result = g.conn.execute(text(cmd)).fetchall()
        if request.form.get('btn_random') == 'Random':
            cols=2
            cmd = "SELECT R.rid, R.dba\
                   FROM Restaurant as R, Locations AS L\
                   WHERE R.lid=L.lid AND L.district=(:district)"
            result = g.conn.execute(text(cmd), district=userdis).fetchall()
            result = list(np.array(result)[np.random.choice(len(result), 10, replace=False)])
            ic(result)
        if request.form.get("keywordsSearch") == 'Search':
            # Text input
            cols=2
            word = request.form['keywords']
            if word !='':
                # ic(word)
                cmd= "SELECT R.rid, R.dba FROM Restaurant AS R WHERE R.dba LIKE (:name) LIMIT 10"
                name_format = "%"+word.upper()+"%"
                result = g.conn.execute(
                    text(cmd), name=name_format).fetchall()

    return render_template("home/homepage.html", result=result,num_col=cols)


# @bp.before_app_request
# def load_session():
#     # ic("Loading user session")
#     g.conn = get_db_conn()
#     userid = session.get('userid')
#     userdis = session.get('district')
#     # ic(userid)
#     if userid is None:
#         g.user = None
#     else:
#         cmd = 'SELECT * FROM Users WHERE userid = (:id)'
#         # ic(cmd)
#         g.user = g.conn.execute(text(cmd), id=userid).fetchone()
