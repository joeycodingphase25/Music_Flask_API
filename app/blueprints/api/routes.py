from . import api
from flask import jsonify, request
from .auth import basic_auth, token_auth
from app.blueprints.api.models import User, Keysignature, Era, Composer, Song, translate


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
    new_keys = ''
    for key in keys.replace(' ', '').split(','):
        if key in translate: 
            new_keys += str(translate[key])
    about = data['about']
    more_info = data['more_info']
    new_key=Keysignature(key_signature=key_sig, keys=new_keys, about=about, more_info=more_info)
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
def get_keys():
    key_sigs = Keysignature.query.all()
    return jsonify([k.to_dict() for k in key_sigs])


# Get a Single Era by ID
@api.route('/key/<int:key_id>')
def get_single_key(key_id):
    key = Keysignature.query.get_or_404(key_id)
    return jsonify(key.to_dict())

################################################
################ ERA ROUTES ####################
################################################

# Get all eras 
# #// NESTED LIST OF COMPOSERS AND COMPOSER NESTED WITH SONGS
@api.route('/eras')
def get_eras():
    eras = Era.query.all()
    ## Note that dict of composer objects populate under "composers" key
    return jsonify([e.to_dict() for e in eras])

# Get a Single Era by ID
@api.route('/era/<int:era_id>')
def get_single_era(era_id):
    era = Era.query.get_or_404(era_id)
    return jsonify(era.to_dict())


# CREATE AN ERA
@api.route('/era/create', methods=['POST'])
@token_auth.login_required
def create_era():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get data from request body
    data = request.json
    # Check to make sure all required fields are present
    for field in ['era','date', 'about_era', 'more_info']:
        if field not in data:
            # if not return a 400 response with error
            return jsonify({'error': f'{field} must be in request body'}), 400
    # Get fields from data dict
    era = data['era']
    date = data['date']
    about_era = data['about_era']
    more_info = data['more_info']
    new_era=Era(era=era, date=date, about_era=about_era, more_info=more_info)
    return jsonify(new_era.to_dict()), 201

# EDIT AN ERA
@api.route('/era/update/<int:era_id>', methods=['PUT'])
@token_auth.login_required
def edit_era(era_id):
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for key in data.keys():
        if key not in {'era', 'date', 'about_era', 'more_info'}:
            return jsonify({'error': f'{key} is not an acceptable property'}), 400
    # filter object needs to be here for some reason
    era = Era.query.filter_by(id=era_id).first()
    era.update(**data)
    return jsonify(era.to_dict())


################################################
############ COMPOSER ROUTES ###################
################################################

# Get all Composers
# #// NESTED LIST OF SONGS
@api.route('/composers')
def get_composers():
    composers = Composer.query.all()
    ## Note that dict of composer objects populate under "composers" key
    return jsonify([c.to_dict() for c in composers])

# get single composer
@api.route('/composer/<int:composer_id>')
def get_single_composer(composer_id): 
    composer = Composer.query.get_or_404(composer_id)
    return jsonify(composer.to_dict())

# CREATE A COMPOSER
@api.route('/composer/create', methods=['POST'])
@token_auth.login_required
def create_composer():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get data from request body
    data = request.json
    # Check to make sure all required fields are present
    for field in ['composer_name', 'more_info', 'image_url', 'era_id']:
        if field not in data:
            # if not return a 400 response with error
            return jsonify({'error': f'{field} must be in request body'}), 400
    # Get fields from data dict
    composer_name = data['composer_name']
    image_url = data['image_url']
    more_info = data['more_info']
    era_id = data['era_id']
    new_composer=Composer(composer_name=composer_name, image_url=image_url, more_info=more_info, era_id=era_id)
    return jsonify(new_composer.to_dict()), 201

# EDIT A COMPOSER
@api.route('/composer/update/<int:composer_id>', methods=['PUT'])
@token_auth.login_required
def edit_composer(composer_id):
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for key in data.keys():
        if key not in {'composer_name', 'more_info', 'image_url', 'era_id'}:
            return jsonify({'error': f'{key} is not an acceptable property'}), 400
    # filter object needs to be here for some reason
    composer = Composer.query.filter_by(id=composer_id).first()
    composer.update(**data)
    return jsonify(composer.to_dict())


################################################
################ SONG ROUTES ###################
################################################

# Get all Songs
# #// NESTED LIST OF SONGS
@api.route('/songs')
def get_songs():
    songs = Song.query.all()
    ## Note that dict of composer objects populate under "composers" key
    return jsonify([s.to_dict() for s in songs])


# get single song
@api.route('/song/<int:song_id>')
def get_single_song(song_id): 
    song = Song.query.get_or_404(song_id)
    return jsonify(song.to_dict())

# CREATE A SONG
## IF THE COMPOSER_ID and SONG NAME ALREADY EXIST DISPLAY AN ERROR MESSAGE
@api.route('/song/create', methods=['POST'])
@token_auth.login_required
def create_song():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get data from request body
    data = request.json
    # Check to make sure all required fields are present
    for field in ['song_name', 'song_info', 'song_link', 'more_info', 'difficulty', 'keysignature_id', 'composer_id']:
        if field not in data:
            # if not return a 400 response with error
            return jsonify({'error': f'{field} must be in request body'}), 400
    # Get fields from data dict
    song_name = data['song_name']
    song_info = data['song_info']
    song_link = data['song_link']
    difficulty = data['difficulty']
    keysignature_id = data['keysignature_id']
    composer_id = data['composer_id']
    new_song=Song(song_name=song_name, song_info=song_info, song_link=song_link, difficulty=difficulty, keysignature_id=keysignature_id, composer_id=composer_id)
    return jsonify(new_song.to_dict()), 201

# EDIT A SONG
@api.route('/song/update/<int:song_id>', methods=['PUT'])
@token_auth.login_required
def edit_song(song_id):
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for key in data.keys():
        if key not in {'song_name', 'song_info', 'song_link', 'more_info', 'difficulty', 'keysignature_id', 'composer_id'}:
            return jsonify({'error': f'{key} is not an acceptable property'}), 400
    # filter object needs to be here for some reason
    song = Song.query.filter_by(id=song_id).first()
    song.update(**data)
    return jsonify(song.to_dict())

