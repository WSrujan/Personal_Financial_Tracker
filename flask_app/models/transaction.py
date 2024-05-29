from operator import or_
from flask_app import DB_NAME
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.expense import Expense
from flask_app.models.income import Income


class Transaction:
    @classmethod
    def get_dashboard_data(cls, user_id, limit=5):
        # Get total income
        query = "SELECT SUM(amount) as total FROM incomes WHERE user_id = %(user_id)s;"
        data = {"user_id": user_id}
        result = connectToMySQL(DB_NAME).query_db(query, data)
        total_income = result[0]['total'] if result[0]['total'] else 0

        # Get total expenses
        query = "SELECT SUM(amount) as total FROM expenses WHERE user_id = %(user_id)s;"
        result = connectToMySQL(DB_NAME).query_db(query, data)
        total_expenses = result[0]['total'] if result[0]['total'] else 0

        # Get recent incomes
        query = "SELECT * FROM incomes WHERE user_id = %(user_id)s ORDER BY date DESC LIMIT %(limit)s;"
        data = {"user_id": user_id, "limit": limit}
        results = connectToMySQL(DB_NAME).query_db(query, data)
        recent_incomes = [Income(row) for row in results]

        # Get recent expenses
        query = "SELECT * FROM expenses WHERE user_id = %(user_id)s ORDER BY date DESC LIMIT %(limit)s;"
        data = {"user_id": user_id, "limit": limit}
        results = connectToMySQL(DB_NAME).query_db(query, data)
        recent_expenses = [Expense(row) for row in results]

        # Combine and sort recent transactions
        recent_transactions = sorted(recent_incomes + recent_expenses, key=lambda x: x.date, reverse=True)[:limit]

        return total_income, total_expenses, recent_transactions
