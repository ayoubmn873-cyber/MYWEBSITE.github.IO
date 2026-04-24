"""
Add external authority links to all recipe articles:
- USDA nutrition source after nutrition grid
- Food safety link where relevant
"""
import os, re

base = os.path.dirname(os.path.abspath(__file__))

ARTICLES = [
    'air-fryer-chicken', 'avocado-toast', 'baked-salmon', 'banana-bread',
    'buddha-bowl', 'budget-fried-rice', 'buttermilk-pancakes', 'chocolate-chip-cookies',
    'fudgy-brownies', 'green-smoothie-bowl', 'high-protein-meal-prep', 'honey-garlic-chicken',
    'mediterranean-bowl', 'no-bake-cheesecake', 'no-bake-chocolate-bars', 'one-pot-pasta',
    'overnight-oats', 'pasta-carbonara', 'sheet-pan-chicken', 'stuffed-bell-peppers',
    'turmeric-lentil-soup',
]

SOURCE_NOTE = (
    '<p class="nutrition-note" style="font-size:.78rem;color:#888;margin-top:10px;line-height:1.5">'
    'Nutrition estimates based on <a href="https://fdc.nal.usda.gov/" target="_blank" rel="noopener" '
    'style="color:#E8570C">USDA FoodData Central</a>. Values are per serving and may vary.'
    '</p>'
)

for slug in ARTICLES:
    filepath = os.path.join(base, f'{slug}.html')
    if not os.path.exists(filepath):
        print(f'MISSING: {filepath}')
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'fdc.nal.usda.gov' in content:
        print(f'Skipped (already has USDA link): {slug}.html')
        continue

    # Insert after the closing </div> of the nutrition-grid, before </section>
    new_content = content.replace(
        '</div>\n      </section>',
        f'</div>\n      {SOURCE_NOTE}\n      </section>',
        1  # only first occurrence (the nutrition grid)
    )

    if new_content == content:
        print(f'Pattern not found: {slug}.html')
        continue

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Added USDA link: {slug}.html')

print('\nDone!')
