from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, UserMixin
from werkzeug.security import check_password_hash
from sqlalchemy import text
import os, secrets, sqlite3
import threading, time

# Initialize SQLAlchemy instance and flask app
db = SQLAlchemy()
app = Flask(__name__)

# Define User class for SQLAlchemy (centralized database used for authentication and copied to user sessions)
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)

# Main page that shows the product listing
@app.route('/')
def index():
	
	# Get products from the database
	try:
		con = sqlite3.connect(session['db_path'])
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		res = cur.execute("SELECT * from Products")
		products = [dict(row) for row in res.fetchall()]
		con.close()
	except sqlite3.Error as er:
		flash("Unexpected error... try closing and reopening your browser.")

	return render_template('index.html', products=products)

# Create page where users can create a new product
@app.route('/create/', methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
		name = request.form['name']
		price = request.form['price']
		desc = request.form['desc']

		# Correct, never do this in real life.
		query_string = f"INSERT INTO Products (name, price, desc) VALUES ('{name}', '{price}', '{desc}');"
		
		# Conencts to individual user instance database
		try:
			con = sqlite3.connect(session['db_path'])
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			res = cur.execute(query_string)
			con.commit()
			con.close()
			flash("Success! Added new product to database.")
		except sqlite3.Error as er:
			flash(f"Error in Statement: {query_string}")
			flash(str(er))
			con.close()
			return redirect(url_for('index'))
		return redirect(url_for('index'))
	return render_template('create.html')

# Authentication Page to get the flag
@app.route('/login')
def login():
    return render_template('login.html')

# This authentication uses proper authentication (not intentionally vulnerable)
@app.route('/login', methods=['POST'])
def login_post():
	name = request.form.get('name')
	password = request.form.get('password')
	
	debug_flag = request.form.get('DEV_ONLY_debug_mode')
	if not debug_flag == None:
		if 'on' in debug_flag:
			src_ip = request.headers.get('X-Forwarded-For')
			if(not src_ip is None):
				if(not src_ip == '127.0.0.1'):
					flash('Debug mode only available for loopback interface.')
				else:
					flash('Debug Mode:')
					flash(f"SELECT * FROM Users WHERE name = '{name}' AND password = '{password}' LIMIT 1;")
					flash('NOTE: This feature is depreciated. Prepared statements are now used for authentication requests.')
			else:
				flash('Debug mode only available for loopback interface.')

	user = Users.query.filter_by(name=name).first()
	#print(f'Looking for a user... and that user is: {user}')

	if not user or not check_password_hash(user.password, password) or user.name != 'website_admin_account':
		# Password authentication failed
		return redirect(url_for('login'))
	login_user(user)
	return redirect(url_for('admin'))

@app.route('/admin')
@login_required
def admin():
    contents = open('flag.txt', 'r').read()
    return contents

@app.before_request
def before_request():
	if(session.get('token') and session.get('db_path')):
		# As far as flask knows, this is an established session. Now, check if the custom DB is still around.
		if(not os.path.isfile(session['db_path'])):
			# Flask thinks the DB exists but it was deleted after 30 minutes. Recreate from template and restart the clock...
			os.system(f"cp {os.path.join(basedir, 'db.sqlite')} {session['db_path']}")
			thread = threading.Thread(target=clean_db, args=(session['db_path'],))
			thread.start()

	else:
		#print('New Session, making custom session token...')
		session['token'] = secrets.token_hex(6)
		#print(f"New session token is: {session['token']}")
		session['db_path'] = os.path.join(app.config['DATABASE_DIR'], session['token'] + '_db.sqlite')
		#print(f"New DB session path is: {session['db_path']}. Copying base database to session database...")
		os.system(f"cp {os.path.join(basedir, 'db.sqlite')} {session['db_path']}")
		thread = threading.Thread(target=clean_db, args=(session['db_path'],))
		thread.start()
		
def clean_db(db_path):
	time.sleep(1800)
	os.system(f"rm -f {db_path}")
		

if __name__ == '__main__':
	basedir = os.path.abspath(os.path.dirname(__file__))
	app.config['SECRET_KEY'] = secrets.token_urlsafe(12)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
	app.config['DATABASE_DIR'] = os.path.join(basedir, 'session_databases')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	login_manager = LoginManager()
	login_manager.login_view = 'login'
	login_manager.init_app(app)

	# Used by flask's black magic for user management for login page. Don't ask questions if you don't really want to know.
	@login_manager.user_loader
	def load_user(id):
		#print('Loaded a user... I think?')
		return Users.query.get(int(id))

	app.run(debug=False, host='0.0.0.0', port=5000)