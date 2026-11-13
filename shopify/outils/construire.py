"""Construit le dossier shopify/ : les deux pages (accueil Bolzo + KLARSICHT)
prêtes à ajouter à un thème Shopify.

Usage, depuis n'importe où :  python3 shopify/outils/construire.py
Relancer après chaque modification de index.html ou de klarsicht/index.html.
"""
import re, shutil, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "shopify"

def must(cond, msg):
    if not cond:
        sys.exit("Construction impossible : " + msg)

# ---------- outil commun : limite le CSS à un bloc ----------
def scope_css(css, prefix, font_dir_map):
    def scope_selector(sel):
        sel = sel.strip()
        if sel in ("html", "body::before"):
            return None
        if sel in (":root", "body"):
            return prefix
        if sel.startswith(":root"):
            return prefix + sel[len(":root"):]
        return prefix + " " + sel
    def walk(block):
        res, i = [], 0
        while i < len(block):
            j = block.find("{", i)
            if j < 0:
                res.append(block[i:]); break
            head = block[i:j]; depth, k = 1, j + 1
            while depth:
                depth += {"{": 1, "}": -1}.get(block[k], 0); k += 1
            body = block[j + 1:k - 1]
            h = re.sub(r"/\*.*?\*/", "", head, flags=re.S).strip()
            if h.startswith("@media"):
                res.append(h + "{" + walk(body) + "}")
            elif h.startswith("@font-face"):
                for d in font_dir_map:
                    body = re.sub(r"url\(" + re.escape(d) + r"([^)]+)\)", r"url({{ '\1' | asset_url }})", body)
                res.append(h + "{" + body + "}")
            elif h:
                sels = [s for s in (scope_selector(x) for x in h.split(",")) if s]
                if sels:
                    res.append(",".join(sels) + "{" + body + "}")
            i = k
        return "\n".join(res)
    reset = (prefix + " h1," + prefix + " h2," + prefix + " h3," + prefix + " p," + prefix + " a," + prefix + " button,"
             + prefix + " img," + prefix + " ul," + prefix + " li," + prefix + " figure," + prefix + " details," + prefix + " summary"
             "{color:inherit;text-transform:none;letter-spacing:normal;font-family:inherit;font-size:inherit;font-weight:inherit;"
             "line-height:inherit;margin:0;border:0;background:none;box-shadow:none;text-decoration:none}\n")
    return reset + walk(css)

# ---------- 1. KLARSICHT : on réutilise son convertisseur ----------
subprocess.run([sys.executable, str(ROOT / "klarsicht/shopify/outils/convertir.py")], check=True)

# ---------- 2. Accueil Bolzo ----------
src = (ROOT / "index.html").read_text(encoding="utf-8")
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
css = scope_css(css, ".bz", ["assets/fonts/"])
main = re.search(r'<main id="top">(.*?)</main>', src, re.S).group(1)
html = main
html = html.replace('src="assets/img/klarsicht-face.jpg"', """src="{{ 'face.jpg' | file_url }}" """.rstrip())
html = html.replace('src="assets/img/klarsicht.jpg"', """src="{{ 'duo.jpg' | file_url }}" """.rstrip())
must("assets/img" not in html, "image locale restante dans l'accueil")
must('href="klarsicht/"' in html, "lien vers KLARSICHT introuvable")
html = html.replace('href="klarsicht/"', """href="{{ section.settings.product.url | default: '/products/klarsicht' }}" """.rstrip())
html = html.replace("<strong>CHF 29.90</strong>", "<strong>{% if section.settings.product %}{{ section.settings.product.price_min | money }}{% else %}CHF 29.90{% endif %}</strong>")
html = html.replace("hello@bolzo.example", "{{ section.settings.contact_email | default: shop.email }}")
must("bolzo.example" not in html, "adresse provisoire restante")

js = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
js = js.replace('var root = document.documentElement;', 'var root = document.getElementById("bz");\n  if (!root) return;')
js = re.sub(r'  var KEY = "bolzo-lang";\n', "", js)
js = re.sub(r'  var lang = "(?:fr|de)";\n  try \{[^\n]*\n', '  var lang = root.classList.contains("fr") ? "fr" : "de";\n', js)
js = re.sub(r'    root\.lang = [^\n]*\n', "", js)
js = re.sub(r'    document\.querySelectorAll\("\[data-set-lang\]"\)\.forEach\(function\(b\)\{\n      b\.setAttribute\("aria-pressed"[^\n]*\n    \}\);\n', "", js)
js = re.sub(r'  document\.querySelectorAll\("\[data-set-lang\]"\)\.forEach\(function\(b\)\{.*?\n  \}\);\n', "", js, flags=re.S)
must("KEY" not in js and "data-set-lang" not in js, "JavaScript de l'accueil mal converti")

fonts_link = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', src).group(0)
schema = """{% schema %}
{
  "name": "Bolzo accueil",
  "tag": "section",
  "class": "bz-section",
  "enabled_on": { "templates": ["index"] },
  "settings": [
    { "type": "product", "id": "product", "label": "Produit KLARSICHT", "info": "Sert au lien et au prix « dès » de la carte produit." },
    { "type": "text", "id": "contact_email", "label": "Adresse e-mail de contact", "info": "Vide = adresse de la boutique." }
  ],
  "presets": [{ "name": "Bolzo accueil" }]
}
{% endschema %}"""
home = f"""{{%- comment -%}}
  Page d'accueil Bolzo.ch, générée depuis index.html par shopify/outils/construire.py.
  L'en-tête, le bandeau et le pied de page sont ceux du thème.
{{%- endcomment -%}}
{fonts_link}
<style>
{css}
</style>

<div class="bz{{% if request.locale.iso_code == 'fr' %}} fr{{% endif %}}" id="bz">
{html}
</div>

<script>{js}</script>

{schema}
"""

# ---------- 3. Le dossier shopify/ ----------
for d in ("sections", "templates", "assets", "fichiers"):
    p = OUT / d
    if p.exists(): shutil.rmtree(p)
    p.mkdir(parents=True)
(OUT / "sections/bolzo-accueil.liquid").write_text(home, encoding="utf-8")
shutil.copy(ROOT / "klarsicht/shopify/sections/klarsicht-produit.liquid", OUT / "sections/")
shutil.copy(ROOT / "klarsicht/shopify/templates/product.klarsicht.json", OUT / "templates/")
(OUT / "templates/index.json").write_text(
    '{\n  "sections": {\n    "bolzo": {\n      "type": "bolzo-accueil",\n      "settings": { "product": "klarsicht", "contact_email": "" }\n    }\n  },\n  "order": ["bolzo"]\n}\n',
    encoding="utf-8")
for f in ["assets/fonts/Overshoot-GentleBreeze.woff2", "klarsicht/fonts/Malabard-ExtraBold.woff2", "klarsicht/fonts/ISOCIRCLE-050.woff2"]:
    shutil.copy(ROOT / f, OUT / "assets/")
klar = (OUT / "sections/klarsicht-produit.liquid").read_text(encoding="utf-8")
needed = sorted(set(re.findall(r"'([^']+\.(?:jpg|png))' \| file_url", klar + home)))
for n in needed:
    shutil.copy(ROOT / "klarsicht/img" / n, OUT / "fichiers/")
shutil.copy(ROOT / "klarsicht/video/demo.mp4", OUT / "fichiers/")
for n in ["logo-bolzo-rouge.png", "logo-bolzo-blanc.png", "favicon-180.png"]:
    shutil.copy(ROOT / "marque" / n, OUT / "fichiers/")
print("Construit : shopify/ —", len(needed), "images, 1 vidéo, 2 logos, 3 polices, 2 sections, 2 modèles")
