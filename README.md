<h1>Role-Based Database Access Control Manager</h1>

<hr>

<h2>📌 Project Overview</h2>
<p>
The <b>Role-Based Database Access Control Manager</b> is a web-based application
developed using <b>Flask</b> and <b>MySQL</b>.
It demonstrates <b>Role-Based Access Control (RBAC)</b>, where users are granted
permissions based on their assigned roles.
</p>

<hr>

<h2>🎯 Objectives</h2>
<ul>
  <li>Implement Role-Based Access Control (RBAC)</li>
  <li>Authenticate users using MySQL database</li>
  <li>Restrict access based on user roles</li>
  <li>Demonstrate secure database interaction</li>
</ul>

<hr>

<h2>🛠️ Technologies Used</h2>
<ul>
  <li>Python</li>
  <li>Flask Framework</li>
  <li>MySQL (MySQL Workbench)</li>
  <li>HTML & CSS</li>
  <li>Git & GitHub</li>
</ul>

<hr>

<h2>🧑‍💻 User Roles and Permissions</h2>
<table border="1" cellpadding="8" cellspacing="0">
  <tr>
    <th>Role</th>
    <th>Permissions</th>
  </tr>
  <tr>
    <td>Admin</td>
    <td>Read, Write, Delete</td>
  </tr>
  <tr>
    <td>Manager</td>
    <td>Read, Write</td>
  </tr>
  <tr>
    <td>User</td>
    <td>Read</td>
  </tr>
</table>

<hr>

<h2>🗂️ Project Structure</h2>
<pre>
RBAC_Database_Project/
│
├── app.py
├── db_config.py   (ignored in GitHub)
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── manager_dashboard.html
│   └── user_dashboard.html
│
└── venv/
</pre>

<hr>

<h2>🔐 Security Features</h2>
<ul>
  <li>Database credentials stored locally</li>
  <li>Sensitive files excluded using <code>.gitignore</code></li>
  <li>Session-based authentication</li>
  <li>Role-based authorization</li>
</ul>

<hr>

<h2>⚙️ Database Design</h2>
<p>The database contains the following tables:</p>
<ul>
  <li>users</li>
  <li>roles</li>
  <li>permissions</li>
  <li>role_permissions</li>
</ul>

<hr>

<h2>▶️ How to Run the Project (Local)</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.x</li>
  <li>MySQL Server</li>
  <li>MySQL Workbench</li>
</ul>

<h3>Steps</h3>
<ol>
  <li>Install dependencies:
    <pre>pip install -r requirements.txt</pre>
  </li>
  <li>Create database <b>rbac_db</b> in MySQL Workbench</li>
  <li>Create required tables and insert sample data</li>
  <li>Run the application:
    <pre>python app.py</pre>
  </li>
  <li>Open browser:
    <pre>http://127.0.0.1:5000</pre>
  </li>
</ol>

<hr>

<h2>📌 Notes</h2>
<ul>
  <li>This project is for <b>academic purposes</b></li>
  <li>Database is maintained locally using MySQL Workbench</li>
  <li>Cloud deployment is not required</li>
</ul>

<hr>

<h2>🎓 Academic Relevance</h2>
<p>
This project demonstrates authentication, authorization,
Role-Based Access Control (RBAC), and secure database access
using Flask and MySQL.
</p>

<hr>

<h2>👤 Author</h2>
<p><b>Ganesh Kumar Seepana</b></p>

<hr>

<h2>📜 License</h2>
<p>Educational use only.</p>
