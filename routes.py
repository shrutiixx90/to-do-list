from flask import request, jsonify
from . import app, keycloak_openid
from .models import db, User

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    token = keycloak_openid.token(data['username'], data['password'])
    user_info = keycloak_openid.userinfo(token['access_token'])
    user = User.query.filter_by(username=user_info['preferred_username']).first()
    if not user:
        user = User(username=user_info['preferred_username'], email=user_info['email'])
        db.session.add(user)
        db.session.commit()
    return jsonify({'access_token': token['access_token']})

@app.route('/buy_pro', methods=['POST'])
def buy_pro():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user:
        user.is_pro = True
        db.session.commit()
    return jsonify({'message': 'Pro license purchased successfully'})
