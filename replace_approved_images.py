from pathlib import Path

root = Path(r'C:\Users\patelsa\Desktop\ascolite')
replacements = {
    'uploads/images/1726050486-1_crop.webp': 'uploads/images/approved/1000231818.jpg',
    'uploads/images/1726054121-1_crop.webp': 'uploads/images/approved/1000231810.jpg',
    'uploads/images/1724487756-1_crop.webp': 'uploads/images/approved/1000231825.jpg',
    'uploads/images/1726059398-1_crop.webp': 'uploads/images/approved/1000231823.jpg',
}

count = 0
for html in sorted(root.rglob('*.html')):
    try:
        text = html.read_text(encoding='utf-8')
    except Exception:
        continue
    original = text
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        html.write_text(text, encoding='utf-8')
        count += 1
print(f'Updated {count} HTML files with approved product imagery.')
