import re, json, os

# Article metadata: slug -> (display title, category label, category url)
ARTICLES = {
    'air-fryer-chicken':      ('Crispy Air Fryer Chicken Thighs',     'Dinner',    'dinner'),
    'avocado-toast':          ('Avocado Toast with Poached Eggs',      'Breakfast', 'breakfast'),
    'baked-salmon':           ('Baked Lemon Herb Salmon',              'Dinner',    'dinner'),
    'banana-bread':           ('Best Moist Banana Bread',              'Breakfast', 'breakfast'),
    'buddha-bowl':            ('Rainbow Buddha Bowl',                  'Healthy',   'healthy'),
    'budget-fried-rice':      ('Budget Chicken Fried Rice',            'Dinner',    'dinner'),
    'buttermilk-pancakes':    ('Fluffy Buttermilk Pancakes',           'Breakfast', 'breakfast'),
    'chocolate-chip-cookies': ('Best Chewy Chocolate Chip Cookies',    'Desserts',  'desserts'),
    'fudgy-brownies':         ('Double Chocolate Fudge Brownies',      'Desserts',  'desserts'),
    'green-smoothie-bowl':    ('Green Detox Smoothie Bowl',            'Healthy',   'healthy'),
    'high-protein-meal-prep': ('High Protein Meal Prep Bowls',         'Healthy',   'healthy'),
    'honey-garlic-chicken':   ('Easy Honey Garlic Chicken',            'Dinner',    'dinner'),
    'mediterranean-bowl':     ('Mediterranean Quinoa Bowl',            'Healthy',   'healthy'),
    'no-bake-cheesecake':     ('No-Bake Cheesecake Jars',              'Desserts',  'desserts'),
    'no-bake-chocolate-bars': ('No-Bake Chocolate Peanut Butter Bars', 'Desserts',  'desserts'),
    'one-pot-pasta':          ('Easy One-Pot Pasta Primavera',         'Dinner',    'dinner'),
    'overnight-oats':         ('Easy Overnight Oats',                  'Breakfast', 'breakfast'),
    'pasta-carbonara':        ('Authentic Pasta Carbonara',            'Dinner',    'dinner'),
    'sheet-pan-chicken':      ('Sheet Pan Chicken and Veggies',        'Dinner',    'dinner'),
    'stuffed-bell-peppers':   ('Easy Stuffed Bell Peppers',            'Dinner',    'dinner'),
    'turmeric-lentil-soup':   ('Anti-Inflammatory Turmeric Lentil Soup','Healthy',  'healthy'),
}

base = os.path.dirname(os.path.abspath(__file__))

for slug, (title, cat, cat_slug) in ARTICLES.items():
    filepath = os.path.join(base, f'{slug}.html')
    if not os.path.exists(filepath):
        print(f'MISSING: {filepath}')
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Only add if not already present
    if 'BreadcrumbList' in content:
        print(f'Skipped (already has breadcrumb): {slug}.html')
        continue

    breadcrumb = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://binrecipes.com/'},
            {'@type': 'ListItem', 'position': 2, 'name': cat,   'item': f'https://binrecipes.com/#{cat_slug}'},
            {'@type': 'ListItem', 'position': 3, 'name': title, 'item': f'https://binrecipes.com/{slug}'},
        ]
    }

    block = f'<script type="application/ld+json">\n{json.dumps(breadcrumb, ensure_ascii=False)}\n</script>'
    content = content.replace('</head>', f'{block}\n</head>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Added breadcrumb: {slug}.html')

print('\nDone!')
