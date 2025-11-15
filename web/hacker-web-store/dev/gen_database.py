from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy import text
import os, secrets

db = SQLAlchemy()
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
os.system(f'rm {os.path.join(basedir, "db.sqlite")}')
app.config['SECRET_KEY'] = secrets.token_urlsafe(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)

class Products(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	price = db.Column(db.Integer)
	desc = db.Column(db.Text)


with app.app_context():
    db.create_all()
    product_laptop = Products(name='Desktop Computer', price=1800, desc='Beautiful, sleek, desktop computer built for you by some starving bug bounty hunters to aid you on your hacking endeavors.')
    product_desktop = Products(name='Laptop', price=1200, desc='A boring laptop on Amazon that probably has terrible RAM and an old motherboard... but hey! It is cheap.')
    product_hoodie = Products(name='Hacker Hoodie', price=40, desc='The most important item in any hacker\'s wardrobe.')
    product_energy = Products(name='Coffee', price=7, desc='At this point, my blood has more caffine than oxygen.')
    db.session.add(product_laptop)
    db.session.add(product_desktop)
    db.session.add(product_hoodie)
    db.session.add(product_energy)
    user_joram = Users(name='Joram', password=generate_password_hash('possiblebutidbeimpressed', method='pbkdf2:sha256'))
    user_james = Users(name='James', password=generate_password_hash('ifyagetthisoneithinkthesourcecodegotleaked', method='pbkdf2:sha256'))
    user_admin = Users(name='website_admin_account', password=generate_password_hash('ntadmin1234', method='pbkdf2:sha256'))
    db.session.add(user_joram)
    db.session.add(user_james)
    db.session.add(user_admin)
    db.session.commit()
