from loginapp import create_app, db
from loginapp.models import Users, UserAccess
from flask_migrate import Migrate


app = create_app("develop")

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(User=Users,
                UserAccess=UserAccess,
                db=db)
