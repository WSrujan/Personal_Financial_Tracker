from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.models.income import Income
from flask_app.models.user import User

# Create Income Page
@app.route("/income", methods = ["GET", "POST"])
def income_page():
    # Route protection
    if 'user_id' not in session:
        return redirect("/")
    logged_user = User.get_one_by_id(session['user_id'])
    incomes = Income.get_all_with_owner(logged_user.id)  # Pass the user_id to the method
    return render_template("income.html", incomes=incomes, logged_user=logged_user, transaction_type='income')  # Pass incomes and logged_user to the template

@app.route("/income/create", methods=["GET", "POST"])
def create_income():
    # Route protection
    if 'user_id' not in session:
        return redirect("/")
    logged_user = User.get_one_by_id(session['user_id'])
    if request.method == "POST": 
        form_data = dict(request.form)
        form_data["user_id"] = session["user_id"]
        Income.save(form_data)
        return redirect("/income")
    return render_template("income.html", logged_user=logged_user)

@app.route("/income/delete/<int:id>")
def delete_income(id):
    # Route protection
    if 'user_id' not in session:
        return redirect("/")
    Income.delete_one_by_id(id)
    return redirect("/income")