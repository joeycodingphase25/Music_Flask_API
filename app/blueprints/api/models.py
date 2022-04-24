import base64
import os
from app import db, login
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

###### MODEL BREAKDOWN ############
# USER model to hold a list of unique users that enables access to platform
# Key-signature model that will hold the bulk of information AND serve as a Foreign-Key in the SONG model
# SONG model that holds a list of all songs with the Foreingn-keys of {'COMPOSER', 'KEY_SIGNATURE'}
# Composer Model that holds a list of all composers and has a Foreign-key of MUSICAL_ERA model
# MUSICAL_ERA model will hold a list of all the music eras and about info, serving as a Foreign-key in the compsoser model

# Note that the composers that bleed into multiple eras will be moved into a single era to make the complexity of the models more attainable
########################################

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

## flask shell tester - new_user=User(username='joseph', email='joey@gmail.com', password='123')
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # token columns
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User|{self.username}>"

    def __str__(self):
        return self.username
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Token Methods
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created,
        }

## flask shell tester -- new_key=Keysignature(key_signature='C Major', keys='13568acd', about='This is about section test', more_info='this is more_info test')
## this works --> key.update(about="updated about")
################################
#########-KEY-SIGNATURE##########
## Key signature will be a attached as a foreign key to SONGS
class Keysignature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_signature = db.Column(db.String(20), unique=True, nullable=False)
    keys = db.Column(db.String(24), nullable=False) # WILL BE A STRING, can be manipulated later
    about = db.Column(db.String(), nullable=False)
    more_info = db.Column(db.String(), nullable=False)
    songs = db.relationship('Song', backref='keysignature', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        # object display method
        return f"<Key|{self.key_signature}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            # can update all values for this shell model
            if key in {'key_signature', 'keys', 'about', 'more_info'}:
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            # dont really need to json the ID here
            'key_signature': self.key_signature,
            'keys': self.keys,
            'body': self.about,
            'more_info': self.more_info
        }

 ## flask shell era test -- new_era=Era(era='Baroque', about_era='this is about era test', more_info='this is more info era test')       
################################
#########-Musical Era -##########
## serves as foreign key in composer
class Era(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    era = db.Column(db.String(150), nullable=False, unique=True)
    about_era = db.Column(db.String(), nullable=False) 
    more_info = db.Column(db.String(), nullable=False) 
    composers = db.relationship('Composer', backref='era', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        # object display method
        return f"<Era|{self.era}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            # can update all values for this shell model
            if key in {'era', 'about_era', 'more_info'}:
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            # dont really need to json the ID here
            'era': self.era,
            'about_era': self.about_era,
            'more_info': self.more_info,
            ## functioning
            'composers': [composer.to_dict() for composer in Composer.query.filter_by(era_id=self.id).all()]
        }


## flask composer test -- new_comp=Composer(composer_name='Chopin', more_info='composer moreinfo test', famous_work='etudes', era_id=1)
################################
#########-Composer-##########
## contains the music_era foreign key
## Serves as Foreign key for Song
class Composer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    composer_name = db.Column(db.String(100), nullable=False, unique=True)
    more_info = db.Column(db.String()) # WILL BE A STRING, can be manipulated later
    famous_work = db.Column(db.String())
    era_id = db.Column(db.Integer, db.ForeignKey('era.id'), nullable=False)
    composer_id = db.relationship('Song', backref='composer', lazy=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        # object display method
        return f"< Composer|{self.composer_name}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            # can update all values for this shell model
            if key in {'composer_name', 'more_info', 'famous_work'}: # cant update foreign keyssssss *probably
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        ## IMPORTANT ADDED THE SONGS AS A TO_DICT INSTEAD OF A RELATIONSHIP
        ## THIS IS BECAUSE WE WANT A LIST OF SONGS TO POPULATE
        return {
            # dont really need to json the ID here
            'composer_name': self.composer_name,
            'more_info': self.more_info,
            'famous_work': self.famous_work,
            'era': self.more_info,
            # fixed
            'songs': [song.to_dict() for song in Song.query.filter_by(composer_id=self.id).all()]
        }        


## flask shell song test -- new_song=Song(song_name='Op 28 No 1', song_info='prelude', song_link='link test', more_info='more info test', keysignature_id=1, composer_id=1)
################################
#########-SONGS-##########
## contains the foreign key 'key_signature'
## contains the foreign key 'composer'
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), nullable=False)
    song_info = db.Column(db.String(), nullable=False) 
    song_link = db.Column(db.String())
    more_info = db.Column(db.String(), nullable=False)
    keysignature_id = db.Column(db.Integer, db.ForeignKey('keysignature.id'), nullable=False)
    composer_id = db.Column(db.Integer, db.ForeignKey('composer.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        # object display method
        return f"<Song|{self.song_name}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            # can update all values for this shell model
            if key in {'song_name', 'song_info', 'song_link', 'more_info', 'key_singature'}:
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            # dont really need to json the ID here
            'song_name': self.song_name,
            'song_info': self.song_info,
            'song_link': self.song_link,
            'more_info': self.more_info,
            'keysignature_id': self.keysignature_id,
            'composer_id': self.composer_id
        }


