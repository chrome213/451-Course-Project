import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def list2Str(lst):
    """Converts a list to a string format to store in PostgreSQL."""
    return ','.join(str(e) for e in lst)

def insert2BusinessTable():
    #reading the JSON file
    with open('./yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS businessTable (business_id VARCHAR(255),name VARCHAR(255),  address VARCHAR(255), state VARCHAR(255), city VARCHAR(255),zipcode VARCHAR(255),latitude FLOAT, longitude FLOAT,stars FLOAT, reviewcount INT,numCheckins INT,openStatus BOOLEAN);")
        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO businessTable (business_id, name, address,state,city,zipcode,latitude,longitude,stars,reviewcount,numCheckins,openStatus) " \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["address"]) + "','" + \
                      cleanStr4SQL(data["state"]) + "','" + cleanStr4SQL(data["city"]) + "','" + cleanStr4SQL(data["postal_code"]) + "'," + str(data["latitude"]) + "," + \
                      str(data["longitude"]) + "," + str(data["stars"]) + "," + str(data["review_count"]) + ",0 ,"  + \
                      int2BoolStr(data["is_open"]) + ");"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to businessTABLE failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2ReviewTable():
    with open('./yelp_review.JSON', 'r') as f:
        # Optional: Uncomment the next line if you want to write the INSERT statements to an output file for logging purposes
        # outfile = open('./yelp_review.SQL', 'w')
        
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
            return
        
        cur = conn.cursor()
        # Assuming the reviewTable does not exist, let's create it with appropriate fields
        cur.execute("CREATE TABLE IF NOT EXISTS reviewTable (review_id VARCHAR(255), user_id VARCHAR(255), business_id VARCHAR(255), stars INT, date DATE, text TEXT, useful INT, funny INT, cool INT);")

        while line:
            data = json.loads(line)
            # Preparing the SQL INSERT statement to insert the review data
            sql_str = f"INSERT INTO reviewTable (review_id, user_id, business_id, stars, date, text, useful, funny, cool) VALUES ('{cleanStr4SQL(data['review_id'])}', '{cleanStr4SQL(data['user_id'])}', '{cleanStr4SQL(data['business_id'])}', {data['stars']}, '{data['date']}', '{cleanStr4SQL(data['text'])}', {data['useful']}, {data['funny']}, {data['cool']});"
            
            try:
                cur.execute(sql_str)
            except Exception as e:
                print(f"Insert to reviewTable failed! Error: {e}")
            
            conn.commit()

            # Optional: Write the INSERT statement to a file
            # outfile.write(sql_str + '\n')

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()
        print(count_line)
        # Optional: Close the output file if you are writing the INSERT statements to it
        # outfile.close()

def insert2UserTable():
    with open('./yelp_user.JSON', 'r') as f:
        # Optional: Uncomment the next line if you're outputting INSERT statements to a file.
        # outfile = open('./yelp_user.SQL', 'w')
        
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
            return
        
        cur = conn.cursor()
        # Create the userTable if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS userTable (
                user_id VARCHAR(255),
                name VARCHAR(255),
                review_count INT,
                yelping_since DATE,
                useful INT,
                funny INT,
                cool INT,
                elite TEXT, -- Storing as text, could be normalized into a separate table
                friends TEXT, -- Storing as text, could be normalized
                fans INT,
                average_stars FLOAT,
                compliment_hot INT,
                compliment_more INT,
                compliment_profile INT,
                compliment_cute INT,
                compliment_list INT,
                compliment_note INT,
                compliment_plain INT,
                compliment_cool INT,
                compliment_funny INT,
                compliment_writer INT,
                compliment_photos INT
            );
        """)

        while line:
            data = json.loads(line)
            # Convert lists to strings for storage
            elite_str = list2Str(data.get('elite', []))
            friends_str = list2Str(data.get('friends', []))
            
            sql_str = f"""
                INSERT INTO userTable (user_id, name, review_count, yelping_since, useful, funny, cool, elite, friends, fans, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos)
                VALUES ('{cleanStr4SQL(data['user_id'])}', '{cleanStr4SQL(data['name'])}', {data['review_count']}, '{data['yelping_since']}', {data['useful']}, {data['funny']}, {data['cool']}, '{elite_str}', '{friends_str}', {data['fans']}, {data['average_stars']}, {data['compliment_hot']}, {data['compliment_more']}, {data['compliment_profile']}, {data['compliment_cute']}, {data['compliment_list']}, {data['compliment_note']}, {data['compliment_plain']}, {data['compliment_cool']}, {data['compliment_funny']}, {data['compliment_writer']}, {data['compliment_photos']});
            """
            
            try:
                cur.execute(sql_str)
            except Exception as e:
                print(f"Insert to userTable failed! Error: {e}")
            
            conn.commit()

            # Optional: Write the INSERT statement to a file.
            # outfile.write(sql_str + '\n')

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()
        print(count_line)
        # Optional: Close the output file if you are writing INSERT statements to it.
        # outfile.close()

def insert2CheckinTable():
    with open('./yelp_checkin.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='0213'")
        except:
            print('Unable to connect to the database!')
            return
        
        cur = conn.cursor()
        # Create the checkinTable if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS checkinTable (
                business_id VARCHAR(255),
                day VARCHAR(10),
                hour VARCHAR(5),
                checkin_count INT
            );
        """)

        while line:
            data = json.loads(line)
            business_id = data['business_id']
            for day, hours in data['time'].items():
                for hour, count in hours.items():
                    sql_str = f"""
                        INSERT INTO checkinTable (business_id, day, hour, checkin_count)
                        VALUES ('{business_id}', '{day}', '{hour}', {count});
                    """
                    try:
                        cur.execute(sql_str)
                    except Exception as e:
                        print(f"Insert to checkinTable failed! Error: {e}")
                    
                    conn.commit()
            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()
        print(count_line)

insert2CheckinTable()
insert2UserTable()
insert2ReviewTable()
insert2BusinessTable()