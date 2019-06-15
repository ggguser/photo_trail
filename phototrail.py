from app import app, db
from app.models import User, Trail, Photo


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Trail': Trail, 'Photo': Photo}