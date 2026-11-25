// Keep fixed-header offsets accurate when text, fonts, or the menu change size.
(() => {
  const navbar = document.querySelector('.skope-navbar');
  if (!navbar) return;
  const update = () => document.documentElement.style.setProperty(
    '--skope-navbar-height', `${Math.ceil(navbar.getBoundingClientRect().height)}px`,
  );
  document.documentElement.classList.remove('no-js');
  update();
  if ('ResizeObserver' in window) new ResizeObserver(update).observe(navbar);
  else window.addEventListener('resize', update);
})();
