from flasktodo import jwt
from flask import flash,make_response,redirect

@jwt.unauthorized_loader
def unauthoziederror(error):
    flash(f'User not Authenticated',category="danger")
    resp=make_response(redirect('login'))
    return resp

@jwt.invalid_token_loader
def invalidToken(error):
    flash(f'Invalid token',category='danger')
    resp=make_response(redirect('login'))
    return resp

@jwt.expired_token_loader
def expired(jwt_header,jwt_payload):
    flash(f'Session Expired',category="dark")
    resp=make_response(redirect('login'))
    return resp