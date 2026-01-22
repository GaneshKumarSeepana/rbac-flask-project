from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "rbac_secret_key"

# ================= DATABASE CONNECTION =================
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 3306))
)

cursor = db.cursor(dictionary=True)

# ================= LOGIN PAGE =================
@app.route('/')
def login():
    return render_template('login.html')

# ================= LOGIN ACTION =================
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    user_query = """
    SELECT users.username, roles.role_name, roles.role_id
    FROM users
    JOIN roles ON users.role_id = roles.role_id
    WHERE users.username=%s AND users.password=%s
    """
    cursor.execute(user_query, (username, password))
    user = cursor.fetchone()

    if not user:
        return "Invalid username or password"

    role_id = user['role_id']

    permission_query = """
    SELECT permissions.permission_name
    FROM permissions
    JOIN role_permissions
    ON permissions.permission_id = role_permissions.permission_id
    WHERE role_permissions.role_id = %s
    """
    cursor.execute(permission_query, (role_id,))
    permissions = [p['permission_name'] for p in cursor.fetchall()]

    session['username'] = user['username']
    session['role'] = user['role_name']
    session['permissions'] = permissions

    return redirect(url_for('dashboard'))

# ================= DASHBOARD =================
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

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ================= HEALTH CHECK (FOR RENDER) =================
@app.route('/healthz')
def healthz():
    return "OK", 200

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
