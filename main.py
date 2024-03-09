import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QPixmap
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


qtCreatorFile = "milestone1App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class myApp(QMainWindow):  # Inherit from DatabaseClass
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectToDB()
        self.loadStates()
        self.ui.StateBox.currentIndexChanged.connect(self.loadCities)  # Connect state change signal
        self.ui.CityList.itemClicked.connect(self.loadBusinessesForCity)  # Connect city change signal

    def connectToDB(self):
        try:
            self.conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='0213'")
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print(f'Unable to connect to the database! Error: {e}')
            sys.exit(1)

    def loadStates(self):
        self.connectToDB()
        try:
            self.cur.execute("SELECT DISTINCT state FROM business ORDER BY state;")
            states = self.cur.fetchall()
            for state in states:
                self.ui.StateBox.addItem(state[0])
        except psycopg2.Error as e:
            print(f'Failed to fetch states. Error: {e}')

    def loadCities(self):
        selected_state = self.ui.StateBox.currentText()  # Make sure you access StateBox correctly
        self.ui.CityList.clear()  # Clear existing items
        try:
            self.cur.execute("SELECT DISTINCT city FROM business WHERE state=%s ORDER BY city;", (selected_state,))
            cities = self.cur.fetchall()
            for city in cities:
                # Create a QListWidgetItem for each city and add it to the CityList
                self.ui.CityList.addItem(city[0])  # This should work as expected for QListWidget
        except psycopg2.Error as e:
            print(f'Failed to fetch cities. Error: {e}')

    def loadBusinessesForCity(self):
        selected_city = self.ui.CityList.currentItem().text()  # Get the selected city
        self.ui.BusinessTable.clearContents()  # Clear existing contents
        self.ui.BusinessTable.setColumnCount(3)  # Set column count
        self.ui.BusinessTable.setHorizontalHeaderLabels(['Name', 'State', 'City'])  # Set column headers
        
        try:
            self.cur.execute("SELECT name, state, city FROM business WHERE city=%s ORDER BY name;", (selected_city,))
            businesses = self.cur.fetchall()
            self.ui.BusinessTable.setRowCount(len(businesses))  # Set row count
            for row, (name, state, city) in enumerate(businesses):
                self.ui.BusinessTable.setItem(row, 0, QTableWidgetItem(name))
                self.ui.BusinessTable.setItem(row, 1, QTableWidgetItem(state))
                self.ui.BusinessTable.setItem(row, 2, QTableWidgetItem(city))
        except psycopg2.Error as e:
            print(f'Failed to fetch businesses for city {selected_city}. Error: {e}')    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')