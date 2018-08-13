# import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__='items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

        # 使用sqlite3連結sqlite資料庫
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     # (*row) 與 (row[0], row[1])等價
        #     # return cls(row[0], row[1])
        #     return cls(*row)


    def save_to_db(self):
        # db.session.add()使用update或是upsert方式將資料存進table中，所以將insert()及update()取代
        db.session.add(self)
        db.session.commit()

    # def insert(self):
        # 使用sqlite3連結sqlite資料庫
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()

    # def update(self):
        # 使用sqlite3連結sqlite資料庫
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.price, self.name))
        # connection.commit()
        # connection.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        # 使用sqlite3連結sqlite資料庫
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (self.name,))
        # connection.commit()
        # connection.close()
