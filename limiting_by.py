from flask import Flask, redirect
# rom flask.ext.login import LoginManager
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user
)

from flask_limiter import Limiter

app = Flask(__name__)

# flask-login
app.secret_key = 'super secret string'
login_manager = LoginManager()
login_manager.init_app(app)

# flask-limiter
limiter = Limiter(app)


# user class
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = id


# memory storage
users = [User('waseem')]


@login_manager.user_loader
def load_user(user_id):
    return users[0]


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/login')
def login():
    if not current_user.is_authenticated:
        login_user(users[0])
    return redirect('/secured')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/secured')
@login_required
@limiter.limit("2 per day", key_func=lambda: current_user.username)
def secured():
    return f"Hello, {current_user.id}"
# @app.errorhandler(429)
# def ratelimit_handler(e):
#     return "You have exceeded your rate-limit"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
