from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from .models import db
from sqlalchemy import text

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  #// fix this
    query = text("SELECT * FROM recipes;")
    result = db.session.execute(query)
    recipes = result.fetchall()
    return render_template('main/home.html', recipes=recipes)

# continue with the rest of the routes