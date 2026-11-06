(function () {
  'use strict';

  var groups = {
    products: {
      title: 'Product Listing',
      sections: [
        { title: 'All Products', links: [['View all products', 'products/index.html']] },
        { title: 'Walling', links: [['Ready Mix Plaster', 'products/walling-solutions/ready-mix-plaster.html'], ['Block Joining Mortar', 'products/walling-solutions/block-joining-mortar.html'], ['GypLife Silver', 'products/walling-solutions/gyplife-silver.html']] },
        { title: 'Structural Repair & Grouting', links: [['Non Shrink Grout', 'products/walling-solutions/non-shrink-grout.html'], ['Micro Concrete', 'products/walling-solutions/micro-concrete.html'], ['Dry Mix Concrete', 'products/walling-solutions/dry-mix-concrete.html']] },
        { title: 'Flooring', links: [['Floor Hardener', 'products/walling-solutions/floor-hardener.html'], ['Floor Screed', 'products/walling-solutions/floor-screed.html']] },
        { title: 'Tile Installation', links: [['Tile Bond S-01 Ceramic Master', 'products/walling-solutions/tile-bond-s01.html'], ['Tile Bond S-02 Vitrified Master', 'products/walling-solutions/tile-bond-s02.html'], ['Tile Bond S-03 Stone & Marble Master', 'products/walling-solutions/tile-bond-s03.html'], ['Tile Adhesive S-04', 'products/walling-solutions/tile-adhesive-s04.html'], ['Tile Adhesive S-05 White', 'products/walling-solutions/tile-adhesive-s05.html']] }
      ]
    },
    about: { title: 'About Us', sections: [{ title: 'About HI TECH', links: [['Overview', 'about/index.html'], ['Our Team', 'team/index.html'], ['Our Customers', 'clients/index.html']] }] },
    knowledge: { title: 'Knowledge Center', sections: [{ title: 'Explore', links: [['Testimonials', 'testimonials/index.html'], ['Project Showcases', 'project/index.html'], ['Blogs', 'blog/index.html']] }] },
    media: { title: 'Media', sections: [{ title: 'News & Updates', links: [['Newsletter', 'newsletter/index.html'], ['Press Release', 'press/index.html']] }] }
  };

  function initializeNavigation() {
    var header = document.querySelector('header');
    if (!header) return;

    var stylesheet = document.createElement('link');
    stylesheet.rel = 'stylesheet';
    stylesheet.href = 'assets/js/shared-header.css';
    document.head.appendChild(stylesheet);

    header.className = 'site-header';
    header.innerHTML = '<nav class="site-nav" aria-label="Main navigation">' +
      '<a class="site-nav-logo" href="index.html"><img src="images/svg/logo.svg?v=hi-tech" alt="HI TECH home"></a>' +
      '<button class="site-nav-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="site-nav-links"><span></span><span></span><span></span></button>' +
      '<div class="site-nav-links" id="site-nav-links">' +
      '<button type="button" data-shared-menu="about" aria-haspopup="dialog" aria-expanded="false">About Us</button>' +
      '<button type="button" data-shared-menu="products" aria-haspopup="dialog" aria-expanded="false">Product Listing</button>' +
      '<a href="application/index.html">Application Areas</a>' +
      '<button type="button" data-shared-menu="knowledge" aria-haspopup="dialog" aria-expanded="false">Knowledge Center</button>' +
      '<a href="resources/index.html">Resources</a>' +
      '<button type="button" data-shared-menu="media" aria-haspopup="dialog" aria-expanded="false">Media</button>' +
      '<a href="contact/index.html">Contact Us</a>' +
      '<a href="career/index.html">Life At HI TECH</a>' +
      '</div></nav>';

    var overlay = document.createElement('div');
    overlay.className = 'shared-menu-overlay';
    overlay.hidden = true;
    overlay.innerHTML = '<div class="shared-menu-panel" role="dialog" aria-modal="true" aria-labelledby="shared-menu-title">' +
      '<div class="shared-menu-heading"><h2 id="shared-menu-title"></h2><button class="shared-menu-close" type="button" aria-label="Close menu">&times;</button></div>' +
      '<div class="shared-menu-content"></div></div>';
    document.body.appendChild(overlay);

    var toggle = header.querySelector('.site-nav-toggle');
    var links = header.querySelector('.site-nav-links');
    var closeButton = overlay.querySelector('.shared-menu-close');
    var content = overlay.querySelector('.shared-menu-content');
    var previousFocus;

    function closeMenu() {
      if (overlay.hidden) return;
      overlay.hidden = true;
      document.body.classList.remove('shared-menu-open');
      if (previousFocus) {
        previousFocus.setAttribute('aria-expanded', 'false');
        previousFocus.focus();
      }
    }

    toggle.addEventListener('click', function () {
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      toggle.setAttribute('aria-label', expanded ? 'Open navigation' : 'Close navigation');
      links.classList.toggle('is-open', !expanded);
    });

    header.addEventListener('click', function (event) {
      var button = event.target.closest('[data-shared-menu]');
      if (!button) return;
      var group = groups[button.getAttribute('data-shared-menu')];
      previousFocus = button;
      button.setAttribute('aria-expanded', 'true');
      overlay.querySelector('#shared-menu-title').textContent = group.title;
      content.replaceChildren();
      group.sections.forEach(function (section) {
        var sectionElement = document.createElement('section');
        var title = document.createElement('h3');
        title.textContent = section.title;
        sectionElement.appendChild(title);
        section.links.forEach(function (item) {
          var link = document.createElement('a');
          link.href = item[1];
          link.textContent = item[0];
          sectionElement.appendChild(link);
        });
        content.appendChild(sectionElement);
      });
      overlay.hidden = false;
      document.body.classList.add('shared-menu-open');
      closeButton.focus();
    });

    closeButton.addEventListener('click', closeMenu);
    overlay.addEventListener('click', function (event) {
      if (event.target === overlay) closeMenu();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeMenu();
      if (event.key !== 'Tab' || overlay.hidden) return;
      var focusable = overlay.querySelectorAll('button, a[href]');
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeNavigation);
  } else {
    initializeNavigation();
  }
}());