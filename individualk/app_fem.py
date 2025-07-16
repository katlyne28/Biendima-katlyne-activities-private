from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import config_fem
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = config_fem.SECRET_KEY

def get_db():
    return mysql.connector.connect(
        host=config_fem.DB_HOST,
        user=config_fem.DB_USER,
        password=config_fem.DB_PASSWORD,
        database=config_fem.DB_NAME
    )

@app.route('/')
def index():
    return redirect('/login_fem')

@app.route('/register_fem', methods=['GET', 'POST'])
def register_fem():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        flash('Account successfully created.', 'success')
        return redirect('/login_fem')
    return render_template('auth_register.html')

@app.route('/login_fem', methods=['GET', 'POST'])
def login_fem():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], password_input):
            session['user_id'] = user[0]
            flash('Welcome back!', 'success')
            return redirect('/employee_list_fem')
        flash('Invalid credentials.', 'danger')
    return render_template('auth_login.html')

@app.route('/logout_fem')
def logout_fem():
    session.clear()
    flash('Logged out.', 'info')
    return redirect('/login_fem')

@app.route('/employee_list_fem')
def employee_list_fem():
    if 'user_id' not in session:
        return redirect('/login_fem')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('employee_list.html', employees=employees)

@app.route('/add_employee_fem', methods=['POST'])
def add_employee_fem():
    if 'user_id' not in session:
        return redirect('/login_fem')
    name = request.form['name']
    position = request.form['position']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, position) VALUES (%s, %s)", (name, position))
    conn.commit()
    flash('Employee added.', 'success')
    return redirect('/employee_list_fem')

@app.route('/edit_employee_fem/<int:id>', methods=['GET', 'POST'])
def edit_employee_fem(id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        cursor.execute("UPDATE employees SET name=%s, position=%s WHERE id=%s", (name, position, id))
        conn.commit()
        flash('Employee updated.', 'success')
        return redirect('/employee_list_fem')
    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()
    return render_template('employee_edit.html', employee=employee)

@app.route('/delete_employee_fem/<int:id>')
def delete_employee_fem(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    conn.commit()
    flash('Employee deleted.', 'warning')
    return redirect('/employee_list_fem')

if __name__ == '__main__':
    app.run(debug=True)
