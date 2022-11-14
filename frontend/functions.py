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
v_page_stats = {}


@bp.route('/restaurants', methods=(['POST', 'GET']))
def restaurants():
    # ic(g.user)
    result = []
    if request.method == 'POST':
        # Get all possible form answers
        district = request.form['district']
        rating = request.form['rating']
        has_vio = request.form['vio']
        # Text input
        dba = request.form['res_keyword']
        cuisine = request.form['cui_keyword']
        # ic(district)
        data = []
        if district != 'None':
            cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R JOIN Locations as L on R.lid=L.lid  WHERE L.district=(:district)"
            district_data = g.conn.execute(
                text(cmd), district=district).fetchall()
            data.append(district_data)

        if rating != 'None':
            cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R, Graded as GR, Grade as G WHERE GR.rid = R.rid AND GR.gid = G.gid AND G.grade=(:rating)"
            grade_data = g.conn.execute(
                text(cmd), rating=rating).fetchall()
            data.append(grade_data)

        if has_vio != 'None':
            cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R, Violate AS VR \
                   WHERE R.rid=VR.rid"
            if has_vio == 'Yes':
                vio_data = g.conn.execute(text(cmd)).fetchall()
            else:
                cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R EXCEPT " + cmd
                vio_data = g.conn.execute(text(cmd)).fetchall()
            data.append(vio_data)

        if dba != "":
            cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R \
                   WHERE UPPER(R.dba) LIKE (:dba)"
            dba_format = "%"+dba.upper()+"%"
            ic(dba_format)
            dba_data = g.conn.execute(text(cmd), dba=dba_format).fetchall()
            data.append(dba_data)

        if cuisine != "":
            cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R \
                   WHERE UPPER(R.cuisine) LIKE (:cuisine)"
            cuisine_format = "%"+cuisine.upper()+"%"
            ic(cuisine_format)
            cuisine_data = g.conn.execute(
                text(cmd), cuisine=cuisine_format).fetchall()
            data.append(cuisine_data)

        # List intersection
        # Fetch all restaurants first
        cmd = "SELECT R.rid, R.dba, R.cuisine FROM Restaurant AS R"
        result = g.conn.execute(
            text(cmd), district=district).fetchall()
        # Get intersection based on selection
        for item in data:
            result = set(result) & set(item)
        # Sort results based on rid
        result = sorted(result, key=lambda x: x[0], reverse=False)
    return render_template('functions/restaurants.html', data=result)

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

        # Get recent violation records
        cmd = "SELECT V.v_time, Vn.code, Vn.v_description, Vn.critical_flag, I.i_type \
               FROM Restaurant AS R, Violate AS V , Violation AS Vn, Inspect AS IR, Inspection AS I \
               WHERE Vn.vid=V.vid AND R.rid=V.rid AND R.rid=(:rid) AND IR.rid=R.rid AND I.iid=IR.iid AND IR.i_time=V.v_time \
               ORDER BY V.v_time"
        violation = g.conn.execute(text(cmd), rid=rid).fetchall()
        page_stats['violation'] = violation

        # Get recent grading records
        cmd = "SELECT GR.g_time, G.grade, G.score\
               FROM Grade AS G, Restaurant AS R, Graded AS GR\
               WHERE G.gid=GR.gid AND R.rid=GR.rid AND R.rid=(:rid)"
        grades = g.conn.execute(text(cmd), rid=rid).fetchall()
        page_stats['grade'] = grades

    state = page_stats['state']
    # Handle like/dislike request using state machine
    update_comment = False
    error = None
    if request.method == 'POST':
        if request.form.get('post') != None:
            reviews = request.form['comment']
            # TODO: add error handler here by modifying add_reviews function
            add_reviews(g.conn, userid, rid, reviews)
            update_comment = True
        elif request.form.get('delrev') != None:
            revid = request.form['delrev'].partition('#')[-1]
            ic(revid)
            del_reviews(g.conn, revid)
            update_comment = True
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

    if request.method == 'GET' or update_comment:
        # Get reviews
        rev = []
        cmd = "SELECT userid, content, post_time, rev_id FROM Reviews_Post_Own WHERE rid = (:id)"
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
                           feel=page_stats['feel'], state=page_stats['state'], grade=page_stats['grade'],
                           stats=page_stats['stats'], userid=userid, violation=page_stats['violation'])


@bp.route('/violations', methods=(['POST', 'GET']))
def violations():
    # stats: inspections by types
    stats = []
    cmd = "SELECT I.i_type, COUNT(*) AS count\
           FROM Inspection as I, inspect AS IR, Restaurant AS R\
           WHERE I.iid = IR.iid AND R.rid = IR.rid\
           GROUP BY I.i_type\
           ORDER BY COUNT(*) DESC"
    stats = g.conn.execute(text(cmd)).fetchall()
    ic(stats)

    # find violations by inspection types
    cmd = "SELECT I.i_type, COUNT(*) AS count\
        FROM Inspection as I, inspect AS IR, Restaurant AS R, Violate AS VR\
        WHERE I.iid = IR.iid AND R.rid = IR.rid AND VR.rid=R.rid\
        GROUP BY I.i_type\
        ORDER BY COUNT(*) DESC"
    violation_dict = dict(g.conn.execute(text(cmd)).fetchall())
    for idx, (itype, num) in enumerate(stats):
        ic(itype)
        ic(num)
        if violation_dict.get(itype) is not None:
            stats[idx] = list(stats[idx]) + [violation_dict[itype]]
        else:
            stats[idx] = list(stats[idx]) + [0]

    ic(stats)
    # Process data
    # for type, num in stats:

    # stats2: violations by critical
    stats2 = []
    cmd = "SELECT Vn.critical_flag, COUNT(*) AS count FROM Restaurant AS R, Violate AS V , Violation AS Vn WHERE Vn.vid=V.vid AND R.rid=V.rid GROUP BY Vn.critical_flag"
    stats2 = g.conn.execute(text(cmd)).fetchall()

    # stats3: violation by district
    stats3 = []
    cmd = "SELECT L.district, COUNT(*) AS count\
           FROM Restaurant AS R, Inspect AS IR, Locations AS L\
           WHERE R.lid=L.lid AND IR.rid = R.rid\
           GROUP BY L.district"
    stats3 = g.conn.execute(text(cmd)).fetchall()

    cmd = "SELECT L.district, COUNT(*) AS count\
           FROM Restaurant AS R, Violate AS V, Locations AS L\
           WHERE R.lid=L.lid AND V.rid = R.rid\
           GROUP BY L.district"
    district_vio_dict = dict(g.conn.execute(text(cmd)).fetchall())
    # TODO: optimization later
    for idx, (dtype, num) in enumerate(stats3):
        if district_vio_dict.get(dtype) is not None:
            stats3[idx] = list(stats3[idx]) + [district_vio_dict[dtype]]
        else:
            stats3[idx] = list(stats3[idx]) + [0]
    stats3 = sorted(stats3, key=lambda x: x[2]/x[1], reverse=True)

    mostRestaurant_data = []
    data = []
    if request.method == 'POST':
        if request.form.get('btn_mostRecent') == 'Most Recent':
            cmd = "SELECT R.rid, R.dba, V.v_time, Vn.code, Vn.v_description, Vn.critical_flag\
                 FROM Restaurant AS R, Violate AS V , Violation AS Vn\
                 WHERE Vn.vid=V.vid AND R.rid=V.rid\
                 ORDER BY V.v_time DESC\
                 LIMIT 10"
            data = g.conn.execute(text(cmd)).fetchall()
        if request.form.get('btn_mostCritical') == 'Most Critical':
            cmd = "SELECT R.rid, R.dba, V.v_time, Vn.code, Vn.v_description, Vn.critical_flag\
                 FROM Restaurant AS R, Violate AS V , Violation AS Vn\
                 WHERE Vn.vid=V.vid AND R.rid=V.rid AND Vn.critical_flag='Critical'\
                 ORDER BY V.v_time DESC\
                 LIMIT 10"
            data = g.conn.execute(text(cmd)).fetchall()
        if request.form.get('btn_mostNonCritical') == 'Most non-critical':
            cmd = "SELECT R.rid, R.dba, V.v_time, Vn.code, Vn.v_description, Vn.critical_flag\
                 FROM Restaurant AS R, Violate AS V , Violation AS Vn\
                 WHERE Vn.vid=V.vid AND R.rid=V.rid AND Vn.critical_flag='Not Critical'\
                 ORDER BY V.v_time DESC\
                 LIMIT 10"
            data = g.conn.execute(text(cmd)).fetchall()
            # cmd = "SELECT R2.rid, R2.dba, COUNT(*) FROM Violate AS V2, Restaurant AS R2 WHERE V2.rid=R2.rid GROUP BY R2.rid ORDER BY COUNT(*) DESC LIMIT 10"
            # mostRestaurant_data = g.conn.execute(text(cmd)).fetchall()

            # cmd = "SELECT R.rid, R.dba, V.v_time, Vn.code, Vn.v_description, Vn.critical_flag FROM (SELECT R2.rid FROM Violate AS V2, Restaurant AS R2 WHERE V2.rid=R2.rid GROUP BY R2.rid ORDER BY COUNT(*) DESC LIMIT 10) AS R0, Restaurant AS R, Violate AS V , Violation AS Vn WHERE Vn.vid=V.vid AND R.rid=V.rid AND R0.rid=R.rid"
            # data = g.conn.execute(text(cmd)).fetchall()
    return render_template('functions/violations.html', stats=stats, stats2=stats2, stats3=stats3, data=data, mostRestaurant_data=mostRestaurant_data)


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
