from flask import Blueprint, render_template, redirect, request, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from .models import db
from sqlalchemy import text


categories = Blueprint('categories', __name__)

@categories.route('/categories')
def all_categories():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    query = text("SELECT * FROM categories WHERE user_id = :user_id;")
    result = db.session.execute(query, {"user_id": session['user_id']})
    categories = result.fetchall()

    return render_template('categories/categories.html', categories=categories)

@categories.route('/category/<int:category_id>')
def view_category(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    category_query = text("SELECT * FROM categories WHERE id = :category_id AND user_id = :user_id;")
    category_result = db.session.execute(category_query, {"category_id": category_id, "user_id": session['user_id']})
    category = category_result.fetchone()

    if not category:
        flash("You don't have permission to view this category.", category='error')
        return redirect(url_for('categories.all_categories'))

    recipe_query = text("""
        SELECT recipes.* FROM recipes
        JOIN users ON recipes.author_id = users.id
        WHERE recipes.id IN (
            SELECT recipe_id FROM recipes_categories WHERE category_id=:category_id
        ) AND users.id = :user_id;
    """)
    recipe_result = db.session.execute(recipe_query, {"category_id": category_id, "user_id": session['user_id']})
    recipes = recipe_result.fetchall()

    return render_template('categories/view_category.html', category=category, recipes=recipes)

@categories.route('/add_category', methods=['GET', 'POST'])
@categories.route('/add_category/<origin>', methods=['GET', 'POST'])
def add_category(origin=None):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form['name']
        query = text("INSERT INTO categories (name, user_id) VALUES (:name, :user_id);")
        db.session.execute(query, {"name": name, "user_id": session['user_id']})
        db.session.commit()
        flash('Category added successfully!', category='success')
        return redirect(url_for('categories.all_categories'))
    
    return render_template('categories/add_category.html', origin=origin)

@categories.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    remove_associations_query = text("DELETE FROM recipes_categories WHERE category_id = :category_id;")
    db.session.execute(remove_associations_query, {"category_id": category_id})
    db.session.commit()

    delete_query = text("DELETE FROM categories WHERE id = :category_id;")
    db.session.execute(delete_query, {"category_id": category_id})
    db.session.commit()

    flash('Category deleted successfully!', category='success')
    return redirect(url_for('categories.all_categories'))

@categories.route('/recipe/<int:recipe_id>/update_categories', methods=['POST'])
def update_recipe_categories(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    query = text("DELETE FROM recipes_categories WHERE recipe_id=:recipe_id;")
    db.session.execute(query, {"recipe_id": recipe_id})
    db.session.commit() 

    categories = request.form.getlist('categories')
    for category in categories:
        query = text("INSERT INTO recipes_categories (recipe_id, category_id) VALUES (:recipe_id, :category_id);")
        db.session.execute(query, {"recipe_id": recipe_id, "category_id": category})
        db.session.commit()

    flash('Categories updated successfully!', category='success')
    return redirect(url_for('recipes.recipe', recipe_id=recipe_id))

@categories.route('/category/<int:category_id>/add_recipes', methods=['POST'])
def add_recipes_to_category(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    recipes = request.form.getlist('recipes')
    for recipe_id_str in recipes:
        recipe_id = int(recipe_id_str)

        recipe_query = text("SELECT * FROM recipes WHERE id = :recipe_id;")
        recipe_result = db.session.execute(recipe_query, {"recipe_id": recipe_id})
        recipe = recipe_result.fetchone()

        if recipe:
            query = text("INSERT INTO recipes_categories (recipe_id, category_id) VALUES (:recipe_id, :category_id);")
            db.session.execute(query, {"recipe_id": recipe_id, "category_id": category_id})
            db.session.commit()
        else:
            flash(f'Recipe with ID {recipe_id} does not exist and could not be added to the category.', category='error')

    flash('Recipes added to the category successfully!', category='success')
    return redirect(url_for('categories.view_category', category_id=category_id))

@categories.route('/category/<int:category_id>/recipe/<int:recipe_id>/remove', methods=['POST'])
def remove_recipe_from_category(category_id, recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    delete_query = text("DELETE FROM recipes_categories WHERE recipe_id = :recipe_id AND category_id = :category_id;")
    db.session.execute(delete_query, {"recipe_id": recipe_id, "category_id": category_id})
    db.session.commit()

    flash('Recipe removed from category successfully!', category='success')
    return redirect(url_for('categories.view_category', category_id=category_id))

@categories.route('/category/<int:category_id>/add_recipes_form')
def add_recipes_to_category_form(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    all_recipes_query = text("""
        SELECT * FROM recipes
        WHERE author_id = :user_id AND id NOT IN (
            SELECT recipe_id FROM recipes_categories WHERE category_id = :category_id
        );
    """)
    all_recipes_result = db.session.execute(all_recipes_query, {"user_id": session['user_id'], "category_id": category_id})
    all_recipes = all_recipes_result.fetchall()

    return render_template('categories/add_recipes_to_category.html', category_id=category_id, all_recipes=all_recipes)


