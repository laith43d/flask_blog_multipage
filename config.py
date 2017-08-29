from flask import Flask

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.secret_key = '6523e58bc0eec42c31b9635d5e0dfc23b6d119b73e633bf3a5284c79bb4a1ede'
