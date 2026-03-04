from flask import render_template, request
from flask_login import login_required
from app.main import bp
from app.models import (
    HealthConcern, Ingredient,
    NutrientIngredient, HealthConcernNutrient,
    Recipe, RecipeIngredient
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
    concern_id = request.form.get('concern_id', type=int)
    ingredient_ids = request.form.getlist('ingredient_ids', type=int)
    concern = HealthConcern.query.get_or_404(concern_id)

    # Find recipes that contain at least one selected ingredient
    matching = RecipeIngredient.query.filter(
        RecipeIngredient.ingredient_id.in_(ingredient_ids)
    ).all()

    # Score recipes by how many selected ingredients they contain
    recipe_scores = {}
    for ri in matching:
        recipe_scores[ri.recipe_id] = recipe_scores.get(ri.recipe_id, 0) + 1

    # Sort by score and take top 3
    top_ids = sorted(recipe_scores, key=recipe_scores.get, reverse=True)[:3]
    recipes = Recipe.query.filter(Recipe.id.in_(top_ids)).all()

    # Sort recipes by score
    recipes = sorted(recipes, key=lambda r: recipe_scores.get(r.id, 0), reverse=True)

    return render_template('main/recipes.html',
                           concern=concern,
                           recipes=recipes,
                           selected_ingredient_ids=ingredient_ids)