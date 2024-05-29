from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import incomes
from flask_app.controllers import expenses
from flask_app.controllers import transactions

if __name__=="__main__":
    app.run(debug=True)