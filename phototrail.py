from app import create_app, db
from app.models import User, Trail, Photo

app = create_app()


# db.init_app(app)
# db.create_all()



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Trail': Trail, 'Photo': Photo}


