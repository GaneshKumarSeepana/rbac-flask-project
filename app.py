from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "rbac_secret_key"

# -----------------------------
# LOCAL MySQL CONNECTION
# -----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gunman",   # your local MySQL password
    database="rbac_db"   # your existing database
)

cursor = db.cursor(dictionary=True)

# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route('/')
def login():
    return render_template('login.html')

# -----------------------------
# LOGIN LOGIC
# -----------------------------
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    user_query = """
    SELECT u.username, r.role_name, r.role_id
    FROM users u
    JOIN roles r ON u.role_id = r.role_id
    WHERE u.username = %s AND u.password = %s
    """
    cursor.execute(user_query, (username, password))
    user = cursor.fetchone()

    if not user:
        return "Invalid username or password"

    role_id = user['role_id']

    permission_query = """
    SELECT p.permission_name
    FROM role_permissions rp
    JOIN permissions p ON rp.permission_id = p.permission_id
    WHERE rp.role_id = %s
    """
    cursor.execute(permission_query, (role_id,))
    permissions = [p['permission_name'] for p in cursor.fetchall()]

    session['username'] = user['username']
    session['role'] = user['role_name']
    session['permissions'] = permissions

    return redirect(url_for('dashboard'))

# -----------------------------
# DASHBOARD ROUTER
# -----------------------------
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    role = session['role']

    if role == 'Admin':
        return render_template(
            'admin_dashboard.html',
            username=session['username'],
            permissions=session['permissions']
        )

    elif role == 'Manager':
        return render_template(
            'manager_dashboard.html',
            username=session['username'],
            permissions=session['permissions']
        )

    else:
        return render_template(
            'user_dashboard.html',
            username=session['username'],
            permissions=session['permissions']
        )

# -----------------------------
# LOGOUT
# -----------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -----------------------------
# RUN LOCALLY
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
