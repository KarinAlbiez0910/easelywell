import sys
from run import app
from app import db
from app.models import Ingredient, Recipe

INGREDIENT_FLAGS = {
    # vegetable
    "Spinach":        dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    "Broccoli":       dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    "Sweet Potato":   dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    "Kale":           dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    "Garlic":         dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    "Beetroot":       dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    # legume
    "Lentils":        dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Chickpeas":      dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    # fish
    "Salmon":         dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Sardines":       dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    # nut
    "Almonds":        dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=False, is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Walnuts":        dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=False, is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    # fruit — avocado exception: low_sugar=True
    "Avocado":        dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    "Blueberries":    dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=False, is_high_protein=False, is_mediterranean=True),
    # dairy
    "Greek Yogurt":   dict(is_gluten_free=True,  is_dairy_free=False, is_nut_free=True,  is_egg_free=True,  is_low_sugar=False, is_high_protein=True,  is_mediterranean=True),
    "Kefir":          dict(is_gluten_free=True,  is_dairy_free=False, is_nut_free=True,  is_egg_free=True,  is_low_sugar=False, is_high_protein=True,  is_mediterranean=True),
    # grain — quinoa exception: gluten_free=True
    "Oats":           dict(is_gluten_free=False, is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=False, is_high_protein=False, is_mediterranean=True),
    "Quinoa":         dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=False, is_high_protein=False, is_mediterranean=True),
    # protein — eggs exception: egg_free=False, mediterranean=False
    "Eggs":           dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=False, is_low_sugar=True,  is_high_protein=True,  is_mediterranean=False),
    # spice
    "Turmeric":       dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    "Ginger":         dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    # seed
    "Pumpkin Seeds":  dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    # other — corrected: pure dark chocolate is gluten-free and dairy-free
    "Dark Chocolate": dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=False, is_egg_free=True,  is_low_sugar=False, is_high_protein=False, is_mediterranean=True),
    # oil
    "Olive Oil":      dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    # herb
    "Chamomile":      dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    # meat — lamb exception: mediterranean=True
    "Chicken Breast": dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=False),
    "Beef Steak":     dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=False),
    "Turkey":         dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=False),
    "Lamb":           dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
}

RECIPE_FLAGS = {
    "Sardine & Cheese Toast":               dict(is_gluten_free=False, is_dairy_free=False, is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Mushroom & Egg Scramble":              dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=False, is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Salmon & Avocado Bowl":                dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Spinach & Lentil Power Bowl":          dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Blueberry Oat Breakfast":              dict(is_gluten_free=False, is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=False, is_high_protein=False, is_mediterranean=False),
    "Turmeric Chickpea Stew":               dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Kale & Quinoa Salad":                  dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Greek Yogurt Parfait":                 dict(is_gluten_free=True,  is_dairy_free=False, is_nut_free=True,  is_egg_free=True,  is_low_sugar=False, is_high_protein=True,  is_mediterranean=True),
    "Walnut & Dark Chocolate Energy Bites": dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=False, is_egg_free=True,  is_low_sugar=False, is_high_protein=False, is_mediterranean=False),
    "Beetroot & Quinoa Salad":              dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=False, is_mediterranean=True),
    "Chicken & Spinach Stir Fry":           dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
    "Beef & Broccoli Bowl":                 dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=False),
    "Turkey & Sweet Potato Bake":           dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=False),
    "Lamb & Chickpea Stew":                 dict(is_gluten_free=True,  is_dairy_free=True,  is_nut_free=True,  is_egg_free=True,  is_low_sugar=True,  is_high_protein=True,  is_mediterranean=True),
}

def run():
    with app.app_context():
        ing_updated = 0
        ing_missing = []
        for name, flags in INGREDIENT_FLAGS.items():
            rows = Ingredient.query.filter_by(name=name).update(flags)
            if rows:
                ing_updated += rows
            else:
                ing_missing.append(name)

        rec_updated = 0
        rec_missing = []
        for name, flags in RECIPE_FLAGS.items():
            rows = Recipe.query.filter_by(name=name).update(flags)
            if rows:
                rec_updated += rows
            else:
                rec_missing.append(name)

        db.session.commit()

        print(f"Ingredients updated: {ing_updated}/{len(INGREDIENT_FLAGS)}")
        if ing_missing:
            print(f"  Not found: {ing_missing}")
        print(f"Recipes updated:     {rec_updated}/{len(RECIPE_FLAGS)}")
        if rec_missing:
            print(f"  Not found: {rec_missing}")

if __name__ == "__main__":
    run()
