""" Data representation - Routines for user to interact with the API. """

import os
import sys
import datetime
import re
import pytz
import psycopg2
import bcrypt
import jwt




class DatabaseManager():
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



    def db_error_handle(self, error):
        """ Roll back Transaction and exit incase of error """
        if self.conn:
            self.conn.rollback()
            print('An Error Occured: {}'.format(error))
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


class UserOps(DatabaseManager):
    """ Holds method to register a new user """
    def __init__(self, user_reg_info, admin=False):
        super().__init__(config_mode=None)
        self.raw_email = user_reg_info['email']
        self.raw_password = user_reg_info['password']
        self.raw_username = user_reg_info['username']
        self.name = user_reg_info['name']
        self.admin = admin

        self.verified_username = None
        self.verified_email = None
        self.verified_password = None

        self.hashed_password = None
        self.verified_hashed_password = None

        self.datetime_registered = None
        self.login_status = False

        self.auth_token = None
        self.encoded_token = None
        self.decoded_token = None


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
            username_check = cur.fetchone()
            if username_check == None:
                self.verified_username = self.raw_username
                msg_out = 'Valid Username'
            else:
                msg_out = 'Invalid Username'

            return msg_out
        except psycopg2.DatabaseError as err:
            self.db_error_handle(err)

        finally:
            self.close_database()

    def email_check(self):
        """ Checks provided email for syntax
            contains only one @
            Does not contain any of {{~`!#$%^&*+=|\'";:,}}
        """
        if not re.search(r'[~`!#$%^&*+=|;:,]', self.raw_email):
            if re.search(r'@', self.raw_email):
                self.verified_email = self.raw_email
                msg_out = 'Valid Email'
            else:
                msg_out = 'Invalid Email'
        else:
            msg_out = 'Invalid Email'

        return msg_out

    def password_check(self):
        """ Checks password Alteast 8 chars """
        if len(self.raw_password) > 8:
            self.verified_password = self.raw_password.encode()
            msg_out = 'Valid Password'
        else:
            msg_out = 'Invalid Password'
        return msg_out

    def auth_token_encoding(self):
        """ Generate Authentication Token """
        try:
            self.encoded_token = jwt.encode(
                {'username': self.verified_username},
                os.getenv('SECRET'),
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
                os.getenv('SECRET'),
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
            self.verified_password, bcrypt.gensalt()
        )

    def verify_passwd_hash(self):
        """verify hashed password matches raw password """
        if bcrypt.checkpw(self.verified_password, self.hashed_password):
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
                    login_status, reg_datetime, password
                    ) 
                VALUES (DEFAULT, %s,%s,%s,%s,%s,%s,%s);""", (
                    self.verified_username, self.name, self.verified_email, \
                    self.admin, self.login_status, utc_timestamp, \
                    self.hashed_password.decode()
                )
            )
            self.save_database()
            return {"Registration success": " User stored in DB"}

        except psycopg2.DatabaseError as err:
            self.db_error_handle(err)

        finally:
            self.close_database()
                    

class UserLogs(UserOps, DatabaseManager):
    """ Holds methods to log in/out """
    def __init__(self, user_login_info, admin=False):
        
        self.raw_username = user_login_info['username']
        self.raw_password = user_login_info['password']
        self.login_status = False
        
    def fetch_and_verify_user_login(self):
        """ Fetch user matching login details """
           
        try:
            cur = super().connect_to_db()
            cur.execute(
                    "SELECT * from users WHERE username LIKE '%s';", (self.raw_username) 
                )
            user_details = cur.fetchone()
            if bcrypt.hashpw(
                    self.raw_password,bcrypt.gensalt()
                ).decode() in user_details[7]:
                msg_out = True
                self.login_status = True
            elif user_details == None:
                msg_out = False

            return msg_out

        except psycopg2.DatabaseError as err:
            super().db_error_handle(err)
        
        finally:
            super().close_database()


class MenuOps(DatabaseManager):
    """ Operations on menu items"""
    def fetch_menu_items(self):
        return

if __name__ == '__main__':
    pass
 
