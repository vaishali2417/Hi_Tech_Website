import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from bs4 import BeautifulSoup, Comment


ROOT = Path(__file__).resolve().parent
APPROVED = {
    '22': 'products/walling-solutions/masonry-mortars/ascofix-bjm/index.html',
    '25': 'products/walling-solutions/ready-mix-plasters/ready-mix-mortar/index.html',
    '58': 'products/structural-repairs-sealants-and-grouts/non-shrink-grouts/aascogrout65/index.html',
    '77': 'products/structural-repairs-sealants-and-grouts/floor-hardener/ascotop-fh-111/index.html',
}
IMAGES = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.avif', '.ico'}
OLD_NAME = re.compile(
    r'\b(?:fixobond\w*|fixoprime\w*|gypbond\w*|asco(?:fine|poxy|clean|repell|plast|putty|bond|flex|guard|shield|proof|prime|seal|crete|fill|repair|plug|screed)\w*'
    r'|ascofix\s+gpm|ascotop\s+fh\s*333|ascogrout\s*(?:40|50|pr|ep)|ascogrout\s*\(20|ready\s+mix\s+mortar\s*\(fr\))\b', re.I)
OLD_TOPIC = re.compile(r'waterproof|tile|epoxy|gypsum|putty|fly.ash|aerated|aac.block|crack.fill|sealant|protective.coating', re.I)
PRODUCT_ID = re.compile(r'^a?product(\d+)$')
URL_PATTERN = re.compile(r'''(?<![\w])url\(\s*["']?([^"')]+)["']?\s*\)''')


def read(path):
    return path.read_text(encoding='utf-8-sig', errors='replace')


def local_url(value, page, base=None):
    value = value.strip()
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    origin = 'https://local/'
    address = urljoin(origin, page)
    if base:
        address = urljoin(address, base)
    return unquote(urlsplit(urljoin(address, value)).path).lstrip('/')


def references(text, page):
    soup = BeautifulSoup(text, 'html.parser')
    base = soup.find('base', href=True)
    base = base.get('href') if base else None
    result = set()
    for node in soup.find_all(True):
        for attribute in ('href', 'src', 'poster', 'data-src', 'data-background'):
            value = node.get(attribute)
            if isinstance(value, str):
                target = local_url(value, page, base)
                if target:
                    result.add(target)
        for item in node.get('srcset', '').split(','):
            if item.strip():
                target = local_url(item.strip().split()[0], page, base)
                if target:
                    result.add(target)
    for match in URL_PATTERN.finditer(text):
        target = local_url(match.group(1).strip(), page, base)
        if target:
            result.add(target)
    return result


def pages():
    return sorted(path for path in ROOT.rglob('*')
                  if path.suffix.lower() in {'.html', '.php'}
                  and not any(part.startswith('.') for part in path.relative_to(ROOT).parts))


def remove(node):
    if node.parent is not None:
        node.decompose()


def transform(text, page, deleted, legacy_images=None, preserved_menus=None):
    soup = BeautifulSoup(text, 'html.parser')
    for selector, markup in (preserved_menus or {}).items():
        current = soup.select_one(selector)
        if current:
            current.replace_with(BeautifulSoup(markup, 'html.parser'))
    base_node = soup.find('base', href=True)
    base = base_node.get('href') if base_node else None
    for image in list(soup.find_all('img', src=True)):
        if image.attrs is None:
            continue
        target = local_url(image['src'], page, base)
        obsolete_gallery = image.find_parent(class_='product-show') and not (target or '').startswith('uploads/images/approved/')
        if target in (legacy_images or set()) or obsolete_gallery:
            parent = image.find_parent(class_='items')
            remove(parent if parent else image)
    if page in APPROVED.values():
        for carousel in list(soup.select('.showcase')):
            section = carousel.find_parent('section')
            remove(section if section else carousel)
    for comment in list(soup.find_all(string=lambda value: isinstance(value, Comment))):
        if OLD_NAME.search(str(comment)) or 'products/' in str(comment):
            comment.extract()
    for node in list(soup.find_all(True)):
        if node.attrs is None:
            continue
        match = PRODUCT_ID.fullmatch(node.get('id', '') or node.get('data-toggle', ''))
        if match and match.group(1) not in APPROVED:
            remove(node)
    for node in list(soup.find_all(['a', 'img', 'source', 'link'])):
        if node.attrs is None:
            continue
        value = node.get('href', node.get('src', ''))
        target = local_url(value, page, base)
        if not target:
            continue
        missing_catalog = target.startswith(('products/', 'blog/')) and not (ROOT / target).exists()
        supported_category = target.startswith('products/') and target.endswith('index.html') and any(
            route.startswith(target[:-10]) for route in APPROVED.values())
        if node.name == 'a' and missing_catalog and supported_category:
            node.unwrap()
            continue
        if target in deleted or target.startswith('uploads/documents/') or missing_catalog:
            parent = node.find_parent(class_='items') or node.find_parent(['li', 'button'])
            remove(parent if parent else node)
        elif Path(target).name.lower() in {'ascolite-logo.svg', 'ascon-logo.svg', 'hi-tech-logo.svg'}:
            node['src' if node.name == 'img' else 'href'] = 'images/svg/logo.svg?v=hi-tech'
    for node in list(soup.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'button', 'a', 'option'])):
        if node.attrs is not None and OLD_NAME.search(node.get_text(' ', strip=True)):
            remove(node)
    for text_node in list(soup.find_all(string=True)):
        parent = getattr(text_node, 'parent', None)
        if parent and parent.name not in {'script', 'style'} and OLD_NAME.search(str(text_node)):
            remove(parent)
    for node in list(soup.select('.menusets')):
        if not node.find('button', attrs={'data-toggle': PRODUCT_ID}):
            remove(node)
    for node in list(soup.select('.secondmenuitem, .productsdetails, .productitem')):
        if node.attrs is not None and not node.get_text(strip=True) and not node.find('img'):
            remove(node)
    for node in list(soup.find_all(attrs={'data-toggle': True})):
        if node.attrs is None:
            continue
        target = node.get('data-toggle')
        if target and not PRODUCT_ID.fullmatch(target) and soup.find(id=target) is None:
            remove(node)
    for node in list(soup.select('.products-menu .menuitems, .applications-menu .menuitems')):
        if node.attrs is not None and not node.select('.innermenu button'):
            remove(node)
    for badge in soup.select('.products-menu .rounded-full-badge, .applications-menu .rounded-full-badge'):
        badge.string = str(len(APPROVED))
    for node in soup.select('[id^="aproduct"]'):
        match = PRODUCT_ID.fullmatch(node.get('id', ''))
        if match and match.group(1) in APPROVED:
            original = soup.find(id='product' + match.group(1))
            if original and original.find('img') and node.find('img'):
                node.find('img')['src'] = original.find('img')['src']
            link = node.find('a')
            if link:
                link['href'] = APPROVED[match.group(1)]
    return str(soup)


def plan():
    contents = {path.relative_to(ROOT).as_posix(): read(path) for path in pages()}
    deleted = set()
    legacy_images = set()
    preserved_menus = {}
    for page in contents:
        original = subprocess.run(['git', 'show', 'HEAD:' + page], cwd=str(ROOT),
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding='utf-8', errors='replace')
        if original.returncode:
            continue
        soup = BeautifulSoup(original.stdout, 'html.parser')
        preserved_menus[page] = {selector: str(soup.select_one(selector))
                     for selector in ('.about-menu', '.resource-menu', '.products-menu .firstmenulist')
                     if soup.select_one(selector)}
        base_node = soup.find('base', href=True)
        base = base_node.get('href') if base_node else None
        for card in soup.select('.items'):
            obsolete = OLD_NAME.search(card.get_text(' ', strip=True))
            for anchor in card.find_all('a', href=True):
                target = local_url(anchor['href'], page, base)
                if target and target.startswith('products/') and not (ROOT / target).exists():
                    obsolete = True
            if obsolete:
                for image in card.find_all('img', src=True):
                    target = local_url(image['src'], page, base)
                    if target and not target.startswith('uploads/images/approved/'):
                        legacy_images.add(target)
    for page, text in contents.items():
        soup = BeautifulSoup(text, 'html.parser')
        title = ' '.join(node.get_text(' ', strip=True) for node in soup.find_all(['title', 'h1']))
        if page.startswith('product-') or (page.startswith('products/') and page not in APPROVED.values()
                                         and not any(route.startswith(page[:-10]) for route in APPROVED.values())):
            deleted.add(page)
        elif page.startswith('blog/') and (OLD_NAME.search(title) or OLD_TOPIC.search(title)):
            deleted.add(page)
    changed = {}
    for page, text in contents.items():
        if page not in deleted:
            replacement = transform(text, page, deleted, legacy_images, preserved_menus.get(page))
            if replacement != text:
                changed[page] = replacement
    used = set()
    for page, text in contents.items():
        if page not in deleted:
            used.update(references(changed.get(page, text), page))
    for path in list((ROOT / 'css').rglob('*.css')) + list((ROOT / 'assets').rglob('*.css')):
        used.update(references(read(path), path.relative_to(ROOT).as_posix()))
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(part.startswith('.') for part in path.relative_to(ROOT).parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith('uploads/images/approved/'):
            continue
        legacy_logo = path.name.lower() in {'ascolite-logo.svg', 'ascon-logo.svg'}
        candidate = relative.startswith(('uploads/', 'blog/wp-content/')) or relative in legacy_images or relative == 'images/webp/product-2.webp'
        old_image = path.suffix.lower() in IMAGES and candidate and relative not in used
        old_document = relative.startswith('uploads/documents/')
        if legacy_logo or old_image or old_document:
            deleted.add(relative)
    return changed, deleted


def check():
    failures = []
    preexisting = set()
    tracked = set(subprocess.check_output(['git', 'ls-files'], cwd=str(ROOT), text=True).splitlines())
    for route in APPROVED.values():
        if not (ROOT / route).is_file():
            failures.append('Missing approved product: ' + route)
    for path in pages():
        page = path.relative_to(ROOT).as_posix()
        text = read(path)
        soup = BeautifulSoup(text, 'html.parser')
        for image in soup.select('.product-show img'):
            if not image.get('src', '').startswith('uploads/images/approved/'):
                failures.append(page + ': unapproved gallery image ' + image.get('src', ''))
        for node in soup.find_all(True):
            match = PRODUCT_ID.fullmatch(node.get('id', '') or node.get('data-toggle', ''))
            if match and match.group(1) not in APPROVED:
                failures.append(page + ': obsolete product ID ' + match.group(0))
        for node in soup.find_all(string=True):
            if not isinstance(node, Comment) and node.parent.name not in {'script', 'style'} and OLD_NAME.search(str(node)):
                failures.append(page + ': obsolete product text ' + str(node).strip()[:100])
        for target in references(text, page):
            if target.startswith(('products/', 'uploads/', 'images/', 'blog/')) and not (ROOT / target).exists():
                if target not in tracked and not target.startswith(('products/', 'blog/')):
                    preexisting.add(target)
                else:
                    failures.append(page + ': missing reference ' + target)
    print(json.dumps({'approved_products': len(APPROVED), 'failures': failures,
                      'preexisting_missing_assets': sorted(preexisting)}, indent=2))
    return 1 if failures else 0


def self_test():
    sample = '<div id="product22"><img src="uploads/images/approved/test.jpg"></div><div id="aproduct8"><p>FIXOBOND</p></div><button data-toggle="aproduct8">Old</button><a href="products/old/index.html">Old</a>'
    result = transform(sample, 'index.html', {'products/old/index.html'})
    assert 'aproduct8' not in result and 'FIXOBOND' not in result and 'products/old' not in result
    assert 'product22' in result and 'approved/test.jpg' in result
    assert local_url('uploads/images/test.jpg', 'about/index.html', '../') == 'uploads/images/test.jpg'
    assert 'images/svg/icon (1).svg' in references('<img src="images/svg/icon (1).svg">', 'index.html')
    assert not references('<script>new URL(t.value)</script>', 'index.html')
    assert 'product999' not in transform('<button><a href="products/missing/index.html">product999</a></button>', 'index.html', set())
    gallery = '<div class="product-show"><div class="items"><img src="uploads/old.jpg"></div><div class="items"><img src="uploads/images/approved/test.jpg"></div></div>'
    cleaned = transform(gallery, 'index.html', set())
    assert 'uploads/old.jpg' not in cleaned and 'approved/test.jpg' in cleaned
    navigation = '<div class="about-menu"><div class="menuitems"><a href="about/index.html">Overview</a></div></div>'
    assert 'Overview' in transform(navigation, 'index.html', set())
    category = '<button><a href="products/structural-repairs-sealants-and-grouts/index.html">Structural repairs</a></button>'
    category_result = transform(category, 'index.html', set())
    assert 'Structural repairs' in category_result and 'href=' not in category_result
    article = '<article><h2>Project planning</h2><p>Keep this guidance.</p><a href="products/missing/index.html">Old product</a></article>'
    assert 'Keep this guidance.' in transform(article, 'index.html', set())
    print('Cleanup self-test passed')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.check:
        return check()
    changed, deleted = plan()
    already_deleted = subprocess.check_output(['git', 'diff', 'HEAD', '--name-only', '--diff-filter=D'], cwd=str(ROOT), universal_newlines=True).splitlines()
    report = {'deleted_files': sorted(set(already_deleted) | deleted), 'updated_pages': sorted(changed),
              'approved_products': sorted(APPROVED.values())}
    report_path = ROOT / 'product-cleanup-report.json'
    if report_path.exists():
        previous = json.loads(read(report_path))
        report['updated_pages'] = sorted(set(report['updated_pages']) | set(previous['updated_pages']))
    print(json.dumps({'pages_updated': len(changed), 'files_to_delete': len(deleted),
                      'already_deleted': len(already_deleted), 'deletions_by_extension': {
                          extension: sum(Path(path).suffix.lower() == extension for path in deleted)
                          for extension in sorted({Path(path).suffix.lower() for path in deleted})}}, indent=2))
    if args.apply:
        for page, text in changed.items():
            (ROOT / page).write_text(text, encoding='utf-8')
        for relative in deleted:
            (ROOT / relative).unlink()
        (ROOT / 'product-cleanup-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())