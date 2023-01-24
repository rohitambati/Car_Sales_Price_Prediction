### Importing the packages
import sqlite3
from sqlite3 import Error

import pandas as pd

### Global variable
data_filename = 'Car_sales.csv'
normalized_database_filename = 'car_sales.db'

# CREATE CONNECTION FUNCTION
def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)
    return conn

#CREATE TABLE FUNCTION
def create_table(conn, create_table_sql, drop_table_name=None):
    if drop_table_name: #You can optionally pass drop_table_name to drop the table. 
        try:
            c = conn.cursor()
            c.execute("""DROP TABLE IF EXISTS %s""" % (drop_table_name))
        except Error as e:
            print(e)
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#EXECUTE SQL QUERIES FUNCTION
def execute_sql_statement(sql_statement, conn):
    cur = conn.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()
    return rows

#CREATE MANUFACTURER NORMALISED TABLE
def create_manufacturer_table(data_filename, normalized_database_filename):
    header_flag = True
    manufacturer = []
    manufacturer_id = []
    manufacturer_index = -1


    with open(data_filename) as file:
        for line in file:
            if(header_flag == True):
                header = line.strip().split(",")
                manufacturer_index = header.index("Manufacturer")
                header_flag = False
            else:
                data_line = line.strip().split(",")
                if(data_line[manufacturer_index].strip() not in manufacturer):
                    manufacturer.append(data_line[manufacturer_index].strip())
        for i in range(1, len(manufacturer)+1):
            manufacturer_id.append(i)
        # print(manufacturer_id)
    manufacturer.sort()
    # print(manufacturer)
    l = list(zip(manufacturer_id,manufacturer))
    # manufacturer = [[m] for m in manufacturer]

    # print(list(l))
    
    #CREATING TABLE Manufacturer
    conn_normalised_db = create_connection(normalized_database_filename)
    create_table_sql = "CREATE TABLE IF NOT EXISTS Manufacturer (manufacturerID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Manufacturer_Name TEXT NOT NULL);"
    create_table(conn_normalised_db, create_table_sql, drop_table_name= "Manufacturer")
    
    #INSERTING RECORDS INTO TABLE REGION
    insert_sql = "INSERT INTO Manufacturer (manufacturerID, Manufacturer_Name) VALUES(?,?)"
    cur = conn_normalised_db.cursor()
    with conn_normalised_db:
        cur.executemany("INSERT INTO Manufacturer VALUES (?,?)", l)
    conn_normalised_db.close()
# create_manufacturer_table("Car_sales.csv", "car_sales.db")

#MANUFACTURER TO MANUFACTURER_ID DICTIONARY
def create_manufacturer_to_manufacturerid_dictionary(normalized_database_filename):
    manufacturer_to_manufacturerid_dict = {}
    conn_normalised_db = create_connection(normalized_database_filename)
    cursor = conn_normalised_db.cursor()
    select_all = "SELECT * FROM Manufacturer"
    rows = cursor.execute(select_all).fetchall()
    # Output to the console screen
    for r in rows:
        manufacturer_to_manufacturerid_dict[r[1]] = r[0]
    return manufacturer_to_manufacturerid_dict
# create_manufacturer_to_manufacturerid_dictionary("car_sales.db")


#CREATING AND INSERTING DATA INTO MODELS TABLE
def create_models_table(data_filename, normalized_database_filename):
    #CREATING TABLE PRODUCT
    conn_normalised_db = create_connection(normalized_database_filename)
    create_table_sql = """CREATE TABLE IF NOT EXISTS Models (ModelID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                        Model_Name TEXT NOT NULL,
                        ManufacturerID INTEGER NOT NULL,
                        Vehicle_Type TEXT,
                        Engine_Size REAL,
                        Horsepower INTEGER,
                        Wheelbase REAL,
                        Width REAL,
                        Length REAL,
                        Curb_Weight REAL,
                        Fuel_Capacity REAL,
                        Fuel_Efficiency REAL,
                        Latest_Launch_Date DATE,
                        Power_Per_Factor REAL,
                        Sales_in_thousands REAL NOT NULL,
                        Year_resale_value REAL NOT NULL,
                        Price_in_thousands REAL NOT NULL,
                        FOREIGN KEY(ManufacturerID) REFERENCES Manufacturer(ManufacturerID));"""
    create_table(conn_normalised_db, create_table_sql, drop_table_name = "Models")
    header_flag = True
    final_records = []
    manufacturer_to_manufacturerid_dict = create_manufacturer_to_manufacturerid_dictionary(normalized_database_filename)
    with open(data_filename) as file:
        for line in file:
            if(header_flag == True):
                header = line.strip().split(",")
                model_index = header.index("Model")
                manufacturer_index = header.index("Manufacturer")
                vehicle_type_index = header.index("Vehicle_type")
                engine_size_index = header.index("Engine_size")
                horsepower_index = header.index("Horsepower")
                wheelbase_index = header.index("Wheelbase")
                width_index = header.index("Width")
                length_index = header.index("Length")
                curb_weight_index = header.index("Curb_weight")
                fuel_capacity_index = header.index("Fuel_capacity")
                fuel_efficiency_index = header.index("Fuel_efficiency")
                latest_launch_index = header.index("Latest_Launch")
                power_perf_factor_index = header.index("Power_perf_factor")
                resale_index = header.index("__year_resale_value")
                sale_index = header.index("Sales_in_thousands")
                price_index = header.index("Price_in_thousands")
                header_flag = False
            else:
                data_line = line.strip().split(",")
                temp_record = []
                temp_record.append(data_line[model_index].strip())
                manufacturer_id = manufacturer_to_manufacturerid_dict[data_line[manufacturer_index].strip()]
                temp_record.append(manufacturer_id)
                temp_record.append(data_line[vehicle_type_index].strip())
                temp_record.append(data_line[engine_size_index].strip())
                temp_record.append(data_line[horsepower_index].strip())
                temp_record.append(data_line[wheelbase_index].strip())
                temp_record.append(data_line[width_index].strip())
                temp_record.append(data_line[length_index].strip())
                temp_record.append(data_line[curb_weight_index].strip())
                temp_record.append(data_line[fuel_capacity_index].strip())
                temp_record.append(data_line[fuel_efficiency_index].strip())
                temp_record.append(data_line[latest_launch_index].strip())
                temp_record.append(data_line[power_perf_factor_index].strip())
                temp_record.append(data_line[resale_index].strip())
                temp_record.append(data_line[sale_index].strip())
                temp_record.append(data_line[price_index].strip())
                final_records.append(temp_record)
    
    #INSERTING RECORDS INTO TABLE MODELS
    insert_sql = "INSERT INTO Models (Model_Name, ManufacturerID, Vehicle_Type, Engine_Size, Horsepower, Wheelbase, Width, Length, Curb_Weight, Fuel_Capacity, Fuel_Efficiency, Latest_Launch_Date, Power_Per_Factor, Year_resale_value, Sales_in_thousands, Price_in_thousands) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    with conn_normalised_db:
        cursor = conn_normalised_db.cursor()
        cursor.executemany(insert_sql, final_records)
    conn_normalised_db.close()
# create_models_table("car_sales.csv", "car_sales.db")


#MODEL TO MODEL_ID DICTIONARY
def step4_create_model_to_modelid_dictionary(normalized_database_filename):
    model_to_modelid_dict = {}
    conn_normalised_db = create_connection(normalized_database_filename)
    cursor = conn_normalised_db.cursor()
    select_all = "SELECT ModelID, Model_Name FROM Models"
    rows = cursor.execute(select_all).fetchall()
    # Output to the console screen
    for r in rows:
        model_to_modelid_dict[r[1]] = r[0]
    return model_to_modelid_dict 
# step4_create_model_to_modelid_dictionary("car_sales.db")


### Function to be called in analysis.py    
def setup_database():
    create_manufacturer_table(data_filename, normalized_database_filename)
    create_models_table(data_filename, normalized_database_filename)

## to return


def manufacturer_table_data():
    conn = create_connection("car_sales.db", False)
    data = pd.read_sql_query("SELECT * FROM Manufacturer", conn)
    conn.close()
    return data


def models_table_data():
    conn = create_connection("car_sales.db", False)
    data = pd.read_sql_query("SELECT * FROM Models", conn)
    conn.close()
    return data

