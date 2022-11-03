import os
from os import abort
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from icecream import ic


def get_db_conn():
    DB_USER = 'xs2485'
    DB_PASSWORD = "Sxy20000425"
    DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
    DATABASEURI = "postgresql://"+DB_USER+":" + \
        DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"
    # local_database = "postgresql://postgres:Sxy20000425@localhost/proj1part3"
    # engine = create_engine(local_database)
    # This line creates a database engine that knows how to connect to the URI above
    #
    engine = create_engine(DATABASEURI)
    return engine.connect()

