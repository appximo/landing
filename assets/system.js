/* Appximo — comportamiento compartido de las páginas comerciales.
   Sin JS la página es completa (contrato a); con reduced-motion queda quieta (b);
   con motion, nada queda en opacity:0 (c): el fallback de 2,5 s lo garantiza. */
(function () {
  var root = document.documentElement, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* nav: transparente sobre el hero → sólida al scrollear */
  var nav = document.getElementById('nav');
  function solid() { if (nav) nav.classList.toggle('is-solid', (window.scrollY || 0) > 24); }
  solid(); addEventListener('scroll', solid, { passive: true });

  /* click-to-play (comercial: nunca autoplay) */
  document.querySelectorAll('.vframe').forEach(function (f) {
    var v = f.querySelector('video'), b = f.querySelector('.vplay');
    if (v && b) b.addEventListener('click', function () { b.style.display = 'none'; v.play(); });
  });

  /* reveal por IntersectionObserver */
  var rv = document.querySelectorAll('.reveal');
  if (rv.length && 'IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
    document.querySelectorAll('.bar, .ring').forEach(function (el) { io.observe(el); });
    setTimeout(function () { document.querySelectorAll('.reveal, .bar, .ring').forEach(function (el) { el.classList.add('in'); }); }, 2500);
  } else { rv.forEach(function (el) { el.classList.add('in'); }); document.querySelectorAll('.bar, .ring').forEach(function (el) { el.classList.add('in'); }); }

  /* el hero: la idea se ESCRIBE una vez; después se arma la plataforma (sin JS o con reduced-motion: todo visible, quieto) */
  document.querySelectorAll('.flow').forEach(function (flow) {
    var t = flow.querySelector('.fl-type'); if (!t) return;
    if (reduce || getComputedStyle(flow).display === 'none') { flow.classList.add('typed'); return; }
    var full = t.getAttribute('data-text') || t.textContent, i = 0; t.textContent = ''; flow.classList.add('typing');
    var start = function () { (function step() { i += 1; t.textContent = full.slice(0, i); if (i < full.length) setTimeout(step, 28 + Math.random() * 30); else { flow.classList.remove('typing'); flow.classList.add('typed'); } })(); };
    setTimeout(start, 700);
    setTimeout(function () { if (!flow.classList.contains('typed')) { t.textContent = full; flow.classList.remove('typing'); flow.classList.add('typed'); } }, 9000);
  });

  /* skeleton → imagen cargada */
  document.querySelectorAll('.media-skel > img').forEach(function (img) {
    var done = function () { img.classList.add('is-loaded'); };
    if (img.complete && img.naturalWidth) done(); else { img.addEventListener('load', done); img.addEventListener('error', done); }
  });

  /* count-up de cifras: una sola vez, apagado con reduced-motion */
  var els = document.querySelectorAll('[data-count]');
  if (els.length) {
    var fmt = function (v, dec, suf) { return v.toLocaleString('es-CO', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf; };
    var run = function (el) {
      var target = parseFloat(el.dataset.count), dec = (el.dataset.dec | 0), suf = el.dataset.suf || '', dur = 1400;
      if (reduce) { el.textContent = fmt(target, dec, suf); return; }
      var t0 = null;
      (function step(t) { if (!t0) t0 = t; var p = Math.min((t - t0) / dur, 1); p = 1 - Math.pow(1 - p, 3); el.textContent = fmt(target * p, dec, suf); if (p < 1) requestAnimationFrame(step); })(performance.now());
    };
    if ('IntersectionObserver' in window) {
      var io2 = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { run(e.target); io2.unobserve(e.target); } }); }, { threshold: .6 });
      els.forEach(function (el) { io2.observe(el); });
    } else els.forEach(run);
  }

  /* barra móvil: aparece cuando el CTA del hero sale de vista */
  var cta = document.querySelector('.hero .cta-row');
  if (cta && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { root.classList.toggle('show-bar', !en[0].isIntersecting); }, { threshold: 0 }).observe(cta);
  } else root.classList.add('show-bar');
})();
