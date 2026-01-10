DB_HOST = "192.168.1.1"
DB_NAME = "db"
DB_USER = "postgres"
DB_PASS = "password"

import psycopg2
from sqlalchemy import create_engine

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432)
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}')

import random
import pandas as pd
from faker import Faker
from barnum import gen_data

fake = Faker()
locale_list = ['pl-PL']
locale_fake = Faker(locale_list)



# create a data frame with customers data 
def createCustomer(n=100):
    customer_ids = [x for x in range(1000000, 9999999)]
    customer_df = pd.DataFrame(columns=['customer_id', 'name', 'city', 'phone', 'email'])
    for i in range(n):
        customer_df.loc[i, 'customer_id'] = customer_ids[i]
        customer_df.loc[i, 'name'] = locale_fake.name()
        customer_df.loc[i, 'city'] = locale_fake.city()
        customer_df.loc[i, 'phone'] = locale_fake.phone_number()
        customer_df.loc[i, 'email'] = locale_fake.email()
    return customer_df


# create a data frame with lockers data
def createLocker(n=100):
    locker_ids = [x for x in range(100000, 999999)]
    locker_df = pd.DataFrame(columns=['locker_id', 'locker_city'])
    for i in range(n):
        locker_df.loc[i, 'locker_id'] = locker_ids[i]
        locker_df.loc[i, 'locker_city'] = locale_fake.city()
        # locker_df.loc[i, 'Locker Street'] = locale_fake.street()
    return locker_df


# create a data frame with items data
def createItem(n=100):
    item_ids = [x for x in range(100000, 999999)]
    item_df = pd.DataFrame(columns = ['item_id', 'item_name'])
    for i in range(n):
        item_df.loc[i, 'item_id'] = item_ids[i]
        item_df.loc[i, 'item_name'] = gen_data.create_nouns(max=1)
    return item_df


# create a data frame with orders data
def createOrders(n=100, uniqe_customers_list=[], uniqe_lockers_list=[]):
    order_ids = [x for x in range(100000, 999999)]

    order_df = pd.DataFrame(columns=['order_id', 'customer_id', 'locker_id'])
    for i in range(n):
        order_df.loc[i, 'order_id'] = order_ids[i]
        order_df.loc[i, 'customer_id'] = random.choice(uniqe_customers_list)
        order_df.loc[i, 'locker_id'] = random.choice(uniqe_lockers_list)
        # order_df.loc[i, 'Item_ID'] = random.randint(100000, 999999)
    return order_df


# create a data frame that connects items with orders (1 order can have multiple items)
def createItemToOrder(unique_orders_list=[], unique_items_list=[]):
    itemToOrders_df = pd.DataFrame(columns=['order_id', 'item_id'])
    line = 0
    for i in range(len(unique_orders_list)):
        for j in range (1, random.randint(2,5)):
            itemToOrders_df.loc[line, 'order_id'] = unique_orders_list[i]
            itemToOrders_df.loc[line, 'item_id'] = random.choice(unique_items_list)
            line += 1
    return itemToOrders_df
    


# create a data frame with waybills data
def createWaybillsToOrder(df_ItemToOrder=pd.DataFrame()):
    waybill_df = pd.DataFrame(columns=['order_id', 'waybill', 'courier'])
    df_num = 0
    waybill_num = 100000
    for i in df_ItemToOrder['order_id'].unique():
        courier = random.choice(['DHL', 'UPS', 'FedEx', 'InPost', 'DPD', 'Poczta_Polska', 'GLS'])
        for _ in range(random.randint(1, len(df_ItemToOrder[df_ItemToOrder['order_id'] == i]['item_id']))):
            waybill_df.loc[df_num, 'order_id'] = i
            waybill_df.loc[df_num, 'waybill'] = waybill_num
            waybill_df.loc[df_num, 'courier'] = courier
            waybill_num += 1
            df_num += 1
    return waybill_df

# creating a data frame that connects shipment statuses with waybills
def createStatusToWaybills(df_Waybills=pd.DataFrame()):
    status_df = pd.DataFrame(columns=['waybill', 'status', 'date'])
    df_num = 0
    statuses = ['waybill wygenerowany', 'nadano', 'w drodze', 'dostarczono', 'odebrano']
    for i in df_Waybills['waybill'].unique():
        first_date = fake.date_time_between(start_date='-1y', end_date='now')
        # for 95% of shipments whose first status appeared more than 20 days ago, the parcels have the status ‘collected’
        if first_date < pd.Timestamp.now()-pd.Timedelta(days=20) and random.randint(1,100) > 5:
            status_number = 5
        # otherwise, the last parcel status at which the shipment stopped is randomly selected
        else:
            status_number = random.randint(1, 5)
        for j in range(status_number):
            status_df.loc[df_num, 'waybill'] = i
            status_df.loc[df_num, 'status'] = statuses[j]
            # in 5% of cases, one of the stages of shipment may take up to 20 days 
            if random.randint(1,100) <= 5:
                first_date = fake.date_time_between_dates(datetime_start=first_date, datetime_end=first_date+pd.Timedelta(days=20))
            # otherwise
            else:
                # if the parcel is at the ‘in transit’ stage, the time between the ‘in transit’ and ‘delivered’ stages is 1-3 days
                if j == 3:
                    first_date = fake.date_time_between_dates(datetime_start=first_date+pd.Timedelta(days=1), datetime_end=first_date+pd.Timedelta(days=3))
                # for every other stage, the time between stages is 0-2 days
                else:
                    first_date = fake.date_time_between_dates(datetime_start=first_date, datetime_end=first_date+pd.Timedelta(days=2))
            status_df.loc[df_num, 'date'] = first_date
            df_num += 1
            
    return status_df

def create_tables():
    cur = conn.cursor()
    commands = (
        """
        DROP TABLE IF EXISTS Customers3 CASCADE;
        DROP TABLE IF EXISTS Lockers3 CASCADE;
        DROP TABLE IF EXISTS Items3 CASCADE;
        DROP TABLE IF EXISTS WaybillsToOrder3 CASCADE;
        DROP TABLE IF EXISTS ItemToOrder3 CASCADE;
        DROP TABLE IF EXISTS StatusToWaybills3 CASCADE;
        DROP TABLE IF EXISTS Orders3 CASCADE;
        """,
        """
        CREATE TABLE Customers3 (
            Customer_ID INT NOT NULL,
            Name VARCHAR(255),
            City VARCHAR(255),
            Phone VARCHAR(255),
            Email VARCHAR(255),
            PRIMARY KEY (Customer_ID))
        """,
        """
        CREATE TABLE Lockers3 (
            Locker_ID INT NOT NULL, 
            Locker_City VARCHAR(255),
            PRIMARY KEY (Locker_ID)
            )
        """,
        """
        CREATE TABLE Items3 (
            Item_ID INT NOT NULL, 
            Item_Name VARCHAR(255),
            PRIMARY KEY (Item_ID)
            )
        """,
        """
        CREATE TABLE Orders3 (
            Order_ID INT NOT NULL, 
            Customer_ID INT NOT NULL, 
            Locker_ID INT NOT NULL,
            PRIMARY KEY (Order_ID),
            FOREIGN KEY (Customer_ID) REFERENCES Customers3(Customer_ID),
            FOREIGN KEY (Locker_ID) REFERENCES Lockers3(Locker_ID)
        )
        """,
        """
        CREATE TABLE WaybillsToOrder3 (
            Order_ID INT NOT NULL,
            Waybill INT NOT NULL, 
            Courier VARCHAR,
            PRIMARY KEY (Waybill),
            FOREIGN KEY (Order_ID) REFERENCES Orders3(Order_ID)
            )
        """,
        """
        CREATE TABLE ItemToOrder3 (
            Order_ID INT NOT NULL,
            Item_ID INT NOT NULL,
            FOREIGN KEY (Order_ID) REFERENCES Orders3(Order_ID)
            )
        """,
        """
        CREATE TABLE StatusToWaybills3 (
            Waybill INT NOT NULL, 
            Status VARCHAR(255),
            Date TIMESTAMP,
            FOREIGN KEY (Waybill) REFERENCES WaybillsToOrder3(Waybill)
            )
        """,
    )
    try:
        for command in commands:
            cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(command)
        print(error)
    conn.commit()
    cur.close()
        




if __name__ == "__main__":
    df_Customer = createCustomer(100000)
    uniqe_customers_list = df_Customer['customer_id'].unique()
    print('Customers created')

    df_Locker = createLocker(100000)
    uniqe_lockers_list = df_Locker['locker_id'].unique()
    print('Lockers created')

    df_Item = createItem(100000)
    unique_items_list = df_Item['item_id'].unique()
    print('Items created')
 
    df_Order = createOrders(100000, uniqe_customers_list, uniqe_lockers_list)
    unique_orders_list = df_Order['order_id'].unique()
    print('Orders created')

    df_ItemToOrder = createItemToOrder(unique_orders_list, unique_items_list)
    print('ItemToOrder created')

    df_Waybills = createWaybillsToOrder(df_ItemToOrder)
    print('WaybillsToOrder created')

    df_Statuses = createStatusToWaybills(df_Waybills)
    print('StatusToWaybills created')

    create_tables()

    df_Customer.to_sql('customers3', engine, if_exists='append', index=False)
    df_Locker.to_sql('lockers3', engine, if_exists='append', index=False)
    df_Item.to_sql('items3', engine, if_exists='append', index=False)
    df_Order.to_sql('orders3', engine, if_exists='append', index=False)
    df_ItemToOrder.to_sql('itemtoorder3', engine, if_exists='append', index=False)
    df_Waybills.to_sql('waybillstoorder3', engine, if_exists='append', index=False)
    df_Statuses.to_sql('statustowaybills3', engine, if_exists='append', index=False)
