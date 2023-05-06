from flask import Blueprint, render_template, redirect, request, url_for, flash, session, abort
from .models import db
from sqlalchemy import text


ingredients = Blueprint('ingredients', __name__)


@ingredients.route('/recipe/<int:recipe_id>/add_ingredient', methods=['GET', 'POST'])
def add_ingredient(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        ingredient = request.form['ingredient']
        amount = int(request.form['amount'])
        unit = request.form['unit']

        query = text("INSERT INTO ingredients (recipe_id, ingredient, amount, unit) VALUES (:recipe_id, :ingredient, :amount, :unit)")
        db.session.execute(query, {"recipe_id": recipe_id, "ingredient": ingredient, "amount": amount, "unit": unit})
        db.session.commit()

        return redirect(url_for('recipes.recipe', recipe_id=recipe_id))


@ingredients.route('/ingredient/<int:ingredient_id>/delete', methods=['POST'])
def delete_ingredient(ingredient_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    query = text("SELECT recipe_id FROM ingredients WHERE id=:ingredient_id;")
    result = db.session.execute(query, {"ingredient_id": ingredient_id})
    recipe_id = result.fetchone()[0]

    query = text("DELETE FROM ingredients WHERE id=:ingredient_id;")
    db.session.execute(query, {"ingredient_id": ingredient_id})
    db.session.commit()

    flash('Ingredient deleted successfully!', category='success')
    return redirect(url_for('recipes.recipe', recipe_id=recipe_id))
