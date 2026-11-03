import argparse
import copy
import importlib.util
import subprocess
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
MENU_SELECTORS = ('.products-menu', '.applications-menu', '.about-menu', '.resource-menu', '.media-menu')
PRODUCTS = [
    ('ASCOFIX BJM/TBM', 'uploads/images/approved/1000231818.jpg',
     'products/walling-solutions/masonry-mortars/ascofix-bjm/index.html', 'Pre-mixed mortar for block masonry.'),
    ('READY MIX MORTAR', 'uploads/images/approved/1000231810.jpg',
     'products/walling-solutions/ready-mix-plasters/ready-mix-mortar/index.html', 'Ready-mixed mortar for walling and plaster applications.'),
    ('ASCOGROUT 65', 'uploads/images/approved/1000231825.jpg',
     'products/structural-repairs-sealants-and-grouts/non-shrink-grouts/aascogrout65/index.html', 'Non-shrink cementitious grout for construction applications.'),
    ('ASCOTOP FH 111', 'uploads/images/approved/1000231823.jpg',
     'products/structural-repairs-sealants-and-grouts/floor-hardener/ascotop-fh-111/index.html', 'Dry-shake floor hardener for concrete surfaces.'),
]
NEWSLETTER = 'newsletter/ascolife-the-first-edition/index.html'
PRESS_PRODUCTS = 'press/ascolite-opens-its-first-state-of-the-art-display-centre-in-surat-1/index.html'
PRESS_PROJECTS = 'press/ascolite-secures-greenpro-certification-reinforces-commitment-to-sustainable-construction-1/index.html'
RECOVERED = {}


def parse(path):
    return BeautifulSoup(path.read_text(encoding='utf-8-sig'), 'html.parser')


def hero(title, category, image='images/banners/commercial-building.jpg'):
    return '<section class="hero"><img src="{}" alt=""/><div class="content"><h1>{}</h1><p><a href="index.html">Home</a> / {} / {}</p></div></section>'.format(image, escape(title), escape(category), escape(title))


def card(title, image, target, summary, product=False):
    return '<article class="editorial-card"><a href="{0}"><img class="{4}" src="{1}" alt="{2}" loading="lazy"/></a><h2><a href="{0}">{2}</a></h2><p>{3}</p><a class="read-more" href="{0}">Read more<span class="visually-hidden">: {2}</span></a></article>'.format(escape(target), escape(image), escape(title), escape(summary), 'product-cover' if product else '')


def product_grid():
    return '<div class="editorial-products">' + ''.join(
        '<article><a href="{2}"><img src="{1}" alt="{0}"/><h2>{0}</h2></a><p>{3}</p></article>'.format(*product)
        for product in PRODUCTS) + '</div>'


def media_menu(soup):
    menu = soup.select_one('.media-menu .firstmenulist')
    if not menu:
        return
    for existing in list(menu.select('.menuitems')):
        existing.decompose()
    for title, route in [('Newsletter', 'newsletter/index.html'), ('Press Release', 'press/index.html')]:
        fragment = BeautifulSoup('<div class="menuitems"><a href="{}">{}</a></div>'.format(route, title), 'html.parser')
        menu.append(fragment)


def dependencies(soup):
    for route in ['css/style.css', 'css/site-content.css']:
        if not soup.find('link', href=route):
            node = soup.new_tag('link', rel='stylesheet', href=route)
            soup.head.append(node)
    if not soup.find('script', src='assets/js/site-navigation.js'):
        node = soup.new_tag('script', src='assets/js/site-navigation.js', defer='')
        soup.head.append(node)
    for button in soup.select('[data-dismiss="modal"]'):
        button['data-bs-dismiss'] = 'modal'


def shell(home, route, title, content):
    soup = BeautifulSoup('<!DOCTYPE html><html lang="en"><head></head><body></body></html>', 'html.parser')
    soup.head.append(soup.new_tag('meta', charset='utf-8'))
    soup.head.append(soup.new_tag('meta', attrs={'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}))
    base = soup.new_tag('base', href='../' * (len(Path(route).parts) - 1))
    soup.head.append(base)
    title_node = soup.new_tag('title')
    title_node.string = title + ' | HI TECH'
    soup.head.append(title_node)
    for node in home.head.find_all(['link', 'script'], recursive=False):
        if node.name == 'link' and ('stylesheet' in node.get('rel', []) or 'icon' in ' '.join(node.get('rel', []))):
            soup.head.append(copy.copy(node))
        elif node.name == 'script' and node.get('src'):
            soup.head.append(copy.copy(node))
    menu_style = home.head.find('style')
    if menu_style:
        soup.head.append(copy.copy(menu_style))
    soup.body['class'] = ['editorial-page']
    for selector in ('header', '.searchmodal') + MENU_SELECTORS:
        node = home.select_one(selector)
        if node:
            soup.body.append(copy.copy(node))
    main = soup.new_tag('main')
    main.append(BeautifulSoup(content, 'html.parser'))
    soup.body.append(main)
    soup.body.append(copy.copy(home.find('footer')))
    for source in ['assets/external/cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
                   'assets/external/cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js']:
        soup.body.append(soup.new_tag('script', src=source))
    init = soup.new_tag('script')
    init.string = 'if (window.AOS) AOS.init({once:true, duration:500});'
    soup.body.append(init)
    dependencies(soup)
    media_menu(soup)
    return soup


def articles():
    result = []
    spec = importlib.util.spec_from_file_location('catalog_cleanup', ROOT / 'cleanup-products.py')
    cleanup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cleanup)
    for path in sorted((ROOT / 'blog').glob('*/index.html')):
        if path.parent.name in {'category', 'tag', 'wp-json', 'wp-content', 'wp-includes'}:
            continue
        route = path.relative_to(ROOT).as_posix()
        original = subprocess.run(['git', 'show', '49b260c:' + route], cwd=str(ROOT),
                      stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding='utf-8', errors='replace')
        soup = BeautifulSoup(original.stdout, 'html.parser') if original.returncode == 0 else parse(path)
        article = soup.select_one('main article')
        heading = soup.select_one('main .blog-title') or soup.select_one('main h2')
        if not heading:
            continue
        title = heading.get_text(' ', strip=True)
        if not title or not article:
            continue
        summary = next((node.get_text(' ', strip=True) for node in article.select('p')
                        if len(node.get_text(' ', strip=True)) > 100), '')
        summary = summary[:180].rsplit(' ', 1)[0].rstrip('.,') + '.' if summary else title
        image = 'images/banners/contemporary-architecture.jpg'
        if 'mortar' in title.lower() or 'plaster' in title.lower():
            image = PRODUCTS[1][1]
        elif 'contractor' in title.lower():
            image = 'images/site-photos/teamwork.jpg'
        elif 'sustain' in title.lower() or 'green' in title.lower():
            image = 'images/site-photos/sustainability.jpg'
        for node in list(article.select('.blog-image, .sharebuttons, .sharenow, .tags, .d-flex')):
            if node.parent:
                node.decompose()
        cleaned = BeautifulSoup(cleanup.transform(str(article), route, set()), 'html.parser')
        for node in list(cleaned.find_all('img', src=True)):
            if not (ROOT / node['src']).is_file():
                node.decompose()
        content = hero(title, 'Blogs', image) + '<section class="container py-5"><div class="editorial-article">' + str(cleaned) + '<p class="mt-4"><a href="blog/index.html">Back to Blogs</a></p></div></section>'
        RECOVERED[route] = content
        result.append((title, image, route, summary))
    return result


def update_home(home):
    for tile in home.select('.watchcontent'):
        image = tile.find('img')
        video_id = tile['data-video'].rstrip('/').split('/')[-1]
        image['src'] = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(video_id)
        image['data-fallback'] = 'images/site-photos/teamwork.jpg' if video_id == 'mPp_eeAM1W0' else 'images/site-photos/facade.jpg'
        image['alt'] = tile.get_text(' ', strip=True)
        image.attrs.pop('title', None)
    for index, image in enumerate(home.select('.stories img')):
        title, source, route, summary = PRODUCTS[index % len(PRODUCTS)]
        image['src'] = source
        image['alt'] = title + ' video'
        image['aria-label'] = 'Watch video: ' + title
        image.attrs.pop('title', None)
    facebook = home.select_one('#fbContainer')
    if facebook:
        facebook.clear()
        facebook.append(BeautifulSoup('<a href="https://youtube.com/@hi-tech" target="_blank" rel="noopener"><img class="keep-connected-image" src="images/site-photos/teamwork.jpg" alt="Connect with HI TECH on YouTube"/></a>', 'html.parser'))
    modal = home.select_one('#videoModal')
    if modal:
        modal['aria-label'] = 'HI TECH video player'
        close = modal.select_one('.close')
        if close:
            close['data-bs-dismiss'] = 'modal'
    return home


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        sample = BeautifulSoup('<html><head></head><body><div class="media-menu"><div class="firstmenulist"><h3>Media</h3></div></div></body></html>', 'html.parser')
        media_menu(sample)
        dependencies(sample)
        assert len(sample.select('.media-menu a')) == 2
        assert sample.find('script', src='assets/js/site-navigation.js')
        assert all((ROOT / product[1]).exists() for product in PRODUCTS)
        print('Media content self-test passed')
        return
    home = update_home(parse(ROOT / 'index.html'))
    entries = articles()
    assert entries, 'No retained blog articles found'
    listing = hero('Blogs', 'Knowledge Center', 'images/banners/contemporary-architecture.jpg')
    listing += '<section class="container py-5"><div class="editorial-intro"><h2>Construction Insights</h2><p>Project planning, walling materials and construction practices.</p></div><div class="editorial-grid">'
    listing += ''.join(card(*entry, product=entry[1].startswith('uploads/images/approved/')) for entry in entries) + '</div></section>'
    generated = {}
    for route, content in RECOVERED.items():
        title = next(entry[0] for entry in entries if entry[2] == route)
        generated[route] = shell(home, route, title, content)
    for path in (ROOT / 'blog').glob('index*.html'):
        route = path.relative_to(ROOT).as_posix()
        generated[route] = shell(home, route, 'Blogs', listing)
    bulletin = hero('HI TECH Bulletin', 'Newsletter') + '<section class="container py-5"><article class="editorial-article"><p class="text-prime">PRODUCT FOCUS / EDITION 01</p><h2>Materials for Masonry, Grouting and Concrete Floors</h2><p>Explore the HI TECH product range, with dedicated solutions for block masonry, ready-mixed mortar, non-shrink grouting and concrete floor hardening.</p>' + product_grid() + '<h2>Projects in Focus</h2><p>Explore residential developments, business buildings and hospitality projects in our Project Showcase.</p><a class="btn-sec d-inline-block" href="project/index.html">View Project Showcase</a></article></section>'
    generated[NEWSLETTER] = shell(home, NEWSLETTER, 'HI TECH Bulletin', bulletin)
    newsletter = hero('Newsletter', 'Media') + '<section class="container py-5"><div class="editorial-intro"><h2>HI TECH Bulletin</h2><p>Product information and highlights from our project showcase.</p></div><div class="editorial-grid">' + card('HI TECH Bulletin: Product Focus', PRODUCTS[0][1], NEWSLETTER, 'Masonry mortars, non-shrink grout and floor hardener, alongside highlights from our project showcase.', True) + '</div></section>'
    generated['newsletter/index.html'] = shell(home, 'newsletter/index.html', 'Newsletter', newsletter)
    product_release = hero('HI TECH Product Range', 'Press Release') + '<section class="container py-5"><article class="editorial-article"><p class="text-prime">PRODUCT INFORMATION</p><h2>Four Products for Essential Construction Applications</h2><p>HI TECH offers masonry mortar, ready-mixed mortar, non-shrink grout and concrete floor hardener. Product pages provide application, coverage and storage information for each material.</p>' + product_grid() + '<p>For project-specific product enquiries, <a href="contact/index.html">contact HI TECH</a>.</p><a href="press/index.html">Back to Press Release</a></article></section>'
    generated[PRESS_PRODUCTS] = shell(home, PRESS_PRODUCTS, 'HI TECH Product Range', product_release)
    project_release = hero('Project Showcase Highlights', 'Press Release') + '<section class="container py-5"><article class="editorial-article"><img src="uploads/images/1720602961-1_crop.jpg" alt="L&amp;T Business Park, Mumbai"/><h2>Residential, Corporate and Commercial Projects</h2><p>Our existing Project Showcase includes Aasthaa Onyx, Apollo DB City, Ultima Lifestyle, L&amp;T Business Park, Dharmanandan Diamonds, Ramada International Hotel and Surat Diamond Bourse.</p><p>Browse building photographs, project names and locations in the complete showcase.</p><a class="btn-sec d-inline-block" href="project/index.html">View Project Showcase</a><p class="mt-4"><a href="press/index.html">Back to Press Release</a></p></article></section>'
    generated[PRESS_PROJECTS] = shell(home, PRESS_PROJECTS, 'Project Showcase Highlights', project_release)
    press = hero('Press Release', 'Media') + '<section class="container py-5"><div class="editorial-intro"><h2>Company &amp; Product Updates</h2><p>Information about our product range and projects.</p></div><div class="editorial-grid">' + card('HI TECH Product Range', PRODUCTS[2][1], PRESS_PRODUCTS, 'Four products for block masonry, ready-mixed mortar, grouting and concrete floors.', True) + card('Project Showcase Highlights', 'uploads/images/1720602961-1_crop.jpg', PRESS_PROJECTS, 'Explore residential, corporate and commercial buildings from the HI TECH project showcase.') + '</div></section>'
    generated['press/index.html'] = shell(home, 'press/index.html', 'Press Release', press)
    changed = 0
    for path in ROOT.rglob('*'):
        if path.suffix not in {'.html', '.php'} or any(part.startswith('.') for part in path.relative_to(ROOT).parts):
            continue
        route = path.relative_to(ROOT).as_posix()
        if route in generated:
            soup = generated[route]
        else:
            soup = home if route == 'index.html' else parse(path)
            if not soup.head or not soup.body:
                continue
            if route == 'index-ae21f5bd4d.html':
                for title in ['OUR GALLERY', 'KEEP IN TOUCH']:
                    source = home.find('h2', string=title)
                    target = soup.find('h2', string=title)
                    if source and target:
                        target.find_parent('section').replace_with(copy.copy(source.find_parent('section')))
            if route.startswith('blog/') and soup.find('header'):
                soup.find('header').replace_with(copy.copy(home.find('header')))
                for selector in MENU_SELECTORS:
                    current = soup.select_one(selector)
                    original = home.select_one(selector)
                    if current and original:
                        current.replace_with(copy.copy(original))
                soup.body['class'] = list(soup.body.get('class', [])) + ['editorial-page', 'blog-article']
                menu_style = copy.copy(home.head.find('style'))
                menu_style['id'] = 'shared-menu-layout'
                old_style = soup.find(id='shared-menu-layout')
                if old_style:
                    old_style.replace_with(menu_style)
                else:
                    soup.head.append(menu_style)
                for node in soup.find_all(['link', 'script']):
                    attribute = 'href' if node.name == 'link' else 'src'
                    value = node.get(attribute, '')
                    if 'themes/hi-tech-blog/' in value:
                        node[attribute] = value.replace('themes/hi-tech-blog/', 'themes/ascolite-blog/')
            dependencies(soup)
            media_menu(soup)
        output = str(soup)
        if output != path.read_text(encoding='utf-8-sig'):
            path.write_text(output, encoding='utf-8')
            changed += 1
    print('Updated {} pages; retained {} blog articles.'.format(changed, len(entries)))


if __name__ == '__main__':
    main()