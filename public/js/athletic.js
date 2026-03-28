// Athletic theme JS

// Live clock in navbar
function updateClock() {
  const el = document.getElementById('nav-clock');
  if (!el) return;
  const now = new Date();
  const h = String(now.getHours()).padStart(2,'0');
  const m = String(now.getMinutes()).padStart(2,'0');
  el.textContent = `${h}:${m} IST`;
}
updateClock();
setInterval(updateClock, 10000);

// Theme toggle
(function() {
  var btn = document.getElementById('theme-toggle');
  if (!btn) return;

  function getTheme() {
    return document.documentElement.getAttribute('data-theme') || 'dark';
  }

  function updateIcon() {
    btn.textContent = getTheme() === 'dark' ? '\u2600' : '\u263E';
  }

  updateIcon();

  btn.addEventListener('click', function() {
    var next = getTheme() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateIcon();
  });
})();
