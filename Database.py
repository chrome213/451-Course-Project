import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QPixmap
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import Database

def load():
    #connect to yelpdb database on postgres server using psycopg2
    #TODO: update the database name, username, and password
    try:
        conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='0213'")
    except:
        print('Unable to connect to the database!')
    cur = conn.cursor()