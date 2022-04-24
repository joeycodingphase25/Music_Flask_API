from app import app, db
from app.blueprints.api.models import User, Keysignature, Era


@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Keysignature': Keysignature, 'Era': Era}

# , 'Composer' : Composer, 'Keysignature': Keysignature, 'Song': Song, 'Era': Era