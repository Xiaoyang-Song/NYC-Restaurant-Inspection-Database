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

bp = Blueprint('help', __name__, url_prefix='/help')


@bp.route('/helppage', methods=(['GET']))
def helppage():
    return render_template("help/helppage.html")
