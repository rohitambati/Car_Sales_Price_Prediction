import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import backend as bk
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
import pickle

bk.setup_database()
print(bk.manufacturer_table_data())
print(bk.models_table_data())
# print(bk.create)

dataset = bk.models_table_data()
print(dataset.columns)
def plt_avg_price():
    ### BEGIN SOLUTION
    sql_statement = f"""Select m.Manufacturer_Name, avg(c.Price_in_thousands) Average_price from Manufacturer m, Models c WHERE m.ManufacturerID = c.ManufacturerID GROUP BY m.Manufacturer_Name ORDER BY Average_price DESC LIMIT 10 """
    df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    Manufacturer = df['Manufacturer_Name']
    Average_Price = df['Average_price']
    # fig = plt.figure(figsize=(40, 10))
    # sns.barplot()
    sns.barplot(x=Manufacturer, y=Average_Price, alpha=.8)
    plt.xlabel("Car Manufacturers", fontsize=14)
    plt.ylabel("Average Car Price in Thousands", fontsize=12)
    plt.title("Average Car Price w.r.t to Manufacturer", fontsize=16)
    plt.savefig('plt_avg_price.png')

#     print(df['Average_price'])
conn = bk.create_connection("car_sales.db")
plt_avg_price()

### Vehicle Type Plot:
conn = bk.create_connection("car_sales.db")
def plt_vehicletype():
    sql_statement = "SELECT Vehicle_Type, COUNT(Vehicle_Type) number FROM Models GROUP BY Vehicle_Type"
    df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    Vehicle_Type = df['Vehicle_Type']
    Count = df['number']
    fig = plt.figure(figsize = (20, 8))
    sns.barplot(x=Vehicle_Type, y=Count, alpha = .8)
#     plt.bar(Vehicle_Type, Count, color = 'red',width = 0.4)
    plt.xlabel("Vehicle Type", fontsize = 14)
    plt.ylabel("Number of Cars", fontsize = 12)
    plt.title("Different Vehicles Types Count", fontsize = 16)
    plt.savefig('plt_vehicletype.png')

plt_vehicletype()


### Cars Per Manufacturer
def plt_manufacturers():
    sql_statement = """Select m.Manufacturer_Name, Count(c.ManufacturerID) number 
                        from Manufacturer m, Models c 
                        WHERE m.ManufacturerID = c.ManufacturerID GROUP BY m.ManufacturerID """
    df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    Manufacturer = df['Manufacturer_Name']
    Count = df['number']
    fig = plt.figure(figsize = (40, 10))
    sns.barplot(x=Manufacturer, y=Count, alpha = .8)
    plt.xlabel("Manufacturers", fontsize = 14)
    plt.ylabel("Number of Cars", fontsize = 14)
    plt.title("Car Count according to Manufacturer", fontsize = 16)
    plt.savefig('plt_manufacturers.png')

plt_manufacturers()

def handling_missing_data(dataset):
    # Handling missing values - Price_in_thousands
    filtered_dataset = dataset[dataset['Price_in_thousands'].notna()]

    # Handling missing values - Year_resale_value
    year_index = [int(value) for value in list(~filtered_dataset['Year_resale_value'].isnull())]
    median_year = np.median(filtered_dataset['Year_resale_value'].loc[year_index])
    filtered_dataset['Year_resale_value'].fillna(median_year, inplace=True)

    # Handling missing values - Fuel_efficiency 
    fuel_index = [float(value) for value in list(~filtered_dataset['Fuel_Efficiency'].isnull())]
    median_fuel = np.median(filtered_dataset['Fuel_Efficiency'].loc[fuel_index])
    filtered_dataset['Fuel_Efficiency'].fillna(median_fuel, inplace=True)
    return filtered_dataset

def feature_selection(dataset):
    filtered_dataset = handling_missing_data(dataset)
    modified_dataset = filtered_dataset[['Sales_in_thousands', 'Year_resale_value', 'Price_in_thousands', 'Wheelbase', 'Width',
                                         'Fuel_Efficiency', 'Latest_Launch_Date']]

    modified_dataset['Year_resale_value'] = [float(value) if value != '' else 0 for value in modified_dataset['Year_resale_value']]
    modified_dataset['Price_in_thousands'] = [float(value) if value != '' else 0 for value in modified_dataset['Price_in_thousands']]
    modified_dataset['Wheelbase'] = [float(value) if value != '' else 0 for value in modified_dataset['Wheelbase']]
    modified_dataset['Width'] = [float(value) if value != '' else 0 for value in modified_dataset['Width']]
    modified_dataset['Fuel_Efficiency'] = [float(value) if value != '' else 0 for value in modified_dataset['Fuel_Efficiency']]
    modified_dataset['Latest_Launch_Date'] = [2022 - int(value.split('/')[2]) for value in list(modified_dataset['Latest_Launch_Date'])]
    return modified_dataset

def data_preprocessing(dataset):
    dataset = feature_selection(dataset)
    X = dataset.iloc[:, [0, 1, 3, 4, 5, 6]].values
    Y = dataset.iloc[:, 2].values
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 27, shuffle = True)
    return X_train, X_test, Y_train, Y_test

# print(data_preprocessing(dataset))

def random_forest_regression():
    X_train, X_test, Y_train, Y_test = data_preprocessing(dataset)
    random_forest_regressor = RandomForestRegressor(n_estimators = 100, random_state = 27)
    random_forest_regressor.fit(X_train, Y_train)
    Y_pred = random_forest_regressor.predict(X_test)
    mse = round(mean_squared_error(Y_test, Y_pred), 3)
    rmse = round(sqrt(mse), 3)
    # print(rmse)
    # Saving model to disk
    pickle.dump(random_forest_regressor, open('model.pkl', 'wb'))
random_forest_regression()







