import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# 在正式生產環境中，secret_key不應該存在於source code中，
# 而應該使用其他方式帶入，考慮環境變數或是其他可能
app.secret_key = os.environ.get('SECRET_KEY', 'hughe')
api = Api(app)

# JWT會創造一個新的端點/auth，當用戶發送username及password到/auth時，
# JWT會使用它們，透過authenticate()來驗證並發送JWT Token，並在之後的request中
# 透過identity()調用符合身分的用戶。
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
