# Landing comercial de Appximo — `appximo.com`

Sitio **estático puro** (un `index.html` + `assets/`), sin build, sin dependencias.
Se publica con **GitHub Pages** sirviendo desde la **raíz** del repo (rama `main`).

> **Por qué este repo está separado del framework:** la landing habla a dueños de
> negocio en lenguaje comercial. El repo open source habla a desarrolladores. Si un
> desarrollador ve copy comercial dentro del proyecto técnico, desconfía — por eso
> los dos frentes no se mezclan. La página técnica sigue en
> `appximo.github.io/appximo` y no se toca desde acá.

## Estructura

```
CNAME          → appximo.com  (lo lee GitHub Pages; no borrar)
index.html     → toda la landing (una sola página)
assets/        → capturas reales, video demo, favicon
README.md      → este archivo
```

Se sirve desde la raíz (no `/docs`) porque el repo solo contiene el sitio — no hay
nada más de qué separarlo, y la raíz es la configuración con menos pasos.

## El número de WhatsApp

**Ya está puesto el número real** (desde 2026-08-17). Esta sección queda como
referencia del mecanismo por si algún día hay que cambiarlo:

```bash
# Reemplazar {{WHATSAPP_NUMBER}} por el número real, con indicativo de país,
# solo dígitos (ejemplo Colombia: 573001234567):
sed -i 's/{{WHATSAPP_NUMBER}}/573001234567/g' index.html

# Verificar que no quedó ninguno:
grep -c '{{WHATSAPP_NUMBER}}' index.html   # debe imprimir 0 (grep sale con 1)
```

El mensaje pre-escrito que llega al chat es:
**«Hola, vengo de la página de Appximo. Quiero una demostración para mi negocio.»**
(está URL-encodeado dentro de cada link `wa.me`; si se quiere cambiar el texto,
cambiarlo en TODOS los links — son el mismo CTA repetido a propósito).

## Publicar (pasos exactos)

### 1. Crear el repo en GitHub y pushear

```bash
# En github.com: crear el repo appximo/landing (público, vacío, sin README)
cd /root/appximo-landing
git push -u origin main
```

### 2. Activar GitHub Pages

En `github.com/appximo/landing` → **Settings → Pages**:

- **Source:** `Deploy from a branch`
- **Branch:** `main` / carpeta `/ (root)` → **Save**
- En **Custom domain** escribir `appximo.com` → **Save**
  (GitHub lo valida contra el archivo `CNAME` del repo; puede tardar unos minutos
  mientras emite el certificado)
- Cuando el certificado esté listo, marcar **Enforce HTTPS**

### 3. DNS en Cloudflare

En el dashboard de Cloudflare, zona `appximo.com` → **DNS → Records**.

**Registros A del apex** (IPs oficiales de GitHub Pages, verificadas en
[docs.github.com — Managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
el 2026-08-17):

| Tipo | Nombre | Contenido | Proxy |
|---|---|---|---|
| A | `@` | `185.199.108.153` | **DNS only** (nube gris) |
| A | `@` | `185.199.109.153` | **DNS only** |
| A | `@` | `185.199.110.153` | **DNS only** |
| A | `@` | `185.199.111.153` | **DNS only** |
| CNAME | `www` | `appximo.github.io` | **DNS only** |

Opcional (IPv6, mismas fuentes): cuatro registros AAAA `2606:50c0:8000::153`,
`2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.

**⚠ El modo SSL — esto es lo que evita el bucle de redirección:**

- **Recomendado: dejar los registros en "DNS only" (nube gris).** GitHub emite el
  certificado de `appximo.com` y sirve HTTPS directo. Cero configuración extra.
- Si más adelante se quiere el proxy naranja de Cloudflare: **SSL/TLS → Overview →
  modo `Full (strict)`**. Con el modo `Flexible` + "Enforce HTTPS" de GitHub se
  produce el clásico **bucle infinito de redirecciones** (Cloudflare pide HTTP al
  origen, GitHub redirige a HTTPS, y así). `Full (strict)` funciona porque GitHub
  ya tiene certificado propio para el dominio.
- Importante: mientras GitHub está **emitiendo** el certificado (primeros minutos),
  el proxy naranja impide la validación. Si el certificado no sale: poner los
  registros en DNS only, esperar a que Pages muestre el certificado activo, y
  recién ahí decidir si se activa el proxy.

**⚠ Los subdominios existentes no se tocan:** `tiendita.appximo.com`,
`petfriendly.appximo.com`, `crisblogs.appximo.com` (apuntan al VPS de producción)
siguen igual — esto solo agrega el apex `@` y `www`.

### 4. Verificar

```bash
dig appximo.com +short          # → las 4 IPs 185.199.108-111.153
curl -sI https://appximo.com | head -3    # → HTTP/2 200
```

## Actualizar la página

Editar `index.html` (o `assets/`), commit, push a `main`. Pages redepliega solo
(1–2 minutos). No hay build: lo que está en el repo es lo que se sirve.

## De dónde sale el material visual

Todo es real — nada de stock, nada de mockups:

- `assets/votaciones.webp`, `assets/casos.webp` — capturas de una app real de
  administración de conjuntos (votaciones con % y quórum, casos PQRS) generada
  con el motor el 2026-08-18 en el servidor de desarrollo, con datos de ejemplo
  legibles sembrados por la API. La instancia y su base se borraron al cierre.
- `assets/pedidos.webp`, `assets/citas.webp`, `assets/demo-clip.mp4`,
  `assets/poster.webp` — la app demo de pedidos/citas (repostería) de la sesión
  LANDING-COMMERCIAL-S1, mismo método. El clip lleva subtítulos en español
  quemados (ffmpeg + libass).
- `assets/tienda.webp` — captura de `tiendita.appximo.com`, tienda demo REAL en
  producción (dominio y certificado propios).
- `assets/og.jpg` — recorte de la captura de votaciones para el preview social.

Los detalles de cómo se generaron: repo interno, sesiones LANDING-COMMERCIAL-S1
y LANDING-REDESIGN-S1.
