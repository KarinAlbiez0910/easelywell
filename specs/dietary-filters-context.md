# Dietary Filters Extension — Context Document

## Task Summary
Extend dietary preference filtering in EaselyWell from 3 existing filters
to 11 filters by adding 8 new boolean flags to the ingredient model,
filtering logic, and UI.

## Final Filter List
| # | Filter | Status |
|---|--------|--------|
| 1 | No restrictions | ✅ existing |
| 2 | Vegan | ✅ existing |
| 3 | Vegetarian | ✅ existing |
| 4 | Pescatarian | ✅ existing |
| 5 | Gluten-free | 🆕 new |
| 6 | Dairy-free / Lactose-free | 🆕 new |
| 7 | Nut-free | 🆕 new |
| 8 | Egg-free | 🆕 new |
| 9 | Low sugar / Diabetic-friendly | 🆕 new |
| 10 | High protein | 🆕 new |
| 11 | Mediterranean | 🆕 new |

## Sub-Agent Job (Read-Only, Context Control)
The sub-agent runs BEFORE implementation starts.
It is read-only and must return a summary under 200 tokens.

### Sub-agent trigger
When the main agent starts the task and needs to understand
the existing filter pattern before implementing new ones.

### Sub-agent instructions
Read the following files and return a concise summary of:
1. How existing filters (vegan/vegetarian/pescatarian) are stored
   in the Ingredient model (column names, data types)
2. How the filter is applied in the Flask route (query logic)
3. How the filter options are rendered in the Jinja2 template
4. How the most recent migration was structured for reference

Return ONLY:
- File names and line references
- Column names and types
- The query pattern used
- The template rendering pattern
No full file contents. Max 200 tokens.

### Sub-agent output example
```
models.py: Ingredient has is_vegan (Boolean), is_vegetarian (Boolean),
is_pescatarian (Boolean). Filter applied in routes/concerns.py line ~45
via .filter_by(is_vegan=True). Template: preferences.html renders
filter options as checkbox list. Migration: versions/xxxx_add_vegan.py
uses op.add_column with Boolean nullable=True default=False.
```

## What Stays OUT of Main Context
- Full migration history (only most recent pattern needed)
- Full ingredient seed data (structure only, not content)
- n8n workflow files (irrelevant for this task)
- Unrelated Flask routes and templates
- Full DB schema (only ingredients table relevant)

## What Should Be Kept Minimal
- Sub-agent output: max 200 tokens
- DB schema reference: ingredients table only
- Template reference: filter section only, not full template

## Implementation Scope
### In scope
- Add 7 new boolean columns to Ingredient model
- Create DB migration for new columns
- Update filtering logic in relevant Flask route
- Update Jinja2 template to render new filter options
- Re-tag existing ingredients with new flags
- Add tests for new filters

### Out of scope
- n8n workflow changes
- New health concern mappings
- UI redesign
- Nutritional data (e.g. sodium levels, glycemic index)
- Fructose-free, Low sodium (deferred)

## Key Risk
Inconsistency across layers — a filter added to the DB but missed
in the template or query will silently fail without an obvious error.
Tests must cover the full chain for each new filter.