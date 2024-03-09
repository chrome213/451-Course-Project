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
        self.ui.CityList.currentItemChanged.connect(self.loadBusinesses)

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

    def loadBusinesses(self):
        selected_city = self.ui.CityList.currentItem().text() if self.ui.CityList.currentItem() else None
        if not selected_city:  # Check if a city is selected
            return
        self.ui.BusinessTable.setColumnCount(3)  # set column count
        self.ui.BusinessTable.setRowCount(0)  # Clear existing rows
        self.BusinessTable.setHorizontalHeaderLabels(['Name', 'City', 'State'])  # Set column headers
        try:
        # Use placeholders %s for parameterized queries
            query = "SELECT name, city, state FROM business WHERE city=%s AND state=%s ORDER BY name;"
            self.cur.execute(query, (selected_city, selected_state))
            businesses = self.cur.fetchall()
            
            for business in businesses:
                row_position = self.ui.BusinessTable.rowCount()
                self.ui.BusinessTable.insertRow(row_position)  # Insert a new row
                
                # Add data to the row for each business
                for column, item in enumerate(business):
                    self.ui.BusinessTable.setItem(row_position, column, QTableWidgetItem(str(item)))
                    
        except psycopg2.Error as e:
            print(f'Failed to fetch businesses. Error: {e}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')