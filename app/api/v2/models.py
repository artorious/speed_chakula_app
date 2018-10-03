""" Data representation - Routines for user to interact with the API. """

import sys
import datetime
import re
from os import getenv
from flask import current_app
import pytz
import psycopg2
import bcrypt
import jwt



class DatabaseManager():
    """ Database methods """
    def __init__(self):
        self.conn = None
        self.user_table_query = "CREATE TABLE users (\
            userid SERIAL PRIMARY KEY, \
            username VARCHAR(25) UNIQUE NOT NULL,\
            name VARCHAR(50) NOT NULL, \
            email VARCHAR(50) UNIQUE NOT NULL, \
            admin_priviledges bool NOT NULL,\
            registration_timestamp TIMESTAMPTZ NOT NULL, \
            password VARCHAR NOT NULL \
            );"
        self.menu_table_query = "CREATE TABLE menu (\
            foodid SERIAL PRIMARY KEY, \
            userid INT NOT NULL REFERENCES users(userid), \
            unit_price INT NOT NULL, \
            description VARCHAR(100) UNIQUE NOT NULL\
            );"
        self.food_orders_query = "CREATE TABLE orders (\
            orderid SERIAL PRIMARY KEY, \
            userid INT NOT NULL REFERENCES users(userid), \
            order_date DATE NOT NULL DEFAULT CURRENT_DATE, \
            order_cost INT NOT NULL, \
            orderstatus VARCHAR(15) NOT NULL, \
            deliverylocation VARCHAR(50) NOT NULL, \
            orderDescription VARCHAR(100) UNIQUE NOT NULL\
            );"

    def connect_to_db(self):
        """ Create connection to database and return cursor """
        try:
            self.conn=psycopg2.connect(current_app.config['DATABASE_URL'])
            output = self.conn.cursor()
        except Exception as err:
            output = None
            print('An Error Occured: {}'.format(err))

        return output

    def close_database(self):
        """ Closes database connection """
        if self.conn:
            self.conn.close()

    def save_database(self):
        """ Saves database's current state """
        if self.conn:
            self.conn.commit()

    def create_table(self, table_name):
        curs = self.connect_to_db()
        curs.execute(table_name)
        self.conn.commit()

    def create_all_tables(self):
        """ Create users, menu and orders tables """
        try:
            self.create_table(self.user_table_query)
            self.create_table(self.menu_table_query)
            self.create_table(self.food_orders_query)
            self.save_database()
            self.close_database()
            print('Tables created successfully!')

        except psycopg2.DatabaseError as err:
            if self.conn:
                self.conn.rollback()
            print('An Error Occured: {}'.format(err))
            sys.exit(1)

    def drop_all_tables(self):
        """ Drops all tables """
        try:
            curs = self.connect_to_db()
            curs.execute("DROP TABLE IF EXISTS users CASCADE")
            curs.execute("DROP TABLE IF EXISTS menu CASCADE")
            curs.execute("DROP TABLE IF EXISTS orders CASCADE")
            self.conn.commit()
        except psycopg2.DatabaseError as err:
            if self.conn:
                self.conn.rollback()
            print('An Error Occured: {}'.format(err))
            sys.exit(1)


class OperationsOnNewUsers(DatabaseManager):
    """ Holds method to register a new user """
    def __init__(self, user_reg_info, admin=False):
        self.verified_username = user_reg_info['username']
        self.verified_password = user_reg_info['password']
        self.encoded_password = self.verified_password.encode()
        self.verified_email = user_reg_info['email']
        self.name = user_reg_info['name']
        self.admin = admin
        self.hashed_password = None
        self.verified_hashed_password = None
        self.datetime_registered = None
        self.auth_token = None
        self.encoded_token = None
        self.decoded_token = None

    def auth_token_encoding(self):
        """ Generate Authentication Token """
        try:
            self.encoded_token = jwt.encode(
                {'username': self.verified_username},
                getenv('SECRET'),
                algorithm='HS256'
            )
            return self.encoded_token
        except Exception as err:
            return err

    def auth_token_decoding(self):
        """ Generates string from decoded Token """
        try:
            payload = jwt.decode(
                self.auth_token,
                getenv('SECRET'),
                algorithms='HS256'
            )
            self.decoded_token = payload[self.verified_username]
            return self.decoded_token
        except Exception as err:
            return err

    def gen_passwd_hash(self):
        """ generates hashed password and assigns to self.hashed_password var
        """
        self.hashed_password = bcrypt.hashpw(
            self.encoded_password, bcrypt.gensalt()
        )

    def verify_passwd_hash(self):
        """verify hashed password matches raw password """
        if bcrypt.checkpw(self.encoded_password, self.hashed_password):
            self.verified_hashed_password = self.hashed_password

    def register_user(self):
        """ Save user to DB or return msg to user      
        """
        try:
            raw_timestamp = pytz.utc.localize(datetime.datetime.utcnow())
            utc_timestamp = raw_timestamp.isoformat()
            
            cur = self.connect_to_db()  
            cur.execute("""
                INSERT INTO users (
                    userid, username, name, email, admin_priviledges,\
                    registration_timestamp, password
                    ) 
                VALUES (DEFAULT, %s,%s,%s,%s,%s,%s);""", (
                    self.verified_username, self.name, self.verified_email, \
                    self.admin, utc_timestamp, \
                    self.hashed_password.decode()
                )
            )
            self.save_database()
            return {"Registration success": " User stored in DB"}

        except psycopg2.DatabaseError as err:
            self.db_error_handle(err)

        finally:
            self.close_database()
                    

class UserLogInOperations(OperationsOnNewUsers):
    """ Holds methods to login route"""
    def __init__(self, user_login_info, admin=False):
        self.raw_username = user_login_info['username']
        self.raw_password = user_login_info['password']
        
    def fetch_and_verify_user_login(self):
        """ Fetch user matching login details provided """
           
        try:
            cur = self.connect_to_db()
            cur.execute(
                    "SELECT * from users WHERE username LIKE '%s';", (self.raw_username) 
                )
            user_details = cur.fetchone()
            if bcrypt.hashpw(
                    self.raw_password,bcrypt.gensalt()
                ).decode() in user_details[6]:
                msg_out = True
                self.login_status = True
            elif user_details == None:
                msg_out = False

            return msg_out

        except psycopg2.DatabaseError as err:
            self.db_error_handle(err)
        
        finally:
            self.close_database()


class MenuOps(DatabaseManager):
    """ Operations on menu items"""
    def fetch_menu_items(self):
        """ Fetch all available menu items, return custom messaege if none """
        try:
            cur = self.connect_to_db()
            cur.execute("SELECT * FROM menu;")
            menu_items = cur.fetchall()
            if menu_items == None:
                menu_display = {'Menu Items': 'No menu items yet'}
            else:
                menu_display = {}
                for menu_item in menu_items:
                    menu_display[menu_item[0]] = {menu_item[3]:menu_item[2]}
            return menu_display
        except psycopg2.DatabaseError as err:
            self.db_error_handle(err)


class UserCredentialsValidator(OperationsOnNewUsers):
    """ Holds methods to validate Usename, password, Email validator """
    def __init__(self, raw_user_reg_data):
        self.raw_email = raw_user_reg_data['email']
        self.raw_password = raw_user_reg_data['password']
        self.raw_username = raw_user_reg_data['username']

    def username_check(self):
        """ Checks for username in DB, 
            returns custom msg if username is taken,
            else assigns it to self.hashed password var
        """
        try:
            cur = self.connect_to_db()
            cur.execute(
                    "SELECT * from users WHERE username LIKE '{}';".format(self.raw_username) 
                )
            username_fetch = cur.fetchone()
            if username_fetch == None:
                msg_out = 'Valid Username'
            else:
                msg_out = 'Invalid Username'

            return msg_out
        except psycopg2.DatabaseError as err:
            self.db_error_handle(err)

        finally:
            self.close_database()

    def email_check(self):
        """ Chserecks provided email for syntax
            contains atleast one @ and a . after it
        """
        if re.search(r'[^@]+@[^@]+\.[^@]+', self.raw_email):
            msg_out = 'Valid Email'
        else:
            msg_out = 'Invalid Email'

        return msg_out

    def password_check(self):
        """ Checks password Alteast 8 chars """
        if len(self.raw_password) > 8:
            msg_out = 'Valid Password'
        else:
            msg_out = 'Invalid Password'
        return msg_out


if __name__ == '__main__':
    pass

