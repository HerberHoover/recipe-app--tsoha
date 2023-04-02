# Recipe Application


RecipeApp is a web application that allows users to manage their favorite recipes. Users can create, view, update, and delete recipes. They can also search for recipes based on various criteria.

## Main Features

- User registration and authentication
- Create, read, update, and delete operations for recipes
- Search for recipes by name, ingredients, or other criteria
- View individual recipe detail

## Prerequisites

- Python 3.x
- PostgreSQL

## Setting up the virtual environment

1. Create and activate virtual environment:

- python3 -m venv venv
- source venv/bin/activate


2. Install dependencies

- pip install flask
- pip install Flask-SQLAlchemy
- pip install python-dotenv
- pip install psycopg2-binary

3. Setup PostgreSQL

- sudo apt-get install postgresql postgresql-contrib
- sudo -i -u postgres
- createdb recipe_app_db

3. Create .env file to project root

- SECRET_KEY=<your_secret_key>
- SQLALCHEMY_DATABASE_URI=<your_database_uri>

4. Run application

python run.py


PS
"Registered late, but hoping to still join the course."

