# Generador de las tres páginas comerciales (REDISENO-VISUAL-S2).
# Uso: python3 tools/gen2.py — regenera index/conjuntos/caso desde las plantillas y
# ABORTA si el conjunto de enlaces wa.me (18 orígenes) cambia respecto a lo comiteado.
import urllib.parse, re, string
import os; OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'
def wa(m): return 'https://wa.me/573115175472?text='+urllib.parse.quote(m,safe='')
WA='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.53 14.9L2 22l5.25-1.47A9.9 9.9 0 1 0 12.04 2Zm0 1.67a8.22 8.22 0 1 1-4.2 15.3l-.3-.18-3.12.87.84-3.04-.2-.31a8.22 8.22 0 0 1 6.98-12.64Zm-3.3 4.42c-.18 0-.47.07-.72.34-.25.27-.95.93-.95 2.27 0 1.34.97 2.63 1.11 2.81.13.18 1.87 3 4.63 4.08 2.3.9 2.77.72 3.27.68.5-.05 1.62-.66 1.85-1.3.23-.65.23-1.2.16-1.31-.07-.11-.25-.18-.52-.32-.27-.13-1.62-.8-1.87-.9-.25-.09-.43-.13-.61.14-.18.27-.7.9-.86 1.08-.16.18-.32.2-.59.07-.27-.14-1.15-.42-2.19-1.35-.81-.72-1.35-1.61-1.51-1.88-.16-.27-.02-.42.12-.55.12-.12.27-.32.4-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.6-1.46-.83-2-.2-.46-.4-.44-.61-.45h-.53Z"/></svg>'
LOCK='<svg viewBox="0 0 12 14" fill="none" aria-hidden="true"><rect x="1" y="6" width="10" height="7" rx="1.6" fill="currentColor"/><path d="M3.5 6V4.2a2.5 2.5 0 0 1 5 0V6" stroke="currentColor" stroke-width="1.6"/></svg>'
PLAY='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'
ICON='<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 64 64\'%3E%3Crect width=\'64\' height=\'64\' rx=\'14\' fill=\'%2325d366\'/%3E%3Ctext x=\'32\' y=\'45\' font-family=\'Inter,Arial,sans-serif\' font-size=\'38\' font-weight=\'900\' fill=\'%23062b16\' text-anchor=\'middle\'%3EA%3C/text%3E%3C/svg%3E">'
HEAD='''<meta name="theme-color" content="#0b1512">
<link rel="preload" href="assets/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/system.css">
'''+ICON
def bbar(url): return f'<div class="bbar" aria-hidden="true"><span class="bdots"><i></i><i></i><i></i></span><span class="burl">{LOCK}{url}</span></div>'
def cta(href,label='Pedir mi demostración gratis',extra=''): return f'<a class="btn btn-wa{extra}" href="{href}">{WA}{label}</a>'
def ring(pct,label,size='7.5rem',extra=''):
    return f'<div class="ring {extra}" style="--size:{size};--c:264;--p:{pct/100:.4f}" role="img" aria-label="{pct:.1f} por ciento {label}"><svg viewBox="0 0 100 100"><circle class="bg" cx="50" cy="50" r="42"/><circle class="fg" cx="50" cy="50" r="42"/></svg><div class="num"><span>{str(pct).replace(".",",")}<span style="font-size:.55em"> %</span></span><small>{label}</small></div></div>'
def bar(lbl,val,w,sub='',d=0):
    return f'<div class="bar" style="--w:{w}%;--d:{d}s"><span class="lbl">{lbl}</span><span class="val">{val}</span><div class="track"><div class="fill"></div></div>'+(f'<span class="sub">{sub}</span>' if sub else '')+'</div>'
def nav(menu,links='',back=''):
    b=f'<a class="nav-links" href="/" style="text-decoration:none;color:var(--ink-text-dim)">{back}</a>' if back else f'<div class="nav-links">{links}</div>'
    return f'''<nav class="nav" id="nav"><div class="container-x nav-in">
  <a class="logo" href="/"><span class="logo-mark">A</span>appximo</a>
  {b}
  <a class="btn btn-wa compact" href="{menu}">{WA}Demostración gratis</a>
</div></nav>'''
def hero_grid(imgs):
    return '<div class="hero-grid-bg" aria-hidden="true">'+''.join('<div><img src="assets/%s" alt="" width="%s" height="%s" decoding="async" fetchpriority="%s"%s></div>'%(src,w,h,'high' if i==0 else 'low',' loading="lazy"' if i>=2 else '') for i,(src,w,h) in enumerate(imgs))+'</div><div class="hero-veil" aria-hidden="true"></div>'
def foot(extra=''):
    return f'''<footer class="foot"><div class="container-x">
  {extra}
  <p class="t-xs">¿Trabaja en tecnología? La herramienta detrás de esto es un proyecto de código abierto: <a href="https://appximo.github.io/appximo/" rel="noopener">appximo.github.io/appximo</a></p>
  <span class="foot-mark" aria-hidden="true">appximo</span>
</div></footer>'''
SCRIPTS='''<script>document.documentElement.classList.add('js');</script>
<script src="assets/system.js" defer></script>'''
PAGE_CSS='''<style>
  .hero-float{position:absolute;right:var(--gutter);top:clamp(4.5rem,9vw,7rem);z-index:3;display:none;width:15.5rem}
  @media(min-width:1000px){.hero-float{display:block}}
  .hero-float .card-dark{padding:.9rem 1rem}
  .notif{display:flex;align-items:center;gap:.7rem;padding:.55rem 0;border-top:1px solid var(--ink-line)}
  .notif:first-child{border-top:none;padding-top:0}
  .notif .ci{width:1.8rem;height:1.8rem;border-radius:50%;background:var(--color-brand-500);display:flex;align-items:center;justify-content:center;flex:none}
  .notif .ci svg{width:.9rem;height:.9rem}
  .notif b{display:block;font-size:.84rem;line-height:1.2}
  .notif span{display:block;font-size:.72rem;color:var(--ink-text-mute)}
  .case{display:grid;gap:1.6rem;align-items:center}
  @media(min-width:900px){.case{grid-template-columns:7fr 5fr;gap:3rem}.case.flip .case-media{order:2}}
  .case+.case{margin-top:clamp(3rem,7vw,5rem);padding-top:clamp(3rem,7vw,5rem);border-top:1px solid var(--zinc-200)}
  .case h3{font-size:clamp(1.5rem,3.2vw,2.1rem);letter-spacing:-.03em;line-height:1.12;margin:.6rem 0 .7rem;font-weight:800}
  .case p{color:var(--text-2);font-size:1rem}
  .case-media{display:grid;gap:.9rem}
  .case-links{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1.1rem}
  .case-panel{margin-top:1.1rem;padding:1.1rem 1.2rem}
  .case-panel .eyebrow{margin-bottom:.6rem}
  .meaning{margin-top:1rem;background:var(--color-brand-50);border:1px solid var(--color-brand-200);border-left:4px solid var(--color-brand-500);border-radius:var(--radius-xl);padding:.85rem 1rem;color:var(--color-ink);font-size:.95rem}
  .door-grid{display:grid;gap:1rem;align-items:center}
  @media(min-width:860px){.door-grid{grid-template-columns:1fr auto;gap:2rem}}
  .door h2{font-size:clamp(1.35rem,2.8vw,1.8rem);letter-spacing:-.03em}
  .door p{opacity:.85;font-size:.98rem;margin-top:.35rem}
  .invite{display:grid;gap:.9rem;margin-top:1.5rem}
  @media(min-width:700px){.invite{grid-template-columns:1fr 1fr}}
  .pick{display:grid;grid-template-columns:5rem 1fr;gap:1rem;align-items:center;padding:.9rem 1rem;text-decoration:none;color:inherit}
  .pk-img{width:5rem;height:5rem;border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--zinc-200);background:var(--zinc-100)}
  .pk-img img{width:100%;height:100%;object-fit:cover;object-position:top left}
  .pick b{display:block;color:var(--text);font-size:1rem;line-height:1.3}
  .pick span{display:block;color:var(--text-2);font-size:.86rem;line-height:1.45}
  .pick .chip{margin-top:.45rem}
  .steps{display:grid;gap:1.2rem;margin-top:2rem}
  @media(min-width:860px){.steps{grid-template-columns:repeat(4,1fr);gap:1.4rem}}
  .step h3{font-size:1.06rem;margin:.6rem 0 .3rem;color:#fff}
  .step p{color:var(--ink-text-dim);font-size:.94rem}
  .how-grid{display:grid;gap:1.4rem;margin-top:2.4rem;align-items:start}
  @media(min-width:900px){.how-grid{grid-template-columns:7fr 5fr;gap:2.4rem}}
  .no-risk{margin-top:1.4rem;background:rgba(255,255,255,.06);border:1px solid var(--ink-line);border-left:4px solid var(--color-brand-500);border-radius:var(--radius-xl);padding:.95rem 1.1rem;color:#fff;font-size:.97rem}
  .who-grid{display:grid;gap:1.2rem;margin-top:1.8rem}
  @media(min-width:860px){.who-grid{grid-template-columns:3fr 2fr;align-items:start}}
  .people{display:grid;gap:.9rem;margin-top:1rem}
  @media(min-width:520px){.people{grid-template-columns:1fr 1fr}}
  .person{display:flex;gap:.9rem;align-items:center;padding:1rem 1.1rem}
  .person b{display:block;font-size:1rem;line-height:1.25}
  .person span{display:block;font-size:.84rem;color:var(--text-2);line-height:1.4}
  .person .avatar{display:inline-flex;font-size:1.05rem;color:#fff;line-height:1}
  .cred-list{list-style:none;margin-top:.7rem}
  .cred-list li{padding-left:1.5rem;position:relative;margin:.55rem 0;color:var(--text-2);font-size:.95rem}
  .cred-list li::before{content:"✓";position:absolute;left:0;color:var(--color-brand-600);font-weight:800}
  .contact{display:grid;gap:.5rem;margin-top:1rem;font-size:.95rem}
  .contact div{display:flex;gap:.6rem;align-items:baseline}
  .contact b{min-width:6.5rem;color:var(--text-3);font-weight:600;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase}
  .nots{display:grid;gap:.7rem;margin-top:1.4rem;max-width:46rem}
  .not{background:var(--white);border:1px solid var(--zinc-200);border-left:4px solid var(--color-ink);border-radius:var(--radius-lg);padding:.75rem 1rem;color:var(--text-2);font-size:.97rem;box-shadow:var(--shadow-soft)}
  .not b{color:var(--text)}
  .closing{position:relative;overflow:hidden}
  .closing::before{content:"";position:absolute;inset:-40% -20% auto;height:120%;background:radial-gradient(60rem 30rem at 20% 0%,color-mix(in srgb,var(--color-brand-700) 45%,transparent) 0%,transparent 60%);pointer-events:none}
  .closing .container-x{position:relative}
  .closing h2{max-width:16ch}
  .tech{padding:2.4rem 0;border-top:1px solid var(--zinc-200)}
  .tech p{color:var(--text-2);font-size:.92rem;max-width:46rem;margin-top:.5rem}
  .autom{display:grid;gap:1.2rem;align-items:center;padding:1.4rem 1.5rem;margin-top:1.4rem}
  @media(min-width:760px){.autom{grid-template-columns:3fr 2fr;gap:2rem}}
  .autom h3{font-size:1.35rem;color:#fff;margin-bottom:.35rem}
  .autom p{color:var(--ink-text-dim);font-size:.96rem}
  .autom-visual{margin:0 auto;max-width:20rem;width:100%}
  @media(max-width:759px){.hero .cta-row .btn-wa{font-size:.95rem;padding:.8rem 1.25rem;gap:.5rem}}
</style>'''

FOOT_I=foot('''<p><strong style="color:#fff">Appximo</strong> — plataformas y sistemas a la medida, hechos en Colombia. WhatsApp: <a href="$M_PIE">+57 311 517 5472</a></p>
  <p>Pruebe los sistemas abiertos: <a href="https://tiendita.appximo.com" rel="noopener">tiendita.appximo.com</a> · <a href="https://petfriendly.appximo.com" rel="noopener">petfriendly.appximo.com</a> · <a href="https://atina.appximo.com" rel="noopener">atina.appximo.com</a></p>
  <p>¿Administra un conjunto residencial? <a href="conjuntos.html">Software para la administración de conjuntos</a> · <a href="caso.html">el caso VecinGo</a></p>''')
FOOT_C=foot('''<p><strong style="color:#fff">Appximo</strong> — plataformas y sistemas a la medida, hechos en Colombia. <a href="/">Todos los sistemas que hacemos</a> · <a href="caso.html">El caso VecinGo</a></p>
  <p>Esta página es para administradores de conjuntos residenciales y propiedad horizontal. ¿Tiene una tienda, un consultorio o una empresa? <a href="/">La página principal es la suya</a>.</p>''')
FOOT_K=foot('''<p><strong style="color:#fff">Appximo</strong> — plataformas y sistemas a la medida, hechos en Colombia. <a href="/">Página principal</a> · <a href="conjuntos.html">Software para conjuntos</a></p>''')
# ============================================================ index.html
m=dict(
 M_MENU=wa('Hola, quiero una demostración gratis para mi negocio. Los vi en appximo.com (menú).'),
 M_TEL=wa('Hola, quiero una demostración gratis para mi negocio. Los vi en appximo.com (teléfono).'),
 M_PRECIO=wa('Hola, quiero saber un rango de precio para mi caso antes de una reunión. (appximo.com · precio)'),
 M_PIE=wa('Hola, quiero una demostración gratis para mi negocio. Los vi en appximo.com (pie de página).'),
 CTA_INICIO=cta(wa('Hola, quiero una demostración gratis para mi negocio. Los vi en appximo.com (inicio).'),extra=' btn-pulse'),
 M_VIDEO=wa('Hola, vi el video de la idea que se vuelve sistema y quiero una demostración gratis para mi negocio. (appximo.com · video)'),
 CTA_PASOS=cta(wa('Hola, quiero contarles qué se me volvió un problema y pedir la demostración gratis. (appximo.com · pasos)')),
 CTA_FINAL=cta(wa('Hola, quiero una demostración gratis para mi negocio. Los vi en appximo.com (final).')),
 CTA_CEL=cta(wa('Hola, quiero una demostración gratis para mi negocio. Los vi en appximo.com (celular).')),
)
JSONLD='{"@context":"https://schema.org","@type":"ProfessionalService","name":"Appximo","url":"https://appximo.com/","description":"Sistemas y plataformas a la medida para negocios, hechos en Colombia: tienda, ERP, agenda, administración de conjuntos. Demostración gratis por WhatsApp.","telephone":"+57 311 517 5472","areaServed":[{"@type":"City","name":"Pereira"},{"@type":"City","name":"Dosquebradas"},{"@type":"Country","name":"Colombia"}],"address":{"@type":"PostalAddress","addressLocality":"Pereira","addressRegion":"Risaralda","addressCountry":"CO"},"sameAs":["https://github.com/appximo/appximo","https://appximo.github.io/appximo/"],"contactPoint":{"@type":"ContactPoint","contactType":"sales","telephone":"+57 311 517 5472","availableLanguage":"es","url":"https://wa.me/573115175472"}}'
index=f'''<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Appximo — Plataformas y sistemas a la medida, en días</title>
<meta name="description" content="Deje de perder pedidos, citas y cuentas: su negocio entero en un solo sistema hecho a su medida. Lo difícil ya está construido; queda andando en días, y lo ve funcionando antes de pagar. Demostración gratis por WhatsApp.">
<meta property="og:title" content="Appximo — Plataformas y sistemas a la medida, en días">
<meta property="og:description" content="Su negocio entero en un solo sistema hecho a su medida, andando en días. Lo ve funcionando antes de pagar.">
<meta property="og:image" content="https://appximo.com/assets/og.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="https://appximo.com/">
<meta property="og:locale" content="es_CO">
<link rel="canonical" href="https://appximo.com/">
<meta name="robots" content="index,follow,max-image-preview:large">
{HEAD}
<script type="application/ld+json">{JSONLD}</script>
{PAGE_CSS}
</head>
<body>
{nav('$M_MENU','<a href="#casos">Casos</a><a href="#pruebe">Pruébelo</a><a href="#como">Cómo funciona</a><a href="#preguntas">Preguntas</a>')}

<header class="hero grain">
  {hero_grid([('tienda-hero.webp',640,600),('pf-panel.webp',1280,640),('tablero-hero.webp',1080,483),('atina-portal.webp',1280,640)])}
  <div class="hero-float" aria-hidden="true"><div class="card-dark">
    <div class="notif"><span class="ci"><svg viewBox="0 0 24 24" fill="none"><path d="M4 12 20 5l-5 14-3.5-5.5L4 12Z" fill="#062b16"/></svg></span><span><b>Pedido nuevo</b><span>Marta · 2 tortas</span></span></div>
    <div class="notif"><span class="ci"><svg viewBox="0 0 24 24" fill="none"><path d="M5 12.5l4.5 5L19 7" stroke="#062b16" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span><b>Pago confirmado</b><span>Aviso al cliente, solo</span></span></div>
    <div class="notif"><span class="ci" style="background:var(--color-ink-500)"><svg viewBox="0 0 24 24" fill="none"><path d="M12 7v6l4 2" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="12" r="9" stroke="#fff" stroke-width="2.2"/></svg></span><span><b>Cita de mañana</b><span>Recordatorio enviado</span></span></div>
  </div></div>
  <div class="container-x">
    <div class="hero-copy">
      <p class="eyebrow">Sistemas a la medida para empresas y organizaciones</p>
      <h1 class="t-6xl" id="hero-h1">Deje de perder pedidos, citas y cuentas: su negocio entero <em>en un solo lugar</em>.</h1>
      <p class="sub" id="hero-sub">Hecho a su medida, no un programa genérico. Lo difícil ya está construido — diez años de oficio en sistemas de bancos — y queda andando en días: una plataforma entera salió en 3 horas y media. <strong>Lo ve funcionando antes de pagar</strong>.</p>
      <div class="cta-row">
        $CTA_INICIO
        <p class="cta-trust">Gratis y sin compromiso · Sin claves ni pagos por adelantado<br><b>Le responde Miguel Acosta, no un robot.</b> Pereira y Dosquebradas, Colombia · <a href="$M_TEL">+57 311 517 5472</a></p>
        <p class="cta-alt">¿Prefiere mirar antes de escribir? <a href="#pruebe">Abra un sistema funcionando, sin registrarse ↓</a></p>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><b>3½<span class="u">h</span></b><span>en que quedó andando una plataforma de 18 módulos</span><span class="stat-x"><a href="caso.html">el caso, documentado paso a paso</a></span></div>
      <div class="stat"><b><span data-count="32" data-dec="0">32</span></b><span>módulos tiene la plataforma que otro desarrollador construyó con nuestra tecnología</span><span class="stat-x"><a href="#casos">contados en su contrato público</a></span></div>
      <div class="stat"><b><span data-count="10" data-dec="0" data-suf="+">10+</span><span class="u">años</span></b><span>en sistemas de bancos detrás de quien le responde</span></div>
    </div>
  </div>
</header>

<template id="hero-retador">
  <span class="v-h1">No le pedimos que nos crea: <em>véalo funcionando</em> ahora mismo.</span>
  <span class="v-sub">Dos sistemas hechos con nuestra tecnología están abiertos en internet: una tienda y una agenda veterinaria. Éntreles sin registrarse y mire cómo cargan al instante. El suyo se hace igual — rápido, seguro y a su medida — y <strong>lo ve funcionando antes de pagar</strong>.</span>
</template>
<template id="hero-puente">
  <span class="v-h1">Un sistema hecho para su negocio, <em>andando en días</em>.</span>
  <span class="v-sub">¿Días de verdad? Una plataforma entera — 18 módulos — quedó funcionando en 3 horas y media. No es magia: es tecnología propia, rápida y segura, con años de oficio en sistemas de bancos detrás. <strong>Lo ve funcionando antes de pagar</strong>.</span>
</template>
<script>
  (function(){{
    var HERO_DEFAULT = 'control'; // ← CAMBIAR AQUÍ para publicar otro hero
    var v = new URLSearchParams(location.search).get('hero') || HERO_DEFAULT;
    if (v === 'control') return;
    var t = document.getElementById('hero-' + v); if (!t) return;
    var d = t.content;
    document.getElementById('hero-h1').innerHTML = d.querySelector('.v-h1').innerHTML;
    document.getElementById('hero-sub').innerHTML = d.querySelector('.v-sub').innerHTML;
  }})();
</script>

<section class="section s-white" id="casos"><div class="container-x">
  <p class="eyebrow reveal">Lo que ya salió de aquí</p>
  <h2 class="t-5xl reveal" style="max-width:18ch">Dos plataformas completas, la misma tecnología</h2>
  <p class="lead reveal" style="margin-top:1rem">No son maquetas: una está abierta en internet y la otra le sirve a un conjunto residencial. Cada cifra aguanta un clic.</p>

  <article class="case" style="margin-top:clamp(2.4rem,6vw,4rem)">
    <div class="case-media">
      <div class="bframe reveal media-skel">{bbar('atina.appximo.com')}<img src="assets/atina-portal.webp" alt="El portal público de atina: nueve ofertas de empleo con filtros por provincia, área y contrato" width="1280" height="640" loading="lazy"></div>
      <figure class="media reveal" style="--d:.1s"><div class="vframe"><video class="demovid" controls muted playsinline preload="none" poster="assets/poster-atina.webp" width="1280" height="720" aria-label="Video: recorrido de 57 segundos por la plataforma atina — portal, matching, kanban y marca propia"><source src="assets/atina-57.mp4" type="video/mp4"></video><button class="vplay" aria-label="Reproducir el recorrido de atina"><span class="vplay-btn">{PLAY}Ver por dentro · 57 s</span></button></div><figcaption>Grabado sobre la plataforma real. Datos de demostración.</figcaption></figure>
    </div>
    <div class="reveal" style="--d:.15s">
      <span class="chip chip-brand">Prueba de capacidad</span>
      <h3>atina: la construyó otro desarrollador — sin nosotros</h3>
      <p>Una plataforma completa de selección de personal — portal público, área del candidato y panel de la empresa. <strong>La construyó un desarrollador externo</strong> con nuestra tecnología y la documentación publicada. Está en internet: puede abrirla.</p>
      <div class="card case-panel">
        <p class="eyebrow">Qué tiene, contado en su contrato público</p>
        <div class="bars">
          {bar('Módulos (tablas de datos)','32',67,d=0)}
          {bar('Funciones propias, además de lo generado','48',100,d=.1)}
          {bar('Pantallas: portal, candidato, panel y consola','30+',63,d=.2)}
        </div>
      </div>
      <div class="meaning"><b>Qué significa para usted:</b> su sistema no depende de una sola persona. Si otro construyó esto sin nuestra ayuda, cualquier ingeniero puede mantener el suyo.</div>
      <div class="case-links"><a class="btn btn-ghost" href="https://atina.appximo.com" rel="noopener" target="_blank">Abrir atina.appximo.com ↗</a></div>
    </div>
  </article>

  <article class="case flip" id="caso-vecingo">
    <div class="case-media">
      <div class="bframe reveal media-skel">{bbar('vecingo — demo')}<img src="assets/tablero-hero.webp" alt="Tablero del conjunto: PQRS abiertas, unidades en mora con su valor, obras, reservas, visitantes y la asamblea en curso" width="1080" height="483" loading="lazy"></div>
      <figure class="media reveal" style="--d:.1s"><div class="vframe"><video class="demovid" controls muted playsinline preload="none" poster="assets/poster-vecingo.webp" width="1280" height="720" aria-label="Video: recorrido de 5 minutos por la plataforma de conjuntos de 18 módulos, en modo demostración"><source src="assets/vecingo-caso.mp4" type="video/mp4"></video><button class="vplay" aria-label="Reproducir el video del caso"><span class="vplay-btn">{PLAY}Ver el sistema · 5 min</span></button></div><figcaption>Video con datos ficticios. <a href="caso.html">El caso, pantalla por pantalla</a>.</figcaption></figure>
    </div>
    <div class="reveal" style="--d:.15s">
      <span class="chip chip-brand">El caso documentado</span>
      <h3>VecinGo: la administración de un conjunto, en una tarde</h3>
      <p>18 módulos — asambleas por coeficiente, radicados, cartera, parqueaderos sobre el plano — construida en una tarde para un conjunto residencial. El problema que resolvió: la asamblea que se impugna, la cartera en un Excel y las PQRS que se vencen.</p>
      <div class="card case-panel ring-row">
        {ring(58.2,'quórum')}
        <div>
          <b style="display:block;font-size:1rem;line-height:1.25">Quórum por coeficiente, en tiempo real</b>
          <span class="t-sm" style="color:var(--text-2);display:block;margin-top:.3rem">Una asamblea de demostración en curso: 58,2 % de los coeficientes presentes — con quórum, y cada voto ponderado. Se acabó contar papelitos.</span>
          <div style="display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.7rem"><span class="chip">18 módulos</span><span class="chip">3½ h documentadas</span><span class="chip">Asambleas · cartera · PQRS</span></div>
        </div>
      </div>
      <div class="case-links"><a class="btn btn-ghost" href="conjuntos.html">¿Administra un conjunto? Su página →</a><a class="btn btn-ghost" href="caso.html">El caso, en español</a></div>
    </div>
  </article>
</div></section>

<section class="band s-brand door" id="conjuntos"><div class="container-x door-grid">
  <div class="reveal">
    <p class="eyebrow">Para administradores de propiedad horizontal</p>
    <h2>¿Administra un conjunto? Esta es su página.</h2>
    <p>Asambleas con quórum por coeficiente, cartera y mora a la vista, PQRS con radicado. Un sistema hecho para su oficio, no para «cualquier negocio».</p>
  </div>
  <a class="btn btn-ghost reveal" style="--d:.1s" href="conjuntos.html">Ver el sistema para conjuntos →</a>
</div></section>

<section class="section-tight s-zinc" id="pruebe"><div class="container-x">
  <p class="eyebrow reveal">Y además, puede entrar a tocar</p>
  <h2 class="t-3xl reveal">Dos sistemas abiertos en internet, sin registrarse</h2>
  <p class="lead reveal t-sm" style="margin-top:.5rem">No le pedimos que nos crea. Entre, toque, y mire cómo cargan.</p>
  <div class="invite">
    <a class="card card-hover pick reveal" href="https://tiendita.appximo.com" rel="noopener" target="_blank">
      <span class="pk-img"><img src="assets/tienda-hero.webp" alt="" width="640" height="600" loading="lazy"></span>
      <span><b>¿Vende productos?</b><span>Una tienda con inventario e IVA: compre algo, es de prueba.</span><span class="chip chip-brand"><i class="dot"></i>En internet ahora mismo</span></span>
    </a>
    <a class="card card-hover pick reveal" style="--d:.08s" href="https://petfriendly.appximo.com" rel="noopener" target="_blank">
      <span class="pk-img"><img src="assets/pf-panel.webp" alt="" width="1280" height="640" loading="lazy"></span>
      <span><b>¿Citas y clientes?</b><span>Una agenda veterinaria: toque el panel, nada se guarda.</span><span class="chip chip-brand"><i class="dot"></i>En internet ahora mismo</span></span>
    </a>
  </div>
</div></section>

<section class="section s-ink" id="como"><div class="container-x">
  <p class="eyebrow reveal">Cómo funciona</p>
  <h2 class="t-4xl reveal">Escribir no lo compromete a nada</h2>
  <p class="lead reveal" style="margin-top:1rem">Decidir da miedo: el primer paso es mínimo.</p>
  <div class="steps">
    <div class="step reveal"><div class="step-n">01</div><h3>Escriba, o mande un audio</h3><p>Cuéntenos qué se le volvió un problema.</p></div>
    <div class="step reveal" style="--d:.08s"><div class="step-n">02</div><h3>Una conversación corta</h3><p>Cómo trabaja hoy, quién lo usaría, qué no puede fallar. Sin claves ni cuentas de nada.</p></div>
    <div class="step reveal" style="--d:.16s"><div class="step-n">03</div><h3>La demostración — gratis</h3><p>En una reunión corta lo ve andando con datos de ejemplo y pide cambios.</p></div>
    <div class="step reveal" style="--d:.24s"><div class="step-n">04</div><h3>Solo entonces, el precio</h3><p>Cerrado y por escrito. Si sigue, queda en internet con sus claves.</p></div>
  </div>
  <div class="how-grid">
    <figure class="media reveal"><div class="vframe"><video class="demovid" controls muted playsinline preload="none" poster="assets/poster-idea.webp" width="1280" height="800" aria-label="Video: una idea escrita en español se convierte en un sistema funcionando, en tiempo real"><source src="assets/idea-a-sistema.mp4" type="video/mp4"></video><button class="vplay" aria-label="Reproducir el video"><span class="vplay-btn">{PLAY}Ver · 45 s</span></button></div><figcaption>Así <strong>empieza</strong> la demostración gratis: su idea, en español, funcionando. Grabación real, sin acelerar. <a href="$M_VIDEO">¿Quiere verlo con los datos de su negocio? Pídalo por WhatsApp →</a></figcaption></figure>
    <div class="reveal" style="--d:.1s">
      <div class="card-dark card-pad">
        <p class="eyebrow">Por qué en días y no en meses</p>
        <div class="bars">
          {bar('Lo que ya viene construido y probado — usuarios, claves, permisos, listas, copias, monitoreo','minutos',18,'En el caso documentado: el armazón entero validó en la segunda pasada.',0)}
          {bar('Lo que es solo suyo — sus reglas, sus pantallas, su forma de trabajar','el 70 % del tiempo',70,'Ahí va el oficio. Ahí es donde debe ir.',.15)}
        </div>
      </div>
      <div class="no-risk"><strong>Si la demostración no le sirve, no pasó nada:</strong> no paga, no queda amarrado, no insistimos.</div>
      <p style="margin-top:1.2rem">$CTA_PASOS</p>
    </div>
  </div>
  <div class="card-dark autom reveal">
    <div><h3>Sistemas que trabajan solos</h3><p>El pedido entra y el aviso sale solo. <strong style="color:#fff">Automatizamos lo repetitivo</strong> — chat, correo, entre sistemas — y su operación cuesta menos horas.</p></div>
    <figure class="autom-visual" aria-label="Ilustración: el sistema envía avisos automáticos al celular">
      <svg viewBox="0 0 520 340" role="img" xmlns="http://www.w3.org/2000/svg">
        <rect x="16" y="128" width="150" height="84" rx="14" fill="#182620"/><text x="91" y="164" text-anchor="middle" font-family="Inter,system-ui,Arial" font-weight="700" font-size="18" fill="#fff">Su sistema</text>
        <rect x="40" y="178" width="30" height="7" rx="3.5" fill="#25d366"/><rect x="76" y="178" width="46" height="7" rx="3.5" fill="#2c4034"/><rect x="128" y="178" width="18" height="7" rx="3.5" fill="#2c4034"/>
        <path d="M 170 170 C 214 170 230 168 282 168" stroke="#25d366" stroke-width="3" stroke-dasharray="7 7" fill="none"/><path d="M 226 156 l 26 10 -26 10 6 -10 z" fill="#25d366"/>
        <rect x="296" y="24" width="208" height="292" rx="26" fill="#060d0a"/><rect x="308" y="38" width="184" height="264" rx="16" fill="#fafafa"/>
        <rect x="318" y="56" width="164" height="70" rx="12" fill="#fff" stroke="#e4e4e7"/><circle cx="340" cy="80" r="13" fill="#25d366"/><path d="M 333 80 l 14 -6 -4 12 -3.5 -4 z" fill="#062b16"/><text x="360" y="78" font-family="Inter,system-ui,Arial" font-size="14" font-weight="700" fill="#0b1512">Pedido nuevo</text><text x="360" y="98" font-family="Inter,system-ui,Arial" font-size="12" fill="#52525b">Marta · 2 tortas</text>
        <rect x="318" y="136" width="164" height="70" rx="12" fill="#fff" stroke="#e4e4e7"/><circle cx="340" cy="160" r="13" fill="#c2410c"/><text x="340" y="166" text-anchor="middle" font-family="Inter,system-ui,Arial" font-size="16" font-weight="800" fill="#fff">!</text><text x="360" y="158" font-family="Inter,system-ui,Arial" font-size="14" font-weight="700" fill="#0b1512">Inventario bajo</text><text x="360" y="178" font-family="Inter,system-ui,Arial" font-size="12" fill="#52525b">Harina: quedan 3</text>
        <rect x="318" y="216" width="164" height="70" rx="12" fill="#fff" stroke="#e4e4e7"/><circle cx="340" cy="240" r="13" fill="#25d366"/><path d="M 334 240 l 4.5 5 8 -10" stroke="#062b16" stroke-width="2.6" fill="none" stroke-linecap="round"/><text x="360" y="238" font-family="Inter,system-ui,Arial" font-size="14" font-weight="700" fill="#0b1512">Pago confirmado</text><text x="360" y="258" font-family="Inter,system-ui,Arial" font-size="12" fill="#52525b">Aviso al cliente</text>
      </svg>
    </figure>
  </div>
</div></section>

<section class="section s-white" id="quien"><div class="container-x">
  <p class="eyebrow reveal">Quién responde</p>
  <h2 class="t-4xl reveal">No somos una promesa: ya funciona</h2>
  <div class="who-grid">
    <div class="reveal">
      <p class="lead">El WhatsApp lo contesta quien construye el sistema. <strong>Diez+ años en sistemas de bancos</strong> y una tecnología propia pionera: sistemas completos en días.</p>
      <div class="people">
        <div class="card person" data-pendiente="FOTO-PENDIENTE"><span class="avatar" aria-hidden="true">MA</span><span><b>Miguel Acosta</b><span>Parte técnica · 10 años en sistemas de bancos · Pereira</span></span></div>
        <div class="card person" data-pendiente="SOCIA-PENDIENTE FOTO-PENDIENTE"><span class="avatar" aria-hidden="true" style="--g:1;background:linear-gradient(135deg,var(--color-ink-600),var(--color-ink-800))">·</span><span><b>Ingeniera de sistemas</b><span>La otra mitad del proyecto · Dosquebradas</span></span></div>
      </div>
      <div class="contact">
        <div><b>WhatsApp</b><a href="$M_TEL">+57 311 517 5472</a></div>
        <div><b>Dónde</b><span>Pereira y Dosquebradas, Colombia — y en todo el país por videollamada</span></div>
      </div>
    </div>
    <div class="card card-pad reveal" style="--d:.1s">
      <ul class="cred-list" style="margin-top:0">
        <li><strong>Rápido de verdad:</strong> la <a href="https://tiendita.appximo.com" rel="noopener" target="_blank">tienda</a> y la <a href="https://petfriendly.appximo.com" rel="noopener" target="_blank">agenda</a> abren al instante.</li>
        <li><strong>Seguro por diseño:</strong> estándares OWASP — contraseñas cifradas, archivos verificados, permisos por usuario.</li>
        <li><strong>Se monitorea solo:</strong> vigila su salud y deja registro — incluido.</li>
        <li><strong>Suyo de verdad:</strong> queda en un servidor a su nombre, con sus claves; su equipo técnico, si lo tiene, puede administrarlo.</li>
      </ul>
    </div>
  </div>
</div></section>

<section class="section s-zinc" id="preguntas"><div class="container-x">
  <p class="eyebrow reveal">Para que no haya sorpresas</p>
  <h2 class="t-4xl reveal">Lo que no hacemos</h2>
  <div class="nots">
    <div class="not reveal"><b>No hacemos aplicaciones de celular:</b> va en el navegador.</div>
    <div class="not reveal" style="--d:.06s"><b>No reemplazamos a su contador:</b> las ventas y el IVA salen claros.</div>
    <div class="not reveal" style="--d:.12s"><b>No cobramos por horas abiertas:</b> precio cerrado por escrito, o no empezamos.</div>
    <div class="not reveal" style="--d:.18s"><b>¿Solo necesita una página?</b> Eso sale más barato en otro lado.</div>
  </div>
  <p class="eyebrow reveal" style="margin-top:2.6rem">Preguntas frecuentes</p>
  <h2 class="t-3xl reveal">Lo que todos preguntan</h2>
  <div class="faq reveal">
    <details><summary>¿Cuánto cuesta?</summary><div class="a">
      <p>Depende del tamaño: no cuesta lo mismo ordenar las citas de un consultorio que una plataforma con inventario o votaciones. Una tarifa única sería mentirle en alguna de las dos direcciones.</p>
      <p>Lo que sí es fijo: <strong>la demostración es gratis</strong>, y antes de empezar usted recibe <strong>un precio cerrado, por escrito</strong>. Sin cobros por horas que nadie controla.</p>
      <p>¿Prefiere un rango antes de cualquier reunión? Pregúntelo por WhatsApp y se lo damos el mismo día.</p>
      <p><a href="$M_PRECIO">Pregunte su rango por WhatsApp →</a></p></div></details>
    <details><summary>¿Sirve para la factura electrónica y la DIAN?</summary><div class="a">
      <p>En Colombia la factura electrónica se emite a través de un proveedor autorizado por la DIAN — así lo hacen todos los programas serios, y su sistema se construye para trabajar con el suyo.</p>
      <p>Y las cuentas quedan claras desde el primer día: cada venta con su IVA calculado y a la vista — <a href="https://tiendita.appximo.com" rel="noopener" target="_blank">compruébelo en la tienda de demostración</a>. Que la DIAN deje de ser un susto de fin de mes: de eso se trata.</p></div></details>
    <details><summary>¿Cuánto se demora?</summary><div class="a"><p>La demostración: una reunión de menos de una hora. El sistema andando en internet: <strong>días</strong> en la mayoría de los casos. Un proceso grande, con varias partes, puede tomar algunas semanas. Lo que no va a escuchar de nosotros es «vuelva en seis meses».</p></div></details>
    <details><summary>¿Y si después necesito cambios?</summary><div class="a"><p>Los va a necesitar — los negocios cambian. Agregar un campo, una regla o una pantalla es trabajo de poco tiempo, no un proyecto nuevo. Se piden por WhatsApp y se cotizan igual: precio cerrado antes de hacerlos.</p></div></details>
    <details><summary>¿Se conecta con lo que ya uso?</summary><div class="a"><p>Sí. Los sistemas que construimos se comunican con otras herramientas: avisos automáticos al chat (Telegram) o al correo, y conexión con otros programas cuando su proceso lo necesita. En la demostración le mostramos cómo aplicaría a su caso. Y los informes le salen para su contador cuando los necesite.</p></div></details>
    <details><summary>¿Mi equipo de TI puede administrarlo?</summary><div class="a"><p>Sí — y es un plus grande: paneles de administración, editor visual, API documentada (REST, GraphQL y OpenAPI) y tecnología de código abierto. Además está pensada para IA: generar o desplegar la base no quema tokens — el motor la trae y la IA solo describe el negocio. Su gente lo opera, lo audita y lo extiende; nosotros acompañamos lo que haga falta.</p></div></details>
    <details><summary>¿Y mis datos actuales, quién los pasa?</summary><div class="a"><p>Nosotros. Su Excel o su cuaderno se cargan al arrancar, y usted revisa todo antes de salir en vivo. Eso va dentro del precio cerrado — no es un cobro sorpresa.</p></div></details>
    <details><summary>¿Quién responde si algo falla?</summary><div class="a"><p>El mismo WhatsApp por el que llegó: le contesta el equipo que construyó su sistema, no un centro de llamadas. Además el sistema se monitorea solo — deja registro de qué pasó y cuándo —, y su información tiene copia de seguridad: un daño se arregla sin perder lo trabajado.</p></div></details>
    <details><summary>¿De quién son los datos? ¿Y si ustedes desaparecen?</summary><div class="a">
      <p><strong>Los datos son suyos, siempre.</strong> El sistema queda instalado en un servidor a su nombre, con sus claves, y puede pedir una copia completa cuando quiera. Para la demostración no pedimos claves ni cuentas de nada: se hace con datos de ejemplo.</p>
      <p>Y si nosotros no estamos, el sistema no se cae: la tecnología de base es pública y está documentada — cualquier ingeniero de sistemas puede tomarla y seguir. Usted no queda amarrado a nadie, ni siquiera a nosotros.</p></div></details>
    <details><summary>¿Tengo que saber de tecnología?</summary><div class="a"><p>No. Si usted maneja WhatsApp, maneja esto. Su equipo entra con una clave y ve listas y botones con los nombres de su negocio: pedidos, citas, casos, clientes. De lo demás nos encargamos nosotros.</p></div></details>
  </div>
</div></section>

<section class="section s-ink closing grain"><div class="container-x">
  <div class="reveal">
    <p class="eyebrow">Empiece hoy</p>
    <h2 class="t-5xl">Cuéntenos qué se le volvió un problema</h2>
    <p class="lead" style="margin-top:1rem">Con eso alcanza: le preguntamos y agendamos su demostración gratis.</p>
    <div class="cta-row">$CTA_FINAL
      <p class="cta-trust">Le responde Miguel Acosta directamente · Pereira y Dosquebradas, Colombia · <a href="$M_TEL">+57 311 517 5472</a></p></div>
  </div>
</div></section>

<section class="tech s-white" id="tecnico"><div class="container-x">
  <p class="eyebrow">Para su equipo técnico</p>
  <h2 class="t-2xl">Lo que su ingeniero va a preguntar</h2>
  <p>La base es Appximo, un proyecto de código abierto, público y documentado. Cada sistema se entrega instalado en un servidor a nombre del cliente, con sus claves. Los datos viven en PostgreSQL, con copia de seguridad y restauración probadas. Seguridad alineada con OWASP: argon2id, validación de archivos por contenido, RBAC por rol y aislamiento por inquilino. Observabilidad nativa: métricas, trazas y alertas de anomalías, sin servicios externos. La API queda documentada (REST, GraphQL y OpenAPI). Rendimiento publicado: p50 1,58 ms a 2.000 RPS. La plataforma de 18 módulos quedó andando en 3½ horas (caso documentado).</p>
  <p class="t-sm">Proyecto y documentación: <a href="https://appximo.github.io/appximo/" rel="noopener">appximo.github.io/appximo</a> · Código: <a href="https://github.com/appximo/appximo" rel="noopener">github.com/appximo/appximo</a></p>
</div></section>

{FOOT_I}

<div class="mobile-cta">$CTA_CEL</div>
{SCRIPTS}
</body>
</html>
'''
html=string.Template(index).substitute(m)
old=open(''+OUT+'index.html',encoding='utf-8').read()
a=set(re.findall(r'https://wa\.me/[^"]+',old)); b=set(re.findall(r'https://wa\.me/[^"]+',html))
assert a==b, ('wa set changed', a^b)
open(OUT+'index.html','w',encoding='utf-8').write(html); print('index ok',len(html))

# ============================================================ conjuntos.html
c=dict(
 M_NAV=wa('Hola, administro un conjunto residencial y quiero una demostración gratis. Los vi en appximo.com/conjuntos (menú).'),
 CTA_HERO=cta(wa('Hola, administro un conjunto residencial y quiero una demostración gratis del sistema de asambleas, cartera y PQRS. (appximo.com/conjuntos · inicio)'),extra=' btn-pulse'),
 CTA_MID=cta(wa('Hola, administro un conjunto y vi la plataforma VecinGo. Quiero una demostración gratis. (appximo.com/conjuntos · caso)'),'Quiero algo así para mi conjunto'),
 CTA_END=cta(wa('Hola, administro un conjunto residencial y quiero una demostración gratis. (appximo.com/conjuntos · final)')),
 CTA_BAR=cta(wa('Hola, administro un conjunto residencial y quiero una demostración gratis. (appximo.com/conjuntos · celular)')),
 M_TEL=wa('Hola, administro un conjunto residencial y quiero una demostración gratis. (appximo.com/conjuntos · teléfono)'),
)
conj=f'''<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Software para administración de conjuntos residenciales — asambleas por coeficiente, cartera y PQRS | Appximo</title>
<meta name="description" content="Sistema a la medida para administradores de propiedad horizontal en Pereira, Dosquebradas y toda Colombia: asambleas con quórum por coeficiente, cartera y mora, PQRS con radicado, parqueaderos y comunicados. Demostración gratis por WhatsApp.">
<link rel="canonical" href="https://appximo.com/conjuntos.html">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:title" content="Software para administración de conjuntos residenciales — Appximo">
<meta property="og:description" content="Asambleas con quórum por coeficiente, cartera al día, PQRS con radicado. Un sistema hecho para la administración de su conjunto. Demostración gratis.">
<meta property="og:image" content="https://appximo.com/assets/og.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="https://appximo.com/conjuntos.html">
<meta property="og:locale" content="es_CO">
{HEAD}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Service","name":"Software para administración de conjuntos residenciales","serviceType":"Sistema de administración de propiedad horizontal a la medida","provider":{{"@type":"ProfessionalService","name":"Appximo","url":"https://appximo.com/","telephone":"+57 311 517 5472","address":{{"@type":"PostalAddress","addressLocality":"Pereira","addressRegion":"Risaralda","addressCountry":"CO"}}}},"areaServed":[{{"@type":"City","name":"Pereira"}},{{"@type":"City","name":"Dosquebradas"}},{{"@type":"Country","name":"Colombia"}}],"audience":{{"@type":"Audience","audienceType":"Administradores de propiedad horizontal"}},"url":"https://appximo.com/conjuntos.html","offers":{{"@type":"Offer","description":"Demostración gratis con datos de ejemplo; precio cerrado por escrito antes de empezar","url":"https://wa.me/573115175472"}}}}</script>
{PAGE_CSS}
<style>
  .pains{{display:grid;gap:1rem;margin-top:1.6rem}}
  @media(min-width:760px){{.pains{{grid-template-columns:repeat(3,1fr)}}}}
  .pain{{padding:1.15rem 1.2rem}}
  .pain h3{{font-size:1.12rem;margin:.55rem 0 .35rem}}
  .pain p{{color:var(--text-2);font-size:.95rem}}
  .pain p b{{color:var(--color-ink)}}
  .vg{{display:grid;gap:1.4rem;margin-top:2rem;align-items:start}}
  @media(min-width:900px){{.vg{{grid-template-columns:7fr 5fr;gap:2.4rem}}}}
  .mods{{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.9rem}}
  .steps2{{margin-top:1.6rem;display:grid;gap:1rem}}
  @media(min-width:760px){{.steps2{{grid-template-columns:repeat(2,1fr)}}}}
  .steps2 .card{{padding:1.1rem 1.2rem}}
  .steps2 .step-n{{color:var(--color-brand-ink);font-size:2rem}}
  .steps2 h3{{font-size:1.05rem;margin:.4rem 0 .25rem}}
  .steps2 p{{color:var(--text-2);font-size:.95rem}}
</style>
</head>
<body>
{nav('$M_NAV',back='← Todos los sistemas')}

<header class="hero grain">
  {hero_grid([('caso-asamblea.webp',1080,245),('tablero-hero.webp',1080,483),('caso-plano.webp',1080,498),('caso-muro.webp',1080,498)])}
  <div class="container-x">
    <div class="hero-copy">
      <p class="eyebrow">Para administradores de propiedad horizontal</p>
      <h1 class="t-5xl" style="max-width:18ch">La asamblea, la cartera y las PQRS de su conjunto, <em>en un solo sistema</em> hecho para usted.</h1>
      <p class="sub">Quórum por coeficiente calculado al instante, cartera con la mora a la vista, PQRS con radicado y respuesta en plazo. <strong>Lo ve funcionando antes de pagar</strong>, con los datos de un conjunto de ejemplo.</p>
      <div class="cta-row">
        $CTA_HERO
        <p class="cta-trust">Gratis y sin compromiso · Sin claves ni pagos por adelantado<br><b>Le responde Miguel Acosta, no un robot.</b> Pereira y Dosquebradas, Colombia · <a href="$M_TEL">+57 311 517 5472</a></p>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><b>18</b><span>módulos en un solo sistema: asambleas, cartera, PQRS, parqueaderos, reservas, obras…</span></div>
      <div class="stat"><b>3½<span class="u">h</span></b><span>de construcción, documentadas paso a paso en el informe del caso</span></div>
      <div class="stat"><b>58,2<span class="u">%</span></b><span>de quórum por coeficiente, calculado en tiempo real en una asamblea</span></div>
    </div>
  </div>
</header>

<section class="section s-white" id="dolores"><div class="container-x">
  <p class="eyebrow reveal">Lo que le quita el tiempo</p>
  <h2 class="t-4xl reveal">Tres cosas del oficio que hoy se hacen a mano</h2>
  <p class="lead reveal" style="margin-top:1rem">Un administrador de conjunto no necesita «software»: necesita que la asamblea cierre con el quórum correcto, que la cartera esté al día sin perseguir un Excel, y que ninguna PQRS se venza sin respuesta. Eso es lo que el sistema hace.</p>
  <div class="pains">
    <article class="card card-hover pain reveal"><span class="chip chip-brand">Ley 675</span><h3>La asamblea y el quórum</h3><p>La Ley 675 manda votar por coeficiente, no por cabeza. Sumar coeficientes a mano, con gente entrando y saliendo, es la fuente de las impugnaciones. <b>El sistema registra la asistencia, calcula el quórum al instante y pondera cada voto por su coeficiente.</b> El acta sale con los números correctos.</p></article>
    <article class="card card-hover pain reveal" style="--d:.08s"><span class="chip chip-brand">Cartera</span><h3>La cartera y la mora</h3><p>Cuotas de administración, extraordinarias, intereses de mora y acuerdos de pago viven en hojas de cálculo que solo una persona entiende. <b>Cada unidad tiene su estado de cuenta, la mora se ve en el tablero y los paz y salvos salen del sistema</b>, no de la memoria.</p></article>
    <article class="card card-hover pain reveal" style="--d:.16s"><span class="chip chip-brand">PQRS</span><h3>Las PQRS con radicado</h3><p>Una petición, queja o reclamo que llega por WhatsApp se pierde, y el residente dice que nunca le respondieron. <b>Cada PQRS recibe un radicado, un responsable y un plazo</b>; el consejo ve cuáles están abiertas y cuáles se vencen esta semana.</p></article>
  </div>
</div></section>

<section class="section s-ink" id="vecingo"><div class="container-x">
  <p class="eyebrow reveal">Así se ve, por dentro</p>
  <h2 class="t-4xl reveal" style="max-width:22ch">Una plataforma de 18 módulos para un conjunto, construida en una tarde</h2>
  <p class="lead reveal" style="margin-top:1rem">Se llama VecinGo y está hecha con nuestra tecnología. Datos de demostración, pantallas reales.</p>
  <div class="vg">
    <div style="display:grid;gap:.9rem">
      <div class="bframe reveal media-skel">{bbar('vecingo — modo demostración')}<img src="assets/tablero-hero.webp" alt="Tablero del conjunto: PQRS abiertas, unidades en mora con su valor, obras, reservas, visitantes y la asamblea en curso" width="1080" height="483" loading="lazy"></div>
      <figure class="media reveal" style="--d:.1s"><div class="vframe"><video id="casovid" controls muted playsinline preload="none" poster="assets/poster-vecingo.webp" width="1280" height="720" aria-label="Video: recorrido de 5 minutos por la plataforma VecinGo en modo demostración"><source src="assets/vecingo-caso.mp4" type="video/mp4"></video><button class="vplay" aria-label="Reproducir el recorrido"><span class="vplay-btn">{PLAY}Ver el recorrido · 5 min</span></button></div><figcaption>Recorrido completo por la plataforma, en modo demostración. <a href="caso.html">El caso, pantalla por pantalla</a>.</figcaption></figure>
    </div>
    <div class="reveal" style="--d:.15s">
      <div class="card-dark card-pad ring-row">
        {ring(58.2,'quórum','7rem','dark')}
        <div><b style="display:block;font-size:1rem;line-height:1.25">Quórum por coeficiente, en tiempo real</b><span class="t-sm" style="color:var(--ink-text-dim);display:block;margin-top:.3rem">Una asamblea de demostración: 58,2 % de los coeficientes presentes — con quórum, cada voto ponderado.</span></div>
      </div>
      <div class="card-dark card-pad" style="margin-top:.9rem">
        <p class="eyebrow">Los 18 módulos</p>
        <div class="mods"><span class="chip chip-ghost">Asambleas y votaciones</span><span class="chip chip-ghost">Cartera y mora</span><span class="chip chip-ghost">PQRS con radicado</span><span class="chip chip-ghost">Parqueaderos con plano</span><span class="chip chip-ghost">Reservas de zonas comunes</span><span class="chip chip-ghost">Visitantes</span><span class="chip chip-ghost">Obras</span><span class="chip chip-ghost">Comunicados</span><span class="chip chip-ghost">Muro del conjunto</span><span class="chip chip-ghost">Unidades y residentes</span><span class="chip chip-ghost">Paz y salvos</span><span class="chip chip-ghost">Paquetes en recepción</span><span class="chip chip-ghost">Roles y permisos</span><span class="chip chip-ghost">Copias de seguridad</span><span class="chip chip-ghost">+ 4 de operación</span></div>
      </div>
      <p style="margin-top:1.2rem">$CTA_MID</p>
    </div>
  </div>
</div></section>

<section class="section s-zinc" id="no-hacemos"><div class="container-x">
  <p class="eyebrow reveal">Para que no haya sorpresas</p>
  <h2 class="t-4xl reveal">Lo que este sistema no hace</h2>
  <div class="nots">
    <div class="not reveal"><b>No reemplaza al contador ni al revisor fiscal:</b> la cartera y los recaudos quedan claros y exportables; la contabilidad sigue siendo de ellos.</div>
    <div class="not reveal" style="--d:.06s"><b>No es una aplicación de celular de tienda:</b> se usa en el navegador del celular o del computador, sin instalar nada.</div>
    <div class="not reveal" style="--d:.12s"><b>No es un programa enlatado:</b> se arma sobre cómo trabaja su conjunto — sus módulos, sus reglas de reserva, sus tipos de cuota. Lo que no usa, no se construye.</div>
    <div class="not reveal" style="--d:.18s"><b>No cobramos por horas abiertas:</b> precio cerrado por escrito antes de empezar, o no empezamos.</div>
  </div>
</div></section>

<section class="section s-white" id="pasos"><div class="container-x">
  <p class="eyebrow reveal">Cómo empieza</p>
  <h2 class="t-4xl reveal">Escribir no lo compromete a nada</h2>
  <div class="steps2">
    <div class="card reveal"><div class="step-n">01</div><h3>Escriba, o mande un audio</h3><p>Cuéntenos de su conjunto: cuántas unidades, qué se le está volviendo un problema — la asamblea, la cartera, las PQRS.</p></div>
    <div class="card reveal" style="--d:.06s"><div class="step-n">02</div><h3>Una conversación corta</h3><p>Cómo trabaja hoy, quién lo usaría (usted, el consejo, la portería, los residentes) y qué no puede fallar. Sin claves ni cuentas de nada.</p></div>
    <div class="card reveal" style="--d:.12s"><div class="step-n">03</div><h3>La demostración — gratis</h3><p>En una reunión corta lo ve andando con los datos de un conjunto de ejemplo y pide cambios.</p></div>
    <div class="card reveal" style="--d:.18s"><div class="step-n">04</div><h3>Solo entonces, el precio</h3><p>Cerrado y por escrito. Si sigue, el sistema queda en internet, con sus claves y sus datos, y nosotros pasamos su Excel de cartera al arrancar.</p></div>
  </div>
  <div class="meaning reveal" style="max-width:46rem;margin-top:1.4rem"><b>Si la demostración no le sirve, no pasó nada:</b> no paga, no queda amarrado, no insistimos.</div>
</div></section>

<section class="section s-ink closing grain"><div class="container-x">
  <div class="reveal">
    <p class="eyebrow">Empiece hoy</p>
    <h2 class="t-5xl">Cuéntenos qué se le volvió un problema en su conjunto</h2>
    <p class="lead" style="margin-top:1rem">Con eso alcanza: le preguntamos lo demás y agendamos su demostración gratis.</p>
    <div class="cta-row">$CTA_END
      <p class="cta-trust">Le responde Miguel Acosta directamente · Pereira y Dosquebradas, Colombia · <a href="$M_TEL">+57 311 517 5472</a></p></div>
  </div>
</div></section>

{FOOT_C}

<div class="mobile-cta">$CTA_BAR</div>
{SCRIPTS}
</body>
</html>
'''
html=string.Template(conj).substitute(c)
old=open(''+OUT+'conjuntos.html',encoding='utf-8').read()
assert set(re.findall(r'https://wa\.me/[^"]+',old))==set(re.findall(r'https://wa\.me/[^"]+',html)),'conjuntos wa set changed'
open(OUT+'conjuntos.html','w',encoding='utf-8').write(html); print('conjuntos ok',len(html))

# ============================================================ caso.html
k=dict(M_CASO=wa('Hola, vi el caso VecinGo y quiero una demostración gratis para mi conjunto o mi negocio. (appximo.com · caso)'))
k['CTA_CASO']=cta(k['M_CASO'])
caso=f'''<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>El caso VecinGo — una plataforma de 18 módulos, en español y con pruebas</title>
<meta name="description" content="Una plataforma completa para un conjunto residencial — asambleas con quórum, cartera, parqueaderos, PQRS — construida con la tecnología de Appximo. El caso, en español y con pantallas reales.">
<meta property="og:title" content="El caso VecinGo — 18 módulos para un conjunto real">
<meta property="og:description" content="Asambleas con quórum en tiempo real, cartera, parqueaderos, PQRS. Construida con la tecnología de Appximo. Véala por dentro.">
<meta property="og:image" content="https://appximo.com/assets/og.jpg">
<meta property="og:type" content="article">
<meta property="og:url" content="https://appximo.com/caso.html">
<link rel="canonical" href="https://appximo.com/caso.html">
<meta name="robots" content="index,follow,max-image-preview:large">
{HEAD}
{PAGE_CSS}
<style>
  .shots{{display:grid;gap:1.2rem;margin-top:1.6rem}}
  @media(min-width:760px){{.shots{{grid-template-columns:1fr 1fr}}}}
  .shot figcaption{{padding:.8rem 1.05rem;font-size:.9rem;color:var(--text-2);border-top:1px solid var(--zinc-200)}}
  .shot figcaption b{{color:var(--text)}}
</style>
</head>
<body>
{nav('$M_CASO',back='← Volver a la página principal')}

<header class="hero grain">
  {hero_grid([('tablero-hero.webp',1080,483),('caso-asamblea.webp',1080,245),('caso-plano.webp',1080,498),('caso-muro.webp',1080,498)])}
  <div class="container-x">
    <div class="hero-copy">
      <p class="eyebrow">El caso, en español y con pruebas</p>
      <h1 class="t-5xl" style="max-width:20ch">Una plataforma de 18 módulos para un conjunto real, <em>construida en una tarde</em>.</h1>
      <p class="sub">Se llama VecinGo: la administración completa de un conjunto residencial, construida con nuestra tecnología. Su construcción está <strong>documentada paso a paso</strong> en un informe público. Estas son sus pantallas, tal cual.</p>
    </div>
    <div class="stats">
      <div class="stat"><b>18</b><span>módulos: asambleas, cartera, PQRS, parqueaderos, reservas, obras…</span></div>
      <div class="stat"><b>3½<span class="u">h</span></b><span>de construcción, documentadas paso a paso en el informe del caso</span></div>
      <div class="stat ring-row" style="align-items:center">{ring(58.2,'quórum','6rem','dark')}<span style="margin-top:0">de quórum por coeficiente, calculado en tiempo real en una asamblea</span></div>
    </div>
  </div>
</header>

<section class="section s-white"><div class="container-x">
  <p class="eyebrow reveal">Por dentro, pantalla por pantalla</p>
  <h2 class="t-4xl reveal">Lo que la administración ve todos los días</h2>
  <div class="shots">
    <figure class="bframe paper shot reveal media-skel">{bbar('vecingo — modo demostración')}<img src="assets/tablero-hero.webp" alt="Tablero del conjunto: PQRS abiertas, unidades en mora con su valor, obras, reservas, visitantes y la asamblea en curso" width="1080" height="483" loading="lazy"><figcaption><b>El tablero.</b> Todo el estado del conjunto en una pantalla: PQRS abiertas, cartera en mora con su valor, obras, reservas, visitantes — y la asamblea en curso con su quórum.</figcaption></figure>
    <figure class="bframe paper shot reveal media-skel">{bbar('vecingo — modo demostración')}<img src="assets/caso-asamblea.webp" alt="Asambleas y votaciones: quórum por coeficiente y voto ponderado en tiempo real, 58,2 % presente, con quórum" width="1080" height="245" loading="lazy"><figcaption><b>Asambleas y votaciones.</b> Quórum por coeficiente y voto ponderado, calculados en tiempo real. Se acabó contar papelitos a medianoche.</figcaption></figure>
    <figure class="bframe paper shot reveal media-skel">{bbar('vecingo — modo demostración')}<img src="assets/caso-plano.webp" alt="Plano de parqueaderos dibujado en el sistema: 106 cupos, 144 vehículos registrados, zonas pintadas" width="1080" height="498" loading="lazy"><figcaption><b>El plano de parqueaderos.</b> Los cupos se dibujan sobre el plano del conjunto: 106 cupos, 144 vehículos registrados, visitantes vigentes y zonas prohibidas.</figcaption></figure>
    <figure class="bframe paper shot reveal media-skel">{bbar('vecingo — modo demostración')}<img src="assets/caso-muro.webp" alt="Muro del conjunto: publicaciones de los residentes con etiquetas de agradecimiento y convivencia" width="1080" height="498" loading="lazy"><figcaption><b>El muro del conjunto.</b> Lo que los vecinos publican, con moderación y registro de quién leyó cada comunicado.</figcaption></figure>
  </div>
  <p class="lead reveal" style="margin-top:1.2rem">Las pantallas son del <strong>modo demostración</strong> de la plataforma: los datos son ficticios a propósito — la comunidad real no se expone.</p>
</div></section>

<section class="section s-ink"><div class="container-x">
  <p class="eyebrow reveal">El recorrido completo</p>
  <h2 class="t-4xl reveal">Véala funcionando, 5 minutos</h2>
  <figure class="media reveal" style="margin-top:1.4rem;max-width:52rem"><div class="vframe"><video id="casovid" controls muted playsinline preload="none" poster="assets/poster-vecingo.webp" width="1280" height="720" aria-label="Video: recorrido de 5 minutos por la plataforma VecinGo en modo demostración"><source src="assets/vecingo-caso.mp4" type="video/mp4"></video><button class="vplay" aria-label="Reproducir el recorrido"><span class="vplay-btn">{PLAY}Ver el recorrido · 5 min</span></button></div><figcaption>El recorrido lo grabó el autor de la plataforma, con sus propios rótulos.</figcaption></figure>
  <div class="card-dark card-pad reveal" style="max-width:40rem;margin-top:1.6rem">
    <p style="font-weight:600;font-size:1.08rem;line-height:1.4">El informe técnico completo — qué se construyó, cuánto tardó cada parte y qué falló — está publicado.</p>
    <p class="t-sm" style="margin-top:.7rem;color:var(--ink-text-dim)"><a href="https://github.com/appximo/appximo/blob/main/docs/CASE_STUDY_VECINGO.md" rel="noopener">Léalo aquí</a> (en inglés). ¿Administra un conjunto? <a href="conjuntos.html">Esta es su página</a>.</p>
  </div>
</div></section>

<section class="section s-ink closing grain" style="border-top:1px solid var(--ink-line)"><div class="container-x">
  <div class="reveal">
    <h2 class="t-5xl">¿Su conjunto — o su negocio — necesita algo así?</h2>
    <p class="lead" style="margin-top:1rem">Cuéntenos qué se le está volviendo un problema. La demostración es gratis, y el precio se cierra por escrito antes de empezar.</p>
    <div class="cta-row">$CTA_CASO</div>
  </div>
</div></section>

{FOOT_K}
{SCRIPTS}
</body>
</html>
'''
html=string.Template(caso).substitute(k)
old=open(''+OUT+'caso.html',encoding='utf-8').read()
assert set(re.findall(r'https://wa\.me/[^"]+',old))==set(re.findall(r'https://wa\.me/[^"]+',html)),'caso wa set changed'
open(OUT+'caso.html','w',encoding='utf-8').write(html); print('caso ok',len(html))
