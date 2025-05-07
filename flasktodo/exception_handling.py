from flasktodo import jwt
from flask import flash,make_response,redirect

@jwt.unauthorized_loader
def unauthoziederror(error):
    flash(f'User not Authenticated',category="danger")
    resp=make_response(redirect('login'))
    return resp