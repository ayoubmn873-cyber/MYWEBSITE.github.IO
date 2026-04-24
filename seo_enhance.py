import re, json

ARTICLES = {
    'air-fryer-chicken': {
        'rating': '4.9', 'count': 412,
        'faqs': [
            ('What temperature should I cook chicken thighs in the air fryer?',
             'Cook chicken thighs at 400°F (200°C) in the air fryer. This high heat crisps the skin perfectly while keeping the meat juicy inside.'),
            ('How long do bone-in chicken thighs take in the air fryer?',
             'Bone-in chicken thighs take 18–20 minutes total at 400°F — 10 minutes skin-side down, then 8–10 minutes skin-side up. Always verify internal temperature reaches 165°F (74°C).'),
            ('Can I use boneless chicken thighs in the air fryer?',
             'Yes! Boneless skinless chicken thighs cook in about 15–18 minutes at 400°F. They won\'t be as crispy as bone-in but are incredibly juicy. Reduce cook time by 3–5 minutes.'),
            ('Do I need to preheat my air fryer for chicken?',
             'Yes, preheat for 3–5 minutes at 400°F before adding chicken. A preheated air fryer gives you crispier skin and more even cooking results.'),
        ]
    },
    'avocado-toast': {
        'rating': '4.8', 'count': 245,
        'faqs': [
            ('How do you keep avocado from browning on toast?',
             'Squeeze fresh lemon or lime juice over the mashed avocado immediately before serving. The citric acid prevents oxidation and keeps it green and fresh.'),
            ('What is the best bread for avocado toast?',
             'Sourdough is the most popular choice for avocado toast — the tangy flavor and sturdy crumb hold up to toppings beautifully. Thick-cut whole grain toast or rye bread are excellent alternatives.'),
            ('Is avocado toast healthy for breakfast?',
             'Yes! Avocado toast is a nutritious breakfast packed with heart-healthy monounsaturated fats, fiber, B vitamins, and potassium. Adding a poached egg boosts the protein content significantly.'),
            ('Can I make avocado toast in advance?',
             'Avocado toast is best made fresh — the avocado browns quickly and the toast goes soggy. Prep takes only 5 minutes, so make it right before eating for best results.'),
        ]
    },
    'baked-salmon': {
        'rating': '4.8', 'count': 278,
        'faqs': [
            ('What temperature should I bake salmon at?',
             'Bake salmon at 400°F (200°C) for 12–15 minutes depending on thickness. For a 1-inch thick fillet, 12 minutes gives moist, just-cooked salmon. The internal temperature should reach 145°F (63°C).'),
            ('How do I know when baked salmon is done?',
             'Salmon is done when it flakes easily with a fork and the flesh has changed from translucent pink to opaque. The internal temperature should read 145°F (63°C). Avoid overcooking — salmon continues cooking briefly after being removed from the oven.'),
            ('Should I cover salmon when baking?',
             'Baking uncovered at high heat (400°F) gives you better caramelization and a slightly crispy exterior. Cover with foil if you prefer very moist, steamed-style salmon or if your fillets are thin to prevent drying out.'),
            ('Can I bake frozen salmon without thawing?',
             'Yes! Bake frozen salmon at 400°F for 20–25 minutes (instead of 12–15). Rinse off any ice glaze first and season as normal. The texture is slightly less perfect than fresh, but very convenient.'),
        ]
    },
    'banana-bread': {
        'rating': '5.0', 'count': 2847,
        'faqs': [
            ('How ripe should bananas be for banana bread?',
             'The riper the better! Use bananas with brown or black-spotted peels — the fruit inside is sweeter and softer, making the bread much more moist and flavorful. Completely black peels are perfectly fine and give the sweetest result.'),
            ('Can I freeze banana bread?',
             'Yes! Banana bread freezes beautifully for up to 3 months. Cool completely, then wrap individual slices or the whole loaf tightly in plastic wrap followed by foil. Thaw at room temperature for 2–3 hours or overnight in the fridge.'),
            ('Why is my banana bread dense and gummy?',
             'Dense or gummy banana bread is usually caused by overmixing the batter (develops too much gluten), using too much banana, or underbaking. Mix only until just combined, measure flour accurately, and test with a toothpick — it should come out clean.'),
            ('How do I know when banana bread is fully baked?',
             'Insert a toothpick or thin knife into the center — it should come out clean or with just a few dry crumbs (not wet batter). The bread should also pull away from the sides of the pan and feel springy on top. Total bake time is 55–65 minutes at 350°F.'),
        ]
    },
    'buddha-bowl': {
        'rating': '4.7', 'count': 167,
        'faqs': [
            ('What grains can I use in a buddha bowl?',
             'Quinoa is most popular because it is high in protein and cooks quickly. Brown rice, farro, barley, millet, or even cauliflower rice are all great alternatives. Cook the grain according to package instructions and season lightly.'),
            ('Can I meal prep buddha bowls ahead of time?',
             'Yes! Store each component separately in airtight containers in the fridge for up to 4 days. Keep the dressing separate until serving to prevent sogginess. Assemble bowls fresh each morning in under 2 minutes.'),
            ('Are buddha bowls vegan and gluten-free?',
             'Buddha bowls are easily made fully vegan — use chickpeas, tofu, or tempeh as the protein. For gluten-free, use quinoa or rice as the base and ensure your dressing ingredients are gluten-free certified.'),
            ('What dressing is best for a buddha bowl?',
             'Tahini-based dressings are the most popular choice for buddha bowls — creamy, nutty, and complements vegetables and grains perfectly. Lemon-herb vinaigrette, miso ginger, or peanut sauce are also delicious options.'),
        ]
    },
    'budget-fried-rice': {
        'rating': '4.9', 'count': 689,
        'faqs': [
            ('Why do recipes say to use day-old rice for fried rice?',
             'Day-old (leftover) rice has dried out in the fridge, which means each grain is separate and less sticky. Fresh hot rice has too much moisture and steams in the pan instead of frying, resulting in a mushy texture.'),
            ('What if I only have fresh rice?',
             'Spread fresh cooked rice on a baking sheet and refrigerate uncovered for 30–60 minutes to dry it out. Alternatively, cook the rice with slightly less water, then spread and cool completely before frying.'),
            ('What vegetables can I add to fried rice?',
             'Almost any vegetable works great in fried rice! Frozen peas and carrots are the classic choice for convenience. You can also use corn, broccoli florets, diced zucchini, mushrooms, bean sprouts, or any leftover vegetables you have on hand.'),
            ('Can I make fried rice without a wok?',
             'Absolutely! A large cast iron skillet or nonstick frying pan works well. The key is high heat and not overcrowding the pan. Cook in batches if necessary to ensure the rice fries rather than steams.'),
        ]
    },
    'buttermilk-pancakes': {
        'rating': '4.9', 'count': 389,
        'faqs': [
            ('Can I make pancakes without buttermilk?',
             'Yes! Make your own buttermilk substitute by adding 1 tablespoon of white vinegar or fresh lemon juice to 1 cup of regular milk. Stir and let sit for 5 minutes until slightly curdled. It works just as well in pancake batter.'),
            ('Why are my pancakes flat instead of fluffy?',
             'Flat pancakes are usually caused by overmixing the batter (which develops gluten and deflates air bubbles) or stale baking powder. Stir batter only until just combined — lumps are perfectly fine. Also wait until bubbles form on the surface before flipping.'),
            ('How do I keep pancakes warm for the whole family?',
             'Place cooked pancakes on a baking rack set over a baking sheet in a 200°F (93°C) oven. This keeps them warm and slightly crispy without getting soggy. Avoid stacking warm pancakes directly — they steam each other and go limp.'),
            ('Can I freeze leftover pancakes?',
             'Yes! Cool pancakes completely, then freeze in a single layer on a baking sheet for 1 hour. Transfer to a zip-lock bag and freeze for up to 2 months. Reheat directly in the toaster for crispy edges, or microwave for 60–90 seconds.'),
        ]
    },
    'chocolate-chip-cookies': {
        'rating': '5.0', 'count': 3192,
        'faqs': [
            ('How do you make chocolate chip cookies chewy instead of crispy?',
             'For chewy cookies: use more brown sugar than white (brown sugar retains moisture), slightly underbake them (pull out when centers look underdone), let them cool on the pan for 5 minutes, and use melted or room-temperature butter rather than cold.'),
            ('Can I freeze chocolate chip cookie dough?',
             'Yes! Scoop dough into balls and freeze on a baking sheet for 1 hour, then transfer to a zip-lock bag. Freeze for up to 3 months. Bake directly from frozen — add 2–3 extra minutes to the bake time. No need to thaw.'),
            ('Why do my cookies spread too much when baking?',
             'Cookies spread too much when butter is too warm or melted, the dough is too warm when it goes in the oven, or there is too little flour. Chill the dough for 30 minutes before baking, and make sure your butter is softened but still cool.'),
            ('Can I use salted butter in chocolate chip cookies?',
             'Yes, salted butter works fine. Just reduce or omit the added salt in the recipe by about half (or about ¼ teaspoon per stick of butter). The slight extra salt can actually enhance the chocolate flavor.'),
        ]
    },
    'fudgy-brownies': {
        'rating': '5.0', 'count': 632,
        'faqs': [
            ('How do I know when brownies are done baking?',
             'Insert a toothpick into the center — for fudgy brownies, it should come out with a few moist crumbs but no wet batter. The edges should be set and pulling away from the pan, while the center may still look slightly underdone. They firm up as they cool.'),
            ('How do I make brownies more fudgy vs cakey?',
             'Fudgy brownies use more fat (butter and chocolate) relative to flour, fewer eggs, and less baking powder. Cakey brownies use more flour, an extra egg, and baking powder. For the fudgiest result, underbake slightly and use both butter and chocolate (not just cocoa powder).'),
            ('Do I need a mixer to make brownies?',
             'No mixer needed! Brownies come together with just a whisk and spatula. Melt the butter and chocolate, whisk in sugar and eggs by hand, then fold in the flour gently. Overmixing can actually make brownies tough, so hand-mixing is ideal.'),
            ('How long do homemade brownies stay fresh?',
             'Brownies stay fresh at room temperature in an airtight container for 3–4 days. In the refrigerator, they last up to 1 week but may dry out slightly — bring to room temperature before serving. Brownies freeze beautifully for up to 3 months.'),
        ]
    },
    'green-smoothie-bowl': {
        'rating': '4.6', 'count': 143,
        'faqs': [
            ('How thick should a smoothie bowl base be?',
             'A smoothie bowl should be much thicker than a drinkable smoothie — thick enough that a spoon stands up in it and toppings don\'t sink. Use frozen fruit and minimal liquid. Start with just 2–4 tablespoons of liquid and add more only if needed.'),
            ('What greens taste best in a smoothie bowl?',
             'Baby spinach is the best choice for beginners — it blends smooth and has almost no flavor when mixed with fruit. Kale has a slightly stronger taste but is more nutritious. Frozen cauliflower is a sneaky option that adds creaminess with zero flavor.'),
            ('Can I make a smoothie bowl the night before?',
             'Smoothie bowls are best made and eaten immediately — the base melts and separates within 30 minutes, and toppings go soggy. However, you can pre-portion and freeze the smoothie base ingredients in a zip-lock bag for quick blending in the morning.'),
            ('Are green smoothie bowls actually healthy?',
             'Yes! A green smoothie bowl provides vitamins C, K, and folate from leafy greens, natural energy from fruit carbohydrates, and fiber. Adding protein-rich toppings like nuts, seeds, or Greek yogurt makes it a nutritionally complete meal.'),
        ]
    },
    'high-protein-meal-prep': {
        'rating': '4.9', 'count': 521,
        'faqs': [
            ('How long does meal prep last in the refrigerator?',
             'Most meal prep bowls with cooked protein (chicken, beef, tofu) and grains last 4–5 days in the refrigerator in airtight containers. Seafood should be consumed within 3 days. Keep wet ingredients like sauces and dressings in a separate container to prevent sogginess.'),
            ('What are the best proteins for meal prep?',
             'Chicken breast and thighs are the most popular meal prep proteins — affordable, versatile, and reheat well. Ground turkey, hard-boiled eggs, baked tofu, canned tuna, and legumes (chickpeas, lentils) are all excellent high-protein, budget-friendly options.'),
            ('Can I freeze meal prep bowls?',
             'Cooked grains and proteins freeze well for up to 3 months. Avoid freezing fresh vegetables like lettuce, cucumber, or tomatoes as they become watery. Freeze in individual meal-sized containers and thaw overnight in the fridge before reheating.'),
            ('How many calories are in a high-protein meal prep bowl?',
             'A standard high-protein meal prep bowl with 150g chicken, ½ cup quinoa, and roasted vegetables contains approximately 450–550 calories and 40–50g of protein. Adjust portion sizes based on your specific calorie and macro targets.'),
        ]
    },
    'honey-garlic-chicken': {
        'rating': '4.9', 'count': 743,
        'faqs': [
            ('Can I use chicken breast instead of thighs for honey garlic chicken?',
             'Yes! Chicken breasts work well but cook faster — reduce the cook time to avoid drying out. Pound thicker breasts to an even thickness and cook 6–8 minutes per side over medium heat. Check for an internal temperature of 165°F (74°C).'),
            ('How do I make honey garlic sauce less sweet?',
             'To balance a too-sweet honey garlic sauce, add more soy sauce (for saltiness), a splash of rice vinegar or apple cider vinegar (for acidity), or a pinch of chili flakes (for heat). Reducing the honey by 1–2 tablespoons also works.'),
            ('How long does honey garlic chicken last in the fridge?',
             'Store honey garlic chicken with the sauce in an airtight container for up to 4 days in the refrigerator. Reheat in a skillet over medium heat for 3–4 minutes for the best texture, or microwave in 30-second bursts. The sauce thickens as it cools.'),
            ('What should I serve with honey garlic chicken?',
             'Honey garlic chicken pairs perfectly with steamed white or fried rice to soak up the sauce, steamed broccoli or bok choy, or noodles. Egg fried rice, cauliflower rice, or a simple cucumber salad are also excellent lighter options.'),
        ]
    },
    'mediterranean-bowl': {
        'rating': '4.9', 'count': 287,
        'faqs': [
            ('What grains work best in a Mediterranean bowl?',
             'Quinoa is the most popular choice for its high protein content and quick cooking time. Brown rice, farro, bulgur wheat, couscous, or orzo all work beautifully. For a low-carb option, use cauliflower rice or a bed of arugula.'),
            ('Can I substitute the protein in a Mediterranean bowl?',
             'Absolutely! Traditional options include grilled chicken, lamb, or falafel. For a vegetarian or vegan version, use crispy chickpeas, baked tofu, or grilled halloumi. Grilled shrimp is a delicious lighter seafood alternative.'),
            ('How long does a Mediterranean bowl last in the fridge?',
             'Store assembled Mediterranean bowls for up to 4 days in airtight containers. Keep the dressing and any fresh herbs or delicate toppings (like cucumber and tomatoes) in a separate container to prevent sogginess. Add right before eating.'),
            ('Is the Mediterranean diet healthy?',
             'The Mediterranean diet is consistently ranked as one of the healthiest in the world. It is associated with reduced risk of heart disease, improved brain health, and better longevity. It emphasizes olive oil, vegetables, legumes, whole grains, and lean proteins.'),
        ]
    },
    'no-bake-cheesecake': {
        'rating': '4.8', 'count': 194,
        'faqs': [
            ('Why didn\'t my no-bake cheesecake set properly?',
             'The most common reasons a no-bake cheesecake doesn\'t set are: cream cheese not at room temperature (causes lumps and uneven texture), not enough chilling time, or using low-fat cream cheese. Ensure you use full-fat cream cheese and chill for a minimum of 4 hours, ideally overnight.'),
            ('Can I freeze a no-bake cheesecake?',
             'Yes! No-bake cheesecake freezes very well for up to 1 month. Cover tightly with plastic wrap and then foil. Thaw in the refrigerator overnight before serving. Add fresh toppings after thawing for the best presentation.'),
            ('Can I use low-fat or fat-free cream cheese?',
             'It is not recommended to use low-fat or fat-free cream cheese in no-bake cheesecake. The fat content is essential for the creamy texture and for the cheesecake to set firm. Low-fat versions contain more water and will result in a soft, runny cheesecake.'),
            ('How long does no-bake cheesecake need to chill?',
             'No-bake cheesecake needs a minimum of 4 hours in the refrigerator to set, but overnight (8+ hours) is strongly recommended for the best, firmest texture. Do not try to speed up the setting process in the freezer — it changes the texture negatively.'),
        ]
    },
    'no-bake-chocolate-bars': {
        'rating': '5.0', 'count': 743,
        'faqs': [
            ('Can I use crunchy peanut butter in no-bake bars?',
             'Yes! Crunchy peanut butter works great in no-bake chocolate bars and adds a wonderful texture contrast with the smooth chocolate topping. The recipe works identically — just substitute it 1:1 for creamy peanut butter.'),
            ('Do no-bake chocolate peanut butter bars need to be refrigerated?',
             'Yes, these bars must be stored in the refrigerator. The peanut butter layer softens at room temperature and the chocolate top melts. Store in an airtight container in the fridge for up to 1 week. Take out 5 minutes before serving for the best texture.'),
            ('Can I freeze no-bake chocolate peanut butter bars?',
             'Absolutely! These bars freeze beautifully for up to 3 months. Cut into individual portions before freezing, layer between parchment paper in a freezer-safe container. Thaw in the refrigerator for 1–2 hours. They can also be eaten slightly frozen as a cold treat.'),
            ('Can I substitute almond butter or sunflower butter?',
             'Yes! Almond butter makes a slightly less sweet, nuttier version. Sunflower seed butter is a great nut-free option for allergy-friendly bars — note that it may turn slightly green due to a reaction with baking soda, but this is safe and doesn\'t affect flavor.'),
        ]
    },
    'one-pot-pasta': {
        'rating': '4.8', 'count': 334,
        'faqs': [
            ('What type of pasta works best for one-pot pasta?',
             'Long pasta shapes like linguine, spaghetti, or fettuccine work best for one-pot pasta — they cook more evenly in the broth. Shorter pasta like penne or rigatoni also work but may need an extra minute or two of cooking time.'),
            ('Can I use gluten-free pasta in one-pot pasta?',
             'Yes, but gluten-free pasta cooks faster and can get mushy easily. Reduce the cooking time by 2–3 minutes and stir frequently. The pasta may also release more starch into the sauce, making it thicker — add a splash of extra broth if needed.'),
            ('Why does my one-pot pasta taste starchy?',
             'A slight starchiness is actually normal and desirable in one-pot pasta — the pasta starch released during cooking helps create a silky, restaurant-style sauce. If it tastes too thick or heavy, just add a splash of water or broth and stir over heat to loosen it.'),
            ('Can I add chicken or shrimp to one-pot pasta?',
             'Yes! For chicken, dice it into small pieces and sauté in the pot for 5–6 minutes before adding the pasta and broth. For shrimp, add them in the last 3–4 minutes of cooking since they cook very quickly. Both work beautifully with the primavera flavors.'),
        ]
    },
    'overnight-oats': {
        'rating': '4.9', 'count': 1204,
        'faqs': [
            ('Can I heat overnight oats in the morning?',
             'Yes! Transfer your overnight oats to a microwave-safe bowl and heat for 1–2 minutes, stirring halfway through. Add a splash of milk if they\'ve thickened too much overnight. Alternatively, enjoy them cold straight from the jar — both ways are equally delicious.'),
            ('How long do overnight oats last in the refrigerator?',
             'Overnight oats stay fresh for up to 5 days in the refrigerator in a sealed jar or container. This makes them perfect for weekly meal prep — make 5 jars on Sunday and have a healthy breakfast ready every morning. Add fresh fruit toppings just before eating.'),
            ('Are overnight oats healthy?',
             'Yes, overnight oats are one of the healthiest breakfasts you can eat. They are high in fiber (beta-glucan) which supports heart health and keeps you full for hours, rich in protein when made with Greek yogurt, and packed with vitamins and minerals from oats and toppings.'),
            ('Can I make overnight oats without Greek yogurt?',
             'Absolutely! Simply substitute the yogurt with the same amount of extra milk (dairy or plant-based). The oats will be slightly thinner but equally tasty. For a higher-protein version without yogurt, add a scoop of protein powder to the oats before refrigerating.'),
        ]
    },
    'pasta-carbonara': {
        'rating': '4.9', 'count': 511,
        'faqs': [
            ('Why does my carbonara scramble instead of getting creamy?',
             'Carbonara scrambles when the pan is too hot when you add the egg mixture. Remove the pan completely from heat (or move to a cold burner) before adding the eggs and cheese. The residual heat from the pasta and pasta water is enough to gently cook the eggs into a silky sauce.'),
            ('Can I use bacon instead of pancetta in carbonara?',
             'Yes! Use thick-cut unsmoked bacon (or guanciale if available). Avoid pre-cooked or smoked bacon as the flavor can overpower the delicate sauce. The key is rendering the fat until crispy — the flavorful fat becomes part of the sauce.'),
            ('Does traditional carbonara contain cream?',
             'Authentic Italian carbonara contains absolutely no cream. The creamy sauce comes entirely from the emulsification of egg yolks, Pecorino Romano or Parmesan cheese, starchy pasta water, and rendered pancetta fat. Adding cream is considered unnecessary and changes the character of the dish.'),
            ('What pasta shape is best for carbonara?',
             'Spaghetti is the most traditional pasta for carbonara. Rigatoni is a popular modern choice because the tubes trap the sauce beautifully. Tonnarelli (thick square spaghetti) and mezze maniche are also classic choices. Avoid very thin pasta like angel hair.'),
        ]
    },
    'sheet-pan-chicken': {
        'rating': '4.9', 'count': 476,
        'faqs': [
            ('What temperature should I roast sheet pan chicken?',
             'Roast at 425°F (220°C) for the best results — high heat caramelizes the vegetables and crisps the chicken skin beautifully. At lower temperatures the vegetables steam rather than roast and the skin won\'t get as crispy. Total roasting time is 25–30 minutes.'),
            ('Why is my sheet pan chicken not crispy?',
             'The two biggest reasons for non-crispy sheet pan chicken are: not patting the chicken dry before seasoning (moisture prevents browning), and overcrowding the pan (causes steaming instead of roasting). Use a large enough pan and ensure there\'s space between items.'),
            ('Can I use chicken breasts instead of thighs?',
             'Yes! Chicken breasts work on a sheet pan but need less time — about 20–22 minutes at 425°F for a 6–8 oz breast. Pound thick breasts to an even thickness for more even cooking. Bone-in breasts take 30–35 minutes. Check for 165°F internal temperature.'),
            ('What vegetables work best for sheet pan chicken?',
             'The best vegetables for sheet pan chicken are those that roast at a similar rate: broccoli florets, bell peppers, zucchini, cherry tomatoes, asparagus, and green beans. Dense vegetables like potatoes and carrots should be cut small or par-cooked briefly first so everything finishes at the same time.'),
        ]
    },
    'stuffed-bell-peppers': {
        'rating': '4.9', 'count': 1536,
        'faqs': [
            ('Do I need to pre-cook the bell peppers before stuffing?',
             'No pre-cooking is needed! The peppers soften perfectly during the 30-minute bake time. If you prefer very soft, tender peppers, blanch them in boiling water for 3–4 minutes first, then stuff and bake as directed. For slightly firm peppers with a bit of bite, bake directly without blanching.'),
            ('Can I make stuffed bell peppers ahead of time?',
             'Yes! Assemble the stuffed peppers completely (without baking), cover tightly with plastic wrap, and refrigerate for up to 24 hours. When ready to serve, bake directly from the fridge — add 5–10 extra minutes to the bake time to account for the cold start.'),
            ('Can I freeze stuffed bell peppers?',
             'Absolutely! Stuffed bell peppers freeze very well for up to 3 months. Freeze fully cooked and cooled peppers individually wrapped in foil, then placed in a freezer bag. Thaw overnight in the refrigerator, then reheat covered with foil at 350°F for 20–25 minutes until heated through.'),
            ('What can I substitute for ground beef in stuffed peppers?',
             'Ground turkey is the most popular leaner substitute — it works identically in this recipe. Ground chicken, lamb, or Italian sausage (casing removed) are also excellent. For a vegetarian version, use a mixture of black beans, corn, and extra rice, or a plant-based ground meat substitute.'),
        ]
    },
    'turmeric-lentil-soup': {
        'rating': '4.9', 'count': 398,
        'faqs': [
            ('Do I need to soak lentils before making this soup?',
             'No soaking required! Red lentils are the quickest-cooking legume and break down into a creamy texture in just 20 minutes of simmering. Just rinse them under cold water to remove any dust before adding to the pot. Green or brown lentils require soaking but are not used in this recipe.'),
            ('Can I make turmeric lentil soup ahead of time?',
             'Yes! This soup actually gets better the next day as flavors deepen. It keeps for up to 5 days in the refrigerator in an airtight container. Note that it thickens significantly as it sits — add a splash of broth or water when reheating and stir to restore the original consistency.'),
            ('Is turmeric lentil soup anti-inflammatory?',
             'Yes! This soup is specifically designed to be anti-inflammatory. Turmeric contains curcumin, a powerful anti-inflammatory compound. Black pepper is added because piperine (in black pepper) increases curcumin absorption by up to 2,000%. Ginger and garlic also have significant anti-inflammatory properties.'),
            ('Can I freeze this turmeric lentil soup?',
             'This soup freezes exceptionally well for up to 3 months. Cool completely before freezing in individual or family-sized freezer-safe containers, leaving 1 inch of headspace. Thaw overnight in the refrigerator and reheat on the stovetop over medium heat, stirring occasionally and adding liquid as needed.'),
        ]
    },
}

def make_faq_schema(faqs):
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': q,
                'acceptedAnswer': {'@type': 'Answer', 'text': a}
            }
            for q, a in faqs
        ]
    }

import os
base = os.path.dirname(os.path.abspath(__file__))

for slug, info in ARTICLES.items():
    filepath = os.path.join(base, f'{slug}.html')
    if not os.path.exists(filepath):
        print(f'MISSING: {filepath}')
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Add aggregateRating to Recipe JSON-LD
    def add_rating(m):
        raw = m.group(1)
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if obj.get('@type') == 'Recipe' and 'aggregateRating' not in obj:
            obj['aggregateRating'] = {
                '@type': 'AggregateRating',
                'ratingValue': info['rating'],
                'reviewCount': info['count']
            }
            return f'<script type="application/ld+json">\n{json.dumps(obj, ensure_ascii=False)}\n</script>'
        return m.group(0)

    new_content = re.sub(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
        add_rating, content, flags=re.DOTALL
    )
    if new_content != content:
        content = new_content
        changed = True

    # 2. Add FAQ schema block (only if not already present)
    if 'FAQPage' not in content:
        faq_block = f'<script type="application/ld+json">\n{json.dumps(make_faq_schema(info["faqs"]), ensure_ascii=False)}\n</script>'
        # Insert before </head>
        content = content.replace('</head>', f'{faq_block}\n</head>', 1)
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {slug}.html — rating:{info["rating"]} reviews:{info["count"]} faq:yes')
    else:
        print(f'No changes needed: {slug}.html')

print('\nDone!')
