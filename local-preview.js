(function () {
  'use strict';
  var originalOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method) {
    if (!/^(GET|HEAD)$/i.test(method)) {
      alert('This is a local preview. Enquiries and subscriptions are not submitted.');
      throw new Error('Backend submissions are disabled in the local preview.');
    }
    return originalOpen.apply(this, arguments);
  };
  document.addEventListener('submit', function (event) {
    event.preventDefault();
    event.stopImmediatePropagation();
    alert('This is a local preview. Enquiries and subscriptions are not submitted.');
  }, true);
}());