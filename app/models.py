from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    age_range = db.Column(db.String(20))        # e.g. "25-34"
    family_situation = db.Column(db.String(50)) # e.g. "single", "family with kids"
    gender = db.Column(db.String(50))
    dietary_preference = db.Column(db.String(50)) # e.g. "vegan", "vegetarian"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class HealthConcern(db.Model):
    __tablename__ = 'health_concern'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(10))

    nutrients = db.relationship('HealthConcernNutrient', back_populates='health_concern')

    def __repr__(self):
        return f'<HealthConcern {self.name}>'


class Nutrient(db.Model):
    __tablename__ = 'nutrient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    daily_value = db.Column(db.Numeric)

    health_concerns = db.relationship('HealthConcernNutrient', back_populates='nutrient')
    ingredients = db.relationship('NutrientIngredient', back_populates='nutrient')

    def __repr__(self):
        return f'<Nutrient {self.name}>'


class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))            # e.g. vegetable, protein
    is_vegan = db.Column(db.Boolean, default=True)
    is_vegetarian = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255))

    nutrients = db.relationship('NutrientIngredient', back_populates='ingredient')
    recipes = db.relationship('RecipeIngredient', back_populates='ingredient')

    def __repr__(self):
        return f'<Ingredient {self.name}>'


class HealthConcernNutrient(db.Model):
    __tablename__ = 'health_concern_nutrient'

    id = db.Column(db.Integer, primary_key=True)
    health_concern_id = db.Column(db.Integer, db.ForeignKey('health_concern.id'), nullable=False)
    nutrient_id = db.Column(db.Integer, db.ForeignKey('nutrient.id'), nullable=False)

    health_concern = db.relationship('HealthConcern', back_populates='nutrients')
    nutrient = db.relationship('Nutrient', back_populates='health_concerns')


class NutrientIngredient(db.Model):
    __tablename__ = 'nutrient_ingredient'

    id = db.Column(db.Integer, primary_key=True)
    nutrient_id = db.Column(db.Integer, db.ForeignKey('nutrient.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

    nutrient = db.relationship('Nutrient', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='nutrients')


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_vegan = db.Column(db.Boolean, default=True)
    is_vegetarian = db.Column(db.Boolean, default=True)
    prep_time = db.Column(db.Integer)           # in minutes

    ingredients = db.relationship('RecipeIngredient', back_populates='recipe')

    def __repr__(self):
        return f'<Recipe {self.name}>'


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.String(50))         # e.g. "100g", "2 cups"

    recipe = db.relationship('Recipe', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipes')

class UserFavouriteRecipe(db.Model):
    __tablename__ = 'user_favourite_recipe'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='favourites')
    recipe = db.relationship('Recipe', backref='saved_by')