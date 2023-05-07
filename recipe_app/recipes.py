from flask import Blueprint, render_template, redirect, request, url_for, flash, session, abort
from .models import db
from sqlalchemy import text

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipes')
def all_recipes():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    query = text("SELECT * FROM recipes WHERE author_id=:user_id;")
    result = db.session.execute(query, {"user_id": user_id})
    recipes = result.fetchall()
    return render_template('recipes/all_recipes.html', recipes=recipes)

@recipes.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        total_time = int(request.form['total_time'])
        author_id = session['user_id']

        query = text("""
        INSERT INTO recipes (name, description, instructions, total_time, author_id) 
        VALUES (:name, :description, :instructions, :total_time, :author_id) RETURNING id;
        """)

        result = db.session.execute(query, {"name": name, "description": description, "instructions": instructions, "total_time": total_time, "author_id": author_id})
        recipe_id = int(result.fetchone()[0])

        db.session.commit()
        flash('Recipe added successfully!', category='success')
        return redirect(url_for('recipes.recipe', recipe_id=recipe_id))

    return render_template('recipes/add_recipe.html')

@recipes.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    query = text("SELECT * FROM recipes WHERE id=:recipe_id;")
    result = db.session.execute(query, {"recipe_id": recipe_id})
    recipe = result.fetchone()

    ingredients_query = text("""
        SELECT * FROM ingredients WHERE recipe_id=:recipe_id;
    """)
    ingredients_result = db.session.execute(ingredients_query, {"recipe_id": recipe_id})
    ingredients = ingredients_result.fetchall()

    related_categories_query = text("""
        SELECT * FROM categories WHERE id IN (
        SELECT category_id FROM recipes_categories WHERE recipe_id = :recipe_id );
    """)
    related_categories_result = db.session.execute(related_categories_query, {"recipe_id": recipe_id})
    related_categories = related_categories_result.fetchall()

    return render_template('recipes/recipe.html', recipe=recipe, ingredients=ingredients, related_categories=related_categories)

@recipes.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        total_time = request.form['total_time']
        query = text("""
        UPDATE recipes SET name=:name, description=:description, instructions=:instructions, total_time=:total_time WHERE id=:recipe_id;
        """)
        db.session.execute(query, {"name": name, "description": description, "instructions": instructions, "total_time": total_time, "recipe_id": recipe_id})
        db.session.commit()
        flash('Recipe updated successfully!', category='success')
        return redirect(url_for('recipes.recipe', recipe_id=recipe_id))

    query = text("SELECT * FROM recipes WHERE id=:recipe_id;")
    result = db.session.execute(query, {"recipe_id": recipe_id})
    recipe = result.fetchone()
    return render_template('recipes/edit_recipe.html', recipe=recipe)

@recipes.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    delete_ingredients_query = text("DELETE FROM ingredients WHERE recipe_id=:recipe_id;")
    db.session.execute(delete_ingredients_query, {"recipe_id": recipe_id})

    delete_categories_query = text("DELETE FROM recipes_categories WHERE recipe_id=:recipe_id;")
    db.session.execute(delete_categories_query, {"recipe_id": recipe_id})

    delete_recipe_categories_query = text("DELETE FROM recipes_categories WHERE recipe_id=:recipe_id;")
    db.session.execute(delete_recipe_categories_query, {"recipe_id": recipe_id})
    
    delete_recipe_query = text("DELETE FROM recipes WHERE id=:recipe_id;")
    db.session.execute(delete_recipe_query, {"recipe_id": recipe_id})
    
    db.session.commit()
    flash('Recipe deleted successfully!', category='success')
    return redirect(url_for('recipes.all_recipes'))
