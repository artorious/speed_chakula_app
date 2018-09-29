""" Data representation - Routines for user to interact with the API. """

import os
import sys
import datetime
import psycopg2
import bcrypt



class DatabaseManger():
    """ Database methods """
    def __init__(self, config_mode=None):
        self.conn = None
        self.config_mode = config_mode
        self.user = os.getenv("DATABASE_USERENAME")
        self.db_name = os.getenv("DATABASE_NAME")
        self.test_db_name = os.getenv("TEST_DATABASE_NAME")
        self.password = os.getenv("DATABASE_PWD")
        self.host = os.getenv("DATABASE_HOST")
        self.port = os.getenv("DATABASE_PORT")

    def connect_to_db(self):
        """ Create connection to database and return cursor """
        if self.config_mode == 'testing':
            dbname = self.test_db_name
        else:
            dbname = self.db_name

        password = self.password
        user = self.user
        host = self.host
        port = self.port

        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                host=host,
                port=port,
                password=password
            )
            output = self.conn.cursor()
        except Exception as err:
            output = None
            print('An Error Occured: {}'.format(err))

        return output

    def create_users_table(self):
        """ Creates a table that hold user information """
        try:
            curs = self.connect_to_db()
            curs.execute("DROP TABLE IF EXISTS users CASCADE")
            curs.execute(
                "CREATE TABLE users (\
                    userid SERIAL PRIMARY KEY, \
                    username VARCHAR(25) NOT NULL,\
                    name VARCHAR(50) NOT NULL, \
                    email VARCHAR(50) NOT NULL, \
                    admin_priviledges bool NOT NULL,\
                    login_status bool NOT NULL, \
                    reg_datetime TIMESTAMPTZ NOT NULL, \
                    password VARCHAR NOT NULL \
                    );"
                )
            self.conn.commit()

        except psycopg2.DatabaseError as err:
            if self.conn:
                self.conn.rollback()
            print('An Error Occured: {}'.format(err))
            sys.exit(1)

    def create_food_menu_table(self):
        """ Creates a table that holds all available menu/food items """
        try:
            curs = self.connect_to_db()
            curs.execute("DROP TABLE IF EXISTS menu CASCADE")
            curs.execute(
                "CREATE TABLE menu (\
                    foodid SERIAL PRIMARY KEY, \
                    userid INT NOT NULL REFERENCES users(userid), \
                    unit_price INT NOT NULL, \
                    description VARCHAR(100) NOT NULL\
                    );"
                )
            self.conn.commit()
        except psycopg2.DatabaseError as err:
            if self.conn:
                self.conn.rollback()
            print('An Error Occured: {}'.format(err))
            sys.exit(1)

    def create_food_orders_table(self):
        """ Creates table that holds all food orders from users """
        try:
            curs = self.connect_to_db()
            curs.execute("DROP TABLE IF EXISTS orders CASCADE")
            curs.execute(
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
            self.conn.commit()
        except psycopg2.DatabaseError as err:
            if self.conn:
                self.conn.rollback()
            print('An Error Occured: {}'.format(err))
            sys.exit(1)

    def close_database(self):
        """ Closes database connection """
        if self.conn:
            self.conn.close()

    def save_database(self):
        """ Saves database's current state """
        if self.conn:
            self.conn.commit()

    def create_all_tables(self):
        """ Create users, menu and orders tables """
        self.create_users_table()
        self.create_food_menu_table()
        self.create_food_orders_table()
        self.save_database()
        self.close_database()
        print('Tables created successfully!')



class SignUp():
    """ Holds method to register a new user """
    def __init__(self, user_reg_info, admin=False):
        self.raw_email = user_reg_info['email']
        self.raw_password = user_reg_info['password']
        self.raw_username = user_reg_info['username']
        self.admin = admin
        self.hashed_password = None
        self.verified_username = None
        self.datetime_registered = None
        self.verified_email = None

    
    def post(self, verified_reg_info):
        """ Save user to DB or return msg to user      
        """
        pass

    def username_check(self, raw_username):
        """ Checks for username in DB, 
            returns custom msg if username is taken,
            else assigns it to self.hashed password var
        """
        pass
    
    def password_check(self, raw_password):
        """ Checks password is alteast 6 chars """
        pass
    
    def gen_passwd_hash(self):
        """ generates hashed password and assigns to self.hashed_password var
        """
        pass
    
    def verify_passwd_hash(self):
        """verify hashed password matches raw password """
        pass
    
    def auth_token_encoding(self, verified_username):
        """ Generate Authentication Token """
        pass


    
if __name__ == '__main__':
    # test_db_inst = DatabaseManger('testing')
    # test_db_inst = DatabaseManger()
    # test_db_inst.create_all_tables()
    pass
