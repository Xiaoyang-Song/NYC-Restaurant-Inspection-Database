import os
from os import abort
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from icecream import ic


def get_db_conn():
    local_database = "postgresql://postgres:Sxy20000425@localhost/proj1part3"
    engine = create_engine(local_database)
    return engine
