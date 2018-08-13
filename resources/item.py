# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cant be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every Item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'item not found.'}, 400

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)
        try:
            # 使用sqlite3連結sqlite資料庫
            # item.insert()
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500
        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

        # 使用sqlite3連結sqlite資料庫
        # updated_item = ItemModel(name, data['price'])
        # if item is None:
        #     try:
        #         updated_item.insert()
        #     except:
        #         return {'message': 'An error occurred inserting the item.'}, 500
        # else:
        #     try:
        #         updated_item.update()
        #     except:
        #         return {'message': 'An error occurred updating the item.'}, 500
        # return updated_item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {"message": "item is not exist!"}
        else:
            try:
                item.delete()
            except:
                return {"message": "An error occurred deleteing the item."}
        return {'message': 'item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

        # 使用sqlite3連結sqlite資料庫
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query).fetchall()
        # connection.close()
        # return {'items': [ {"name": item[0], "price": item[1]} for item in result]}, 200
