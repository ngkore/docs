document.addEventListener('DOMContentLoaded', function () {
  try {
    // Avoid duplicates on hot reload
    if (document.querySelector('.bottom-logo')) return;

    const container = document.createElement('div');
    container.className = 'bottom-logo';

    const link = document.createElement('a');
    link.className = 'bottom-logo-link';
    link.href = 'https://ngkore.org';
    link.title = 'NgKore';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.setAttribute('aria-label', 'NgKore website');

    const img = document.createElement('img');
    img.className = 'bottom-logo-image';
    img.alt = 'NgKore';
    img.loading = 'lazy';
    img.decoding = 'async';
    // Prefer optimized asset in .sphinx/_static if available; fallback to repo image path
    const urlRoot = document.body.getAttribute('data-url_root') || '/';
    // Prefer the static bundled logo to avoid path issues
    img.src = urlRoot + '_static/ngkore-logo.png';
    // Fallback to absolute path if urlRoot missing
    img.onerror = function () {
      img.onerror = null;
      img.src = '/_static/ngkore-logo.png';
    };

    link.appendChild(img);
    container.appendChild(link);
    document.body.appendChild(container);
  } catch (e) {
    console.warn('Failed to attach bottom logo:', e);
  }
});


