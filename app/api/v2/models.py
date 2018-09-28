""" Data representation - Routines for user to interact with the API. """

import os
import sys
import datetime
import re
import psycopg2
import bcrypt
import jwt
from flask_restful import Resource



CONN = None

USER = os.getenv("DATABASE_USERENAME")
DBNAME = os.getenv("DATABASE_NAME")
HOST = os.getenv("DATABASE_HOST")
PORT = os.getenv("DATABASE_PORT")
PASSWORD = os.getenv("DATABASE_PWD")



def create_db_connection():
    """ Make conectio to db """
    try:
        global CONN
        # Connection
        CONN = psycopg2.connect(
            dbname=DBNAME,
            user=USER,
            host=HOST,
            password=PASSWORD
        )
        CUR = CONN.cursor()

    except Exception as err:
        CUR = None
        print('An Error Occured: {}'.format(err))
        
    finally:
        return CUR

def create_users_table():
    """ Creates a table that hold user information """
    try:
        global CONN
        CUR = create_db_connection()
        CUR.execute("DROP TABLE IF EXISTS users CASCADE")
        CUR.execute(
            "CREATE TABLE users (\
                userid SERIAL PRIMARY KEY, \
                name VARCHAR(50) NOT NULL, \
                password VARCHAR NOT NULL, \
                email VARCHAR(50) NOT NULL, \
                username VARCHAR(25) NOT NULL,\
                admin_priviledges bool NOT NULL,\
                login_status bool NOT NULL, \
                registration_datetime TIMESTAMPTZ NOT NULL \
                );"
            )
        CONN.commit()
    except psycopg2.DatabaseError as err:
        if CONN:
            CONN.rollback()
        print('An Error Occured: {}'.format(err))
        sys.exit(1)
    finally:
        close_database()

def create_food_menu_table():
    """ Creates a table that holds all available menu/food items """
    try:
        CONN = create_db_connection()
        CUR = CONN.cursor()
        CUR.execute("DROP TABLE IF EXISTS menu CASCADE")
        CUR.execute(
            "CREATE TABLE menu (\
                foodid SERIAL PRIMARY KEY, \
                userid INT NOT NULL REFERENCES users(userid), \
                unit_price INT NOT NULL, \
                description VARCHAR(100) NOT NULL, \
                datetime_added TIMESTAMPTZ NOT NULL \
                );"
            )
        CONN.commit()
    except psycopg2.DatabaseError as err:
        if CONN:
            CONN.rollback()
        print('An Error Occured: {}'.format(err))
        sys.exit(1)
    finally:
        close_database()

def create_food_orders_table():
    """ Creates table that holds all food orders from users """
    try:
        CONN = create_db_connection()
        CUR = CONN.cursor()
        CUR.execute("DROP TABLE IF EXISTS orders CASCADE")
        CUR.execute(
            "CREATE TABLE orders (\
                orderid SERIAL PRIMARY KEY, \
                userid INT NOT NULL REFERENCES users(userid), \
                order_cost INT NOT NULL, \
                orderstatus VARCHAR(15) NOT NULL, \
                deliverylocation VARCHAR(50) NOT NULL, \
                orderDescription VARCHAR(100) NOT NULL, \
                order_datetime TIMESTAMPTZ NOT NULL \
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

class SignUp(Resource):
    """ Holds method to register a new user """
    def __init__(self, user_reg_info, admin=False):
        self.raw_email = user_reg_info['email']
        self.raw_password = user_reg_info['password']
        self.raw_username = user_reg_info['username']
        self.name = user_reg_info['name']
        self.admin = admin
        self.verified_password = None
        self.hashed_password = None
        self.verified_hashed_password = None
        self.verified_username = None
        self.datetime_registered = None
        self.verified_email = None
        # self.verified_reg_data = None
        self.encoded_token = None
        self.decoded_token = None
        self.login_status = False
        self.procecessing = True

        while self.procecessing:
            try:
                self.username_check(self.raw_username)
                self.password_check(self.raw_password)
                self.gen_passwd_hash(self.verified_password)
                self.verify_passwd_hash(self.hashed_password)
                self.auth_token_encoding(self.verified_username)
                self.auth_token_decoding(self.encoded_token)

                # self.verified_reg_data = {
                #     'username': self.verified_username,
                #     'email': self.verified_email,
                #     'name': self.name,
                #     'password': self.hashed_password

                # }
                self.procecessing = False

            except Exception as err:
                print(err)
                self.procecessing = False
        
        self.post()
    
    def post(self):
        """ Save user to DB or return msg to user      
        """
        if self.verified_username == None:
            msg = {"Username Error": "Username already exists"}
        elif self.verified_email == None:
            msg = {"Email Error": "Invalid Email address"}
        elif self.verified_password == None:
            msg = {"Password Error": "Invalid password"}
        else:
            try:
                CONN = create_db_connection()
                CUR = CONN.cursor()
                CUR.excecute(
                    "INSERT INTO users VALUES(\
                        DEFAULT, {0}, {1}, {2}, {3}, {4}, {5}, {6} \
                    )".format(
                        self.name,
                        self.hashed_password,
                        self.verified_email,
                        self.verified_username,
                        self.admin,
                        self.login_status,
                        datetime.datetime.now(),
                    )
                )
                CONN.commit()
            except psycopg2.DatabaseError as err:
                if CONN:
                    CONN.rollback()
                print('An Error Occured: {}'.format(err))
                sys.exit(1)
            finally:
                close_database()

    def username_check(self, raw_username):
        """ Checks for username in DB, 
            returns custom msg if username is taken,
            else assigns it to self.hashed password var
        """
        try:
            CUR.execute(
                    "SELECT * from users WHERE username LIKE {}".format(raw_username) 
                )
            username_check = CUR.fetchone()
            if row == None:
                self.verified_username = raw_username
            close_database()

        except psycopg2.DatabaseError as err:
            if CONN:
                CONN.rollback()
            print('An Error Occured: {}'.format(err))
            sys.exit(1)
        finally:
            close_database()
    
    def password_check(self, raw_password):
        """ Checks password Alteast 8 chars """
        if len(raw_password) > 8 :
            self.verified_password = raw_password
    
    def email_check(self, raw_email):
        """ Checks provided email for syntax
        
            contains only one @ 
            Does not contain any of {{~`!@#$%^&*+=|\'";:,}}
        """
        if not re.search(r'[{~`!#$%^&*+=|][\\\'";:,}]', raw_email):
            if re.search(r'@', raw_email):
                self.verified_email = raw_email

    def gen_passwd_hash(self, verified_password):
        """ generates hashed password and assigns to self.hashed_password var
        """
        self.hashed_password = bcrypt.hashpw(
            verified_password, bcrypt.gensalt()
        )

    def verify_passwd_hash(self, passwd_hash):
        """verify hashed password matches raw password """
        if bcrypt.checkpw(self.verified_password, passwd_hash):
            self.verified_hashed_password = passwd_hash
    
    def auth_token_encoding(self, verified_username):
        """ Generate Authentication Token """
        try:
            self.encoded_token = jwt.encode(
                {'username': verified_username}, 
                os.getenv('SECRET'), 
                algorithm='HS256'
            )
            return self.encoded_token
        except Exception as err:
            print(err)

    def auth_token_decoding(self, auth_token):
        """ Generates string from decoded Token """
        try:
            payload = jwt.decode(
                auth_token,
                os.getenv('SECRET'),         
            )
            self.decoded_token = payload['username']
            return self.decoded_token
        except Exception as err:
            print(err)

    

if __name__ == '__main__':
    create_all_tables()
    print('Good to go!!!!')
    # SignUp({
    #         'username': 'mrnoname',
    #         'email': 'mrnoname@email.com',
    #         'password': 'elephantman',
    #         'name': 'Arthur Ngondo',
    #     })

