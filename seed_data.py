from app import create_app, db
from app.models import (
    HealthConcern, Nutrient, Ingredient,
    HealthConcernNutrient, NutrientIngredient,
    Recipe, RecipeIngredient
)

app = create_app()

with app.app_context():

    # ── Clear all existing data ──────────────────────────────────
    from app.models import UserFavouriteRecipe
    UserFavouriteRecipe.query.delete()
    RecipeIngredient.query.delete()
    Recipe.query.delete()
    NutrientIngredient.query.delete()
    HealthConcernNutrient.query.delete()
    Ingredient.query.delete()
    Nutrient.query.delete()
    HealthConcern.query.delete()
    db.session.commit()

    # ── Health Concerns ──────────────────────────────────────────
    concerns = [
        HealthConcern(name="Iron Deficiency",       icon="🩸", description="Support your body's iron levels through food"),
        HealthConcern(name="High Cholesterol",       icon="❤️",  description="Support heart health by focusing on the right fats"),
        HealthConcern(name="High Blood Pressure",    icon="💪",  description="Support healthy blood pressure through diet"),
        HealthConcern(name="Vitamin D Deficiency",   icon="☀️",  description="Boost vitamin D levels through diet and lifestyle"),
        HealthConcern(name="Gut Health",             icon="🌿",  description="Improve digestion and microbiome balance"),
        HealthConcern(name="Low Energy & Fatigue",   icon="⚡",  description="Combat tiredness with energizing nutrients"),
        HealthConcern(name="Bone Health",            icon="🦴",  description="Strengthen bones with calcium and vitamin K"),
        HealthConcern(name="Anxiety & Stress",       icon="🧘",  description="Calm your nervous system with the right foods"),
        HealthConcern(name="Chronic Inflammation",   icon="🔥",  description="Reduce inflammation with anti-inflammatory foods"),
        HealthConcern(name="Immune Support",         icon="🛡️",  description="Strengthen your immune defenses through nutrition"),
    ]
    db.session.add_all(concerns)
    db.session.commit()

    # ── Nutrients ────────────────────────────────────────────────
    nutrients = [
        Nutrient(name="Iron",            daily_value=18),
        Nutrient(name="Vitamin C",       daily_value=90),
        Nutrient(name="Omega-3",         daily_value=1.6),
        Nutrient(name="Fiber",           daily_value=28),
        Nutrient(name="Magnesium",       daily_value=420),
        Nutrient(name="Vitamin D",       daily_value=20),
        Nutrient(name="Calcium",         daily_value=1000),
        Nutrient(name="Vitamin K",       daily_value=120),
        Nutrient(name="Zinc",            daily_value=11),
        Nutrient(name="B Vitamins",      daily_value=None),
        Nutrient(name="Probiotics",      daily_value=None),
        Nutrient(name="Antioxidants",    daily_value=None),
        Nutrient(name="Potassium",       daily_value=4700),
        Nutrient(name="Folate",          daily_value=400),
        Nutrient(name="Vitamin E",       daily_value=15),
    ]
    db.session.add_all(nutrients)
    db.session.commit()

    # ── Ingredients ──────────────────────────────────────────────
    ingredients = [
        Ingredient(name="Spinach",        type="vegetable",   is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Lentils",        type="legume",      is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Salmon",         type="fish",        is_vegan=False, is_vegetarian=False),
        Ingredient(name="Almonds",        type="nut",         is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Avocado",        type="fruit",       is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Blueberries",    type="fruit",       is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Greek Yogurt",   type="dairy",       is_vegan=False, is_vegetarian=True),
        Ingredient(name="Oats",           type="grain",       is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Broccoli",       type="vegetable",   is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Eggs",           type="protein",     is_vegan=False, is_vegetarian=True),
        Ingredient(name="Sweet Potato",   type="vegetable",   is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Chickpeas",      type="legume",      is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Walnuts",        type="nut",         is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Kefir",          type="dairy",       is_vegan=False, is_vegetarian=True),
        Ingredient(name="Turmeric",       type="spice",       is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Ginger",         type="spice",       is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Sardines",       type="fish",        is_vegan=False, is_vegetarian=False),
        Ingredient(name="Pumpkin Seeds",  type="seed",        is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Kale",           type="vegetable",   is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Quinoa",         type="grain",       is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Dark Chocolate", type="other",       is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Garlic",         type="vegetable",   is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Olive Oil",      type="oil",         is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Beetroot",       type="vegetable",   is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Chamomile",      type="herb",        is_vegan=True,  is_vegetarian=True),
        Ingredient(name="Chicken Breast",  type="meat", is_vegan=False, is_vegetarian=False),
        Ingredient(name="Beef Steak",      type="meat", is_vegan=False, is_vegetarian=False),
        Ingredient(name="Turkey",          type="meat", is_vegan=False, is_vegetarian=False),
        Ingredient(name="Lamb",            type="meat", is_vegan=False, is_vegetarian=False),
    ]
    db.session.add_all(ingredients)
    db.session.commit()

    # ── Helper lookups ───────────────────────────────────────────
    def c(name): return HealthConcern.query.filter_by(name=name).first()
    def n(name): return Nutrient.query.filter_by(name=name).first()
    def i(name): return Ingredient.query.filter_by(name=name).first()

    # ── Concern → Nutrient links ─────────────────────────────────
    cn_links = [
        (c("Iron Deficiency"),      n("Iron")),
        (c("Iron Deficiency"),      n("Vitamin C")),
        (c("Iron Deficiency"),      n("Folate")),
        (c("High Cholesterol"),     n("Omega-3")),
        (c("High Cholesterol"),     n("Fiber")),
        (c("High Cholesterol"),     n("Antioxidants")),
        (c("High Blood Pressure"),  n("Potassium")),
        (c("High Blood Pressure"),  n("Magnesium")),
        (c("High Blood Pressure"),  n("Omega-3")),
        (c("Vitamin D Deficiency"), n("Vitamin D")),
        (c("Vitamin D Deficiency"), n("Calcium")),
        (c("Vitamin D Deficiency"), n("Magnesium")),
        (c("Gut Health"),           n("Probiotics")),
        (c("Gut Health"),           n("Fiber")),
        (c("Gut Health"),           n("Zinc")),
        (c("Low Energy & Fatigue"), n("Iron")),
        (c("Low Energy & Fatigue"), n("B Vitamins")),
        (c("Low Energy & Fatigue"), n("Magnesium")),
        (c("Bone Health"),          n("Calcium")),
        (c("Bone Health"),          n("Vitamin D")),
        (c("Bone Health"),          n("Vitamin K")),
        (c("Anxiety & Stress"),     n("Magnesium")),
        (c("Anxiety & Stress"),     n("B Vitamins")),
        (c("Anxiety & Stress"),     n("Omega-3")),
        (c("Chronic Inflammation"), n("Omega-3")),
        (c("Chronic Inflammation"), n("Antioxidants")),
        (c("Chronic Inflammation"), n("Vitamin E")),
        (c("Immune Support"),       n("Vitamin C")),
        (c("Immune Support"),       n("Zinc")),
        (c("Immune Support"),       n("Antioxidants")),
    ]
    for concern, nutrient in cn_links:
        db.session.add(HealthConcernNutrient(
            health_concern_id=concern.id,
            nutrient_id=nutrient.id
        ))
    db.session.commit()

    # ── Nutrient → Ingredient links ──────────────────────────────
    ni_links = [
        (n("Iron"),         i("Spinach")),
        (n("Iron"),         i("Lentils")),
        (n("Iron"),         i("Pumpkin Seeds")),
        (n("Iron"),         i("Quinoa")),
        (n("Vitamin C"),    i("Broccoli")),
        (n("Vitamin C"),    i("Blueberries")),
        (n("Vitamin C"),    i("Kale")),
        (n("Omega-3"),      i("Salmon")),
        (n("Omega-3"),      i("Walnuts")),
        (n("Omega-3"),      i("Sardines")),
        (n("Fiber"),        i("Oats")),
        (n("Fiber"),        i("Chickpeas")),
        (n("Fiber"),        i("Sweet Potato")),
        (n("Magnesium"),    i("Almonds")),
        (n("Magnesium"),    i("Dark Chocolate")),
        (n("Magnesium"),    i("Pumpkin Seeds")),
        (n("Vitamin D"),    i("Salmon")),
        (n("Vitamin D"),    i("Eggs")),
        (n("Vitamin D"),    i("Sardines")),
        (n("Calcium"),      i("Greek Yogurt")),
        (n("Calcium"),      i("Kefir")),
        (n("Calcium"),      i("Kale")),
        (n("Vitamin K"),    i("Kale")),
        (n("Vitamin K"),    i("Spinach")),
        (n("Vitamin K"),    i("Broccoli")),
        (n("Zinc"),         i("Pumpkin Seeds")),
        (n("Zinc"),         i("Chickpeas")),
        (n("Zinc"),         i("Eggs")),
        (n("B Vitamins"),   i("Eggs")),
        (n("B Vitamins"),   i("Salmon")),
        (n("B Vitamins"),   i("Quinoa")),
        (n("Probiotics"),   i("Greek Yogurt")),
        (n("Probiotics"),   i("Kefir")),
        (n("Antioxidants"), i("Blueberries")),
        (n("Antioxidants"), i("Dark Chocolate")),
        (n("Antioxidants"), i("Turmeric")),
        (n("Potassium"),    i("Sweet Potato")),
        (n("Potassium"),    i("Avocado")),
        (n("Potassium"),    i("Beetroot")),
        (n("Folate"),       i("Spinach")),
        (n("Folate"),       i("Lentils")),
        (n("Folate"),       i("Beetroot")),
        (n("Vitamin E"),    i("Almonds")),
        (n("Vitamin E"),    i("Avocado")),
        (n("Vitamin E"),    i("Olive Oil")),
        (n("Iron"),      i("Beef Steak")),
        (n("Iron"),      i("Lamb")),
        (n("Zinc"),      i("Beef Steak")),
        (n("Zinc"),      i("Lamb")),
        (n("Zinc"),      i("Turkey")),
        (n("B Vitamins"), i("Chicken Breast")),
        (n("B Vitamins"), i("Turkey")),
        (n("B Vitamins"), i("Beef Steak"))
                
    ]
    for nutrient, ingredient in ni_links:
        db.session.add(NutrientIngredient(
            nutrient_id=nutrient.id,
            ingredient_id=ingredient.id
        ))
    db.session.commit()

    # ── Recipes ──────────────────────────────────────────────────
    recipes_data = [
        {
            "name": "Sardine & Cheese Toast",
            "description": "Sardines pack vitamin D, calcium, and omega-3s in one tiny fish. Adding eggs multiplies the D content.",
            "instructions": "1. Toast sourdough bread until golden.|2. Layer sardines over toast.|3. Broil for 2 minutes.|4. Serve with a fried egg on top.",
            "prep_time": 10,
            "is_vegan": False,
            "is_vegetarian": False,
            "ingredients": ["Sardines", "Eggs"]
        },
        {
            "name": "Mushroom & Egg Scramble",
            "description": "Eggs are one of the few natural food sources of vitamin D. Olive oil helps absorb fat-soluble vitamins.",
            "instructions": "1. Sauté mushrooms in olive oil for 5 min.|2. Whisk eggs with salt and pepper.|3. Pour eggs over mushrooms and scramble gently.|4. Serve on toast or with salad.",
            "prep_time": 10,
            "is_vegan": False,
            "is_vegetarian": True,
            "ingredients": ["Eggs", "Olive Oil"]
        },
        {
            "name": "Salmon & Avocado Bowl",
            "description": "Salmon is the richest food source of vitamin D. Avocado delivers healthy fats that help absorb fat-soluble vitamins.",
            "instructions": "1. Season salmon and pan-fry 4 min each side.|2. Slice avocado and arrange in a bowl.|3. Add a handful of kale.|4. Place salmon on top and drizzle with olive oil.",
            "prep_time": 15,
            "is_vegan": False,
            "is_vegetarian": False,
            "ingredients": ["Salmon", "Avocado", "Kale", "Olive Oil"]
        },
        {
            "name": "Spinach & Lentil Power Bowl",
            "description": "Lentils and spinach are iron powerhouses. Vitamin C from lemon juice dramatically boosts iron absorption.",
            "instructions": "1. Cook lentils in salted water for 20 min.|2. Wilt spinach in a pan with garlic and olive oil.|3. Combine lentils and spinach in a bowl.|4. Squeeze fresh lemon juice over the top.",
            "prep_time": 25,
            "is_vegan": True,
            "is_vegetarian": True,
            "ingredients": ["Lentils", "Spinach", "Garlic", "Olive Oil"]
        },
        {
            "name": "Blueberry Oat Breakfast",
            "description": "Oats provide slow-release energy and fiber. Blueberries are packed with antioxidants that support energy metabolism.",
            "instructions": "1. Cook oats with milk or water for 5 min.|2. Stir in a handful of blueberries.|3. Top with almonds and a drizzle of honey.|4. Serve warm.",
            "prep_time": 10,
            "is_vegan": True,
            "is_vegetarian": True,
            "ingredients": ["Oats", "Blueberries", "Almonds"]
        },
        {
            "name": "Turmeric Chickpea Stew",
            "description": "Turmeric contains curcumin, a powerful anti-inflammatory compound. Chickpeas add plant protein and zinc to support immunity.",
            "instructions": "1. Sauté garlic in olive oil.|2. Add chickpeas, turmeric, and ginger.|3. Pour in coconut milk and simmer 15 min.|4. Season with salt and serve with rice.",
            "prep_time": 20,
            "is_vegan": True,
            "is_vegetarian": True,
            "ingredients": ["Chickpeas", "Turmeric", "Ginger", "Garlic", "Olive Oil"]
        },
        {
            "name": "Kale & Quinoa Salad",
            "description": "Kale is rich in calcium, vitamin K and vitamin C. Quinoa adds complete protein and magnesium for bone and muscle health.",
            "instructions": "1. Cook quinoa and let cool.|2. Massage kale with olive oil and lemon.|3. Combine kale and quinoa in a bowl.|4. Top with pumpkin seeds and a lemon dressing.",
            "prep_time": 20,
            "is_vegan": True,
            "is_vegetarian": True,
            "ingredients": ["Kale", "Quinoa", "Pumpkin Seeds", "Olive Oil"]
        },
        {
            "name": "Greek Yogurt Parfait",
            "description": "Greek yogurt is rich in probiotics and calcium. Blueberries add antioxidants while oats provide prebiotic fiber.",
            "instructions": "1. Layer Greek yogurt in a glass.|2. Add a handful of blueberries.|3. Top with oats and almonds.|4. Drizzle with honey and serve chilled.",
            "prep_time": 5,
            "is_vegan": False,
            "is_vegetarian": True,
            "ingredients": ["Greek Yogurt", "Blueberries", "Oats", "Almonds"]
        },
        {
            "name": "Walnut & Dark Chocolate Energy Bites",
            "description": "Walnuts are rich in omega-3s and magnesium. Dark chocolate provides antioxidants and a natural mood boost.",
            "instructions": "1. Blend oats, walnuts and dark chocolate in a food processor.|2. Add a spoon of honey and mix well.|3. Roll into small balls.|4. Refrigerate for 30 min before serving.",
            "prep_time": 15,
            "is_vegan": True,
            "is_vegetarian": True,
            "ingredients": ["Walnuts", "Dark Chocolate", "Oats"]
        },
        {
            "name": "Beetroot & Quinoa Salad",
            "description": "Beetroot is high in folate and potassium, supporting blood pressure and red blood cell production.",
            "instructions": "1. Roast beetroot at 200°C for 40 min.|2. Cook quinoa and let cool.|3. Combine beetroot and quinoa.|4. Dress with olive oil, lemon and fresh herbs.",
            "prep_time": 45,
            "is_vegan": True,
            "is_vegetarian": True,
            "ingredients": ["Beetroot", "Quinoa", "Olive Oil"]
        },
        {
    "name": "Chicken & Spinach Stir Fry",
    "description": "Chicken breast is rich in B vitamins and lean protein that supports energy metabolism. Spinach adds iron and folate for red blood cell production.",
    "instructions": "1. Slice chicken breast into strips.|2. Stir fry in olive oil over high heat for 5 min.|3. Add spinach and garlic and cook 2 min.|4. Season with soy sauce and serve with rice.",
    "prep_time": 15,
    "is_vegan": False,
    "is_vegetarian": False,
    "ingredients": ["Chicken Breast", "Spinach", "Garlic", "Olive Oil"]
},
{
    "name": "Beef & Broccoli Bowl",
    "description": "Beef is one of the richest sources of iron and zinc. Broccoli adds vitamin C which dramatically boosts iron absorption from the meat.",
    "instructions": "1. Slice beef steak thinly against the grain.|2. Sear in a hot pan for 3 min each side.|3. Steam broccoli until tender.|4. Combine in a bowl and drizzle with olive oil and lemon.",
    "prep_time": 20,
    "is_vegan": False,
    "is_vegetarian": False,
    "ingredients": ["Beef Steak", "Broccoli", "Olive Oil"]
},
{
    "name": "Turkey & Sweet Potato Bake",
    "description": "Turkey is a lean protein packed with B vitamins and zinc. Sweet potato provides potassium and fiber for sustained energy and gut health.",
    "instructions": "1. Dice sweet potato and roast at 200°C for 25 min.|2. Season turkey with herbs and bake alongside for 20 min.|3. Combine in a baking dish.|4. Serve with a green salad.",
    "prep_time": 35,
    "is_vegan": False,
    "is_vegetarian": False,
    "ingredients": ["Turkey", "Sweet Potato", "Olive Oil"]
},
{
    "name": "Lamb & Chickpea Stew",
    "description": "Lamb is rich in iron, zinc and B12. Chickpeas add fiber and plant protein making this a powerful anti-inflammatory and immune-supporting meal.",
    "instructions": "1. Brown lamb pieces in olive oil.|2. Add chickpeas, turmeric and ginger.|3. Pour in stock and simmer for 30 min.|4. Serve with quinoa or bread.",
    "prep_time": 40,
    "is_vegan": False,
    "is_vegetarian": False,
    "ingredients": ["Lamb", "Chickpeas", "Turmeric", "Ginger", "Olive Oil"]
}
    ]

    for r in recipes_data:
        recipe = Recipe(
            name=r["name"],
            description=r["description"],
            instructions=r["instructions"],
            prep_time=r["prep_time"],
            is_vegan=r["is_vegan"],
            is_vegetarian=r["is_vegetarian"],
        )
        db.session.add(recipe)
        db.session.flush()

        for ing_name in r["ingredients"]:
            ing = Ingredient.query.filter_by(name=ing_name).first()
            if ing:
                db.session.add(RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ing.id
                ))

    db.session.commit()

    print("✅ Seed data loaded successfully!")
    print(f"   {len(concerns)} health concerns")
    print(f"   {len(nutrients)} nutrients")
    print(f"   {len(ingredients)} ingredients")
    print(f"   {len(recipes_data)} recipes")