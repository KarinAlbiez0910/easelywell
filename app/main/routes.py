from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models import (
    HealthConcern, Ingredient,
    NutrientIngredient, HealthConcernNutrient,
    Recipe, RecipeIngredient,
    UserFavouriteRecipe
)

@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/concerns')
@login_required
def concerns():
    concerns = HealthConcern.query.all()
    return render_template('main/concerns.html', concerns=concerns)


@bp.route('/ingredients/<int:concern_id>')
@login_required
def ingredients(concern_id):
    concern = HealthConcern.query.get_or_404(concern_id)
    # Get nutrients linked to this concern
    concern_nutrients = HealthConcernNutrient.query.filter_by(health_concern_id=concern_id).all()
    nutrient_ids = [cn.nutrient_id for cn in concern_nutrients]
    # Get ingredients linked to those nutrients
    ingredient_links = NutrientIngredient.query.filter(
        NutrientIngredient.nutrient_id.in_(nutrient_ids)
    ).all()
    ingredient_ids = list(set([il.ingredient_id for il in ingredient_links]))
    ingredients = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
    return render_template('main/ingredients.html', concern=concern, ingredients=ingredients)


@bp.route('/recipes', methods=['POST'])
@login_required
def recipes():
    from app.models import UserFavouriteRecipe
    concern_id = request.form.get('concern_id', type=int)
    ingredient_ids = request.form.getlist('ingredient_ids', type=int)
    concern = HealthConcern.query.get_or_404(concern_id)

    matching = RecipeIngredient.query.filter(
        RecipeIngredient.ingredient_id.in_(ingredient_ids)
    ).all()

    recipe_scores = {}
    for ri in matching:
        recipe_scores[ri.recipe_id] = recipe_scores.get(ri.recipe_id, 0) + 1

    top_ids = sorted(recipe_scores, key=recipe_scores.get, reverse=True)[:3]
    recipes = Recipe.query.filter(Recipe.id.in_(top_ids)).all()
    recipes = sorted(recipes, key=lambda r: recipe_scores.get(r.id, 0), reverse=True)

    # Get user's saved recipe IDs
    saved = UserFavouriteRecipe.query.filter_by(user_id=current_user.id).all()
    saved_recipe_ids = [f.recipe_id for f in saved]

    return render_template('main/recipes.html',
                           concern=concern,
                           recipes=recipes,
                           selected_ingredient_ids=ingredient_ids,
                           saved_recipe_ids=saved_recipe_ids)

@bp.route('/favourite/<int:recipe_id>', methods=['POST'])
@login_required
def toggle_favourite(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    existing = UserFavouriteRecipe.query.filter_by(
        user_id=current_user.id,
        recipe_id=recipe_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f'"{recipe.name}" removed from favourites.', 'info')
    else:
        fav = UserFavouriteRecipe(user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(fav)
        db.session.commit()
        flash(f'"{recipe.name}" saved to favourites! 🌿', 'success')

    return redirect(url_for('main.index'))