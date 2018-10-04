""" Defines routes for app """


from flask import Blueprint, jsonify, request, make_response
from app.api.v2.models import MenuOps, OperationsOnNewUsers, UserLogInOperations, UserCredentialsValidator, FoodOrderOperations
from app import create_app

v2_base_bp = Blueprint('v2_base', __name__, url_prefix='/api/v2')
v2_auth_bp = Blueprint('v2_auth', __name__, url_prefix='/api/v2/auth')
v2_users_bp = Blueprint('v2_users', __name__,  url_prefix='/api/v2/users')


@v2_base_bp.route('/', methods=['GET'])
def index():
    """ Homepage. Returns welcome message """
    return jsonify("Welcome User. Speedy Chakula delivers fast-food-fast")


@v2_auth_bp.route('/signup', methods=['POST'])
def signup():
    """ Register new user """
    signup_data = request.get_json(force=True)  # user data
    if (
            'username' in signup_data and
            'email' in signup_data and
            'name' in signup_data and
            'password' in signup_data
        ):

        raw_user = UserCredentialsValidator(signup_data)
        # validate username and email
        if raw_user.username_check() != 'Valid Username':
            msg_out = {
                "Status": "Username Error",
                "Message": "Username already exists. Try a different username"
            }
            return make_response(jsonify(msg_out)), 202

        elif raw_user.email_check() != 'Valid Email':
            msg_out = {
                "Status": "Email Error",
                "Message": "Invalid Email address. Check syntax and try again"
            }
            return make_response(jsonify(msg_out)), 202

        elif raw_user.password_check() != 'Valid Password':
            msg_out = {
                "Status" : "Password Error",
                "Message": "Invalid password. Should be atlest 8 characters long"
            }
            return make_response(jsonify(msg_out)), 202
        else:

            new_user = OperationsOnNewUsers(signup_data)  # Instantate
            try:
                new_user.gen_passwd_hash()  # Hash password for storage
                new_user.verify_passwd_hash()  # Verify password is succesfully hashed
                new_user.register_user()   # Insert user to DB
                auth_token = new_user.auth_token_encoding() # Generate Auth token
                msg_out = {
                    "Status": "Success",
                    "Message": "Registration successful",
                    "Authentication token": auth_token.decode()
                }
                return  make_response(jsonify(msg_out)), 201
            
            except Exception as err:
                msg_out = {
                    "Status": "Registration failed",
                    "Message": 'Error: {}'.format(err)
                }
                return  make_response(jsonify(msg_out)), 401
             
    else:
        msg_out = {
            "Status" : "Operation failed",
            "Message": "Sorry.... the provided data is malformed"
        }
        return jsonify(msg_out)


@v2_auth_bp.route('/login', methods=['POST'])
def login():
    """ User Login """
    login_data = request.get_json(force=True)
    if (
            'username' in login_data and
            'password' in login_data        
        ):
        try:
            attempting_user = UserLogInOperations(login_data)  # Instantate
            if attempting_user.fetch_and_verify_user_login():
                auth_token =  attempting_user.auth_token_encoding()
                if auth_token:
                    msg_out = {
                    "Status": "Success",
                    "Message": "Login successful",
                    "Authentication token": auth_token.decode()
                } 
            
            else:
                msg_out = {
                    "Status" : "Login Error",
                    "Message": "Invalid username/password. Try again"
                }
            return  make_response(jsonify(msg_out)), 200
        except Exception as err:
                msg_out = {
                    "Status": "Login failed",
                    "Message": 'Error: {}'.format(err)
                }
                return  make_response(jsonify(msg_out)), 500
    else:
        msg_out = {
            "Status" : "Operation failed",
            "Message": "Sorry.... the provided data is malformed"
        }
        return jsonify(msg_out), 500
 

@v2_base_bp.route('/menu', methods=['GET'])
def menu():
    """ Fetch menu items """
    msg_out = MenuOps()
    return jsonify(msg_out.fetch_menu_items())


@v2_users_bp.route('/users/orders', methods=['POST'])
def place_order():
    """ Place food orders user """
    order_data = request.get_json(force=True)
    msg_out = FoodOrderOperations()

    return jsonify(msg_out.place_new_order(order_data))