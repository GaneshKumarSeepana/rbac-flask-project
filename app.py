from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "rbac_secret_key"

# -------------------------------------------------
# MySQL Database Connection
# Uses ENV vars for hosting
# Falls back to local MySQL for development
# -------------------------------------------------
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),   # forces TCP/IP (fixes named pipe error)
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "gunman"),
    database=os.getenv("DB_NAME", "rbac_db")
)

cursor = db.cursor(dictionary=True)

# -------------------------------------------------
# Login Page
# -------------------------------------------------
@app.route('/')
def login():
    return render_template('login.html')

# -------------------------------------------------
# Login Authentication
# -------------------------------------------------
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
        return render_template('login.html', error="Invalid username or password")

    role_id = user['role_id']
    role_name = user['role_name']

    permission_query = """
    SELECT permissions.permission_name
    FROM role_permissions
    JOIN permissions
    ON role_permissions.permission_id = permissions.permission_id
    WHERE role_permissions.role_id = %s
    """
    cursor.execute(permission_query, (role_id,))
    permissions = [p['permission_name'] for p in cursor.fetchall()]

    session['username'] = username
    session['role'] = role_name
    session['permissions'] = permissions

    return redirect(url_for('dashboard'))

# -------------------------------------------------
# Dashboard Router
# -------------------------------------------------
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

# -------------------------------------------------
# Permission Protected Route (DELETE)
# -------------------------------------------------
@app.route('/delete-data')
def delete_data():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'DELETE' not in session['permissions']:
        return "Access Denied: You do not have DELETE permission"

    return "Data deleted successfully (Demo)"

# -------------------------------------------------
# Logout
# -------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------------------------------------
# Run Application
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
