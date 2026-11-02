import argparse
from collections import Counter, defaultdict
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import urllib.parse


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'image-refresh-report.json'
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif', '.svg', '.ico'}
VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
CSS_URL = re.compile(r'url\(\s*([\'"]?)(.*?)\1\s*\)', re.I)
PRESERVED_CONTEXT = {'productitem', 'product-list', 'prodyct-list', 'logo-row', 'logo-slide', 'navbar-brand'}
LIBRARY = {
    'coatings': ['images/product-categories/protective-coatings.jpg'],
    'concrete': ['images/product-categories/structural-repairs.jpg', 'images/applications/columns-and-beams.jpg'],
    'tiles': ['images/product-categories/tile-and-stone.jpg', 'images/applications/tiled-interior.jpg'],
    'bathroom': ['images/applications/bathroom.jpg', 'images/product-categories/tile-and-stone.jpg'],
    'pool': ['images/product-categories/waterproofing.jpg'],
    'terrace': ['images/applications/terrace.jpg', 'images/applications/podium.jpg'],
    'mosaic': ['images/applications/mosaic-terrace.jpg'],
    'basement': ['images/applications/basement.jpg'],
    'brick': ['images/product-categories/walling-solutions.jpg'],
    'interior': ['images/banners/modern-interior.jpg', 'images/site-photos/workplace.jpg'],
    'residential': ['images/banners/modern-home.jpg', 'images/applications/podium.jpg'],
    'commercial': ['images/banners/commercial-building.jpg', 'images/banners/contemporary-architecture.jpg', 'images/site-photos/facade.jpg'],
    'teamwork': ['images/site-photos/teamwork.jpg', 'images/site-photos/workplace.jpg'],
    'manufacturing': ['images/site-photos/manufacturing.jpg', 'images/applications/columns-and-beams.jpg'],
    'sustainability': ['images/site-photos/sustainability.jpg', 'images/banners/modern-home.jpg'],
}
DESCRIPTIONS = {
    'coatings': 'Surface painting and protective finishing',
    'concrete': 'Concrete construction and structural work',
    'tiles': 'Tiled surfaces and contemporary interior finishes',
    'bathroom': 'Finished bathroom surfaces and wet-area construction',
    'pool': 'Swimming pool and watertight construction surfaces',
    'terrace': 'Exterior terrace surfaces and paving',
    'mosaic': 'Decorative outdoor paving and mosaic surfaces',
    'basement': 'Parking structure and concrete building surfaces',
    'brick': 'Exposed brick masonry surface',
    'interior': 'Contemporary interior and wall finishes',
    'residential': 'Modern residential architecture and exterior finishes',
    'commercial': 'Contemporary commercial architecture and facades',
    'teamwork': 'Collaborative workplace and professional teamwork',
    'manufacturing': 'Industrial storage and material-handling operations',
    'sustainability': 'Landscape and sustainable built-environment inspiration',
}
RULES = [
    ('pool', r'pool|swimming'),
    ('mosaic', r'mosai?c|mosic'),
    ('basement', r'basement|underground'),
    ('bathroom', r'bathroom|wet.area|non.sunk|non sunk|toilet'),
    ('terrace', r'terrace|\broofs?\b|podium'),
    ('brick', r'exposed.brick|brick|aac|fly.ash|walling|masonry|blocks'),
    ('tiles', r'tile|stone|grout|flooring'),
    ('coatings', r'coating|paint|repellent|rust|waterproof|sealer'),
    ('concrete', r'concrete|repair|crack|column|beam|structur|cement|construction.site'),
    ('manufacturing', r'manufactur|factory|production|plant|industrial'),
    ('teamwork', r'career|\bintern(?:ship|s)?\b|training|workforce|work.at|women|recruit|life.at'),
    ('sustainability', r'sustainab|environment|green.build|eco.friendly'),
    ('interior', r'internal.wall|interior|putty|plaster|corporate|office'),
    ('residential', r'residential|home|house|realty'),
    ('commercial', r'commercial|architect|facade|building|infrastructure'),
]


def image_key(value, owner, css=False):
    value = html.unescape(value).strip()
    if not value or value.startswith(('#', 'data:', 'blob:')):
        return None
    parsed = urllib.parse.urlsplit(value)
    if Path(parsed.path).suffix.lower() not in IMAGE_EXTENSIONS:
        return None
    path = urllib.parse.unquote(parsed.path)
    if parsed.netloc:
        if parsed.netloc.lower() in ('ascolite.in', 'www.ascolite.in'):
            path = path.lstrip('/')
        else:
            path = 'assets/external/' + parsed.netloc + '/' + path.lstrip('/')
    elif css:
        path = os.path.normpath(str(Path(owner).parent / path)).replace('\\', '/')
    elif path.startswith('/'):
        path = path.lstrip('/')
    elif not path.startswith(('images/', 'uploads/', 'assets/', 'blog/', 'asco-console/')):
        path = os.path.normpath(str(Path(owner).parent / path)).replace('\\', '/')
    return path


def image_size(path):
    if not path.is_file():
        return None
    with path.open('rb') as image:
        data = image.read(131072)
    if data.startswith(b'\x89PNG') and len(data) >= 24:
        return struct.unpack('>II', data[16:24])
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        if data[12:16] == b'VP8X':
            return (int.from_bytes(data[24:27], 'little') + 1, int.from_bytes(data[27:30], 'little') + 1)
        if data[12:16] == b'VP8 ':
            offset = data.find(b'\x9d\x01\x2a')
            if offset >= 0:
                width, height = struct.unpack('<HH', data[offset + 3:offset + 7])
                return width & 16383, height & 16383
        if data[12:16] == b'VP8L':
            bits = int.from_bytes(data[21:25], 'little')
            return (bits & 16383) + 1, ((bits >> 14) & 16383) + 1
    if data[:2] == b'\xff\xd8':
        offset = 2
        while offset + 9 < len(data):
            if data[offset] != 255:
                offset += 1
                continue
            marker = data[offset + 1]
            offset += 2
            if marker in (0xD8, 0xD9) or marker == 255:
                continue
            length = int.from_bytes(data[offset:offset + 2], 'big')
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                height, width = struct.unpack('>HH', data[offset + 3:offset + 7])
                return width, height
            if length < 2:
                break
            offset += length
    return None


class ImageInventory(HTMLParser):
    def __init__(self, source, owner):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.source = source
        self.owner = owner
        self.stack = []
        self.references = []
        self.heading = ''
        self.lines = [0]
        for match in re.finditer('\n', source):
            self.lines.append(match.end())

    def handle_starttag(self, tag, attributes):
        attrs = {name: value or '' for name, value in attributes}
        parents = ' '.join(node['attrs'].get('class', '') for node in self.stack)
        node = {'tag': tag, 'attrs': attrs, 'text': ''}
        position = self.getpos()
        offset = self.lines[position[0] - 1] + position[1]
        raw = self.get_starttag_text()
        for name, value in attributes:
            if not value:
                continue
            values = []
            if name in ('src', 'data-src', 'data-img', 'data-image', 'data-background', 'poster'):
                values = [value]
            elif name in ('srcset', 'data-srcset'):
                values = [part.strip().split()[0] for part in value.split(',') if part.strip()]
            elif name == 'style':
                values = [match.group(2) for match in CSS_URL.finditer(value)]
            elif tag == 'meta' and name == 'content' and 'image' in (attrs.get('property', '') + attrs.get('name', '')):
                values = [value]
            for url in values:
                key = image_key(url, self.owner)
                if key:
                    self.references.append({'key': key, 'url': url, 'owner': self.owner, 'tag': tag,
                                            'attribute': name, 'attrs': attrs, 'parents': parents,
                                            'heading': self.heading, 'node': node, 'offset': offset, 'raw': raw})
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]['tag'] == tag:
                if re.fullmatch('h[1-6]|title', tag):
                    self.heading = self.stack[index]['text'].strip()
                del self.stack[index:]
                break

    def handle_data(self, value):
        if self.stack and self.stack[-1]['tag'] not in ('script', 'style'):
            node = self.stack[-1]
            if len(node['text']) < 400:
                node['text'] += value[:400]


def protected_reason(reference):
    key = reference['key']
    attrs = reference['attrs']
    classes = set((reference['parents'] + ' ' + attrs.get('class', '')).split())
    owner = reference['owner'].lower()
    if key.startswith(('images/banners/', 'images/product-categories/', 'images/applications/', 'images/site-photos/')):
        return 'already refreshed'
    if Path(key).suffix.lower() in ('.svg', '.ico', '.gif') or '/icons/' in key or '/fonts/' in key:
        return 'branding or interface graphic'
    if re.search(r'logo|favicon|splash|loader|product.system|label|lable|certificate|badge', Path(key).name, re.I):
        return 'authentic branding, product diagram or identity graphic'
    if classes & PRESERVED_CONTEXT:
        return 'authentic product or customer logo'
    if 'main-img' in classes and ('team/' in owner or owner.startswith('team')):
        return 'named staff portrait'
    if owner.startswith(('team/', 'clients/', 'testimonials/')) and reference['tag'] == 'img':
        return 'authentic staff, customer or testimonial image'
    if '/newsletter/' in key:
        return 'newsletter document artwork'
    if 'px-5' in classes or ('w-50' in classes and 'mx-auto' in classes):
        return 'authentic product photograph'
    if any(token in (attrs.get('alt', '') + ' ' + attrs.get('title', '')).lower() for token in ('logo', 'certificate', 'certification', 'award', 'portrait')):
        return 'authentic identity or certification artwork'
    if re.search(r'founder|chairman|managing director|leadership|certificate|certification|award', reference['heading'], re.I):
        return 'named person or documentary artwork'
    style = attrs.get('style', '')
    if re.search(r'(?:max-)?width\s*:\s*(?:[1-9]\d?|1[0-5]\d)px', style):
        return 'interface or product feature icon'
    return None


def classify(references):
    application_notes = [ref['node']['text'] for ref in references if ref['attribute'] == 'data-img']
    filename = Path(references[0]['key']).stem
    tiers = [' '.join(application_notes), filename]
    tiers.extend(' '.join((ref['attrs'].get('alt', ''), ref['attrs'].get('title', ''), ref['heading'])) for ref in references[:8])
    tiers.extend(ref['owner'] for ref in references[:8])
    context = ''
    for note in tiers:
        context = note.lower().replace('-', ' ').replace('_', ' ')
        for category, pattern in RULES:
            if re.search(pattern, context):
                return category, context[:400]
    return 'commercial', context[:400]


def inventory():
    sources = {}
    by_asset = defaultdict(list)
    for path in sorted(ROOT.rglob('*.html')):
        relative = path.relative_to(ROOT).as_posix()
        if any(part in ('.git', '.mirror-cache', '.runtime', 'node_modules') for part in path.relative_to(ROOT).parts):
            continue
        source = path.read_text(encoding='utf-8', errors='replace')
        parser = ImageInventory(source, relative)
        parser.feed(source)
        sources[relative] = (source, parser.references)
        for reference in parser.references:
            by_asset[reference['key']].append(reference)
        for match in CSS_URL.finditer(source):
            key = image_key(match.group(2), relative)
            if key:
                ref = {'key': key, 'url': match.group(2), 'owner': relative,
                       'tag': 'style', 'attribute': 'background', 'attrs': {}, 'parents': '',
                       'heading': relative, 'node': {'text': ''}}
                parser.references.append(ref)
                by_asset[key].append(ref)
    for path in sorted((ROOT / 'css').glob('*.css')):
        relative = path.relative_to(ROOT).as_posix()
        source = path.read_text(encoding='utf-8', errors='replace')
        refs = []
        for match in CSS_URL.finditer(source):
            key = image_key(match.group(2), relative, css=True)
            if key:
                ref = {'key': key, 'url': match.group(2), 'owner': relative,
                       'tag': 'style', 'attribute': 'background', 'attrs': {}, 'parents': '',
                       'heading': relative, 'node': {'text': ''}}
                refs.append(ref)
                by_asset[key].append(ref)
        sources[relative] = (source, refs)
    return sources, by_asset


def build_plan(by_asset):
    replacements = {}
    preserved = {}
    for key, references in by_asset.items():
        reasons = [protected_reason(reference) for reference in references]
        reason = next((value for value in reasons if value), None)
        size = image_size(ROOT / key)
        if not reason and size and (max(size) < 240 or (key.lower().endswith('.png') and max(size) < 500)):
            reason = 'small authentic graphic or portrait'
        if not reason and Path(key).suffix.lower() == '.png' and not size:
            reason = 'unavailable graphic, not a verified contextual photograph'
        if reason:
            preserved[key] = reason
            continue
        category, context = classify(references)
        choices = LIBRARY[category]
        seed = re.sub(r'-\d+x\d+|-scaled', '', key)
        selected = choices[int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16) % len(choices)]
        replacements[key] = {'replacement': selected, 'category': category, 'context': context,
                             'description': DESCRIPTIONS[category], 'references': len(references),
                             'pages': sorted(set(ref['owner'] for ref in references))}
    return replacements, preserved


def rewrite(source, owner, references, replacements):
    variants = {}
    tag_edits = {}
    for reference in references:
        entry = replacements.get(reference['key'])
        if not entry:
            continue
        target = entry['replacement']
        if owner.endswith('.css') or ('<base ' not in source.lower() and '/' in owner):
            target = os.path.relpath(ROOT / target, (ROOT / owner).parent).replace('\\', '/')
        variants[reference['url']] = target
        variants[html.escape(reference['url'], quote=True)] = target
        if reference['tag'] == 'img' and reference['attribute'] == 'src':
            raw = reference['raw']
            description = 'Illustrative photo: ' + entry['description']
            if re.search(r'\balt\s*=', raw, re.I):
                updated = re.sub(r'\balt\s*=\s*([\'"]).*?\1', lambda match: 'alt="' + description + '"', raw, flags=re.I | re.S)
            else:
                updated = raw.replace('<img', '<img alt="' + description + '"', 1)
            updated = re.sub(r'\btitle\s*=\s*([\'"]).*?\1', lambda match: 'title="' + entry['description'] + '"', updated, flags=re.I | re.S)
            tag_edits[reference['offset']] = (len(raw), updated)
    if not variants:
        return source
    for offset in sorted(tag_edits, reverse=True):
        length, updated = tag_edits[offset]
        source = source[:offset] + updated + source[offset + length:]
    pattern = re.compile('|'.join(re.escape(value) for value in sorted(variants, key=len, reverse=True)))
    return pattern.sub(lambda match: variants[match.group(0)], source)


def self_test():
    source = '<html><head><base href="../"></head><body><div class="productitem"><img src="uploads/images/pack.webp"></div><main><h1>Bathroom waterproofing</h1><img src="uploads/images/room.jpg"><h5 data-img="https://ascolite.in/uploads/images/pool.jpg">Swimming pools</h5></main></body></html>'
    parser = ImageInventory(source, 'about/index.html')
    parser.feed(source)
    refs = defaultdict(list)
    for reference in parser.references:
        refs[reference['key']].append(reference)
    replacements, preserved = build_plan(refs)
    assert preserved['uploads/images/pack.webp'] == 'authentic product or customer logo'
    assert replacements['uploads/images/room.jpg']['category'] == 'bathroom'
    assert replacements['uploads/images/pool.jpg']['category'] == 'pool'
    assert classify([{'key': 'uploads/images/123.webp', 'attribute': 'data-img', 'node': {'text': 'INTERNAL WALLS'}, 'attrs': {}, 'heading': '', 'owner': 'application/index.html'}])[0] == 'interior'
    assert classify([{'key': 'blog/Why-Paint-Ascoguard.jpg', 'attribute': 'src', 'attrs': {}, 'heading': 'Roof repairs', 'owner': 'blog/index.html'}])[0] == 'coatings'
    assert classify([{'key': 'blog/waterproofing-exterior-walls.jpg', 'attribute': 'src', 'attrs': {}, 'heading': '', 'owner': 'blog/index.html'}])[0] == 'coatings'
    output = rewrite(source, 'about/index.html', parser.references, replacements)
    assert 'src="uploads/images/pack.webp"' in output
    assert 'src="images/applications/bathroom.jpg"' in output or 'src="images/product-categories/tile-and-stone.jpg"' in output
    assert 'data-img="images/product-categories/waterproofing.jpg"' in output
    assert image_size(ROOT / 'images/banners/modern-home.jpg') == (2000, 1333)
    assert image_size(ROOT / 'images/product-categories/walling-solutions.jpg') == (1200, 780)
    print('PASS: protected products, contextual classification, application controls, link rewriting and image dimensions')


def refine_applied_contexts():
    report = json.loads(REPORT.read_text(encoding='utf-8'))
    corrections = {}
    for key, entry in report['replacements'].items():
        if entry['category'] != 'terrace' or re.search(r'terrace|\broofs?\b|podium', entry['context']):
            continue
        if not re.search(r'waterproof', entry['context']):
            continue
        corrections[key] = dict(entry, replacement=LIBRARY['coatings'][0], category='coatings', description=DESCRIPTIONS['coatings'])
    owners = sorted(set(owner for entry in corrections.values() for owner in entry['pages']))
    changed = []
    for owner in owners:
        source = (ROOT / owner).read_text(encoding='utf-8', errors='replace')
        baseline = subprocess.check_output(['git', 'show', 'HEAD:' + owner], cwd=str(ROOT)).decode('utf-8', 'replace')
        if owner.endswith('.css'):
            previous = list(CSS_URL.finditer(baseline))
            current = list(CSS_URL.finditer(source))
            if len(previous) != len(current):
                raise SystemExit('Stylesheet structure changed; refusing automatic correction: ' + owner)
            edits = []
            for old, new in zip(previous, current):
                key = image_key(old.group(2), owner, css=True)
                if key in corrections and image_key(new.group(2), owner, css=True) == report['replacements'][key]['replacement']:
                    target = os.path.relpath(ROOT / corrections[key]['replacement'], (ROOT / owner).parent).replace('\\', '/')
                    edits.append((new.start(2), new.end(2), target))
            for start, end, target in reversed(edits):
                source = source[:start] + target + source[end:]
        else:
            old_parser = ImageInventory(baseline, owner)
            old_parser.feed(baseline)
            new_parser = ImageInventory(source, owner)
            new_parser.feed(source)
            if len(old_parser.references) != len(new_parser.references):
                raise SystemExit('Image structure changed; refusing automatic correction: ' + owner)
            tags = {}
            for old, new in zip(old_parser.references, new_parser.references):
                key = old['key']
                if key not in corrections or owner not in corrections[key]['pages']:
                    continue
                if new['key'] != report['replacements'][key]['replacement']:
                    continue
                target = corrections[key]['replacement']
                if '<base ' not in source.lower() and '/' in owner:
                    target = os.path.relpath(ROOT / target, (ROOT / owner).parent).replace('\\', '/')
                offset = new['offset']
                raw = tags.get(offset, new['raw'])
                raw = raw.replace(new['url'], target)
                if new['tag'] == 'img':
                    raw = raw.replace('Illustrative photo: ' + report['replacements'][key]['description'], 'Illustrative photo: ' + corrections[key]['description'])
                    raw = raw.replace('title="' + report['replacements'][key]['description'] + '"', 'title="' + corrections[key]['description'] + '"')
                tags[offset] = raw
            lengths = {ref['offset']: len(ref['raw']) for ref in new_parser.references}
            for offset in sorted(tags, reverse=True):
                source = source[:offset] + tags[offset] + source[offset + lengths[offset]:]
        if source != (ROOT / owner).read_text(encoding='utf-8', errors='replace'):
            (ROOT / owner).write_text(source, encoding='utf-8')
            changed.append(owner)
    report['replacements'].update(corrections)
    report['categories'] = dict(Counter(entry['category'] for entry in report['replacements'].values()))
    report['refined_context_files'] = changed
    REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Refined {} image mappings in {} files without changing protected imagery.'.format(len(corrections), len(changed)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--refine-contexts', action='store_true')
    options = parser.parse_args()
    if options.self_test:
        self_test()
        return
    if options.refine_contexts:
        refine_applied_contexts()
        return
    sources, by_asset = inventory()
    replacements, preserved = build_plan(by_asset)
    if options.check:
        report = json.loads(REPORT.read_text(encoding='utf-8'))
        missing = [key for key, entry in report['replacements'].items() if not (ROOT / entry['replacement']).is_file()]
        altered = [key for key, count in report.get('protected_reference_counts', {}).items() if len(by_asset.get(key, [])) != count]
        if missing or replacements or altered:
            raise SystemExit('FAIL: {} missing replacements, {} contextual images still eligible, {} protected references changed'.format(len(missing), len(replacements), len(altered)))
        print('PASS: all contextual image references refreshed; {} protected or already-refreshed assets retained'.format(len(preserved)))
        return
    changed = []
    if options.apply:
        missing = sorted(set(entry['replacement'] for entry in replacements.values() if not (ROOT / entry['replacement']).is_file()))
        if missing:
            raise SystemExit('Download replacement library first: ' + ', '.join(missing))
        for owner, (source, refs) in sources.items():
            updated = rewrite(source, owner, refs, replacements)
            if source != updated:
                if (ROOT / owner).read_text(encoding='utf-8', errors='replace') != source:
                    raise SystemExit('File changed during scan; refusing to overwrite: ' + owner)
                (ROOT / owner).write_text(updated, encoding='utf-8')
                changed.append(owner)
    report = {'mode': 'applied' if options.apply else 'inventory', 'html_pages': sum(owner.endswith('.html') for owner in sources),
              'changed_files': changed, 'replacements': replacements, 'preserved': preserved,
              'protected_reference_counts': {key: len(by_asset[key]) for key, reason in preserved.items() if reason != 'already refreshed'},
              'categories': dict(Counter(entry['category'] for entry in replacements.values()))}
    REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('{} HTML pages; {} contextual images; {} protected/refreshed images; {} files changed'.format(
        report['html_pages'], len(replacements), len(preserved), len(changed)))
    print(json.dumps(report['categories'], sort_keys=True))


if __name__ == '__main__':
    main()