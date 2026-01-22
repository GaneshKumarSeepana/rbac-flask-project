from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

# import DB credentials from local config (NOT pushed to GitHub)
from db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)
app.secret_key = "rbac_secret_key"  # for session handling

# ---------------------------
# Database Connection
# ---------------------------
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = db.cursor()

# ---------------------------
# Login Page
# ---------------------------
@app.route('/')
def login():
    return render_template('login.html')

# ---------------------------
# Login Logic
# ---------------------------
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    user_query = """
        SELECT users.user_id, users.username, roles.role_name, roles.role_id
        FROM users
        JOIN roles ON users.role_id = roles.role_id
        WHERE users.username = %s AND users.password = %s
    """

    cursor.execute(user_query, (username, password))
    user = cursor.fetchone()

    if not user:
        return "Invalid username or password"

    user_id, username, role_name, role_id = user

    permission_query = """
        SELECT permissions.permission_name
        FROM role_permissions
        JOIN permissions ON role_permissions.permission_id = permissions.permission_id
        WHERE role_permissions.role_id = %s
    """

    cursor.execute(permission_query, (role_id,))
    permissions = [p[0] for p in cursor.fetchall()]

    session['username'] = username
    session['role'] = role_name
    session['permissions'] = permissions

    return redirect(url_for('dashboard'))

# ---------------------------
# Dashboard Router
# ---------------------------
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

# ---------------------------
# Logout
# ---------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------------------
# Run App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
