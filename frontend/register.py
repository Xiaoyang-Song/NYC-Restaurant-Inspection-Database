import os
from os import abort
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from icecream import ic


if __name__ == '__main__':
    ic("registration scripts")