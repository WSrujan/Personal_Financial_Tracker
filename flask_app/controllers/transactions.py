from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.models.expense import Expense
from flask_app.models.income import Income
from flask_app.models.transaction import Transaction
from flask_app.models.user import User

# Create Dashboard Page
@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    # Route protection
    if 'user_id' not in session:
        return redirect("/")
    logged_user = User.get_one_by_id(session['user_id'])
    total_income, total_expenses, recent_transactions = Transaction.get_dashboard_data(logged_user.id)

    return render_template('dashboard.html', logged_user=logged_user, total_income=total_income, total_expenses=total_expenses, recent_transactions=recent_transactions)

@app.route("/edit/<string:transaction_type>/<int:id>", methods=["GET", "POST"])
def edit_transaction(transaction_type, id):
    
    # transaction_type should be either 'income' or 'expense'
    # id is the id of the income or expense record to edit

    # Fetch the transaction record from the database
    if transaction_type == 'income':
        transaction = Income.get_by_id(id)
    elif transaction_type == 'expense':
        transaction = Expense.get_by_id(id)
    else:
        return "Invalid transaction type"

    if request.method == "POST":
        # Prepare the new data
        form_data = request.form.to_dict()
        form_data['id'] = id

        # Update the transaction record with the form data
        if transaction_type == 'income':
            Income.edit_one(form_data)
        elif transaction_type == 'expense':
            Expense.edit_one(form_data)

        return redirect("/dashboard")

    return render_template('edit.html', transaction_type=transaction_type, transaction=transaction)


