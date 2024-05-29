from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.models.expense import Expense
from flask_app.models.user import User

# Create Expenses Page
@app.route("/expense", methods = ["GET", "POST"])
def expense_page():
    # Route protection
    if 'user_id' not in session:
        return redirect("/")
    logged_user = User.get_one_by_id(session['user_id'])
    expenses = Expense.get_all_with_owner(logged_user.id)  # Pass the user_id to the method
    return render_template("expense.html", expenses=expenses, logged_user=logged_user, transaction_type='expense')  # Pass expense and logged_user to the template

@app.route("/expense/create", methods=["GET", "POST"])
def create_expense():
    # Route protection
    if 'user_id' not in session:
        return redirect("/")
    logged_user = User.get_one_by_id(session['user_id'])
    if request.method == "POST": 
        form_data = dict(request.form)
        form_data["user_id"] = session["user_id"]
        Expense.save(form_data)
        return redirect("/expense")
    return render_template("expense.html", logged_user=logged_user)

@app.route("/expense/delete/<int:id>")
def delete_expense(id):
    # Route protection
    if 'user_id' not in session:
        return redirect("/")
    Expense.delete_one_by_id(id)
    return redirect("/expense")