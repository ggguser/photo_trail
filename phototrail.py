# from app import create_app, db
from app import app, db
from app.models import User, Trail, Photo
from app.routes import *

# app = create_app()
# db.drop_all(app=create_app())
# db.create_all(app=create_app())
# app.app_context().push()
# db.init_app(app)
# db.create_all()
# app.run(port=9874, debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Trail': Trail, 'Photo': Photo}


