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

  /* escritura por segmentos: las palabras clave nacen resaltadas; al final, sus pestañas se encienden en orden */
  var typeSegs = function (el, onDone) {
    var segs; try { segs = JSON.parse(el.getAttribute('data-segs')); } catch (e) { segs = [{ t: el.textContent }]; }
    el.textContent = ''; var si = 0, ci = 0, cur = null;
    (function step() {
      if (si >= segs.length) { onDone && onDone(); return; }
      var sg = segs[si];
      if (ci === 0) { cur = document.createElement('span'); if (sg.k) { cur.className = 'k'; cur.setAttribute('data-k', sg.k); } el.appendChild(cur); }
      ci += 1; cur.textContent = sg.t.slice(0, ci);
      if (ci >= sg.t.length) { si += 1; ci = 0; }
      setTimeout(step, 26 + Math.random() * 28);
    })();
  };
  /* cada palabra clave VUELA desde la frase hasta su pestaña, con estela, y la enciende al llegar */
  var lightTabs = function (scope, delay) {
    var pairs = []; scope.querySelectorAll('.k[data-k]').forEach(function (k) { var key = k.getAttribute('data-k'); var t = scope.querySelector('.plat-tabs [data-k="' + key + '"]'); if (t && !pairs.some(function (p) { return p.key === key; })) pairs.push({ key: key, from: k, to: t }); });
    pairs.forEach(function (p, i) { setTimeout(function () {
      var a = p.from.getBoundingClientRect(), b = p.to.getBoundingClientRect();
      if (!a.width || !b.width || !('animate' in document.body)) { p.to.classList.add('lit'); return; }
      var chip = document.createElement('span'); chip.className = 'fly'; chip.textContent = p.to.textContent; document.body.appendChild(chip);
      var c = chip.getBoundingClientRect(); var x0 = a.left + a.width / 2 - c.width / 2, y0 = a.top + a.height / 2 - c.height / 2, x1 = b.left + b.width / 2 - c.width / 2, y1 = b.top + b.height / 2 - c.height / 2;
      var mx = (x0 + x1) / 2 + (x1 > x0 ? 40 : -40), my = Math.min(y0, y1) - 60;
      chip.style.left = '0'; chip.style.top = '0';
      var anim = chip.animate([{ transform: 'translate(' + x0 + 'px,' + y0 + 'px) scale(.85)', opacity: 0 }, { transform: 'translate(' + x0 + 'px,' + y0 + 'px) scale(1.05)', opacity: 1, offset: .15 }, { transform: 'translate(' + mx + 'px,' + my + 'px) scale(1)', opacity: 1, offset: .6 }, { transform: 'translate(' + x1 + 'px,' + y1 + 'px) scale(.6)', opacity: 0 }], { duration: 900, easing: 'cubic-bezier(.22,1,.36,1)', fill: 'forwards' });
      for (var d = 0; d < 6; d++) (function (d) { setTimeout(function () { var r = chip.getBoundingClientRect(); if (!r.width) return; var dot = document.createElement('span'); dot.className = 'fly-trail'; dot.style.left = (r.left + r.width / 2) + 'px'; dot.style.top = (r.top + r.height / 2) + 'px'; document.body.appendChild(dot); dot.animate([{ transform: 'scale(1)', opacity: .9 }, { transform: 'scale(.2)', opacity: 0 }], { duration: 500, easing: 'ease-out', fill: 'forwards' }).onfinish = function () { dot.remove(); }; }, 120 + d * 110); })(d);
      anim.onfinish = function () { chip.remove(); p.to.classList.add('lit'); p.to.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.12)' }, { transform: 'scale(1)' }], { duration: 320, easing: 'ease-out' }); };
    }, (delay || 0) + i * 420); });
  };
  var fullText = function (el) { var segs; try { segs = JSON.parse(el.getAttribute('data-segs')); } catch (e) { return; } el.innerHTML = segs.map(function (sg) { return sg.k ? '<span class="k" data-k="' + sg.k + '">' + sg.t + '</span>' : sg.t; }).join(''); };

  /* el hero: la idea se ESCRIBE una vez; después se arma la plataforma (sin JS o con reduced-motion: todo visible, quieto) */
  document.querySelectorAll('.flow').forEach(function (flow) {
    var t = flow.querySelector('.fl-type'); if (!t) return;
    if (getComputedStyle(flow).display === 'none') { flow.classList.add('typed'); return; }
    flow.classList.add('typing');
    var start = function () { typeSegs(t, function () { flow.classList.remove('typing'); flow.classList.add('typed'); var pl = flow.querySelector('.plat'); if (pl) pl.classList.add('assemble'); setTimeout(function () { flow.querySelectorAll('.late-count').forEach(runCount); }, 500); lightTabs(flow, 1000); }); };
    setTimeout(start, 700);
    setTimeout(function () { if (!flow.classList.contains('typed')) { fullText(t); flow.classList.remove('typing'); flow.classList.add('typed'); lightTabs(flow, 300); } }, 9000);
  });

  /* el fondo del hero: atina en video silencioso SOLO en escritorio, después del load, nunca con reduced-motion ni save-data */
  var hv = document.getElementById('hero-vid');
  if (hv && !reduce && matchMedia('(min-width:1000px)').matches && !(navigator.connection && navigator.connection.saveData)) {
    addEventListener('load', function () { setTimeout(function () {
      var w = document.createElement('source'); w.src = hv.getAttribute('data-webm'); w.type = 'video/webm';
      var m = document.createElement('source'); m.src = hv.getAttribute('data-mp4'); m.type = 'video/mp4';
      hv.appendChild(w); hv.appendChild(m); hv.load();
      hv.addEventListener('playing', function () { hv.classList.add('is-ready'); requestAnimationFrame(function () { hv.classList.add('is-on'); }); }, { once: true });
      var pr = hv.play(); if (pr && pr.catch) pr.catch(function () {});
    }, 800); });
  }

  /* «Cómo funciona»: escribe → procesa → construye, una pasada, al entrar en pantalla */
  var build = document.getElementById('build');
  if (build) {
    var bt = build.querySelector('.b-type'), steps = build.querySelectorAll('.b-proc li'), clock = build.querySelector('.b-time');
    var finish = function () { build.classList.add('p2', 'p3'); steps.forEach(function (li) { li.classList.add('done'); }); if (bt) fullText(bt); build.querySelectorAll('.late-count').forEach(function (el) { el.textContent = parseFloat(el.dataset.count).toLocaleString('es-CO'); }); };
    if (!('IntersectionObserver' in window)) finish();
    else {
      var started = false, t0 = 0, tick = null;
      var startBuild = function () {
        if (started) return; started = true; t0 = performance.now();
        tick = setInterval(function () { var s = Math.floor((performance.now() - t0) / 1000); clock.textContent = '00:' + (s < 10 ? '0' : '') + s; }, 250);
        build.classList.add('p1');
        typeSegs(bt, function () { build.classList.remove('p1'); build.classList.add('p2'); proc(0); });
        function proc(k) { if (k > 0) steps[k - 1].classList.replace('on', 'done'); if (k >= steps.length) { build.classList.add('p3'); clearInterval(tick); var pl = build.querySelector('.plat'); if (pl) pl.classList.add('assemble'); setTimeout(function () { build.querySelectorAll('.late-count').forEach(runCount); }, 600); lightTabs(build, 1000); return; } steps[k].classList.add('on'); setTimeout(function () { proc(k + 1); }, 650 + k * 120); }
      };
      var bo = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { bo.disconnect(); startBuild(); } }); }, { threshold: .35 });
      bo.observe(build);
      setTimeout(function () { if (!started && build.getBoundingClientRect().top < innerHeight) startBuild(); }, 4000);
    }
  }

  /* skeleton → imagen cargada */
  document.querySelectorAll('.media-skel > img').forEach(function (img) {
    var done = function () { img.classList.add('is-loaded'); };
    if (img.complete && img.naturalWidth) done(); else { img.addEventListener('load', done); img.addEventListener('error', done); }
  });

  /* count-up de cifras: una sola vez, apagado con reduced-motion */
  var els = document.querySelectorAll('[data-count]:not(.late-count)');
  var runCount = null;
  if (true) {
    var fmt = function (v, dec, suf) { return v.toLocaleString('es-CO', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf; };
    var run = function (el) {
      var target = parseFloat(el.dataset.count), dec = (el.dataset.dec | 0), suf = el.dataset.suf || '', dur = 1400;
      if (reduce && !el.classList.contains('late-count')) { el.textContent = fmt(target, dec, suf); return; }
      var t0 = null;
      setTimeout(function () { el.textContent = fmt(target, dec, suf); }, dur + 80);
      (function step(t) { if (!t0) t0 = t; var p = Math.min((t - t0) / dur, 1); p = 1 - Math.pow(1 - p, 3); el.textContent = fmt(target * p, dec, suf); if (p < 1) requestAnimationFrame(step); })(performance.now());
    };
    runCount = run;
    if (els.length && 'IntersectionObserver' in window) {
      var io2 = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { run(e.target); io2.unobserve(e.target); } }); }, { threshold: .6 });
      els.forEach(function (el) { io2.observe(el); });
    } else els.forEach(run);
  }
  if (reduce) document.querySelectorAll('.late-count').forEach(function (el) { el.textContent = parseFloat(el.dataset.count).toLocaleString('es-CO'); });

  /* barra móvil: aparece cuando el CTA del hero sale de vista */
  var cta = document.querySelector('.hero .cta-row');
  if (cta && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { root.classList.toggle('show-bar', !en[0].isIntersecting); }, { threshold: 0 }).observe(cta);
  } else root.classList.add('show-bar');
})();
