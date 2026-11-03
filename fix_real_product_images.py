from pathlib import Path
import re

root = Path(r'C:\Users\patelsa\Desktop\ascolite')
approved = {'22': 'uploads/images/approved/1000231818.jpg', '25': 'uploads/images/approved/1000231810.jpg', '58': 'uploads/images/approved/1000231825.jpg', '77': 'uploads/images/approved/1000231823.jpg'}

for html_file in sorted(root.rglob('*.html')):
    if '.git' in html_file.parts:
        continue
    try:
        text = html_file.read_text(encoding='utf-8')
    except Exception:
        continue
    for pid, img in approved.items():
        pattern = rf'(?is)(<div\s+class="productitem"\s+id="product{pid}"[^>]*>.*?<img\s+src=")[^"]+("\s*alt=""\s+class="w-75\s+mx-auto\s+img-fluid\s+d-block">)'
        text = re.sub(pattern, rf'\1{img}\2', text, count=1)
        # fallback for other markup styles
        text = re.sub(rf'(?is)(<div\s+class="productitem"\s+id="product{pid}"[^>]*>.*?<img\s+src=")[^"]+("\s*[^>]*>)', rf'\1{img}\2', text, count=1)
    html_file.write_text(text, encoding='utf-8')

# Fix the detail pages themselves.
detail_map = {
    root / 'products' / 'walling-solutions' / 'masonry-mortars' / 'ascofix-bjm' / 'index.html': 'uploads/images/approved/1000231818.jpg',
    root / 'products' / 'walling-solutions' / 'ready-mix-plasters' / 'ready-mix-mortar' / 'index.html': 'uploads/images/approved/1000231810.jpg',
    root / 'products' / 'structural-repairs-sealants-and-grouts' / 'non-shrink-grouts' / 'aascogrout65' / 'index.html': 'uploads/images/approved/1000231825.jpg',
    root / 'products' / 'structural-repairs-sealants-and-grouts' / 'floor-hardener' / 'ascotop-fh-111' / 'index.html': 'uploads/images/approved/1000231823.jpg',
}
for path, img in detail_map.items():
    if path.exists():
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'(?is)(<img\s+src=")[^"]+("\s*[^>]*>)', rf'\1{img}\2', text, count=1)
        path.write_text(text, encoding='utf-8')

print('Updated product-card image URLs to the approved pack shots.')
