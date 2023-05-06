from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from .models import db
from sqlalchemy import text

main = Blueprint('main', __name__)

@main.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    query = text("SELECT * FROM recipes WHERE author_id=:user_id;")
    result = db.session.execute(query, {"user_id": user_id})
    recipes = result.fetchall()
    return render_template('main/home.html', recipes=recipes)

