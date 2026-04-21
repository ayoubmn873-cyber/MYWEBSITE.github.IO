from fpdf import FPDF
import os

FONT_R = r"C:\Windows\Fonts\georgia.ttf"
FONT_B = r"C:\Windows\Fonts\georgiab.ttf"
FONT_I = r"C:\Windows\Fonts\georgiai.ttf"
FONT_C = r"C:\Windows\Fonts\calibri.ttf"
FONT_CB= r"C:\Windows\Fonts\calibrib.ttf"
FONT_E = r"C:\Windows\Fonts\seguiemj.ttf"

# ── Palette ────────────────────────────────────────────────
NAVY   = (15,  20,  40)
GOLD   = (212, 175, 55)
GOLD2  = (255, 215, 80)
CREAM  = (255, 252, 242)
WARM   = (250, 244, 228)
BROWN  = (101, 67,  33)
MID    = (110, 100, 80)
WHITE  = (255, 255, 255)
DKGOLD = (160, 120, 20)


class GoldBook(FPDF):
    def __init__(self):
        super().__init__()
        # Try Georgia first, fall back to Calibri
        try:
            self.add_font('Serif',  '',  FONT_R)
            self.add_font('Serif',  'B', FONT_B)
            self.add_font('Serif',  'I', FONT_I)
            self.serif = 'Serif'
        except Exception:
            self.add_font('Serif',  '',  FONT_C)
            self.add_font('Serif',  'B', FONT_CB)
            self.add_font('Serif',  'I', FONT_C)
            self.serif = 'Serif'
        self.add_font('Sans',   '',  FONT_C)
        self.add_font('Sans',   'B', FONT_CB)
        self.add_font('Emoji',  '',  FONT_E)
        self.set_fallback_fonts(['Emoji'])
        self._on_cover = True

    # ── header / footer ────────────────────────────────────
    def header(self):
        if self._on_cover:
            return
        # thin gold top bar
        self.set_fill_color(*GOLD)
        self.rect(0, 0, 210, 4, 'F')
        self.set_y(7)
        self.set_font('Sans', 'B', 7)
        self.set_text_color(*GOLD)
        self.cell(0, 5, "GRANDMA'S SECRETS OF DELICIOUS FOOD  ·  GOLD EDITION", align='C')
        self.set_draw_color(*GOLD)
        self.set_line_width(0.2)
        self.line(15, 13, 195, 13)

    def footer(self):
        if self._on_cover:
            return
        self.set_draw_color(*GOLD)
        self.set_line_width(0.2)
        self.line(15, 284, 195, 284)
        self.set_y(-13)
        self.set_font('Sans', '', 7.5)
        self.set_text_color(*MID)
        self.cell(95, 8, 'BinRecipes.com  ·  Premium Gold Edition')
        self.cell(95, 8, f'Page {self.page_no()}', align='R')

    # ── helpers ────────────────────────────────────────────
    def gold_rule(self, margin=15):
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.line(margin, self.get_y(), 210 - margin, self.get_y())
        self.ln(5)

    def chapter_page(self, num, emoji, title, subtitle, intro):
        """Full chapter opener page"""
        self._on_cover = False
        self.add_page()
        # dark background strip
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 80, 'F')
        # gold decorative lines
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        self.line(15, 18, 195, 18)
        self.line(15, 72, 195, 72)
        # chapter label
        self.set_font('Sans', 'B', 8)
        self.set_text_color(*GOLD)
        self.set_xy(0, 22)
        self.cell(210, 6, f'C H A P T E R   {num}', align='C')
        # emoji
        self.set_font('Emoji', '', 28)
        self.set_xy(0, 29)
        self.cell(210, 16, emoji, align='C')
        # title
        self.set_font('Serif', 'B', 26)
        self.set_text_color(*WHITE)
        self.set_xy(0, 45)
        self.cell(210, 14, title, align='C')
        # subtitle
        self.set_font('Serif', 'I', 11)
        self.set_text_color(*GOLD)
        self.set_xy(0, 60)
        self.cell(210, 10, subtitle, align='C')
        # intro paragraph
        self.set_y(90)
        self.set_x(20)
        self.set_font('Serif', 'I', 11)
        self.set_text_color(*BROWN)
        self.multi_cell(170, 7, intro)
        self.ln(4)
        self.gold_rule(20)

    def section_title(self, text):
        self.ln(5)
        self.set_font('Serif', 'B', 14)
        self.set_text_color(*NAVY)
        self.set_x(15)
        self.cell(0, 9, text)
        self.ln(10)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        self.line(15, self.get_y() - 3, 90, self.get_y() - 3)

    def body(self, text, size=10):
        self.set_font('Sans', '', size)
        self.set_text_color(*MID)
        self.set_x(15)
        self.multi_cell(180, 6.2, text)
        self.ln(3)

    def grandma_tip(self, text):
        """Gold-bordered grandma wisdom box"""
        self.ln(3)
        y = self.get_y()
        self.set_fill_color(*WARM)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        # draw temp rect (will redraw after measuring height)
        self.set_xy(15, y + 4)
        self.set_font('Sans', 'B', 9)
        self.set_text_color(*DKGOLD)
        self.cell(0, 5, "  Grandma's Wisdom")
        self.set_xy(15, y + 11)
        self.set_font('Serif', 'I', 9.5)
        self.set_text_color(*BROWN)
        y_start = self.get_y()
        self.multi_cell(175, 6, f'  "{text}"')
        y_end = self.get_y() + 4
        h = y_end - y
        # draw box behind
        self.rect(15, y, 180, h, 'FD')
        # gold left accent
        self.set_fill_color(*GOLD)
        self.rect(15, y, 3.5, h, 'F')
        # redraw text on top
        self.set_xy(21, y + 4)
        self.set_font('Sans', 'B', 9)
        self.set_text_color(*DKGOLD)
        self.cell(0, 5, "Grandma's Wisdom")
        self.set_xy(21, y + 11)
        self.set_font('Serif', 'I', 9.5)
        self.set_text_color(*BROWN)
        self.multi_cell(170, 6, f'"{text}"')
        self.set_y(y + h + 4)

    def recipe(self, title, meta, story, ingredients, steps, tip=None):
        """Full recipe card"""
        self.ln(4)
        # recipe title bar - navy
        self.set_fill_color(*NAVY)
        self.rect(15, self.get_y(), 180, 13, 'F')
        self.set_font('Serif', 'B', 13)
        self.set_text_color(*WHITE)
        self.set_x(19)
        self.cell(170, 13, title)
        self.ln(13)
        # gold meta bar
        self.set_fill_color(*GOLD)
        self.rect(15, self.get_y(), 180, 8, 'F')
        self.set_font('Sans', 'B', 8)
        self.set_text_color(*NAVY)
        self.set_x(19)
        self.cell(170, 8, meta)
        self.ln(10)
        # story / intro
        if story:
            self.set_font('Serif', 'I', 9.5)
            self.set_text_color(*BROWN)
            self.set_x(15)
            self.multi_cell(180, 6, story)
            self.ln(3)
        # ingredients
        self.set_font('Sans', 'B', 9)
        self.set_text_color(*DKGOLD)
        self.set_x(15)
        self.cell(0, 6, 'INGREDIENTS')
        self.ln(7)
        self.set_font('Sans', '', 9.5)
        self.set_text_color(*MID)
        for ing in ingredients:
            self.set_x(18)
            self.cell(5, 6, '·')
            self.multi_cell(172, 6, ing)
        self.ln(3)
        # instructions
        self.set_font('Sans', 'B', 9)
        self.set_text_color(*DKGOLD)
        self.set_x(15)
        self.cell(0, 6, 'INSTRUCTIONS')
        self.ln(7)
        for i, step in enumerate(steps, 1):
            # numbered circle
            self.set_fill_color(*GOLD)
            self.ellipse(15, self.get_y() + 0.5, 6, 6, 'F')
            self.set_font('Sans', 'B', 8)
            self.set_text_color(*NAVY)
            self.set_xy(15, self.get_y() + 0.5)
            self.cell(6, 6, str(i), align='C')
            self.set_font('Sans', '', 9.5)
            self.set_text_color(*MID)
            self.set_xy(24, self.get_y())
            self.multi_cell(171, 6, step)
            self.ln(1)
        if tip:
            self.grandma_tip(tip)
        self.ln(3)
        # thin gold divider
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.line(50, self.get_y(), 160, self.get_y())
        self.ln(5)

    def review_card(self, stars, text, name, location):
        self.ln(2)
        y = self.get_y()
        self.set_fill_color(*WARM)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.rect(15, y, 180, 30, 'FD')
        self.set_fill_color(*GOLD)
        self.rect(15, y, 4, 30, 'F')
        self.set_xy(22, y + 3)
        self.set_font('Sans', 'B', 10)
        self.set_text_color(*GOLD)
        self.cell(0, 5, stars)
        self.set_xy(22, y + 10)
        self.set_font('Serif', 'I', 9.5)
        self.set_text_color(*BROWN)
        self.multi_cell(168, 5.5, f'"{text}"')
        self.set_xy(22, y + 23)
        self.set_font('Sans', 'B', 8.5)
        self.set_text_color(*NAVY)
        self.cell(0, 5, f'{name}  ·  {location}')
        self.set_y(y + 33)


# ═══════════════════════════════════════════════════════════
pdf = GoldBook()
pdf.set_auto_page_break(auto=True, margin=24)
pdf.set_margins(15, 20, 15)


# ══════════════════════════════════════════════════════════
#  COVER PAGE
# ══════════════════════════════════════════════════════════
pdf._on_cover = True
pdf.add_page()

# full dark background
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, 210, 297, 'F')

# top gold ornament bar
pdf.set_fill_color(*GOLD)
pdf.rect(0, 0, 210, 6, 'F')
pdf.rect(0, 291, 210, 6, 'F')

# decorative gold border lines
pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.5)
pdf.rect(10, 10, 190, 277)
pdf.set_line_width(0.2)
pdf.rect(13, 13, 184, 271)

# GOLD EDITION badge
pdf.set_fill_color(*GOLD)
pdf.ellipse(155, 15, 42, 42, 'F')
pdf.set_font('Sans', 'B', 7.5)
pdf.set_text_color(*NAVY)
pdf.set_xy(155, 20)
pdf.cell(42, 5, 'PREMIUM', align='C')
pdf.set_font('Sans', 'B', 16)
pdf.set_xy(155, 26)
pdf.cell(42, 9, 'GOLD', align='C')
pdf.set_font('Sans', 'B', 8)
pdf.set_xy(155, 36)
pdf.cell(42, 5, 'EDITION', align='C')
pdf.set_font('Sans', '', 6.5)
pdf.set_text_color(60, 40, 0)
pdf.set_xy(155, 42)
pdf.cell(42, 4, '$9.99  VALUE', align='C')

# eyebrow text
pdf.set_font('Sans', 'B', 8)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 30)
pdf.cell(210, 6, 'B I N R E C I P E S . C O M   ·   P R E M I U M   C O L L E C T I O N', align='C')

# stars
pdf.set_font('Sans', 'B', 12)
pdf.set_text_color(*GOLD2)
pdf.set_xy(0, 38)
pdf.cell(210, 8, '★ ★ ★ ★ ★   Rated 5/5 by 1,200+ Home Cooks', align='C')

# decorative line
pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.6)
pdf.line(40, 50, 170, 50)

# main title
pdf.set_font('Serif', 'B', 18)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 54)
pdf.cell(210, 10, "G R A N D M A ' S", align='C')

pdf.set_font('Serif', 'B', 42)
pdf.set_text_color(*WHITE)
pdf.set_xy(0, 64)
pdf.cell(210, 22, 'SECRETS', align='C')

pdf.set_font('Serif', 'B', 20)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 86)
pdf.cell(210, 12, 'of Delicious Food', align='C')

# thin line
pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.4)
pdf.line(50, 101, 160, 101)

# subtitle
pdf.set_font('Serif', 'I', 11)
pdf.set_text_color(210, 200, 170)
pdf.set_xy(20, 105)
pdf.multi_cell(170, 7, 'Timeless recipes passed down through generations — the real secrets behind the most delicious home-cooked meals.', align='C')

# gold ornament divider
pdf.set_font('Sans', 'B', 14)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 124)
pdf.cell(210, 8, '— ✦ —', align='C')

# what's inside boxes
features = [
    ('35+', 'Family Recipes'),
    ('8',   'Chapters'),
    ('50+', 'Secret Tips'),
    ('30',  'Techniques'),
]
bx_y = 136
for i, (num, lbl) in enumerate(features):
    bx = 20 + i * 45
    pdf.set_fill_color(30, 35, 65)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.4)
    pdf.rect(bx, bx_y, 38, 28, 'FD')
    pdf.set_font('Serif', 'B', 22)
    pdf.set_text_color(*GOLD2)
    pdf.set_xy(bx, bx_y + 2)
    pdf.cell(38, 13, num, align='C')
    pdf.set_font('Sans', 'B', 7.5)
    pdf.set_text_color(200, 190, 160)
    pdf.set_xy(bx, bx_y + 16)
    pdf.cell(38, 8, lbl, align='C')

# benefit list
benefits = [
    '✦  35 exclusive family recipes never published online',
    '✦  The secret ingredient in every iconic dish — finally revealed',
    '✦  Grandma\'s personal tips written exactly as she taught them',
    '✦  Step-by-step techniques with zero guesswork',
    '✦  7-Day Family Dinner Plan included',
    '✦  Printable shopping list for every chapter',
]
y = 174
for b in benefits:
    pdf.set_font('Sans', '', 9.5)
    pdf.set_text_color(200, 195, 175)
    pdf.set_xy(30, y)
    pdf.cell(0, 7, b)
    y += 8

# divider
pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.4)
pdf.line(40, 228, 170, 228)

# author
pdf.set_font('Serif', 'I', 10)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 232)
pdf.cell(210, 7, 'Curated by the BinRecipes Family  ·  With love from our kitchen to yours', align='C')

# bottom branding
pdf.set_fill_color(*GOLD)
pdf.rect(0, 255, 210, 20, 'F')
pdf.set_font('Serif', 'B', 14)
pdf.set_text_color(*NAVY)
pdf.set_xy(0, 259)
pdf.cell(210, 7, 'BinRecipes.com', align='C')
pdf.set_font('Sans', '', 8)
pdf.set_xy(0, 267)
pdf.cell(210, 6, 'Premium Gold Edition  ·  binrecipes@gmail.com', align='C')


# ══════════════════════════════════════════════════════════
#  GRANDMA'S LETTER  (page 2)
# ══════════════════════════════════════════════════════════
pdf._on_cover = False
pdf.add_page()
pdf.ln(6)
pdf.set_font('Serif', 'B', 26)
pdf.set_text_color(*NAVY)
pdf.cell(0, 14, "A Letter from Grandma's Kitchen", align='C')
pdf.ln(2)
pdf.gold_rule()
pdf.ln(4)

pdf.set_font('Serif', 'I', 11)
pdf.set_text_color(*BROWN)
pdf.set_x(20)
pdf.multi_cell(170, 7.5,
    "My dear friend,\n\n"
    "Every recipe in this book carries a memory. The chicken soup that healed every cold. "
    "The Sunday pot roast that made the whole neighborhood knock on our door. "
    "The apple pie that my mother made, and her mother before her.\n\n"
    "For years people asked me: what is your secret? And I always smiled and said: "
    "it is just the recipe. But the truth is, the secrets are in the details — "
    "the pinch of this, the timing of that, the technique that nobody writes down "
    "because it was always just passed from hand to hand in a real kitchen.\n\n"
    "This book is my way of passing it to you. Every tip, every secret, every "
    "technique that makes the difference between a good meal and one that people "
    "talk about for years — it is all here.\n\n"
    "Cook with love. Taste everything. And never rush a good meal.\n\n"
    "With warmth,"
)
pdf.ln(4)
pdf.set_font('Serif', 'I', 16)
pdf.set_text_color(*DKGOLD)
pdf.set_x(20)
pdf.cell(0, 10, 'Grandma Rose  ✦')
pdf.ln(14)
pdf.gold_rule()
pdf.ln(6)

# quick stats
stats = [('35+','Recipes'), ('50+','Secret Tips'), ('8','Chapters'), ('1,200+','Happy Cooks')]
for i, (n, l) in enumerate(stats):
    bx = 15 + i * 46
    pdf.set_fill_color(*WARM)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.rect(bx, pdf.get_y(), 40, 22, 'FD')
    pdf.set_font('Serif', 'B', 20)
    pdf.set_text_color(*NAVY)
    pdf.set_xy(bx, pdf.get_y() + 2)
    pdf.cell(40, 11, n, align='C')
    pdf.set_font('Sans', '', 8)
    pdf.set_text_color(*MID)
    pdf.set_xy(bx, pdf.get_y() + 13)
    pdf.cell(40, 6, l, align='C')
pdf.ln(30)


# ══════════════════════════════════════════════════════════
#  TABLE OF CONTENTS
# ══════════════════════════════════════════════════════════
pdf.add_page()
pdf.ln(4)
pdf.set_font('Serif', 'B', 28)
pdf.set_text_color(*NAVY)
pdf.cell(0, 14, 'Table of Contents', align='C')
pdf.ln(2)
pdf.gold_rule()
pdf.ln(6)

chapters = [
    ('1', '🍲', 'Legendary Soups & Stews',        "Grandma's soul-warming classics — the recipes that heal"),
    ('2', '🍗', 'Sunday Roasts & Chicken',         'The centerpiece of every great family gathering'),
    ('3', '🥧', 'Pies, Cobblers & Baked Goods',   'Buttery, flaky, golden — American baking at its finest'),
    ('4', '🍞', 'Homemade Breads & Biscuits',      'The smell of fresh bread — nothing compares'),
    ('5', '🥘', 'Slow-Cooked Comfort Food',        'Low, slow, and deeply delicious — the Sunday tradition'),
    ('6', '🥗', 'Salads & Sides That Shine',       'The sides everyone always asks for the recipe for'),
    ('7', '🍰', 'Cakes, Cookies & Sweet Memories', 'Desserts that bring everyone back to childhood'),
    ('8', '🔐', "Grandma's Secret Sauces",         'The finishing touches that make everything taste better'),
]

for num, em, title, desc in chapters:
    y = pdf.get_y()
    pdf.set_fill_color(*WARM)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.2)
    pdf.rect(15, y, 180, 17, 'FD')
    pdf.set_fill_color(*GOLD)
    pdf.rect(15, y, 4, 17, 'F')
    pdf.set_font('Sans', 'B', 8)
    pdf.set_text_color(*NAVY)
    pdf.set_xy(22, y + 2.5)
    pdf.cell(12, 5, f'Ch. {num}')
    pdf.set_font('Serif', 'B', 11)
    pdf.set_text_color(*NAVY)
    pdf.set_xy(36, y + 2.5)
    pdf.cell(0, 5, f'{em}  {title}')
    pdf.set_font('Serif', 'I', 8.5)
    pdf.set_text_color(*MID)
    pdf.set_xy(36, y + 9.5)
    pdf.cell(0, 5, desc)
    pdf.set_y(y + 19)

pdf.ln(6)
pdf.set_font('Serif', 'I', 10)
pdf.set_text_color(*DKGOLD)
pdf.cell(0, 7, '✦  All recipes passed down through real family kitchens  ✦', align='C')


# ══════════════════════════════════════════════════════════
#  CHAPTER 1 — SOUPS & STEWS
# ══════════════════════════════════════════════════════════
pdf.chapter_page('1', '🍲', 'Legendary Soups & Stews',
    '"A good soup is the cure for everything"',
    "There is a reason soup appears in every culture's home cooking tradition. "
    "It is forgiving, nourishing, and deeply personal. Grandma Rose always said that "
    "the secret to a great soup is time — you cannot rush a good broth. "
    "These are the recipes she made when someone was sick, sad, or just very hungry.")

pdf.recipe('🍲  Grandma\'s Famous Chicken Noodle Soup',
    'Prep: 20 min  ·  Cook: 2.5 hours  ·  Serves: 8  ·  Easy',
    '"This is the soup. The one people call me about. The secret is roasting the chicken bones first and adding the vegetables in stages — not all at once."',
    ['1 whole chicken (4 lb), OR 3 lb bone-in thighs + 2 lb backs',
     '3 large carrots, cut in thick coins',
     '4 celery stalks, sliced including the leafy tops',
     '1 large yellow onion, quartered',
     '5 garlic cloves, smashed',
     '1 parsnip, sliced (the secret ingredient)',
     '10 cups cold water',
     '2 bay leaves, 8 peppercorns, 4 sprigs fresh thyme',
     '2 tsp kosher salt (plus more to finish)',
     '3 cups wide egg noodles',
     'Fresh dill and flat-leaf parsley to finish'],
    ['Place chicken in a large pot. Cover with cold water. Bring to a boil, then immediately pour off all water. This step removes impurities and gives you a crystal-clear broth.',
     'Return chicken to pot with 10 fresh cups of cold water. Add onion, garlic, bay leaves, peppercorns, and thyme. Bring to a gentle simmer. Never a hard boil.',
     'Skim any foam that rises in the first 20 minutes. Add 2 tsp salt. Simmer very gently 1 hour 30 minutes.',
     'Remove chicken. When cool enough to handle, shred all meat off the bones. Discard bones, skin, and aromatics.',
     'Strain broth through a fine mesh sieve. Return clear broth to pot. Taste — it should be deeply savory.',
     'Add fresh carrots, celery, parsnip, and a big pinch of salt. Simmer 20 minutes until tender.',
     'Add egg noodles and cook according to package — usually 8 minutes.',
     'Return shredded chicken. Finish with a generous handful of fresh dill and parsley. Taste and add salt.'],
    'Never let chicken soup boil hard — it makes the broth cloudy and the chicken tough. Low and gentle is the way. The parsnip is the secret — it adds a sweetness no other vegetable can replicate.')

pdf.recipe('🥣  Old-Fashioned Beef & Vegetable Stew',
    'Prep: 20 min  ·  Cook: 2 hours  ·  Serves: 6  ·  Easy',
    '"The trick is not the recipe — it is the patience. Brown the beef properly, layer the vegetables, and never lift the lid."',
    ['2 lb beef chuck, cut in 1.5-inch cubes',
     '3 tbsp all-purpose flour + 1 tsp smoked paprika',
     '3 tbsp olive oil',
     '1 large onion, roughly diced',
     '3 garlic cloves, minced',
     '2 tbsp tomato paste',
     '1 cup red wine (or extra beef broth)',
     '3 cups beef broth',
     '4 Yukon gold potatoes, cubed',
     '3 large carrots, thick slices',
     '2 parsnips, thick slices',
     '1 sprig rosemary, 2 bay leaves'],
    ['Toss beef cubes with flour, paprika, salt, and pepper until well coated.',
     'Heat oil in a Dutch oven over HIGH heat. Brown beef in 2 batches, 4 min per side. Do not rush. Set aside.',
     'Same pot: cook onion 5 min. Add garlic and tomato paste. Cook 2 min, stirring.',
     'Add wine. Scrape every bit from the bottom — this is pure flavor.',
     'Add broth, rosemary, bay leaves, and browned beef. Bring to simmer. Cover.',
     'Cook on low heat 1 hour. Add potatoes, carrots, and parsnips.',
     'Cover and cook 45 more minutes until everything is completely tender.',
     'Remove bay leaves and rosemary. Taste. Adjust salt. Serve with crusty bread.'],
    'Adding flour directly to the beef before browning serves two purposes: it creates a beautiful crust AND it thickens the stew naturally as it cooks. Never add flour to the liquid — always coat the meat.')

pdf.grandma_tip('For any soup or stew, always make it a day ahead if you can. The flavors develop and deepen overnight in the refrigerator in a way that simply cannot happen in one day. Next-day soup is always better soup.')


# ══════════════════════════════════════════════════════════
#  CHAPTER 2 — ROASTS & CHICKEN
# ══════════════════════════════════════════════════════════
pdf.chapter_page('2', '🍗', 'Sunday Roasts & Chicken',
    '"Sunday dinner is not a meal — it is a ritual"',
    "In Grandma Rose's house, Sunday meant the whole family at the table. "
    "No phones, no rushing. The smell of something roasting in the oven from 2 PM "
    "told everyone: come home. These are those recipes.")

pdf.recipe('🍗  The Perfect Roast Chicken',
    'Prep: 15 min  ·  Dry brine: overnight  ·  Roast: 1 hour 15 min  ·  Serves: 4  ·  Easy',
    '"I have made this chicken every Sunday for forty years. The overnight salt is non-negotiable. Do not skip it."',
    ['1 whole chicken (4-4.5 lb), patted completely dry',
     '1 tbsp kosher salt (for dry brine)',
     '1 tsp black pepper',
     '1 tsp garlic powder',
     '1 tsp dried thyme',
     '3 tbsp unsalted butter, softened',
     '1 lemon, halved',
     '1 whole head of garlic, halved crosswise',
     '4 sprigs fresh thyme',
     '1 onion, quartered (for the roasting pan)'],
    ['THE NIGHT BEFORE: Mix salt, pepper, garlic powder, and dried thyme. Rub all over the outside AND under the skin over the breasts. Place on a rack in the refrigerator uncovered overnight. This dry brine is the secret.',
     'Remove chicken from fridge 45 minutes before roasting. Preheat oven to 425°F.',
     'Rub softened butter all over the outside and generously under the skin.',
     'Stuff the cavity with lemon halves, garlic head, and fresh thyme. Do not truss.',
     'Place onion quarters in the roasting pan. Set chicken on top breast-side up.',
     'Roast at 425°F for 20 minutes, then reduce to 375°F for 50-55 minutes.',
     'Chicken is done when thigh juices run clear and internal temp reaches 165°F.',
     'REST 15 full minutes before carving. This step is absolutely mandatory.'],
    'The overnight dry brine does three things: seasons deeply, tightens the skin for better crisping, and keeps the meat incredibly juicy. Wet brining adds water to the bird. Dry brining concentrates the flavor.')

pdf.recipe('🥩  Classic Sunday Pot Roast with Pan Gravy',
    'Prep: 20 min  ·  Cook: 3.5 hours  ·  Serves: 6-8  ·  Easy',
    '"The pot roast is done when you can pull it apart with just your fingers. Not with a fork — with your fingers."',
    ['3.5 lb beef chuck roast',
     '2 tsp kosher salt + 1 tsp black pepper',
     '2 tbsp vegetable oil',
     '2 large onions, roughly cut',
     '6 garlic cloves',
     '3 tbsp tomato paste',
     '1 cup dry red wine',
     '2 cups beef broth',
     '4 large carrots',
     '1 lb baby potatoes',
     '2 sprigs rosemary, 3 bay leaves',
     '2 tbsp butter + 2 tbsp flour (for gravy)'],
    ['Preheat oven to 300°F. Dry roast completely, season all surfaces.',
     'Heat oil in Dutch oven over very high heat. Sear ALL surfaces of the roast until deeply browned — 3 min per side. Do not rush. This is where the flavor comes from.',
     'Cook onions 5 min in the same fat. Add garlic and tomato paste. Cook 2 min.',
     'Add wine, scrape the pan clean. Add broth, rosemary, bay leaves.',
     'Return roast. Cover tightly. Place in 300°F oven.',
     'After 2 hours, add carrots and potatoes around the roast. Cover again.',
     'After 3.5 total hours, test by pulling with fingers. If it resists, cook 30 more min.',
     'Remove roast and vegetables. For gravy: heat braising liquid on stovetop. Mix butter and flour into a paste. Whisk into simmering liquid until thick. Season generously.'])


# ══════════════════════════════════════════════════════════
#  CHAPTER 3 — PIES & BAKED GOODS
# ══════════════════════════════════════════════════════════
pdf.chapter_page('3', '🥧', 'Pies, Cobblers & Baked Goods',
    '"A homemade pie is the highest form of hospitality"',
    "Grandma Rose won the county fair pie contest eleven years in a row. "
    "Her secret was simple: real butter, cold hands, and respect for the dough. "
    "These are her exact recipes.")

pdf.recipe('🥧  Grandma\'s Blue Ribbon Apple Pie',
    'Prep: 30 min  ·  Chill: 1 hour  ·  Bake: 60 min  ·  Serves: 8',
    '"People ask me every year what makes this pie different. The answer is the apples — always Granny Smith and Honeycrisp together, never one alone."',
    ['For the crust: 2.5 cups flour, 1 tsp salt, 1 tsp sugar, 1 cup COLD butter (cubed), 6-8 tbsp ice water',
     '3 Granny Smith apples, peeled, cored, sliced ¼-inch thick',
     '3 Honeycrisp apples, same preparation',
     '¾ cup granulated sugar',
     '¼ cup light brown sugar, packed',
     '3 tbsp cornstarch',
     '1½ tsp cinnamon, ¼ tsp nutmeg, pinch of cloves',
     '1 tbsp lemon juice + 1 tsp lemon zest',
     '2 tbsp unsalted butter, cut in small pieces',
     '1 egg + 1 tbsp cream (for egg wash)',
     '1 tbsp coarse sugar (for top crust)'],
    ['CRUST: Freeze butter cubes 15 min. Whisk flour, salt, sugar. Cut in butter until pea-sized. Add ice water 1 tbsp at a time until dough just holds. Divide, form 2 discs, wrap and refrigerate 1 hour minimum.',
     'FILLING: Toss all apple slices with both sugars, cornstarch, spices, lemon juice and zest. Let sit 15 min — do not skip this. It draws out excess moisture.',
     'Roll bottom crust into a 12-inch circle. Fit into 9-inch pie plate. Refrigerate while making top.',
     'Fill pie shell with apples, mounding in center. Dot with butter pieces.',
     'Roll top crust. Lay over filling. Trim leaving ¾-inch overhang. Fold and crimp edges firmly.',
     'Cut 5-6 steam vents. Brush with egg wash. Sprinkle coarse sugar generously.',
     'Place on a baking sheet. Bake at 425°F for 20 min, then 375°F for 40-45 min until deeply golden and filling is bubbling through vents.',
     'CRITICAL: Cool at least 3 hours before cutting. The filling is liquid when hot and sets as it cools.'],
    'Mixing two apple varieties is the key. Granny Smith holds its shape and provides tartness. Honeycrisp adds sweetness and a tender texture. Using one variety alone gives you either mush or jaw-breaking chunks.')

pdf.grandma_tip('The vodka trick: replace 2 tablespoons of the ice water with ice-cold vodka. Alcohol does not develop gluten like water, giving you the most tender, most flaky crust you have ever made. The alcohol evaporates completely during baking.')

pdf.recipe('🫐  Summer Blueberry Cobbler',
    'Prep: 10 min  ·  Bake: 40 min  ·  Serves: 8  ·  Easy',
    '"The cobbler crust pours on top as a batter — it rises up through the fruit as it bakes. It looks like magic every single time."',
    ['4 cups fresh blueberries (or frozen, thawed)',
     '¾ cup sugar + 1 tbsp lemon juice (for fruit)',
     '1 cup all-purpose flour',
     '1 cup sugar',
     '1 cup whole milk',
     '½ cup (1 stick) unsalted butter, melted',
     '1½ tsp baking powder',
     '½ tsp salt',
     '1 tsp pure vanilla extract'],
    ['Preheat oven to 350°F. Pour melted butter into a 9x13 baking dish.',
     'Toss blueberries with ¾ cup sugar and lemon juice in a bowl. Set aside.',
     'Whisk together flour, 1 cup sugar, milk, vanilla, baking powder, and salt until smooth.',
     'Pour batter directly over the butter in the dish. Do NOT stir.',
     'Spoon blueberries and all their juices over the batter. Do NOT stir.',
     'Bake 40-45 minutes until golden brown and set. The batter rises up around the fruit.',
     'Serve warm with a big scoop of vanilla ice cream.'])


# ══════════════════════════════════════════════════════════
#  CHAPTER 4 — BREADS & BISCUITS
# ══════════════════════════════════════════════════════════
pdf.chapter_page('4', '🍞', 'Homemade Breads & Biscuits',
    '"A house that smells of fresh bread is a happy house"',
    "There is nothing in the world like the smell of bread baking. "
    "Grandma Rose baked bread every Thursday morning without exception for sixty years. "
    "She said it kept her sane and her family fed. These are her exact recipes.")

pdf.recipe('🍞  Grandma\'s White Sandwich Bread',
    'Prep: 20 min  ·  Rise: 2 hours  ·  Bake: 30 min  ·  Makes: 2 loaves',
    '"My sandwich bread. It toasts perfectly, makes the best French toast, and it never lasts more than one day in this house."',
    ['3 cups warm water (110°F — should feel warm on your wrist)',
     '2 packets (4½ tsp) active dry yeast',
     '3 tbsp honey or sugar',
     '3 tbsp neutral oil',
     '1½ tsp fine salt',
     '6-6.5 cups bread flour (not all-purpose)',
     'Softened butter for the pans and top of loaves'],
    ['Combine warm water, yeast, and honey in a large bowl. Wait exactly 5-7 minutes until foamy. If it does not foam, your yeast is dead — start over with fresh yeast.',
     'Add oil, salt, and 3 cups of flour. Mix until combined. Add remaining flour 1 cup at a time, mixing until dough pulls away from the bowl.',
     'Turn onto a floured surface. Knead vigorously 8-10 minutes until smooth, elastic, and slightly tacky (not sticky). It should pass the windowpane test.',
     'Place in an oiled bowl. Cover with a damp towel. Rise in a warm spot 1 hour until doubled.',
     'Punch down. Divide in half. Shape each into a tight log. Place in buttered 9x5 loaf pans.',
     'Cover and rise 45-60 minutes until dough crowns about 1 inch above the pan rim.',
     'Bake at 375°F for 28-32 minutes until deep golden and hollow-sounding when tapped.',
     'Brush tops immediately with softened butter. Cool in pans 10 min then on a rack.'],
    'The windowpane test tells you when bread dough is properly kneaded: stretch a small piece between your fingers. If it stretches thin enough to see light through without tearing, the gluten is fully developed and your bread will have a perfect structure.')

pdf.recipe('🧈  Southern Drop Biscuits',
    'Prep: 8 min  ·  Bake: 14 min  ·  Makes: 12 biscuits  ·  Easy',
    '"Drop biscuits are for when you need something incredible in 20 minutes. No rolling, no cutting — just drop and bake."',
    ['2 cups all-purpose flour',
     '1 tbsp baking powder',
     '1 tsp sugar, ½ tsp salt',
     '½ tsp baking soda',
     '6 tbsp very cold butter, grated on a box grater',
     '1 cup cold buttermilk',
     '3 tbsp melted butter (for brushing)'],
    ['Preheat oven to 450°F. Line a baking sheet with parchment.',
     'Whisk all dry ingredients together.',
     'Add grated frozen butter. Toss quickly with your fingers until it looks like coarse sand.',
     'Add buttermilk all at once. Stir with a fork until JUST combined — 10 strokes maximum.',
     'Drop by large spoonfuls onto prepared baking sheet, 2 inches apart.',
     'Bake 12-14 minutes until tall and deep golden.',
     'Brush immediately with melted butter. Serve within 10 minutes.'],
    'Grating frozen butter instead of cutting it in gives you perfectly even distribution in half the time. Freeze your butter stick for 15 minutes, then grate it directly into the flour. Works every time.')


# ══════════════════════════════════════════════════════════
#  CHAPTER 5 — SLOW-COOKED COMFORT FOOD
# ══════════════════════════════════════════════════════════
pdf.chapter_page('5', '🥘', 'Slow-Cooked Comfort Food',
    '"The longer it cooks, the more it loves you back"',
    "These are the recipes you start in the morning and come home to in the evening. "
    "The house smells incredible. The meat is falling apart. "
    "Everyone sits down without being asked. That is the magic of slow cooking.")

pdf.recipe('🥘  All-Day Slow Cooker Beef Brisket',
    'Prep: 15 min  ·  Cook: 8-10 hours  ·  Serves: 8  ·  Easy',
    '"Put it in before you leave for work. Come home to the best dinner of the week."',
    ['4 lb beef brisket, flat cut',
     'Dry rub: 2 tsp salt, 1 tsp pepper, 1 tsp garlic powder, 1 tsp onion powder, 1 tsp smoked paprika, ½ tsp cumin',
     '1 large onion, sliced in rings',
     '4 garlic cloves',
     '1 cup beef broth',
     '½ cup ketchup',
     '2 tbsp Worcestershire sauce',
     '2 tbsp brown sugar',
     '1 tbsp apple cider vinegar'],
    ['Mix all dry rub ingredients. Rub all over the brisket generously. If time allows, refrigerate overnight.',
     'Lay onion rings in the bottom of the slow cooker. Place brisket fat-side up on top.',
     'Mix broth, ketchup, Worcestershire, brown sugar, and vinegar. Pour over brisket.',
     'Cook on LOW 8-10 hours. Do not open the lid during cooking.',
     'Remove brisket carefully — it will be extremely tender. Slice against the grain.',
     'Skim fat from cooking liquid. Taste and season. Serve as sauce over sliced brisket.'],
    'Always slice brisket AGAINST the grain — cutting perpendicular to the muscle fibers. Slicing with the grain gives you long, tough, chewy pieces. Look at the meat before you cut and identify which direction the fibers run.')

pdf.recipe('🍲  Creamy White Bean & Ham Soup',
    'Prep: 10 min  ·  Cook: 3 hours  ·  Serves: 8  ·  Easy',
    '"This is what you make with the leftover ham bone after Christmas. Grandma saved every bone — she said throwing away a ham bone was a sin."',
    ['1 leftover ham bone with meat attached (OR 2 smoked ham hocks)',
     '1 lb dried Great Northern or navy beans, soaked overnight',
     '1 large onion, diced',
     '4 celery stalks, diced',
     '4 garlic cloves, minced',
     '3 carrots, diced',
     '8 cups water or unsalted chicken broth',
     '2 bay leaves',
     '1 tsp dried thyme',
     'Salt and pepper to finish',
     'Fresh parsley and good crusty bread to serve'],
    ['Drain and rinse soaked beans.',
     'Place ham bone, beans, onion, celery, garlic, carrots, and bay leaves in a large pot.',
     'Cover with 8 cups water or broth. Bring to a boil.',
     'Reduce heat, cover, and simmer 2.5-3 hours until beans are completely tender.',
     'Remove ham bone. Pull all meat off the bone, shred it, return to pot.',
     'Using a potato masher, mash about 1 cup of beans against the side of the pot to thicken the broth naturally.',
     'Add thyme. Taste — the ham is very salty, you likely need no added salt.',
     'Serve in deep bowls with crusty bread and fresh parsley.'])


# ══════════════════════════════════════════════════════════
#  CHAPTER 6 — SALADS & SIDES
# ══════════════════════════════════════════════════════════
pdf.chapter_page('6', '🥗', 'Salads & Sides That Shine',
    '"The sides are what people remember"',
    "Everyone always remembers the main course. But the sides? "
    "The sides are what people request for years. "
    "These are Grandma Rose's side dishes — the ones that always disappeared first.")

pdf.recipe('🥗  Classic American Potato Salad',
    'Prep: 20 min  ·  Cook: 20 min  ·  Chill: 2 hours  ·  Serves: 8',
    '"The secret is two things: season the potatoes while they are still hot, and use both mayonnaise AND a splash of apple cider vinegar."',
    ['3 lb Yukon Gold potatoes, cubed (unpeeled is fine)',
     '2 tsp salt (for boiling water)',
     '3 tbsp apple cider vinegar (divided)',
     '1 tsp sugar',
     '1 cup good mayonnaise (Duke\'s or Hellmann\'s)',
     '2 tbsp yellow mustard',
     '3 celery stalks, finely diced',
     '5 green onions, thinly sliced',
     '4 hard-boiled eggs, roughly chopped',
     'Salt, black pepper, and sweet paprika to finish'],
    ['Boil potatoes in well-salted water until just tender, about 15 min. Drain.',
     'IMMEDIATELY while still hot: drizzle potatoes with 2 tbsp vinegar and 1 tsp sugar. Toss gently. Let cool.',
     'Mix mayo, mustard, and remaining 1 tbsp vinegar in a large bowl.',
     'Add cooled potatoes, celery, green onions, and chopped eggs.',
     'Fold gently — you want chunks, not mash.',
     'Taste and adjust salt and pepper.',
     'Refrigerate minimum 2 hours. The flavor develops significantly as it chills.',
     'Dust with paprika before serving.'],
    'Hot potatoes absorb the vinegar and sugar like a sponge — this is the step that gives your potato salad that addictive tangy depth. Cold potatoes just sit in the dressing. Season hot, dress cold.')

pdf.recipe('🧀  Creamy Baked Mac & Cheese',
    'Prep: 20 min  ·  Bake: 25 min  ·  Serves: 8',
    '"I have tried every mac and cheese recipe. This is the only one where people always ask for thirds."',
    ['1 lb elbow macaroni',
     '5 tbsp unsalted butter',
     '5 tbsp all-purpose flour',
     '3 cups whole milk (warm)',
     '1 cup heavy cream',
     '2 cups sharp cheddar, freshly grated',
     '1 cup Gruyere or fontina, freshly grated',
     '½ cup Parmesan, freshly grated',
     '1 tsp dry mustard powder',
     '½ tsp smoked paprika',
     '½ tsp garlic powder',
     'Salt, white pepper',
     'Topping: ½ cup panko + 2 tbsp butter + ¼ cup Parmesan'],
    ['Cook pasta 2 minutes LESS than package directions. It will finish in the oven. Drain.',
     'Melt butter in large saucepan over medium heat. Add flour. Cook 2 minutes, stirring — it should smell nutty.',
     'Add warm milk and cream gradually, whisking constantly. Cook until thick enough to coat a spoon.',
     'Remove from heat. Add mustard powder, paprika, garlic powder, and all cheeses except topping Parmesan. Stir until melted.',
     'Season generously with salt and white pepper. Taste — it should be slightly over-seasoned.',
     'Combine pasta with cheese sauce. Transfer to a buttered 9x13 dish.',
     'Mix panko with melted butter and Parmesan. Spread evenly over the top.',
     'Bake at 375°F for 25 minutes until bubbling and golden brown.'],
    'ALWAYS grate your own cheese. Pre-shredded cheese contains anti-caking starch that prevents it from melting smoothly. The difference is a silky vs. gritty sauce. Grating takes 3 extra minutes and makes an enormous difference.')


# ══════════════════════════════════════════════════════════
#  CHAPTER 7 — CAKES, COOKIES & DESSERTS
# ══════════════════════════════════════════════════════════
pdf.chapter_page('7', '🍰', 'Cakes, Cookies & Sweet Memories',
    '"Dessert is not the end of a meal — it is the memory you take home"',
    "Grandma Rose kept a cake on the counter every single day of her life. "
    "She believed a house with no cake is a house that is not quite ready for company. "
    "Here are the recipes that made her famous in the neighborhood.")

pdf.recipe('🎂  Grandma\'s Yellow Butter Cake',
    'Prep: 20 min  ·  Bake: 32 min  ·  Serves: 12',
    '"The simplest cake. The most requested cake. The one I have made for every birthday in this family for forty years."',
    ['3 cups all-purpose flour',
     '2 tsp baking powder',
     '½ tsp salt',
     '1 cup (2 sticks) unsalted butter, room temperature',
     '2 cups granulated sugar',
     '4 large eggs, room temperature',
     '1 cup whole milk, room temperature',
     '2 tsp pure vanilla extract',
     'For frosting: 1 cup butter, 4 cups powdered sugar, 3 tbsp heavy cream, 2 tsp vanilla, pinch of salt'],
    ['Preheat oven to 350°F. Butter and flour two 9-inch round cake pans.',
     'Whisk flour, baking powder, and salt together. Set aside.',
     'Beat butter with sugar on medium-high speed 4-5 minutes until genuinely pale and fluffy. This step is critical.',
     'Add eggs one at a time, beating well after each. Add vanilla.',
     'Add flour mixture in 3 additions, alternating with milk in 2 additions. Start and end with flour. Mix only until just combined.',
     'Divide evenly between pans. Bake 30-32 minutes until a toothpick comes out clean.',
     'Cool in pans 10 min, then turn out onto wire racks. Cool COMPLETELY before frosting.',
     'FROSTING: Beat butter until pale. Add powdered sugar gradually. Add cream, vanilla, and salt. Beat 3 min until light.'],
    'The creaming step — beating butter and sugar until pale and fluffy — is where most home cooks rush. Set a timer for 4 minutes and let the mixer run. Proper creaming incorporates air bubbles that give your cake its lift and delicate crumb.')

pdf.recipe('🍪  The Perfect Chocolate Chip Cookie',
    'Prep: 15 min  ·  Chill: 24 hours  ·  Bake: 11 min  ·  Makes: 24 cookies',
    '"My cookies were ordinary until I started chilling the dough overnight. Now they are the first thing to disappear at every party."',
    ['2¼ cups all-purpose flour',
     '1 tsp baking soda',
     '1 tsp fine salt',
     '1 cup (2 sticks) unsalted butter — melted AND browned',
     '¾ cup granulated sugar',
     '1 cup packed light brown sugar',
     '2 large eggs + 1 egg yolk',
     '2 tsp vanilla extract',
     '2 cups semi-sweet chocolate chips OR chopped dark chocolate',
     'Flaky sea salt for topping (Maldon or fleur de sel)'],
    ['BROWN THE BUTTER: Melt butter in a saucepan over medium heat, swirling often. It will foam, then smell nutty, then turn amber with brown specks. Pour immediately into a bowl. Cool 20 minutes.',
     'Whisk both sugars into browned butter. Add eggs, egg yolk, and vanilla. Whisk vigorously 2 minutes.',
     'Add flour, baking soda, and salt. Fold until just combined.',
     'Fold in chocolate. Cover and refrigerate 24-72 hours (minimum overnight).',
     'Scoop into balls. Place on a parchment-lined sheet. Sprinkle with flaky sea salt.',
     'Bake at 375°F for 10-12 minutes until edges are set but centers look underdone.',
     'Let cool 10 minutes on the pan — they firm up as they cool.'],
    'Brown butter and 24-hour chill are the two secrets. Brown butter adds a toasty, nutty, butterscotch depth that no other cookie has. The overnight chill dries out the dough slightly, concentrating flavor and creating a chewier texture.')


# ══════════════════════════════════════════════════════════
#  CHAPTER 8 — SECRET SAUCES
# ══════════════════════════════════════════════════════════
pdf.chapter_page('8', '🔐', "Grandma's Secret Sauces",
    '"The sauce is where the magic lives"',
    "Grandma Rose said you can take a mediocre dish and make it extraordinary "
    "with the right sauce. And she was right. "
    "These are the secret finishes — passed down exactly as they were taught.")

pdf.section_title("The Pan Sauce — The Professional's Secret")
pdf.body(
    "Every time you sear meat in a pan, you leave behind incredible flavor stuck to the bottom — "
    "called 'fond'. A pan sauce takes 3 minutes and transforms that flavor into something extraordinary.\n\n"
    "THE METHOD:\n"
    "1.  Remove meat from pan. Pour off excess fat, leaving 1-2 tbsp.\n"
    "2.  Add aromatics (minced shallots or garlic). Cook 30 seconds.\n"
    "3.  Add liquid (wine, broth, or brandy). Scrape EVERY bit from the bottom.\n"
    "4.  Simmer until reduced by half — about 2-3 minutes.\n"
    "5.  Add a splash of cream or a knob of cold butter. Swirl to emulsify.\n"
    "6.  Season. Taste. Pour over your meat immediately.\n\n"
    "Variations:\n"
    "  · Red wine + beef broth + thyme = steak\n"
    "  · White wine + chicken broth + lemon + capers = chicken\n"
    "  · Brandy + cream + green peppercorns = pork"
)
pdf.grandma_tip('Never wash your pan between searing the meat and making the sauce. Those browned bits at the bottom are the entire point. Dissolving them in liquid — called deglazing — is where the sauce comes from.')

pdf.section_title("Grandma's Classic Tomato Sauce")
pdf.body(
    "INGREDIENTS: 3 tbsp olive oil  ·  6 garlic cloves, thinly sliced  ·  "
    "2 cans (28 oz each) whole San Marzano tomatoes  ·  1 tsp sugar  ·  "
    "salt  ·  10 fresh basil leaves  ·  3 tbsp good olive oil (to finish)\n\n"
    "METHOD: Heat oil over medium-low. Cook garlic slowly until golden — about 6 minutes. "
    "Add tomatoes, crushing them by hand as they go in. Add sugar and 1 tsp salt. "
    "Simmer uncovered 25-30 minutes until thickened. Tear in basil. "
    "Drizzle with good olive oil. Taste and adjust salt.\n\n"
    "THE SECRET: Slow-cooked garlic in oil, not sautéed garlic. Low and slow caramelizes the "
    "sugars and removes the sharpness. It takes 3 extra minutes and changes everything."
)
pdf.grandma_tip('Add a Parmesan rind to the sauce while it simmers. The rind dissolves slowly and releases a deep, savory, umami richness that people can taste but cannot identify. They just know the sauce tastes extraordinary. Remove the rind before serving.')

pdf.section_title("The Everyday Vinaigrette")
pdf.body(
    "INGREDIENTS: 1 small shallot (minced)  ·  1 tsp Dijon mustard  ·  "
    "3 tbsp red wine vinegar  ·  ½ tsp honey  ·  salt + pepper  ·  "
    "½ cup extra-virgin olive oil\n\n"
    "METHOD: Whisk shallot, mustard, vinegar, honey, salt, and pepper. "
    "While whisking constantly, slowly drizzle in oil until emulsified and creamy. "
    "Taste — it should be tangy and punchy. Season generously.\n\n"
    "KEEPS: 1 week in the refrigerator. Shake before using.\n\n"
    "THE SECRET: The Dijon mustard acts as an emulsifier — it bonds the oil and vinegar "
    "together so they do not separate immediately. This is what makes a vinaigrette creamy "
    "instead of watery."
)


# ══════════════════════════════════════════════════════════
#  REVIEWS PAGE
# ══════════════════════════════════════════════════════════
pdf.add_page()
pdf.ln(4)
pdf.set_font('Serif', 'B', 26)
pdf.set_text_color(*NAVY)
pdf.cell(0, 14, 'What Our Readers Are Saying', align='C')
pdf.ln(2)
pdf.gold_rule()
pdf.ln(2)
pdf.set_font('Serif', 'I', 10)
pdf.set_text_color(*MID)
pdf.cell(0, 7, 'Over 1,200 five-star reviews from home cooks across the United States', align='C')
pdf.ln(8)

reviews = [
    ('★★★★★', "I made Grandma Rose's chicken noodle soup when my daughter was sick and she told me it was the best thing she had ever eaten. I cried. This cookbook is a treasure.", 'Jennifer Crawford', 'Portland, Oregon'),
    ('★★★★★', "The butter cake has been on my counter every Sunday for three months. My family refuses to go back to store-bought anything. Worth every single penny.", 'Michael Thompson', 'Birmingham, Alabama'),
    ('★★★★★', "I have been cooking for 25 years and I learned new things from this book. The pan sauce chapter alone changed how I cook dinner every night.", 'Carol Peterson', 'Madison, Wisconsin'),
    ('★★★★★', "Made the Sunday pot roast for my in-laws. My mother-in-law asked me for the recipe. That has never happened in 15 years of marriage.", 'Amanda Rodriguez', 'San Antonio, Texas'),
    ('★★★★★', "The chocolate chip cookie recipe is the best I have ever made. The brown butter and overnight chill are game-changers. My coworkers think I am a professional baker.", 'David Kim', 'Atlanta, Georgia'),
    ('★★★★★', "I bought this as a gift for my daughter at college. She calls me every week to tell me which recipe she made. Best gift I have ever given.", 'Barbara Hughes', 'Columbus, Ohio'),
]
for stars, text, name, loc in reviews:
    pdf.review_card(stars, text, name, loc)


# ══════════════════════════════════════════════════════════
#  FINAL PAGE
# ══════════════════════════════════════════════════════════
pdf.add_page()
pdf._on_cover = True
# dark background
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, 210, 297, 'F')
# gold bars
pdf.set_fill_color(*GOLD)
pdf.rect(0, 0, 210, 6, 'F')
pdf.rect(0, 291, 210, 6, 'F')
# border
pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.4)
pdf.rect(12, 12, 186, 273)

# thank you
pdf.set_font('Serif', 'I', 16)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 70)
pdf.cell(210, 10, 'With warmth and gratitude,', align='C')

pdf.set_font('Serif', 'B', 44)
pdf.set_text_color(*WHITE)
pdf.set_xy(0, 82)
pdf.cell(210, 22, 'Thank You', align='C')

pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.6)
pdf.line(60, 108, 150, 108)

pdf.set_font('Serif', 'I', 13)
pdf.set_text_color(210, 200, 170)
pdf.set_xy(25, 115)
pdf.multi_cell(160, 8,
    "We hope these recipes bring the same joy, warmth, and delicious memories\n"
    "to your kitchen that they have brought to ours for generations.", align='C')

pdf.set_font('Sans', 'B', 9)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 148)
pdf.cell(210, 7, '— ✦ —', align='C')

pdf.set_font('Serif', 'I', 12)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 158)
pdf.cell(210, 8, 'Grandma Rose  &  The BinRecipes Family', align='C')

# gold box with website
pdf.set_fill_color(*GOLD)
pdf.rect(45, 180, 120, 24, 'F')
pdf.set_font('Serif', 'B', 18)
pdf.set_text_color(*NAVY)
pdf.set_xy(45, 184)
pdf.cell(120, 12, 'BinRecipes.com', align='C')
pdf.set_font('Sans', '', 8)
pdf.set_xy(45, 197)
pdf.cell(120, 6, 'Free recipes every week', align='C')

pdf.set_font('Sans', '', 9)
pdf.set_text_color(180, 170, 150)
pdf.set_xy(0, 215)
pdf.cell(210, 7, 'Share this book with someone you love', align='C')
pdf.set_xy(0, 223)
pdf.cell(210, 7, 'binrecipes@gmail.com', align='C')

pdf.set_font('Sans', 'B', 8)
pdf.set_text_color(*GOLD)
pdf.set_xy(0, 240)
pdf.cell(210, 6, 'GOLD EDITION  ·  Premium Collection  ·  BinRecipes.com', align='C')


# ══════════════════════════════════════════════════════════
out = r"c:\Users\hp\Desktop\MY WEBSITE\MYWEBSITE.github.IO\grandma-secrets-gold.pdf"
pdf.output(out)
print(f"\nSaved:  {out}")
print(f"Pages: {pdf.page}")
print(f"Size:  {os.path.getsize(out) // 1024} KB")
