from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB_NAME
from flask import flash
from flask_app.models.user import User
import re

class Expense:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.amount = data['amount']
        self.category = data['category']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    def get_source_or_category(self):
        return self.category

    def get_type(self):
        return 'Expense'

    #! CREATE
    @classmethod
    def save(cls, form_data):
        query = "INSERT INTO expenses (amount, category, date, user_id) VALUES (%(amount)s, %(category)s, %(date)s, %(user_id)s);"
        result = connectToMySQL(DB_NAME).query_db(query, form_data)
        return result
    
    @classmethod
    def get_all_with_owner(cls, user_id):
        query = "SELECT * FROM expenses WHERE user_id = %(user_id)s;"
        data = {"user_id": user_id}
        results = connectToMySQL(DB_NAME).query_db(query, data)
        expenses = []
        for row in results:
            each_expenses = cls(row) #create item instance
            expenses.append(each_expenses)
        return expenses
    
    @classmethod
    def delete_one_by_id(cls, id):
        id_dict = {'id': id}
        query = "DELETE FROM expenses WHERE id = %(id)s"
        connectToMySQL(DB_NAME).query_db(query, id_dict)
        return True
    
    @classmethod
    def edit_one(cls,form_data):
        query = "UPDATE expenses SET amount = %(amount)s, category = %(category)s, date = %(date)s where id = %(id)s;"
        expenses_id = connectToMySQL(DB_NAME).query_db(query, form_data)
        return expenses_id
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM expenses WHERE id = %(id)s;"
        data = {"id": id}
        results = connectToMySQL(DB_NAME).query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return None
        