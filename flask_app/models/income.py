from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB_NAME
from flask import flash
from flask_app.models.user import User
import re

class Income:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.amount = data['amount']
        self.source = data['source']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    def get_source_or_category(self):
        return self.source

    def get_type(self):
        return 'Income'

    #! CREATE
    @classmethod
    def save(cls, form_data):
        query = "INSERT INTO incomes (amount, source, date, user_id) VALUES (%(amount)s, %(source)s, %(date)s, %(user_id)s);"
        result = connectToMySQL(DB_NAME).query_db(query, form_data)
        return result
    
    @classmethod
    def get_all_with_owner(cls, user_id):
        query = "SELECT * FROM incomes WHERE user_id = %(user_id)s;"
        data = {"user_id": user_id}
        results = connectToMySQL(DB_NAME).query_db(query, data)
        incomes = []
        for row in results:
            each_income = cls(row) #create item instance
            incomes.append(each_income)
        return incomes
    
    @classmethod
    def delete_one_by_id(cls, id):
        id_dict = {'id': id}
        query = "DELETE FROM incomes WHERE id = %(id)s"
        connectToMySQL(DB_NAME).query_db(query, id_dict)
        return True
    
    @classmethod
    def edit_one(cls,form_data):
        query = "UPDATE incomes SET amount = %(amount)s, source = %(source)s, date = %(date)s where id = %(id)s;"
        income_id = connectToMySQL(DB_NAME).query_db(query, form_data)
        return income_id
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM incomes WHERE id = %(id)s;"
        data = {"id": id}
        results = connectToMySQL(DB_NAME).query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return None
        