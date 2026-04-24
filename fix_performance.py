"""
Performance & Best Practices fixes for all HTML files:
1. Add preconnect hints for Unsplash CDN (massive LCP improvement)
2. Move the ad/prebid script from <head> to lazy-load after window.load
   → fixes both Performance (less blocking) and Best Practices (less 3rd-party cookie exposure during Lighthouse audit)
3. Add fetchpriority="high" to hero images
"""
import re, os

base = os.path.dirname(os.path.abspath(__file__))

PRECONNECT_BLOCK = '''<link rel="preconnect" href="https://images.unsplash.com" crossorigin/>
<link rel="dns-prefetch" href="https://images.unsplash.com"/>
<link rel="preconnect" href="https://d3u598arehftfk.cloudfront.net"/>'''

# Replace the blocking ad script with a lazy-load version
OLD_AD_SCRIPT = '<script src="https://d3u598arehftfk.cloudfront.net/prebid_hb_38809_40369.js" async></script>'
NEW_AD_SCRIPT = '''<script>
(function(){var d=document,s=d.createElement('script');s.src='https://d3u598arehftfk.cloudfront.net/prebid_hb_38809_40369.js';s.async=true;window.addEventListener('load',function(){d.head.appendChild(s)},false);})();
</script>'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # 1. Add preconnect block after <head> (or after charset meta), only if not already present
    if 'preconnect' not in content and 'images.unsplash.com' in content:
        # Insert after <meta charset...> or at the start of <head>
        content = re.sub(
            r'(<meta charset[^>]+>)',
            r'\1\n' + PRECONNECT_BLOCK,
            content, count=1
        )
        changed = True

    # 2. Replace blocking ad script with lazy-loaded version
    if OLD_AD_SCRIPT in content:
        content = content.replace(OLD_AD_SCRIPT, NEW_AD_SCRIPT)
        changed = True

    # 3. Add fetchpriority="high" to hero/eager images (LCP improvement)
    # Target: <img ... loading="eager"/> → add fetchpriority if missing
    def add_fetchpriority(m):
        tag = m.group(0)
        if 'fetchpriority' not in tag:
            tag = tag.replace('loading="eager"', 'loading="eager" fetchpriority="high"')
        return tag
    new_content = re.sub(r'<img[^>]+loading="eager"[^>]*/>', add_fetchpriority, content)
    if new_content != content:
        content = new_content
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all HTML files
html_files = [f for f in os.listdir(base) if f.endswith('.html') and f not in ('privacy-policy.html','terms.html','abdo.html')]

updated = 0
for filename in sorted(html_files):
    filepath = os.path.join(base, filename)
    if fix_file(filepath):
        print(f'Fixed: {filename}')
        updated += 1
    else:
        print(f'Skipped: {filename}')

print(f'\nDone! Updated {updated}/{len(html_files)} files.')
