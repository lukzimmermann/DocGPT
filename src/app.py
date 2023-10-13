from flask import Flask
from routes.auth import auth_bp
from routes.chat import chat_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(chat_bp, url_prefix='/chat')

if __name__ == '__main__':
    app.run(debug=True)
