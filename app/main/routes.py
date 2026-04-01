
import requests
import json
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models import (
    HealthConcern, Ingredient,
    NutrientIngredient, HealthConcernNutrient,
    Recipe, RecipeIngredient,
    UserFavouriteRecipe
)
N8N_WEBHOOK_URL = "https://ai-software-egnineering.app.n8n.cloud/webhook/easelywell-classifier"
_nutrient_explanation_cache = {}

def track_event(event_type, concern_id=None, recipe_id=None, meta=None):
    from app.models import Event
    try:
        event = Event(
            event_type=event_type,
            user_id=current_user.id if current_user.is_authenticated else None,
            concern_id=concern_id,
            recipe_id=recipe_id,
            meta=meta
        )
        db.session.add(event)
        db.session.commit()
    except Exception:
        db.session.rollback()


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
    concern_nutrients = HealthConcernNutrient.query.filter_by(health_concern_id=concern_id).all()
    nutrient_ids = [cn.nutrient_id for cn in concern_nutrients]
    ingredient_links = NutrientIngredient.query.filter(
        NutrientIngredient.nutrient_id.in_(nutrient_ids)
    ).all()
    ingredient_ids = list(set([il.ingredient_id for il in ingredient_links]))

    # Base query
    query = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids))

    # Filter by dietary preference
    preference = current_user.dietary_preference
    print(f"DEBUG preference='{preference}'")

    if preference == 'Vegan':
        query = query.filter(Ingredient.is_vegan == True)
    elif preference == 'Vegetarian':
        query = query.filter(Ingredient.is_vegetarian == True)
    elif preference == 'Pescatarian':
        query = query.filter(
            db.or_(
                Ingredient.is_vegetarian == True,
                Ingredient.type == 'fish'
            )
        )
    elif preference == 'Gluten-free':
        query = query.filter(Ingredient.is_gluten_free == True)
    elif preference == 'Dairy-free':
        query = query.filter(Ingredient.is_dairy_free == True)
    elif preference == 'Nut-free':
        query = query.filter(Ingredient.is_nut_free == True)
    elif preference == 'Egg-free':
        query = query.filter(Ingredient.is_egg_free == True)
    elif preference == 'Low sugar':
        query = query.filter(Ingredient.is_low_sugar == True)
    elif preference == 'High protein':
        query = query.filter(Ingredient.is_high_protein == True)
    elif preference == 'Mediterranean':
        query = query.filter(Ingredient.is_mediterranean == True)
    # Flexitarian, No restrictions, and everything else → show all

    ingredients = query.all()
    track_event('concern_selected', concern_id=concern_id)

    return render_template('main/ingredients.html',
                           concern=concern,
                           ingredients=ingredients,
                           dietary_preference=preference)


@bp.route('/recipes', methods=['POST'])
@login_required
def recipes():
    from app.models import UserFavouriteRecipe, Feedback
    concern_id = request.form.get('concern_id', type=int)
    ingredient_ids = request.form.getlist('ingredient_ids', type=int)
    concern = HealthConcern.query.get_or_404(concern_id)

    matching = RecipeIngredient.query.filter(
        RecipeIngredient.ingredient_id.in_(ingredient_ids)
    ).all()

    recipe_scores = {}
    for ri in matching:
        recipe_scores[ri.recipe_id] = recipe_scores.get(ri.recipe_id, 0) + 1

    cooking_device = current_user.cooking_device or 'Standard'
    device_recipe_ids = {
        r.id for r in Recipe.query.filter_by(cooking_device=cooking_device).all()
    }
    device_scores = {
        rid: score for rid, score in recipe_scores.items()
        if rid in device_recipe_ids
    }
    top_ids = sorted(device_scores, key=device_scores.get, reverse=True)[:3]
    query = Recipe.query.filter(Recipe.id.in_(top_ids))

    preference = current_user.dietary_preference
    if preference == 'Vegan':
        query = query.filter(Recipe.is_vegan == True)
    elif preference == 'Vegetarian':
        query = query.filter(Recipe.is_vegetarian == True)
    elif preference == 'Pescatarian':
        query = query.filter(
            db.or_(
                Recipe.is_vegetarian == True,
                Recipe.is_vegan == True
            )
        )
        fish_recipes = db.session.query(Recipe.id).join(
            RecipeIngredient
        ).join(Ingredient).filter(
            Ingredient.type == 'fish',
            Recipe.id.in_(top_ids)
        ).all()
        fish_recipe_ids = [r.id for r in fish_recipes]
        if fish_recipe_ids:
            query = Recipe.query.filter(
                db.or_(
                    db.and_(Recipe.id.in_(top_ids), Recipe.is_vegetarian == True),
                    Recipe.id.in_(fish_recipe_ids)
                )
            )
    elif preference == 'Gluten-free':
        query = query.filter(Recipe.is_gluten_free == True)
    elif preference == 'Dairy-free':
        query = query.filter(Recipe.is_dairy_free == True)
    elif preference == 'Nut-free':
        query = query.filter(Recipe.is_nut_free == True)
    elif preference == 'Egg-free':
        query = query.filter(Recipe.is_egg_free == True)
    elif preference == 'Low sugar':
        query = query.filter(Recipe.is_low_sugar == True)
    elif preference == 'High protein':
        query = query.filter(Recipe.is_high_protein == True)
    elif preference == 'Mediterranean':
        query = query.filter(Recipe.is_mediterranean == True)

    recipes = query.all()
    recipes = sorted(recipes, key=lambda r: recipe_scores.get(r.id, 0), reverse=True)

    saved = UserFavouriteRecipe.query.filter_by(user_id=current_user.id).all()
    saved_recipe_ids = [f.recipe_id for f in saved]

    # Check if user already gave feedback for this concern
    feedback_given_ids = [f.recipe_id for f in Feedback.query.filter_by(
    user_id=current_user.id
    ).all()]

    for recipe in recipes:
        track_event('recipe_viewed', concern_id=concern_id, recipe_id=recipe.id)

    return render_template('main/recipes.html',
                       concern=concern,
                       recipes=recipes,
                       selected_ingredient_ids=ingredient_ids,
                       saved_recipe_ids=saved_recipe_ids,
                       feedback_given_ids=feedback_given_ids)


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

    return redirect(url_for('auth.profile'))

@bp.route('/feedback/<int:recipe_id>', methods=['POST'])
@login_required
def feedback(recipe_id):
    from app.models import Feedback
    rating = request.form.get('rating')
    comment = request.form.get('comment', '').strip()

    if rating in ['yes', 'somewhat', 'no']:
        existing = Feedback.query.filter_by(
            user_id=current_user.id,
            recipe_id=recipe_id
        ).first()
        if not existing:
            fb = Feedback(
                user_id=current_user.id,
                recipe_id=recipe_id,
                rating=rating,
                comment=comment or None
            )
            db.session.add(fb)
            db.session.commit()
            track_event('feedback_submitted',
                       recipe_id=recipe_id,
                       meta=rating)
        flash('Thank you for your feedback! 🌿', 'success')

    return redirect(url_for('main.concerns'))
@bp.route('/analytics')
@login_required
def analytics():
    from app.models import Event, Feedback
    from sqlalchemy import func

    # Total users
    from app.models import User
    total_users = User.query.count()

    # Total concerns selected
    total_concerns = Event.query.filter_by(event_type='concern_selected').count()

    # Total feedback
    total_feedback = Feedback.query.count()

    # Top concerns
    top_concerns = db.session.query(
        HealthConcern,
        func.count(Event.id).label('count')
    ).join(Event, Event.concern_id == HealthConcern.id)\
     .filter(Event.event_type == 'concern_selected')\
     .group_by(HealthConcern.id)\
     .order_by(func.count(Event.id).desc())\
     .limit(10).all()

    # Top recipes viewed
    top_recipes = db.session.query(
        Recipe,
        func.count(Event.id).label('count')
    ).join(Event, Event.recipe_id == Recipe.id)\
     .filter(Event.event_type == 'recipe_viewed')\
     .group_by(Recipe.id)\
     .order_by(func.count(Event.id).desc())\
     .limit(10).all()

    # Feedback breakdown
    feedback_yes      = Feedback.query.filter_by(rating='yes').count()
    feedback_somewhat = Feedback.query.filter_by(rating='somewhat').count()
    feedback_no       = Feedback.query.filter_by(rating='no').count()

    # Recent comments
    recent_comments = Feedback.query.filter(
        Feedback.comment != None
    ).order_by(Feedback.created_at.desc()).limit(10).all()

    return render_template('main/analytics.html',
                           total_users=total_users,
                           total_concerns=total_concerns,
                           total_feedback=total_feedback,
                           top_concerns=top_concerns,
                           top_recipes=top_recipes,
                           feedback_yes=feedback_yes,
                           feedback_somewhat=feedback_somewhat,
                           feedback_no=feedback_no,
                           recent_comments=recent_comments)


@bp.route('/analytics/explain', methods=['POST'])
@login_required
def analytics_explain():
    import os
    from openai import OpenAI
    from app.models import Event, Feedback, User
    from sqlalchemy import func

    total_users = User.query.count()
    total_concerns = Event.query.filter_by(event_type='concern_selected').count()
    total_feedback = Feedback.query.count()

    top_concerns = db.session.query(
        HealthConcern, func.count(Event.id).label('count')
    ).join(Event, Event.concern_id == HealthConcern.id)\
     .filter(Event.event_type == 'concern_selected')\
     .group_by(HealthConcern.id)\
     .order_by(func.count(Event.id).desc())\
     .limit(5).all()

    top_recipes = db.session.query(
        Recipe, func.count(Event.id).label('count')
    ).join(Event, Event.recipe_id == Recipe.id)\
     .filter(Event.event_type == 'recipe_viewed')\
     .group_by(Recipe.id)\
     .order_by(func.count(Event.id).desc())\
     .limit(5).all()

    feedback_yes      = Feedback.query.filter_by(rating='yes').count()
    feedback_somewhat = Feedback.query.filter_by(rating='somewhat').count()
    feedback_no       = Feedback.query.filter_by(rating='no').count()

    context = {
        "total_users": total_users,
        "total_concerns_selected": total_concerns,
        "total_feedback": total_feedback,
        "feedback_breakdown": {
            "helpful": feedback_yes,
            "somewhat": feedback_somewhat,
            "not_helpful": feedback_no
        },
        "top_health_concerns": [
            {"name": c.name, "selections": n} for c, n in top_concerns
        ],
        "top_recipes_viewed": [
            {"name": r.name, "views": n} for r, n in top_recipes
        ]
    }

    prompt = f"""You are a calm, supportive advisor helping a wellness founder understand their app analytics.

Here is the aggregated usage data for EaselyWell, a personalized nutrition guidance app:

{context}

Please provide 3 to 5 plain-language, actionable insights based on this data. Focus on what is working, what could be improved, and what the founder might want to try next. Keep the tone warm, honest, and founder-friendly. No bullet point headers needed — just clear, flowing observations."""

    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"insight": response.choices[0].message.content}


@bp.route('/api/classify', methods=['POST'])
def classify():
    data = request.get_json()
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": data.get("message", "")},
            timeout=10
        )
        raw_text = response.text
        if raw_text.startswith('='):
            raw_text = raw_text[1:]
        raw = json.loads(raw_text)
        reply_text = raw.get("reply", "{}")
        import re
        reply_text = re.sub(r'```json\n|```', '', reply_text).strip()
        inner = json.loads(reply_text)
        concern = inner.get("concern", "unknown")

        replies = {
            "iron_deficiency": "Iron levels - redirecting you now",
            "high_cholesterol": "Cholesterol support - redirecting you now",
            "high_blood_pressure": "Blood pressure support - redirecting you now",
            "vitamin_d_deficiency": "Vitamin D support - redirecting you now",
            "gut_health": "Gut health support - redirecting you now",
            "low_energy_fatigue": "Energy support - redirecting you now",
            "bone_health": "Bone health support - redirecting you now",
            "anxiety_stress": "Stress support - redirecting you now",
            "chronic_inflammation": "Inflammation support - redirecting you now",
            "immune_support": "Immune support - redirecting you now",
            "unknown": "Could you tell me more about how you feel?"
        }

        reply = replies.get(concern, replies["unknown"])
        return jsonify({"reply": reply, "concern_slug": concern})

    except Exception as e:
        print(f"DEBUG Error: {str(e)}")
        return jsonify({"reply": "Sorry, I could not connect right now!"}), 500


@bp.route('/api/explain/nutrient/<int:nutrient_id>')
@login_required
def explain_nutrient(nutrient_id):
    import os
    from openai import OpenAI
    from app.models import Nutrient, HealthConcern
    concern_id = request.args.get('concern_id', type=int)
    nutrient = Nutrient.query.get_or_404(nutrient_id)
    concern = HealthConcern.query.get_or_404(concern_id) if concern_id else None

    concern_name = concern.name if concern else "general wellness"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": (
                f"In 2-3 sentences explain why {nutrient.name} helps with "
                f"{concern_name} in calm, supportive, non-medical, wellness-focused "
                f"language. No diagnosis, no medical claims."
            )
        }],
        max_tokens=120,
    )
    explanation = response.choices[0].message.content.strip()
    return jsonify({"explanation": explanation})


@bp.route('/nutrients/<int:nutrient_id>')
@login_required
def nutrient_detail(nutrient_id):
    import os
    from openai import OpenAI
    from app.models import Nutrient, NutrientIngredient
    nutrient = Nutrient.query.get_or_404(nutrient_id)

    ingredient_links = NutrientIngredient.query.filter_by(nutrient_id=nutrient_id).all()
    ingredients = [link.ingredient for link in ingredient_links]

    if nutrient_id not in _nutrient_explanation_cache:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": (
                    f"In 3-4 sentences explain what {nutrient.name} does for general "
                    f"health and wellness in calm, supportive, non-medical language. "
                    f"No diagnosis, no medical claims, no dosage advice."
                )
            }],
            max_tokens=160,
        )
        _nutrient_explanation_cache[nutrient_id] = response.choices[0].message.content.strip()

    explanation = _nutrient_explanation_cache[nutrient_id]
    return render_template('main/nutrient.html',
                           nutrient=nutrient,
                           ingredients=ingredients,
                           explanation=explanation)
