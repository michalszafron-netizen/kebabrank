import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
import pathlib

cities_dir = pathlib.Path('static/img/cities')
count = 0

for f in sorted(cities_dir.glob('*.jpeg')):
    img = Image.open(f).convert('RGB')

    # Large variant (800x500) — for desktop
    img_lg = img.resize((800, 500), Image.LANCZOS)
    out_lg = f.with_suffix('.webp')
    img_lg.save(out_lg, 'WEBP', quality=82)

    # Small variant (400x250) — for mobile srcset
    img_sm = img.resize((400, 250), Image.LANCZOS)
    out_sm = f.with_name(f.stem + '-sm.webp')
    img_sm.save(out_sm, 'WEBP', quality=78)

    orig_kb = f.stat().st_size // 1024
    lg_kb = out_lg.stat().st_size // 1024
    sm_kb = out_sm.stat().st_size // 1024
    print(f"{f.name} -> {out_lg.name} {orig_kb}KB->{lg_kb}KB  | {out_sm.name} {sm_kb}KB")
    count += 1

print(f"\nConverted {count} city images (large + small variants).")

img = Image.open('static/img/top10.png').convert('RGB')
img.save('static/img/top10.webp', 'WEBP', quality=85)
orig_kb = pathlib.Path('static/img/top10.png').stat().st_size // 1024
new_kb = pathlib.Path('static/img/top10.webp').stat().st_size // 1024
print(f"top10.png -> top10.webp  {orig_kb}KB -> {new_kb}KB")
print("Done.")
