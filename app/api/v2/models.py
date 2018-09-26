""" Data representation - Routines for user to interact with the API. """

import os
import sys
import psycopg2


CONN = None

USER = os.getenv("DATABASE_USERENAME")
DBNAME = os.getenv("DATABASE_NAME")
HOST = os.getenv("DATABASE_HOST")
PORT = os.getenv("DATABASE_PORT")
PASSWORD = os.getenv("DATABASE_PWD")

try:
    # Connectiotion
    CONN = psycopg2.connect(
        dbname=DBNAME,
        user=USER,
        host=HOST,
        password=PASSWORD
    )
    CUR = CONN.cursor()
except Exception as err:
    print('An Error Occured: {}'.format(err))

def create_users_table():
    """ Creates a table that hold user information """
    try:
        CUR.execute("DROP TABLE IF EXISTS users CASCADE")
        CUR.execute(
            "CREATE TABLE users (\
                userid SERIAL PRIMARY KEY, \
                name VARCHAR(50) NOT NULL, \
                password VARCHAR(50) NOT NULL, \
                email VARCHAR(50) NOT NULL, \
                username VARCHAR(25) NOT NULL,\
                admin_priviledges bool NOT NULL,\
                login_status bool NOT NULL\
                );"
            )
        CONN.commit()
    except psycopg2.DatabaseError as err:
        if CONN:
            CONN.rollback()
        print('An Error Occured: {}'.format(err))
        sys.exit(1)

def create_food_menu_table():
    """ Creates a table that holds all available menu/food items """
    try:
        CUR.execute("DROP TABLE IF EXISTS menu CASCADE")
        CUR.execute(
            "CREATE TABLE menu (\
                foodid SERIAL PRIMARY KEY, \
                userid INT NOT NULL REFERENCES users(userid), \
                unit_price INT NOT NULL, \
                description VARCHAR(100) NOT NULL\
                );"
            )
        CONN.commit()
    except psycopg2.DatabaseError as err:
        if CONN:
            CONN.rollback()
        print('An Error Occured: {}'.format(err))
        sys.exit(1)

def create_food_orders_table():
    """ Creates table that holds all food orders from users """
    try:
        CUR.execute("DROP TABLE IF EXISTS orders CASCADE")
        CUR.execute(
            "CREATE TABLE orders (\
                orderid SERIAL PRIMARY KEY, \
                userid INT NOT NULL REFERENCES users(userid), \
                order_date DATE NOT NULL DEFAULT CURRENT_DATE, \
                order_cost INT NOT NULL, \
                orderstatus VARCHAR(15) NOT NULL, \
                deliverylocation VARCHAR(50) NOT NULL, \
                orderDescription VARCHAR(100) NOT NULL\
                );"
            )
        CONN.commit()
    except psycopg2.DatabaseError as err:
        if CONN:
            CONN.rollback()
        print('An Error Occured: {}'.format(err))
        sys.exit(1)

def close_database():
    """ Closes database connection """
    if CONN:
        CONN.close()

def save_database():
    """ Saves database's current state """
    if CONN:
        CONN.commit()

def create_all_tables():
    """ Create users, menu and orders tables """
    create_users_table()
    create_food_menu_table()
    create_food_orders_table()
    save_database()
    close_database()
    print('Tables created successfully!')

if __name__ == '__main__':
    create_all_tables()