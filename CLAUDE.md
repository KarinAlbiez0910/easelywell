# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EaselyWell is a Flask web app for personalized nutrition guidance. Users select health concerns, browse ingredients, and get recipe recommendations filtered by dietary preferences (vegan, vegetarian, pescatarian, flexitarian). An n8n-powered chat widget on the landing page classifies health concerns via AI.

## Development Commands

### Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start local PostgreSQL (via Docker Compose)
docker-compose up -d db

# Initialize/migrate the database
flask db upgrade

# Seed initial data
python seed_data.py
```

### Running the App
```bash
# Development server
python run.py
# or
flask run

# Full stack via Docker Compose
docker-compose up
```

### Database Migrations
```bash
flask db migrate -m "description"   # Generate migration
flask db upgrade                    # Apply migrations
flask db downgrade                  # Revert last migration
```

### Docker
```bash
docker build -t easelywell .
docker-compose up --build
```

## Architecture

### Backend Structure
- **`run.py`** — Entry point; creates Flask app via factory
- **`app/__init__.py`** — App factory: initializes SQLAlchemy, Flask-Migrate, Flask-Login; registers blueprints; adds `/health` endpoint and `ingredient_emoji` Jinja2 filter
- **`config.py`** — Loads env vars; normalizes `postgres://` → `postgresql://` for Railway compatibility
- **`app/models.py`** — All SQLAlchemy models
- **`app/auth/`** — Blueprint for login, register, logout, profile (prefix: `/auth`)
- **`app/main/`** — Blueprint for core app: concerns → ingredients → recipes → analytics (no prefix)
- **`seed_data.py`** — Seeds HealthConcerns, Nutrients, Ingredients, Recipes, and their relationships

### Data Model Flow
```
HealthConcern → (HealthConcernNutrient) → Nutrient → (NutrientIngredient) → Ingredient → (RecipeIngredient) → Recipe
```
Users interact with recipes via `UserFavouriteRecipe`, `Feedback`, and `Event` (analytics) tables.

### Frontend
- Server-side rendered **Jinja2 templates** with Tailwind CSS (CDN)
- Vanilla JS for interactive elements (favorite toggle, feedback forms, chat widget)
- Chat widget POSTs to `/api/classify`, which proxies to the n8n webhook

### AI Integration
The landing page chat widget sends messages to `https://ai-software-egnineering.app.n8n.cloud/webhook/easelywell-classifier` via `/api/classify`. The n8n workflow classifies user input into health concerns and returns a redirect URL.

## Environment Variables
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=...
DATABASE_URL=postgresql://easelyadmin:easely123@localhost/easelywell
```

Docker Compose overrides `DATABASE_URL` to use `db` as the host.

## Deployment
- **Production:** Gunicorn via `Procfile` (`gunicorn run:app`) for Railway/Heroku
- **Docker:** Non-root `appuser`, port 5000, 1 worker/1 thread
- **CI:** GitHub Actions builds Docker image on push (`.github/workflows/ci.yml`) — no automated tests run yet
- `/health` endpoint checks DB connectivity for deployment health checks
