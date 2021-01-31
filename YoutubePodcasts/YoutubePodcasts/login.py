import flask_login
from YoutubePodcasts import app
from YoutubePodcasts.models import Users

app.secret_key = 'fuckyoubitch123'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    record = Users.query.filter_by(username=username).first()
    if record is None:
        return
    user = User()
    user.id = username

    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    record = Users.query.filter_by(username=username).first()
    if record is None:
        return

    user = User()
    user.id = username
    #user.is_authenticated = request.form.get('password') == record.password
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
