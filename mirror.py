import argparse
import concurrent.futures
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.parse

ROOT = Path(__file__).resolve().parent
ORIGIN = 'https://ascolite.in/'
HOSTS = {'ascolite.in', 'www.ascolite.in'}
ASSET_EXTENSIONS = {'.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg',
                    '.ico', '.woff', '.woff2', '.ttf', '.eot', '.otf', '.mp4',
                    '.webm', '.ogg', '.mov', '.pdf', '.zip', '.avif', '.mp3'}
CSS_URL = re.compile(r'url\(\s*([\'"]?)(.*?)\1\s*\)', re.I)
CSS_IMPORT = re.compile(r'(@import\s+)([\'"])(.*?)\2', re.I)
TRACKERS = ('clarity.ms', 'googletagmanager', 'connect.facebook', 'google-analytics', 'facebook.com/tr')


def canonical(value, base=ORIGIN):
    url = urllib.parse.urlsplit(urllib.parse.urljoin(base, html.unescape(value).strip()))
    if url.scheme not in ('http', 'https'):
        return None
    host = url.netloc.lower()
    if host in HOSTS:
        host = 'ascolite.in'
    path = re.sub(r'(?:%20)+$', '', url.path or '/', flags=re.I)
    path = urllib.parse.quote(path, safe="/%:@!$&'()*+,;=-._~")
    query = urllib.parse.quote(url.query, safe="%=&/?@:!$'()*+,;~-._")
    return urllib.parse.urlunsplit(('https', host, path, query, ''))


def is_page(url):
    parsed = urllib.parse.urlsplit(url)
    return parsed.netloc in HOSTS and Path(parsed.path).suffix.lower() not in ASSET_EXTENSIONS


def local_path(url):
    parsed = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(parsed.path).lstrip('/')
    path = '/'.join(re.sub(r'[<>:"\\|?*]', '_', part) for part in path.split('/') if part not in ('.', '..'))
    if parsed.netloc not in HOSTS:
        path = 'assets/external/' + parsed.netloc + '/' + path
    if is_page(url):
        if path.endswith('.php'):
            path = path[:-4] + '.html'
        elif not Path(path).suffix:
            path = path.rstrip('/') + '/index.html' if path.strip('/') else 'index.html'
    if not path or path.endswith('/'):
        path += 'index.html'
    if parsed.query:
        target = Path(path)
        path = str(target.with_name(target.stem + '-' + hashlib.sha256(parsed.query.encode()).hexdigest()[:10] + target.suffix)).replace('\\', '/')
    return path


class Mirror:
    def __init__(self):
        self.pending = {ORIGIN}
        self.pages = {}
        self.assets = set()
        self.failed = {}
        self.external_embeds = set()

    def reference(self, value, base, page=False):
        if not value or value.startswith(('#', 'data:', 'javascript:', 'mailto:', 'tel:', 'blob:')):
            return value
        value = value.strip()
        if value.startswith(('images/', 'uploads/', 'css/', 'js/', 'asco-console/')):
            base = ORIGIN
        if value == 'uploads/images/search.svg' or value == ORIGIN + 'uploads/images/search.svg':
            value = ORIGIN + 'images/svg/search.svg'
        url = canonical(value, base)
        if not url:
            return value
        if any(tracker in url for tracker in TRACKERS):
            return '#'
        parsed = urllib.parse.urlsplit(url)
        if page and parsed.netloc not in HOSTS:
            return value
        if parsed.netloc in HOSTS and any(segment in parsed.path.lower() for segment in ('/admin', '/login', '/wp-admin', '/asco-console/index')):
            return value
        if is_page(url):
            self.pending.add(url)
        else:
            self.assets.add(url)
        fragment = urllib.parse.urlsplit(value).fragment
        return local_path(url) + ('#' + fragment if fragment else '')

    def css(self, text, base):
        def relative(value):
            rewritten = self.reference(value, base)
            if rewritten == value:
                return value
            return os.path.relpath(ROOT / rewritten, (ROOT / local_path(base)).parent).replace('\\', '/')
        text = CSS_URL.sub(lambda match: 'url("' + relative(match.group(2)) + '")', text)
        return CSS_IMPORT.sub(lambda match: match.group(1) + '"' + relative(match.group(3)) + '"', text)

    def download(self, url, raw=False):
        target = ROOT / ('.mirror-cache/' + hashlib.sha256(url.encode()).hexdigest() if raw else local_path(url))
        if target.exists() and target.stat().st_size:
            return target
        os.makedirs(str(target.parent), exist_ok=True)
        temporary = str(target) + '.part'
        result = subprocess.run(['curl.exe', '-L', '--fail', '--silent', '--show-error',
                                 '--retry', '1', '--connect-timeout', '15', '--max-time', '120',
                                 '-A', 'Mozilla/5.0 (compatible; LocalPreview/1.0)', url, '-o', temporary],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode:
            self.failed[url] = result.stderr.decode('utf-8', 'replace').strip()
            if Path(temporary).exists():
                Path(temporary).unlink()
            return None
        Path(temporary).replace(target)
        self.failed.pop(url, None)
        return target

    def build_page(self, url):
        url = canonical(url)
        raw = self.download(url, raw=True)
        if raw is None:
            return
        source = raw.read_text(encoding='utf-8', errors='replace')
        if '<html' not in source.lower() and '<!doctype' not in source.lower():
            self.failed[url] = 'Response was not an HTML page'
            return
        parser = PageParser(self, url)
        parser.feed(source)
        parser.close()
        destination = ROOT / local_path(url)
        os.makedirs(str(destination.parent), exist_ok=True)
        destination.write_text(''.join(parser.output), encoding='utf-8')
        self.pages[url] = local_path(url)

    def build(self, limit):
        visited = set()
        while self.pending and len(visited) < limit:
            batch = sorted(self.pending - visited)[:min(4, limit - len(visited))]
            if not batch:
                break
            self.pending.difference_update(batch)
            visited.update(batch)
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(self.build_page, batch))
            print('Pages: {} | discovered assets: {}'.format(len(self.pages), len(self.assets)), flush=True)
        done = set()
        while self.assets - done:
            batch = sorted(self.assets - done)
            done.update(batch)
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(self.download, batch))
            for url, target in zip(batch, results):
                if target and urllib.parse.urlsplit(url).path.endswith('.css'):
                    original = self.download(url, raw=True)
                    if original:
                        target.write_text(self.css(original.read_text(encoding='utf-8', errors='replace'), url), encoding='utf-8')
            print('Assets processed: {}'.format(len(done)), flush=True)
        report = {'pages': self.pages, 'assets': sorted(done - set(self.failed)),
                  'failed': self.failed, 'external_video_embeds': sorted(self.external_embeds),
                  'uncrawled_pages': sorted(self.pending - visited)}
        (ROOT / 'download-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print('Saved {} pages, {} assets; {} failures, {} pending pages.'.format(
            len(self.pages), len(report['assets']), len(self.failed), len(report['uncrawled_pages'])))


class PageParser(HTMLParser):
    def __init__(self, mirror, url):
        HTMLParser.__init__(self, convert_charrefs=False)
        self.mirror = mirror
        self.url = url
        self.output = []
        self.context = ''
        self.skip = False
        self.script = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'base':
            return
        if tag == 'script' and any(host in values.get('src', '') for host in TRACKERS):
            self.skip = True
            return
        self.context = tag if tag in ('script', 'style') else self.context
        if tag == 'script':
            self.script = []
        rewritten = []
        for name, value in attrs:
            if value is not None:
                if name in ('href', 'src', 'poster', 'data-src', 'data-background', 'data-original', 'data-video'):
                    if (tag == 'iframe' or name == 'data-video') and canonical(value, self.url) and urllib.parse.urlsplit(canonical(value, self.url)).netloc not in HOSTS:
                        self.mirror.external_embeds.add(canonical(value, self.url))
                    else:
                        value = self.mirror.reference(value, self.url, page=tag in ('a', 'iframe'))
                elif name in ('srcset', 'data-srcset'):
                    value = ', '.join(' '.join([self.mirror.reference(item.strip().split()[0], self.url)] + item.strip().split()[1:]) for item in value.split(',') if item.strip())
                elif name == 'style':
                    value = CSS_URL.sub(lambda match: 'url("' + self.mirror.reference(match.group(2), self.url) + '")', value)
                elif name == 'action':
                    value = '#'
            rewritten.append(name if value is None else '{}="{}"'.format(name, html.escape(value, quote=True)))
        start = '<' + tag + (' ' + ' '.join(rewritten) if rewritten else '') + '>'
        (self.script if tag == 'script' else self.output).append(start)
        if tag == 'head':
            depth = len(Path(local_path(self.url)).parts) - 1
            self.output.append('<meta charset="utf-8"><base href="' + ('../' * depth or './') + '"><script src="local-preview.js"></script>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if self.skip and tag == 'script':
            self.skip = False
            self.context = ''
            return
        if not self.skip:
            if tag == 'script':
                content = ''.join(self.script)
                if not any(tracker in content for tracker in TRACKERS) and "gtag('config'" not in content:
                    self.output.append(content + '</script>')
                self.script = []
            else:
                self.output.append('</' + tag + '>')
        if tag == self.context:
            self.context = ''

    def handle_data(self, data):
        if self.skip:
            return
        if self.context == 'style':
            data = CSS_URL.sub(lambda match: 'url("' + self.mirror.reference(match.group(2), self.url) + '")', data)
        if self.context == 'script':
            data = data.replace('https://www.ascolite.in/', '').replace('https://ascolite.in/', '')
            self.script.append(data)
        else:
            self.output.append(data)

    def handle_entityref(self, name):
        self.output.append('&' + name + ';')

    def handle_charref(self, name):
        self.output.append('&#' + name + ';')

    def handle_comment(self, data):
        self.output.append('<!--' + data + '-->')

    def handle_decl(self, decl):
        self.output.append('<!' + decl + '>')


def self_test():
    assert local_path(ORIGIN) == 'index.html'
    assert local_path(ORIGIN + 'about.php') == 'about.html'
    assert canonical('/images/icon (1).svg') == ORIGIN + 'images/icon%20(1).svg'
    assert canonical('  https://ascolite.in/contact.php  ') == ORIGIN + 'contact.php'
    assert canonical(ORIGIN + 'contact.php%20%20') == ORIGIN + 'contact.php'
    assert local_path(ORIGIN + 'products/walling/block') == 'products/walling/block/index.html'
    mirror = Mirror()
    assert mirror.reference('images/webp/product-2.webp', ORIGIN + 'blog/example/') == 'images/webp/product-2.webp'
    parser = PageParser(mirror, ORIGIN + 'blog/example/')
    parser.feed('<html><head></head><body><a href="/about.php">About</a><img src="/uploads/a.webp"><video src="/uploads/a.mp4"></video></body></html>')
    rendered = ''.join(parser.output)
    assert '<base href="../../">' in rendered
    assert 'href="about.html"' in rendered
    assert rendered.index('charset="utf-8"') < 100
    tracking = PageParser(mirror, ORIGIN)
    tracking.feed('<script>load("https://connect.facebook.net/x.js")</script><script>keep()</script>')
    assert 'connect.facebook' not in ''.join(tracking.output)
    assert '<script>keep()</script>' in ''.join(tracking.output)
    assert ORIGIN + 'uploads/a.mp4' in mirror.assets
    assert mirror.css('a{background:url(../images/a.png)}', ORIGIN + 'css/style.css') == 'a{background:url("../images/a.png")}'
    print('PASS: homepage, PHP and nested routes, HTML asset discovery, video and CSS rewriting')


if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--limit', type=int, default=1500)
    arguments.add_argument('--self-test', action='store_true')
    arguments.add_argument('--retry-failed', action='store_true')
    arguments.add_argument('--rebuild', action='store_true')
    options = arguments.parse_args()
    if options.self_test:
        self_test()
    else:
        mirror = Mirror()
        if options.rebuild:
            report = json.loads((ROOT / 'download-report.json').read_text(encoding='utf-8'))
            for url in report['pages']:
                mirror.build_page(url)
            report['pages'] = mirror.pages
            missing = sorted(url for url in mirror.assets if not (ROOT / local_path(url)).exists())
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(mirror.download, missing))
            report['assets'] = sorted(set(report['assets']) | set(url for url, target in zip(missing, results) if target))
            report['failed'].update(mirror.failed)
            report['external_video_embeds'] = sorted(mirror.external_embeds)
            (ROOT / 'download-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            print('Rebuilt {} cached pages; checked {} newly referenced assets.'.format(len(mirror.pages), len(missing)))
            raise SystemExit(0)
        if options.retry_failed:
            report = json.loads((ROOT / 'download-report.json').read_text(encoding='utf-8'))
            mirror.pages = report['pages']
            mirror.assets = set(canonical(url) for url in report['assets'])
            mirror.pending = set(canonical(url) for url in report['failed'] if is_page(url))
            mirror.assets.update(canonical(url) for url in report['failed'] if not is_page(url))
            mirror.external_embeds = set(report['external_video_embeds'])
        mirror.build(options.limit)