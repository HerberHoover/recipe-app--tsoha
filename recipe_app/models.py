from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def create_tables(app):
    with app.app_context():
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            );
        """))

        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS recipes (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                instructions TEXT NOT NULL,
                total_time INT NOT NULL,
                author_id INTEGER REFERENCES users(id)
            );
        """))

        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id SERIAL PRIMARY KEY,
                recipe_id INTEGER NOT NULL,
                ingredient VARCHAR(255) NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id)
            );
        """))

        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE
            );
        """))

        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS recipes_categories (
                id SERIAL PRIMARY KEY,
                recipe_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            );
        """))

        db.session.commit()