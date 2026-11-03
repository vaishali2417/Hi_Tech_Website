(function () {
  'use strict';
  var panels = '.products-menu, .applications-menu, .about-menu, .resource-menu, .media-menu';
  var triggers = {
    'product-listing': '.products-menu',
    'applica-listing': '.applications-menu',
    'about-listing': '.about-menu',
    'resource-listing': '.resource-menu',
    'media-listing': '.media-menu'
  };

  function closeMenus() {
    document.querySelectorAll(panels).forEach(function (panel) {
      panel.classList.remove('active');
      panel.querySelectorAll('.active').forEach(function (item) { item.classList.remove('active'); });
    });
    document.querySelectorAll('[data-site-menu]').forEach(function (trigger) {
      trigger.setAttribute('aria-expanded', 'false');
    });
    document.body.classList.remove('site-menu-open');
  }

  function activate(button) {
    var panel = button.closest(panels);
    var target = document.getElementById(button.getAttribute('data-toggle'));
    if (!panel || !target || !panel.contains(target)) return;
    var column = target.parentElement;
    Array.from(column.children).forEach(function (item) { item.classList.toggle('active', item === target); });
    column.classList.add('active');
    button.classList.add('active');
  }

  document.addEventListener('DOMContentLoaded', function () {
    Object.keys(triggers).forEach(function (name) {
      document.querySelectorAll('.' + name).forEach(function (trigger) {
        trigger.setAttribute('data-site-menu', triggers[name]);
        trigger.setAttribute('aria-expanded', 'false');
        trigger.setAttribute('aria-haspopup', 'true');
      });
    });
    document.querySelectorAll('[data-video]').forEach(function (tile) {
      tile.setAttribute('role', 'button');
      tile.setAttribute('tabindex', '0');
      tile.setAttribute('aria-label', tile.getAttribute('aria-label') || tile.textContent.trim() || tile.getAttribute('alt') || 'Play video');
    });
    document.querySelectorAll('img[data-fallback]').forEach(function (image) {
      image.addEventListener('error', function () {
        if (image.getAttribute('src') !== image.dataset.fallback) image.src = image.dataset.fallback;
      });
    });
  });

  document.addEventListener('click', function (event) {
    var trigger = event.target.closest('[data-site-menu]');
    if (trigger) {
      event.preventDefault();
      event.stopImmediatePropagation();
      var panel = document.querySelector(trigger.getAttribute('data-site-menu'));
      var wasOpen = panel && panel.classList.contains('active');
      closeMenus();
      if (panel && !wasOpen) {
        panel.classList.add('active');
        panel.querySelector('.firstmenulist').classList.add('active');
        trigger.setAttribute('aria-expanded', 'true');
        document.body.classList.add('site-menu-open');
        var collapse = document.querySelector('.navbar-collapse.show');
        if (collapse && window.bootstrap) window.bootstrap.Collapse.getOrCreateInstance(collapse).hide();
      }
      return;
    }
    var panel = event.target.closest(panels);
    var close = event.target.closest('.closemenu');
    if (close || (panel && event.target === panel)) {
      event.preventDefault();
      event.stopImmediatePropagation();
      closeMenus();
      return;
    }
    var toggle = event.target.closest('.menuitems .toggler');
    if (panel && toggle && !event.target.closest('a')) {
      event.preventDefault();
      event.stopImmediatePropagation();
      toggle.closest('.menuitems').classList.toggle('active');
      return;
    }
    var item = event.target.closest('button[data-toggle]');
    if (panel && item) {
      event.preventDefault();
      event.stopImmediatePropagation();
      activate(item);
      return;
    }
    var video = event.target.closest('[data-video]');
    if (video) {
      event.preventDefault();
      event.stopImmediatePropagation();
      var modal = document.getElementById('videoModal');
      var frame = modal && modal.querySelector('iframe');
      if (modal && frame && window.bootstrap) {
        frame.src = video.dataset.video + (video.dataset.video.indexOf('?') < 0 ? '?' : '&') + 'autoplay=1';
        frame.title = video.getAttribute('aria-label') || 'HI TECH video';
        window.bootstrap.Modal.getOrCreateInstance(modal).show();
      } else {
        window.open(video.dataset.video, '_blank', 'noopener');
      }
    }
  }, true);

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') closeMenus();
    if ((event.key === 'Enter' || event.key === ' ') && event.target.matches('[data-video]')) {
      event.preventDefault();
      event.target.click();
    }
  });
  document.addEventListener('hidden.bs.modal', function (event) {
    event.target.querySelectorAll('iframe').forEach(function (frame) { frame.src = ''; });
  });
}());