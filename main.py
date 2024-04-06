import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QHeaderView
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


qtCreatorFile = "milestone2App.ui" 

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class myApp(QMainWindow):  # Class for the main window
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MILSTONE 1
        self.loadStates() # Load states
        self.ui.StateBox.currentIndexChanged.connect(self.loadCities) # Load cities for the selected state
        self.ui.CityList.itemClicked.connect(self.loadBusinessesForCity)  # Load businesses for the selected city 
        
        # MILSTONE 2
        self.m2loadStates()
        self.ui.State.currentIndexChanged.connect(self.m2LoadCities) # Load cities for the selected state using the selectLocation table
        self.ui.City.itemClicked.connect(self.m2LoadZipcode)
        self.ui.Zipcode.itemClicked.connect(self.m2ZipcodeStatistics)

    def connectToDB(self, dbName): # dbName is the name of the database to connect to
        try:
            self.conn = psycopg2.connect(f"dbname='{dbName}' user='postgres' host='localhost' password='0213'")
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print(f'Unable to connect to the {dbName} database! Error: {e}')
            sys.exit(1)

    def loadStates(self): # Function to load states
        self.connectToDB("milestone1db")
        try:
            self.cur.execute("SELECT DISTINCT state FROM business ORDER BY state;")
            states = self.cur.fetchall()
            for state in states:
                self.ui.StateBox.addItem(str(state[0]))
        except psycopg2.Error as e:
            print(f'Failed to fetch states. Error: {e}')

    def loadCities(self): # Function to load cities for the selected state
        self.connectToDB("milestone1db")
        selected_state = self.ui.StateBox.currentText()   
        self.ui.CityList.clear()  
        try:
            self.cur.execute("SELECT DISTINCT city FROM business WHERE state=%s ORDER BY city;", (selected_state,))   # Fetch cities for the selected state
            cities = self.cur.fetchall()
            for city in cities:
                self.ui.CityList.addItem(str(city[0]))
        except psycopg2.Error as e:
            print(f'Failed to fetch cities. Error: {e}')

    def loadBusinessesForCity(self): # Function to load businesses for the selected city
        self.connectToDB("milestone1db")
        selected_city = self.ui.CityList.currentItem().text() # Get the selected city
        self.ui.BusinessTable.clearContents()  
        self.ui.BusinessTable.setColumnCount(3)  
        self.ui.BusinessTable.verticalHeader().setVisible(False)  
        self.ui.BusinessTable.setHorizontalHeaderLabels(['Name', 'State', 'City'])  
        header = self.ui.BusinessTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        try: # Fetch businesses for the selected city
            self.cur.execute("SELECT name, state, city FROM business WHERE city=%s ORDER BY name;", (selected_city,))
            businesses = self.cur.fetchall()
            self.ui.BusinessTable.setRowCount(len(businesses))  # Set row count
            for row, (name, state, city) in enumerate(businesses):
                self.ui.BusinessTable.setItem(row, 0, QTableWidgetItem(name))
                self.ui.BusinessTable.setItem(row, 1, QTableWidgetItem(state))
                self.ui.BusinessTable.setItem(row, 2, QTableWidgetItem(city))
        except psycopg2.Error as e:
            print(f'Failed to fetch businesses for city {selected_city}. Error: {e}')    

    def m2loadStates(self): # Function to load states
        self.connectToDB("milestone2db")
        try:
            self.cur.execute("SELECT DISTINCT state FROM business ORDER BY state;")
            states = self.cur.fetchall()
            for state in states:
                self.ui.State.addItem(str(state[0]))
        except psycopg2.Error as e:
            print(f'Failed to fetch states. Error: {e}')
   
    # function (m2LoadCities) to load cities from the selected state using the selectLocation table
    def m2LoadCities(self):
        self.connectToDB("milestone2db")
        selected_state = self.ui.State.currentText()   
        self.ui.City.clear()  
        try:
            self.cur.execute("SELECT DISTINCT city FROM business WHERE state=%s ORDER BY city;", (selected_state,))   # Fetch cities for the selected state
            cities = self.cur.fetchall()
            for city in cities:
                self.ui.City.addItem(str(city[0]))
        except psycopg2.Error as e:
            print(f'Failed to fetch cities. Error: {e}') 

    # function (m2LoadZipcode) to load zipcodes from the selected city using the selectLocation table
    def m2LoadZipcode(self):
        self.connectToDB("milestone2db")
        selected_city = self.ui.City.currentItem().text() # Get the selected city
        self.ui.Zipcode.clear()  
        try:
            self.cur.execute("SELECT DISTINCT zipcode FROM business WHERE city=%s ORDER BY zipcode;", (selected_city,))   # Fetch zipcodes for the selected city
            zipcodes = self.cur.fetchall()
            for zipcode in zipcodes:
                self.ui.Zipcode.addItem(str(zipcode[0]))
        except psycopg2.Error as e:
            print(f'Failed to fetch zipcodes. Error: {e}')

    def m2ZipcodeStatistics(self):
        self.connectToDB("milestone2db")
        selected_zipcode = self.ui.Zipcode.currentItem().text()  # Get the selected zipcode

        try:
            # Calculate the number of businesses in the selected zipcode
            self.cur.execute("""
                SELECT COUNT(*)
                FROM Business
                WHERE zipcode = %s;
            """, (selected_zipcode,))
            num_businesses = self.cur.fetchone()[0]

            # Fetch population and mean income from the Zipcode table for the selected zipcode
            self.cur.execute("""
                SELECT population, meanincome
                FROM Zipcode
                WHERE zipcode_id = %s;
            """, (selected_zipcode,))
            statistics = self.cur.fetchone()
            population, mean_income = statistics if statistics else (0, 0)

            self.ui.BusinessesStatistic.setText(str(num_businesses))
            self.ui.PopulationStatistic.setText(str(population))
            self.ui.IncomeStatistic.setText(str(mean_income))

            # Fetch unique categories from the Categories table through the Has relationship for the selected zipcode
            self.cur.execute("""
                SELECT DISTINCT C.name
                FROM Categories C
                JOIN Has H ON C.name = H.category_id
                JOIN Business B ON H.business_id = B.business_id
                WHERE B.zipcode = %s;
            """, (selected_zipcode,))
            categories = self.cur.fetchall()
            self.ui.TopCategories.clearContents()
            self.ui.TopCategories.setColumnCount(1)
            self.ui.TopCategories.setHorizontalHeaderLabels(['Category'])
            self.ui.TopCategories.setRowCount(len(categories))
            for row, (category,) in enumerate(categories):
                self.ui.TopCategories.setItem(row, 0, QTableWidgetItem(category))

        except psycopg2.Error as e:
            print(f'Failed to fetch statistics for zipcode {selected_zipcode}. Error: {e}')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')