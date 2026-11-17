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

# ---------- liens : du site statique vers les adresses Shopify ----------
LINKS = {
    "a-propos/": "/pages/a-propos", "contact/": "/pages/contact", "livraison-retours/": "/pages/livraison-retours",
    "impressum/": "/policies/legal-notice", "cgv/": "/policies/terms-of-service", "protection-des-donnees/": "/policies/privacy-policy",
    "#faq": "/#faq", "#produits": "/#produits", "#pourquoi": "/#pourquoi", "": "/",
}
def shop_links(html):
    def one(m):
        h = m.group(1)
        key = h[3:] if h.startswith("../") else h
        if h.startswith("../") and key in LINKS:
            return 'href="{{ routes.root_url | append: \'' + LINKS[key] + '\' | replace: \'//\', \'/\' }}"'
        return m.group(0)
    return re.sub(r'href="([^"{]*)"', one, html)

# ---------- pages simples (À propos, Contact, Livraison et retours) ----------
def build_page(folder, label):
    src = (ROOT / folder / "index.html").read_text(encoding="utf-8")
    css = scope_css((ROOT / "assets/pages.css").read_text(encoding="utf-8"), ".bz", ["fonts/"])
    html = re.search(r'<main id="top">(.*?)</main>', src, re.S).group(1)
    html = shop_links(html)
    must('href="../' not in html, "lien local restant dans " + folder)
    html = html.replace("hello@bolzo.example", "{{ section.settings.contact_email | default: shop.email }}")
    fonts = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', src).group(0)
    js = ""
    if 'id="copy-mail"' in html:
        js = """
<script>
(function(){
  var copy = document.getElementById("copy-mail");
  if (!copy) return;
  copy.addEventListener("click", function(){
    var done = function(){ var c = document.getElementById("copied"); c.hidden = false; setTimeout(function(){ c.hidden = true; }, 3000); };
    var text = document.getElementById("mail").textContent;
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function(){});
  });
})();
</script>"""
    schema = """{% schema %}
{
  "name": "Bolzo @@L@@",
  "tag": "section",
  "class": "bz-section",
  "enabled_on": { "templates": ["page"] },
  "settings": [
    { "type": "text", "id": "contact_email", "label": "Adresse e-mail de contact", "info": "Vide = adresse de la boutique." }
  ],
  "presets": [{ "name": "Bolzo @@L@@" }]
}
{% endschema %}""".replace("@@L@@", label)
    section = f"""{{%- comment -%}}
  Page « {label} », générée depuis {folder}/index.html par shopify/outils/construire.py.
{{%- endcomment -%}}
{fonts}
<style>
{css}
</style>

<div class="bz{{% if request.locale.iso_code == 'fr' %}} fr{{% endif %}}">
{html}
</div>
{js}

{schema}
"""
    template = '{\n  "sections": {\n    "main": { "type": "bolzo-%s", "settings": { "contact_email": "" } }\n  },\n  "order": ["main"]\n}\n' % folder
    return section, template

# ---------- politiques : texte propre, une langue par fichier ----------
from html.parser import HTMLParser
class OneLang(HTMLParser):
    VOID = {"br", "img", "hr"}
    def __init__(self, keep):
        super().__init__(convert_charrefs=False); self.keep = keep; self.out = []; self.stack = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); lang = a.get("lang")
        if tag in self.VOID:
            if not self.skip: self.out.append("<%s>" % tag)
            return
        if self.skip or (lang and lang != self.keep):
            self.skip += 1; self.stack.append("skip"); return
        if tag in ("span", "mark", "div", "svg", "path", "circle") :
            if tag == "mark": self.out.append("["); self.stack.append("mark"); return
            self.stack.append("drop"); return
        keep_attrs = ' href="%s"' % a["href"] if tag == "a" and "href" in a else ""
        self.out.append("<%s%s>" % (tag, keep_attrs)); self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.VOID or not self.stack: return
        t = self.stack.pop()
        if t == "skip": self.skip -= 1
        elif t == "mark": self.out.append("]")
        elif t != "drop": self.out.append("</%s>" % t)
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
    def handle_entityref(self, n):
        if not self.skip: self.out.append("&%s;" % n)
    def handle_charref(self, n):
        if not self.skip: self.out.append("&#%s;" % n)

POLICY_LINKS = {"../livraison-retours/": "/pages/livraison-retours", "../protection-des-donnees/": "/policies/privacy-policy", "../cgv/": "/policies/terms-of-service", "../impressum/": "/policies/legal-notice", "../contact/": "/pages/contact"}
def build_policy(folder, lang):
    src = (ROOT / folder / "index.html").read_text(encoding="utf-8")
    body = re.search(r'<div class="wrap legal">(.*?)</div>\s*</section>', src, re.S).group(1)
    body = re.sub(r'<p class="draft">.*?</p>', "", body, flags=re.S)
    body = re.sub(r'<nav class="toc".*?</nav>', "", body, flags=re.S)
    for a, b in POLICY_LINKS.items(): body = body.replace('href="%s"' % a, 'href="%s"' % b)
    p = OneLang(lang); p.feed(body); p.close()
    text = "".join(p.out)
    text = re.sub(r"<dl>(.*?)</dl>", lambda m: "<table>" + re.sub(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", r"<tr><th>\1</th><td>\2</td></tr>", m.group(1), flags=re.S) + "</table>", text, flags=re.S)
    text = re.sub(r"[ \t]+\n", "\n", text); text = re.sub(r"\n\s*\n+", "\n", text).strip()
    return text + "\n"

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

# Produits d'exemple : pas de page dans Shopify, donc cartes non cliquables, coupées par défaut
minis = re.findall(r'<a class="mini" href="[^"]*">.*?</a>', html, re.S)
must(len(minis) >= 1, "cartes des produits d'exemple introuvables")
for m in minis:
    d = re.sub(r'^<a class="mini" href="[^"]*">', '<div class="mini">', m)
    d = re.sub(r'</a>$', '</div>', d)
    d = re.sub(r'\s*<span class="link">.*?</svg></span>', '', d, flags=re.S)
    html = html.replace(m, "{% if section.settings.show_examples %}" + d + "{% endif %}")
note = re.search(r'<p class="grid-note">.*?</p>', html, re.S)
must(note is not None, "note des produits d'exemple introuvable")
html = html.replace(note.group(0), "{% if section.settings.show_examples %}" + note.group(0) + "{% endif %}")
html = shop_links(html)

js = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
js = js.replace('var root = document.documentElement;', 'var root = document.getElementById("bz");\n  if (!root) return;')
js = re.sub(r'  var KEY = "bolzo-lang";\n', "", js)
js = re.sub(r'  var lang = "(?:fr|de)";\n  try \{[^\n]*\n', '  var lang = root.classList.contains("fr") ? "fr" : "de";\n', js)
js = re.sub(r'    root\.lang = [^\n]*\n', "", js)
js = re.sub(r'    var tm = [^\n]*\n', "", js)
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
    { "type": "text", "id": "contact_email", "label": "Adresse e-mail de contact", "info": "Vide = adresse de la boutique." },
    { "type": "checkbox", "id": "show_examples", "label": "Afficher les produits d'exemple", "default": false, "info": "Produits fictifs, pour une démo uniquement. À laisser décoché sur une vraie boutique." }
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
for d in ("sections", "templates", "assets", "fichiers", "politiques"):
    p = OUT / d
    if p.exists(): shutil.rmtree(p)
    p.mkdir(parents=True)
(OUT / "sections/bolzo-accueil.liquid").write_text(home, encoding="utf-8")
shutil.copy(ROOT / "klarsicht/shopify/sections/klarsicht-produit.liquid", OUT / "sections/")
shutil.copy(ROOT / "klarsicht/shopify/templates/product.klarsicht.json", OUT / "templates/")
(OUT / "templates/index.json").write_text(
    '{\n  "sections": {\n    "bolzo": {\n      "type": "bolzo-accueil",\n      "settings": { "product": "klarsicht", "contact_email": "", "show_examples": false }\n    }\n  },\n  "order": ["bolzo"]\n}\n',
    encoding="utf-8")
PAGES = [("a-propos", "À propos"), ("contact", "contact"), ("livraison-retours", "livraison")]
for folder, label in PAGES:
    section, template = build_page(folder, label)
    (OUT / f"sections/bolzo-{folder}.liquid").write_text(section, encoding="utf-8")
    (OUT / f"templates/page.{folder}.json").write_text(template, encoding="utf-8")
for folder in ("impressum", "cgv", "protection-des-donnees"):
    for lang in ("de", "fr"):
        (OUT / f"politiques/{folder}-{lang}.html").write_text(build_policy(folder, lang), encoding="utf-8")
for f in ["assets/fonts/Overshoot-GentleBreeze.woff2", "klarsicht/fonts/Malabard-ExtraBold.woff2", "klarsicht/fonts/ISOCIRCLE-050.woff2"]:
    shutil.copy(ROOT / f, OUT / "assets/")
klar = (OUT / "sections/klarsicht-produit.liquid").read_text(encoding="utf-8")
needed = sorted(set(re.findall(r"'([^']+\.(?:jpg|png))' \| file_url", klar + home)))
for n in needed:
    shutil.copy(ROOT / "klarsicht/img" / n, OUT / "fichiers/")
shutil.copy(ROOT / "klarsicht/video/demo.mp4", OUT / "fichiers/")
for n in ["logo-bolzo-rouge.png", "logo-bolzo-blanc.png", "favicon-180.png"]:
    shutil.copy(ROOT / "marque" / n, OUT / "fichiers/")
print("Construit : shopify/ —", len(needed), "images, 1 vidéo, logos, 3 polices,", len(list((OUT / "sections").iterdir())), "sections,", len(list((OUT / "templates").iterdir())), "modèles, 6 textes de politiques")
