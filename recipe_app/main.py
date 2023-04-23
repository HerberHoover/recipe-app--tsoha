from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from .models import db
from sqlalchemy import text

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    query = text("SELECT * FROM recipes WHERE author_id=:user_id;")
    result = db.session.execute(query, {"user_id": user_id})
    recipes = result.fetchall()
    return render_template('main/home.html', recipes=recipes)


@main.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
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
        return redirect(url_for('main.recipe', recipe_id=recipe_id))

    return render_template('main/add_recipe.html')



@main.route('/recipe/<int:recipe_id>')
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
            SELECT category_id FROM recipes_categories WHERE recipe_id = :recipe_id
        );
    """)
    related_categories_result = db.session.execute(related_categories_query, {"recipe_id": recipe_id})
    related_categories = related_categories_result.fetchall()

    return render_template('main/recipe.html', recipe=recipe, ingredients=ingredients, related_categories=related_categories)


@main.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
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
        return redirect(url_for('main.recipe', recipe_id=recipe_id))


    query = text("SELECT * FROM recipes WHERE id=:recipe_id;")
    result = db.session.execute(query, {"recipe_id": recipe_id})
    recipe = result.fetchone()
    return render_template('main/edit_recipe.html', recipe=recipe)


@main.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
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
    return redirect(url_for('main.home'))


@main.route('/categories')
def categories():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    query = text("SELECT * FROM categories WHERE user_id = :user_id;")
    result = db.session.execute(query, {"user_id": session['user_id']})
    categories = result.fetchall()

    return render_template('main/categories.html', categories=categories)

@main.route('/category/<int:category_id>')
def view_category(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    category_query = text("SELECT * FROM categories WHERE id = :category_id AND user_id = :user_id;")
    category_result = db.session.execute(category_query, {"category_id": category_id, "user_id": session['user_id']})
    category = category_result.fetchone()

    if not category:
        flash("You don't have permission to view this category.", category='error')
        return redirect(url_for('main.categories'))

    recipe_query = text("""
        SELECT recipes.* FROM recipes
        JOIN users ON recipes.author_id = users.id
        WHERE recipes.id IN (
            SELECT recipe_id FROM recipes_categories WHERE category_id=:category_id
        ) AND users.id = :user_id;
    """)
    recipe_result = db.session.execute(recipe_query, {"category_id": category_id, "user_id": session['user_id']})
    recipes = recipe_result.fetchall()

    return render_template('main/view_category.html', category=category, recipes=recipes)


@main.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form['name']
        query = text("INSERT INTO categories (name, user_id) VALUES (:name, :user_id);")
        db.session.execute(query, {"name": name, "user_id": session['user_id']})
        db.session.commit()
        flash('Category added successfully!', category='success')
        return redirect(url_for('main.categories'))
    
    return render_template('main/add_category.html')


@main.route('/recipe/<int:recipe_id>/update_categories', methods=['POST'])
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
    return redirect(url_for('main.recipe', recipe_id=recipe_id))


@main.route('/category/<int:category_id>/add_recipes', methods=['POST'])
def add_recipes_to_category(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

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
    return redirect(url_for('main.view_category', category_id=category_id))


@main.route('/category/<int:category_id>/add_recipes_form')
def add_recipes_to_category_form(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    all_recipes_query = text("SELECT * FROM recipes WHERE author_id = :user_id;")
    all_recipes_result = db.session.execute(all_recipes_query, {"user_id": session['user_id']})
    all_recipes = all_recipes_result.fetchall()

    return render_template('main/add_recipes_to_category.html', category_id=category_id, all_recipes=all_recipes)


@main.route('/recipe/<int:recipe_id>/add_ingredient', methods=['GET', 'POST'])
def add_ingredient(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        ingredient = request.form['ingredient']
        amount = int(request.form['amount'])
        unit = request.form['unit']

        query = text("INSERT INTO ingredients (recipe_id, ingredient, amount, unit) VALUES (:recipe_id, :ingredient, :amount, :unit)")
        db.session.execute(query, {"recipe_id": recipe_id, "ingredient": ingredient, "amount": amount, "unit": unit})
        db.session.commit()

        return redirect(url_for('main.recipe', recipe_id=recipe_id))

    query = text("SELECT * FROM recipes WHERE id=:recipe_id;")
    result = db.session.execute(query, {"recipe_id": recipe_id})
    recipe = result.fetchone()

    return render_template('main/add_ingredient.html', recipe=recipe)


@main.route('/ingredient/<int:ingredient_id>/delete', methods=['POST'])
def delete_ingredient(ingredient_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    query = text("SELECT recipe_id FROM ingredients WHERE id=:ingredient_id;")
    result = db.session.execute(query, {"ingredient_id": ingredient_id})
    recipe_id = result.fetchone()[0]

    query = text("DELETE FROM ingredients WHERE id=:ingredient_id;")
    db.session.execute(query, {"ingredient_id": ingredient_id})
    db.session.commit()

    flash('Ingredient deleted successfully!', category='success')
    return redirect(url_for('main.recipe', recipe_id=recipe_id))




#### fast debug
@main.route('/debug_recipe_ids')
def debug_recipe_ids():
    query = text("SELECT id FROM recipes;")
    result = db.session.execute(query)
    recipe_ids = [row[0] for row in result.fetchall()]
    return str(recipe_ids)

@main.route('/debug_recipe_7')
def debug_recipe_15():
    query = text("SELECT * FROM recipes WHERE id = 7;")
    result = db.session.execute(query)
    recipe_data = result.fetchall()
    return str(recipe_data)

