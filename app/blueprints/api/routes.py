from . import api
from flask import jsonify, request
from .auth import basic_auth, token_auth
from app.blueprints.api.models import User, Keysignature, Era, Composer, Song


################################################
############### USER ROUTES ####################
################################################
@api.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token, 'expiration': user.token_expiration})

#Create User
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

################################################
###### KEY SIGNATURE ROUTES ####################
################################################

# Create Key Signature // no FK dependencies
@api.route('/key-signature/create', methods=['POST'])
@token_auth.login_required
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get data from request body
    data = request.json
    # Check to make sure all required fields are present
    for field in ['key_signature', 'keys', 'about', 'more_info']:
        if field not in data:
            # if not return a 400 response with error
            return jsonify({'error': f'{field} must be in request body'}), 400
    # Get fields from data dict
    key_sig = data['key_signature']
    keys = data['keys']
    about = data['about']
    more_info = data['more_info']
    new_key=Keysignature(key_signature=key_sig, keys=keys, about=about, more_info=more_info)
    return jsonify(new_key.to_dict()), 201

# Edit a key signature 
@api.route('/key-signature/update/<int:key_sig_id>', methods=['PUT'])
@token_auth.login_required
def edit_post(key_sig_id):
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for key in data.keys():
        if key not in {'key_signature', 'keys', 'about', 'more_info'}:
            return jsonify({'error': f'{key} is not an acceptable property'}), 400
    # filter object needs to be here for some reason
    key = Keysignature.query.filter_by(id=key_sig_id).first()
    key.update(**data)
    return jsonify(key.to_dict())

# Get all Key Signatures
@api.route('/key-signatures')
def get_posts():
    key_sigs = Keysignature.query.all()
    return jsonify([k.to_dict() for k in key_sigs])

################################################
###### ERA ROUTES ####################
################################################