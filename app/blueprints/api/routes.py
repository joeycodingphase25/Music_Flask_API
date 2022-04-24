from . import api
from flask import jsonify, request
from app.blueprints.api.models import User


@api.route('/users/create', methods=["POST"])
def create_user():
    if not request.is_json:
        return jsonify({'error':'Your Request Content-Type Must Be Apllication/Json'}), 400
    data = request.json
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f'{field} must be in request body'}), 400
    username = data['username']
    email = data['email']
    password = data['password']
    new_user = User(username=username, email=email, password=password)
    return jsonify(new_user.to_dict()), 201