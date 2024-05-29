from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Display loreg form
@app.route("/")
def login_page():
    return render_template('login.html')

# Register Route
@app.route("/register", methods=["POST"])
def register_process():
    if not User.validate_user(request.form):
        return redirect("/")
    #hash password and save
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    updated_form = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save(updated_form)
    session['user_id'] = user_id
    return redirect("/dashboard")

# Login Route
@app.route("/login", methods=["POST"])
def login_process():
    if not User.validate_login(request.form):
        return redirect("/")
    potential_user = User.get_by_email(request.form['email'])
    
    session['user_id'] = potential_user.id

    return redirect("/dashboard")


# Logout
@app.route("/logout")
def clear_session():
    session.clear()
    return redirect("/")