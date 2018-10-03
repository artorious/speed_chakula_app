""" Defines routes for app """

from flask import Blueprint, jsonify, request, make_response
from app.api.v2.models import UserOps
from app import create_app

v2_base_bp = Blueprint('v2_base', __name__, url_prefix='/api/v2')
v2_auth_bp = Blueprint('v2_auth', __name__, url_prefix='/api/v2/auth')


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
        new_user = UserOps(signup_data)  # Instantate

        if new_user.username_check() != 'Valid Username':
            msg_out = {
                "Status": "Username Error",
                "Message": "Username already exists. Try a different username"
            }
            return make_response(jsonify(msg_out)), 202

        elif new_user.email_check() != 'Valid Email':
            msg_out = {
                "Status": "Email Error",
                "Message": "Invalid Email address. Check syntax and try again"
            }
            return make_response(jsonify(msg_out)), 202

        elif new_user.password_check() != 'Valid Password':
            msg_out = {
                "Status" : "Password Error",
                "Message": "Invalid password. Should be atlest 8 characters long"
            }
            return make_response(jsonify(msg_out)), 202
        else:
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


    