# HI TECH Local Website

Static HTML copy of public pages linked from https://ascolite.in/, using the original Bootstrap, CSS, JavaScript, images and downloadable media.

## Download

Run `python mirror.py` from this folder. Existing downloads are reused. The default ceiling is 1,500 discovered pages; use `--limit 3000` to raise it. `download-report.json` lists saved pages, assets, failures, external embeds and remaining pages.

Run `python mirror.py --retry-failed` to retry unavailable downloads. Run `python mirror.py --rebuild` to regenerate the HTML from cached source pages after changes to the downloader. Run `python mirror.py --self-test` to check link and asset rewriting.

## Preview

Run `python serve.py`, then open http://127.0.0.1:8081/. Use `--port 8082` if that port is already occupied. The threaded preview server supports Python 3.6 and later.

Pages are ordinary HTML files; no PHP server, Node.js, build step or database is needed. The original site uses Bootstrap 5.3.2, Owl Carousel and AOS alongside custom styles.

## Branding

The displayed company name is HI TECH and the address is Rola, Dungari, Valsad. The shared logo is an SVG recreation of the supplied artwork, maintained in `images/svg/hi-tech-logo.svg` and copied to `images/svg/logo.svg`.

After downloading or rebuilding source pages, run `.\rebrand.ps1` in PowerShell to reapply the branding, then `.\rebrand.ps1 -Check` to validate it. Source downloads and cached pages contain the old catalog: do not publish a rebuild without applying the product cleanup below.

## Approved Product Catalog

Only ASCOFIX BJM/TBM, READY MIX MORTAR, ASCOGROUT 65 and ASCOTOP FH 111 are retained. The approved image bundle is under `uploads/images/approved/`. Legacy product pages, menu entries, related-product cards, packaging images, obsolete product articles and original PDF downloads have been removed. Shared images still used by retained pages are preserved.

The cleanup utility requires Python 3.7+ and Beautiful Soup (`python -m pip install beautifulsoup4`). Run `python cleanup-products.py --self-test`, then `python cleanup-products.py` for a dry run. Apply with `python cleanup-products.py --apply` and validate with `python cleanup-products.py --check`. The exact deleted-file list and retained product routes are saved in `product-cleanup-report.json`.

## Context Photography

Contextual photography is refreshed across the HTML pages while authentic product photographs, named staff portraits, customer logos, branding, interface graphics, and documentary artwork are retained. The manually selected homepage banners, product-category covers, and application photos are retained as already refreshed.

Run `python refresh-images.py --self-test` for the focused rewrite checks. Run `python refresh-images.py --check` to verify local replacement files, complete coverage, and unchanged protected-image reference counts. The source-to-replacement decisions are listed in `image-refresh-report.json`.

After rebuilding the source pages, run `python refresh-images.py --apply` after the branding step, then run `--check`. Finally run the approved product cleanup and its `--check` before publishing. The historical photography report includes assets intentionally removed by the product cleanup. New stock photos are illustrative and do not depict actual HI TECH staff, premises, projects, or certifications. Licensing information is in [Context Photography Credits](images/site-photos/CREDITS.md) and [Application Photo Credits](images/applications/CREDITS.md).

## Limitations

This is a front-end snapshot, not the original backend. Forms do not submit. Social media, maps and YouTube embeds remain online services; only directly referenced downloadable video files can be saved. Unlinked private pages cannot be discovered. Obtain permission before publishing the site's branding and media.

The captured site references 30 YouTube video embeds and no direct MP4/WebM video files. These videos have not been downloaded. The download report also includes source-site 404 responses and non-HTML RSS/API endpoints; those are not recreated pages. Shared image paths and the missing search-icon reference are repaired using the site's existing assets.