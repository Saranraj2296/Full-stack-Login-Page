# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        dob = request.form['dob']
        password = generate_password_hash(request.form['password'])

        db = get_db_connection()
        cursor = db.cursor()
        try:
            # Check if a user already exists with the same email or mobile
            cursor.execute("SELECT * FROM users WHERE email = %s OR mobile = %s", (email, mobile))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('This email or mobile number is already registered. Please use a different one.', 'danger')
                return redirect(url_for('signup'))

            # If no existing user, insert the new user
            cursor.execute(
                "INSERT INTO users (username, email, mobile, dob, password) VALUES (%s, %s, %s, %s, %s)",
                (username, email, mobile, dob, password)
            )
            db.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.rollback()
            flash('Error occurred: ' + str(e), 'danger')
        finally:
            cursor.close()
            db.close()

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and check_password_hash(user[5], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('user_home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/user_home')
def user_home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template('home.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
