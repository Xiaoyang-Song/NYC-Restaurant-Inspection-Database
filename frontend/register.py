import os
from os import abort
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Blueprint, Flask, flash, request, session, render_template, g, redirect, Response, url_for
from icecream import ic
import functools
from werkzeug.security import check_password_hash, generate_password_hash

# bp = Blueprint('register', __name__, url_prefix='/register')


if __name__ == '__main__':
    ic("registration scripts")
