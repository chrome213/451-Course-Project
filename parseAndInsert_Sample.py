import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr(value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def list2Str(lst):
    """Converts a list to a string format to store in PostgreSQL."""
    return ','.join(str(e) for e in lst)

# creates and populates the business table
def insert2BusinessTable():
    with open('./yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Business CASCADE")
        cur.execute("CREATE TABLE Business (business_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), city VARCHAR(255), zipcode INT, address VARCHAR(255), review_count INT, state VARCHAR(255), reviewRating DECIMAL, numCheckins INT, stars DECIMAL, FOREIGN KEY (zipcode) REFERENCES Zipcode(zipcode_id));")
        conn.commit()
        while line:
            data = json.loads(line)
            
            sql_str =  "INSERT INTO Business (business_id, name, city, zipcode, address, review_count, state, reviewRating, numCheckins, stars) " \
                          "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["city"]) + "','" + \
                            cleanStr4SQL(data["postal_code"]) + "','" + cleanStr4SQL(data["address"]) + "'," + "0" + ",'" + cleanStr4SQL(data["state"]) + "'," + \
                            "0.0" + ",0 ," + str(data["stars"]) + ");"
            
            try:
                cur.execute(sql_str)
            except Exception as e:
                print(f"Insert to businessTABLE failed! Error: {e}")
            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

# creates and populates the zipcode table
def insert2ZipcodeDataTable():
    try:
        conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
    except:
        print('Unable to connect to the database!')
        return
    
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS zipcode CASCADE")
    cur.execute("""
        CREATE TABLE zipcode (zipcode_id INT PRIMARY KEY,medianIncome INT NOT NULL,meanIncome INT NOT NULL,population INT NOT NULL);
    """)

    with open('./zipData.sql', 'r') as f:
        sql_str = f.read()
        cur.execute(sql_str)
        conn.commit()

    cur.close()
    conn.close()

# creates and populates the review table
def insert2ReviewTable():
    with open('./yelp_review.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Review CASCADE")
        cur.execute("CREATE TABLE Review (review_id VARCHAR(255) PRIMARY KEY, stars DECIMAL, business_id VARCHAR(255), FOREIGN KEY (business_id) REFERENCES Business(business_id));")
        conn.commit()
        while line:
            data = json.loads(line)
            
            sql_str =  "INSERT INTO Review (review_id, stars, business_id) " \
                          "VALUES ('" + cleanStr4SQL(data['review_id']) + "'," + str(data["stars"]) + ",'" + cleanStr4SQL(data["business_id"]) + "');"
            
            try:
                cur.execute(sql_str)
            except Exception as e:
                print(f"Insert to Review TABLE failed! Error: {e}")
            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

# creates and populates the categories table
def insert2CategoriesTable():
    with open('./yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Categories CASCADE")
        cur.execute("CREATE TABLE Categories (name VARCHAR(255) PRIMARY KEY);")
        conn.commit()
        while line:
            data = json.loads(line)
            categories = data["categories"]
            for category in categories:
                sql_str = "INSERT INTO Categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;"
                cur.execute(sql_str, (cleanStr4SQL(category),))
                conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

# creates and populates the has table
def insert2HasTable():
    with open('./yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Has CASCADE")
        cur.execute("CREATE TABLE Has (business_id VARCHAR(255), category_id VARCHAR(255), PRIMARY KEY (business_id, category_id), FOREIGN KEY (business_id) REFERENCES Business(business_id), FOREIGN KEY (category_id) REFERENCES Categories(name));")
        conn.commit()
        while line:
            data = json.loads(line)
            categories = data["categories"]
            for category in categories:
                sql_str = "INSERT INTO Has (business_id, category_id) VALUES (%s, %s) ON CONFLICT (business_id, category_id) DO NOTHING;"
                cur.execute(sql_str, (cleanStr4SQL(data["business_id"]), cleanStr4SQL(category)))
                conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

# creates and populates the checkin table
def insert2CheckinTable():
    with open('./yelp_checkin.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Check_ins CASCADE")
        cur.execute("CREATE TABLE Check_ins (business_id VARCHAR(255), day VARCHAR(10), count INT, PRIMARY KEY (business_id, day), FOREIGN KEY (business_id) REFERENCES Business(business_id));")
        conn.commit()
        while line:
            data = json.loads(line)
            checkins = data["time"]
            for day in checkins.items():
                sql_str = "INSERT INTO Check_ins (business_id, day, count) VALUES (%s, %s, %s) ON CONFLICT (business_id, day) DO NOTHING;"
                cur.execute(sql_str, (cleanStr4SQL(data["business_id"]), day[0], len(day[1])))
                conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

# updates the checkins column in the business table
def updateCheckins():
    try:
        conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
    except:
        print('Unable to connect to the database!')
        return
    cur = conn.cursor()
    cur.execute("UPDATE Business SET numCheckins = (SELECT SUM(count) FROM Check_ins WHERE Check_ins.business_id = Business.business_id);")
    conn.commit()
    cur.close()
    conn.close()

# updates the review count column in the business table
def updateReviewCount():
    try:
        conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
    except:
        print('Unable to connect to the database!')
        return
    cur = conn.cursor()
    cur.execute("UPDATE Business SET review_count = (SELECT COUNT(*) FROM Review WHERE Review.business_id = Business.business_id);")
    conn.commit()
    cur.close()
    conn.close()

# updates the review rating column in the business table
def updateReviewRating():
    try:
        conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
    except:
        print('Unable to connect to the database!')
        return
    cur = conn.cursor()
    cur.execute("UPDATE Business SET reviewRating = (SELECT AVG(stars) FROM Review WHERE Review.business_id = Business.business_id);")
    conn.commit()
    cur.close()
    conn.close()

#insert2ZipcodeDataTable()
#insert2BusinessTable()
#insert2ReviewTable()
#insert2CategoriesTable()
#insert2HasTable()
#insert2CheckinTable()
#updateCheckins()
#updateReviewCount()
#updateReviewRating()