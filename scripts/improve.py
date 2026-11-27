#!/usr/bin/env python3
"""Raahee Parna SEO / structure upgrade (idempotent; run from the repo root).

    python3 scripts/improve.py

* adds 5 project pages (price list, floor plans, RERA details, amenities, overview)
  under /blog/raahee-parna/ plus a category page, an HTML site map and sitemap.xml entries
* adds a Guides section with image cards + quick links on the home page
* puts the brand in the home H1 (logo alt) and links the site map from every footer
* self-hosts Roboto (removes the render-blocking Google Fonts request)
* adds -800 image variants and srcset/sizes
* adds ?v= cache-busting to local CSS / JS links
"""
import re, os, glob, json, html, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
URL = "https://raaheeparna.com"
DATE = "2026-11-26"
VER = "20261127b"
RERA = "PR1260002602355"
RERA_LINK = "https://maharerait.maharashtra.gov.in/project/view/67633"
CAT = "raahee-parna"
TPL = "blog/buying-a-home-in-moshi-pune-with-raahee-parna/index.html"
FONT_SRC = os.environ.get("FONT_DIR", "/tmp/rf")


def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    open(p, "w", encoding="utf-8").write(t)
def esc(s): return html.escape(s, quote=True)
def slugify(t): return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", t)).lower()).strip("-")
def mins(b): return max(2, round(len(re.sub(r"<[^>]+>", " ", b).split()) / 200))
def cap(s): return s[:1].upper() + s[1:]

# --------------------------------------------------------------------------- content
IMGS = {  # key -> (file base, alt)
    "aerial": ("aerial-1", "Aerial view of the Raahee Parna towers in Dudulgaon near Moshi, Pune"),
    "pool": ("pool", "Club Parna swimming pool and clubhouse at Raahee Parna, Dudulgaon"),
    "river": ("hero-river", "Raahee Parna towers by the Indrayani River in Dudulgaon, near Moshi, Pune"),
    "living": ("living-room", "Sample living room of a 2, 2.5 and 3 BHK flat at Raahee Parna, Pune"),
}

P = {}
P["raahee-parna-price-list"] = dict(
    img="river", tag="Price list",
    t="Raahee Parna Price List: 2, 2.5 & 3 BHK Dudulgaon",
    h="Raahee Parna price list: 2, 2.5 and 3 BHK in Dudulgaon, Moshi",
    d="Raahee Parna price list, Dudulgaon: 2 BHK from ₹58.53 L, 2.5 BHK from ₹68.14 L and 3 BHK from ₹79.06 L, with carpet area for every unit type.",
    dek="Total package prices for 2, 2.5 and 3 BHK homes at Raahee Parna, with carpet area for each unit.",
    body='''<p>Raahee Parna by Raahee Corp is a 3.5 acre project in Dudulgaon, near Moshi in PCMC, Pune, with 686 homes in 7 towers of 14 floors. This page lists the price of each unit type in the current price list so you can compare options before you visit.</p>
<h2>Raahee Parna price list at a glance</h2>
<div class="tw"><table class="compare"><thead><tr><th>Home type</th><th>Carpet area</th><th>Starting total package</th></tr></thead><tbody>
<tr><td>2 BHK</td><td>685 – 707 sq ft</td><td>₹58.53 lakh onwards</td></tr>
<tr><td>2.5 BHK</td><td>832 – 894 sq ft</td><td>₹68.14 lakh onwards</td></tr>
<tr><td>3 BHK</td><td>966 – 1,008 sq ft</td><td>₹79.06 lakh onwards</td></tr></tbody></table></div>
<h2>Unit-wise price list</h2>
<p>Each total package covers the agreement cost, stamp duty, registration and GST.</p>
<div class="tw"><table class="compare"><thead><tr><th>Carpet area (sq ft)</th><th>Type</th><th>Total package</th></tr></thead><tbody>
<tr><td>685</td><td>2 BHK</td><td>₹58.53 lakh</td></tr><tr><td>691</td><td>2 BHK</td><td>₹59.04 lakh</td></tr><tr><td>707</td><td>2 BHK</td><td>₹60.40 lakh</td></tr>
<tr><td>832</td><td>2.5 BHK</td><td>₹68.14 lakh</td></tr><tr><td>894</td><td>2.5 BHK</td><td>₹73.19 lakh</td></tr>
<tr><td>966</td><td>3 BHK</td><td>₹79.06 lakh</td></tr><tr><td>1,008</td><td>3 BHK</td><td>₹82.49 lakh</td></tr></tbody></table></div>
<p>Rates are indicative and may change without prior notice. Final pricing, inventory and taxes are as per the agreement.</p>
<h2>How to use this price list</h2>
<ul><li>Choose the carpet area that fits your family first, then check the budget. See the <a href="../raahee-parna-floor-plans/">Raahee Parna floor plans</a> for layouts.</li><li>Ask whether maintenance, parking and club charges are included or extra.</li><li>Check the registration on the <a href="../raahee-parna-rera-details/">RERA details page</a> before you pay a booking amount.</li></ul>
<p>For the latest availability and a written price list, <a href="../../../#contact">leave your details</a> and the team will call you.</p>''')

P["raahee-parna-floor-plans"] = dict(
    img="aerial", tag="Floor plans",
    t="Raahee Parna Floor Plans & Carpet Areas | Dudulgaon",
    h="Raahee Parna floor plans and carpet areas: B, C and D wings",
    d="Raahee Parna floor plans, Dudulgaon: typical plans for B, C and D wings. 2 BHK 685–707, 2.5 BHK 832–894 and 3 BHK 966–1,008 sq ft carpet.",
    dek="Typical floor plans for the B, C and D wings, with carpet areas for each home type.",
    body='''<p>Raahee Parna has 686 homes in seven towers across the B, C and D wings. Here are the typical floor plans, the carpet areas and what to look for before you choose.</p>
<h2>Carpet area by home type</h2>
<div class="tw"><table class="compare"><thead><tr><th>Home type</th><th>Carpet area</th></tr></thead><tbody>
<tr><td>2 BHK</td><td>685 – 707 sq ft</td></tr><tr><td>2.5 BHK</td><td>832 – 894 sq ft</td></tr><tr><td>3 BHK</td><td>966 – 1,008 sq ft</td></tr></tbody></table></div>
<p>Carpet area is the usable area inside the home, so it is the best figure for comparing projects. The 2.5 BHK adds a flexible extra room that can serve as a study, nursery or home office. See what each size costs in the <a href="../raahee-parna-price-list/">Raahee Parna price list</a>.</p>
<h2>B Wing typical floor plan (2, 2.5 and 3 BHK)</h2>
<figure><img src="../../../images/plan-b-wing.webp" alt="Raahee Parna B Wing typical floor plan, 2, 2.5 and 3 BHK" width="1362" height="943" loading="lazy" decoding="async"></figure>
<h2>C Wing typical floor plan (2, 2.5 and 3 BHK)</h2>
<figure><img src="../../../images/plan-c-wing.webp" alt="Raahee Parna C Wing typical floor plan, 2, 2.5 and 3 BHK" width="1456" height="944" loading="lazy" decoding="async"></figure>
<h2>D Wing typical floor plan</h2>
<figure><img src="../../../images/plan-d-wing.webp" alt="Raahee Parna D Wing typical floor plan" width="1459" height="871" loading="lazy" decoding="async"></figure>
<h2>What to look for in a plan</h2>
<ol><li>Is the living room wide enough for your furniture, and where does the light come from?</li><li>Are the bedrooms and bathrooms placed so doors do not clash?</li><li>Where is the kitchen, and is there room for a utility area?</li><li>How many flats share each lift lobby on the typical floor?</li></ol>
<p>Ask the team which wing and floor each carpet area is in. Plans are indicative and subject to change as per approvals. For detailed plans, <a href="../../../#contact">leave your details</a>.</p>''')

P["raahee-parna-rera-details"] = dict(
    img="pool", tag="RERA details",
    t="Raahee Parna RERA Number & Developer Details",
    h="Raahee Parna RERA number and developer details",
    d="Raahee Parna, Dudulgaon is registered with MahaRERA under PR1260002602355. Developer Raahee Corp. How to verify the registration yourself.",
    dek="The MahaRERA registration number, the developer and the location, and how to check them yourself.",
    body=f'''<p>RERA registration is one of the first things to check before buying an under-construction home. This page lists the details for Raahee Parna, Dudulgaon and shows how to verify them yourself.</p>
<h2>Raahee Parna project details</h2>
<div class="tw"><table class="compare"><thead><tr><th>Detail</th><th>Information</th></tr></thead><tbody>
<tr><td>Project</td><td>Raahee Parna, Dudulgaon, Moshi, Pune</td></tr><tr><td>Developer</td><td>Raahee Corp</td></tr>
<tr><td>MahaRERA registration</td><td>{RERA}</td></tr><tr><td>Land and towers</td><td>3.5 acres, 7 towers of 14 floors</td></tr>
<tr><td>Homes</td><td>686 homes in the B, C and D wings</td></tr><tr><td>Configurations</td><td>2, 2.5 and 3 BHK</td></tr></tbody></table></div>
<h2>How to verify the registration</h2>
<ol><li>Open the <a href="{RERA_LINK}" target="_blank" rel="noopener">Raahee Parna page on the MahaRERA website</a>, or search for the number {RERA} on <a href="https://maharera.maharashtra.gov.in/" target="_blank" rel="noopener">maharera.maharashtra.gov.in</a>.</li><li>Check the project name, the promoter, the address and the dates shown for the project.</li><li>Match the registration number with the one printed on the agreement and the brochure.</li></ol>
<h2>Why it matters</h2>
<p>A RERA-registered project has its approvals, timelines and details on public record. The registration page also shows the possession timeline declared for the project, so read it there and confirm it with the team in writing.</p>
<p>Before you pay anything, read <a href="../raahee-parna-price-list/">the price list</a> and the guide to <a href="../../buying-a-home-in-moshi-pune-with-raahee-parna/">buying a home in Moshi</a>.</p>''')

P["raahee-parna-amenities"] = dict(
    img="pool", tag="Amenities",
    t="Raahee Parna Amenities: Club Parna, Pool & 40+ More",
    h="Raahee Parna amenities: Club Parna, pool, sports and 40+ more",
    d="Raahee Parna amenities, Dudulgaon: Club Parna, swimming pool with kids and adult pools, sports courts, gym, amphitheatre, co-working space and more.",
    dek="The amenities planned at Raahee Parna, grouped into six zones across the 3.5 acre campus.",
    body='''<p>Raahee Parna offers more than 40 lifestyle amenities in six zones, all inside a single 3.5 acre campus. The list is indicative, and images shown are artistic impressions.</p>
<h2>Recreation and sports</h2>
<ul><li>Cricket turf</li><li>Squash and badminton court</li><li>Basketball court</li><li>Climbing wall</li><li>Table tennis and carrom</li><li>Rifle shooting area</li><li>Jogging track and skating rink</li></ul>
<h2>Wellness and fitness</h2>
<ul><li>AC gym and fitness area</li><li>Zumba studio</li><li>Yoga and meditation</li><li>Acupressure pathway</li><li>Open-air gymnasium</li><li>Oxygen park</li></ul>
<h2>Leisure and social</h2>
<ul><li>Clubhouse and multipurpose hall</li><li>Library and cafeteria</li><li>Amphitheatre</li><li>Party lawn</li><li>BBQ and camping fire area</li><li>Swimming pool with separate kids and adult pools</li></ul>
<h2>Nature and outdoors</h2>
<ul><li>Landscape garden</li><li>Walking pathway</li><li>Children's play area</li><li>Senior citizen sit-out</li><li>Temple</li></ul>
<h2>Work and convenience</h2>
<ul><li>Co-working space</li><li>Wi-Fi zone</li><li>Provision for salon and day care</li><li>Common car wash centre</li><li>EV charging facility</li></ul>
<h2>Security and services</h2>
<ul><li>Main gate secure entrance</li><li>CCTV in common areas</li><li>Video door phone</li><li>Power backup</li><li>Fire safety</li></ul>
<p>For a closer look at the clubhouse and pool, read <a href="../../club-parna-lifestyle-amenities-dudulgaon/">Inside Raahee Parna: Club Parna and 40+ amenities</a>. Before you book, ask which amenities will be ready at possession, and check the <a href="../raahee-parna-price-list/">price list</a> for what is included. The amenity list is subject to final sanctioned plans.</p>''')

P["raahee-parna-dudulgaon-overview"] = dict(
    img="river", tag="Project overview",
    t="Raahee Parna Dudulgaon: Project Overview & Facts",
    h="Raahee Parna Dudulgaon: project overview",
    d="Raahee Parna by Raahee Corp, Dudulgaon near Moshi, Pune: 3.5 acres, 686 homes in 7 towers, 2, 2.5 and 3 BHK, 40+ amenities. Overview and facts.",
    dek="Everything about Raahee Parna in Dudulgaon in one place: size, towers, homes, amenities and location.",
    body=f'''<p>Raahee Parna is a residential project by Raahee Corp in Dudulgaon, close to Moshi and Charholi in PCMC, Pune. It is also searched as Raahee Parna Moshi or Raahee Parna Pune, and this page brings the main facts together.</p>
<h2>Project snapshot</h2>
<div class="tw"><table class="compare"><thead><tr><th>Detail</th><th>Information</th></tr></thead><tbody>
<tr><td>Developer</td><td>Raahee Corp</td></tr><tr><td>Location</td><td>Dudulgaon, near Moshi, PCMC, Pune</td></tr>
<tr><td>Land and towers</td><td>3.5 acres, 7 towers of 14 floors</td></tr><tr><td>Homes</td><td>686 homes in the B, C and D wings</td></tr>
<tr><td>Configurations</td><td>2 BHK (685–707 sq ft), 2.5 BHK (832–894 sq ft), 3 BHK (966–1,008 sq ft) carpet</td></tr>
<tr><td>Starting price</td><td>₹58.53 lakh (total package, indicative)</td></tr><tr><td>MahaRERA</td><td>{RERA}</td></tr></tbody></table></div>
<h2>Location</h2>
<p>The project sits near the Indrayani River, with schools, hospitals, shopping and IT hubs close by. Read <a href="../../getting-around-from-raahee-parna-dudulgaon/">getting around from Raahee Parna</a> for approximate travel times, and check live routes on <a href="https://www.google.com/maps/search/?api=1&amp;query=Raahee+Parna+Dudulgaon+Pune" target="_blank" rel="noopener">Google Maps</a>.</p>
<h2>Amenities</h2>
<p>The campus has Club Parna with a swimming pool, clubhouse, gym, sports courts, an amphitheatre and a temple, among more than 40 amenities. See the <a href="../raahee-parna-amenities/">Raahee Parna amenities guide</a> for the full list.</p>
<h2>Next steps</h2>
<ul><li>Compare homes in <a href="../raahee-parna-floor-plans/">floor plans and carpet areas</a>.</li><li>Check the <a href="../raahee-parna-price-list/">price list</a>.</li><li>Verify the <a href="../raahee-parna-rera-details/">RERA details</a>.</li></ul>
<p>Information is indicative and subject to change as per approvals.</p>''')

ORDER = ["raahee-parna-dudulgaon-overview", "raahee-parna-price-list", "raahee-parna-floor-plans", "raahee-parna-rera-details", "raahee-parna-amenities"]
CATNAME = "Raahee Parna project guides"
for s in ORDER: P[s]["slug"] = s

# --------------------------------------------------------------------------- images
RESIZE = {  # base -> target width
    "aerial-1": 800, "aerial-2": 700, "entrance": 800, "living-room": 800, "pool": 800, "amphitheatre": 800,
    "clubhouse": 800, "pool-lounge": 800, "temple": 640, "plan-b-wing": 800, "plan-c-wing": 800, "plan-d-wing": 800, "location-map": 800,
}

def make_variants():
    for base, w in RESIZE.items():
        src, dst = f"images/{base}.webp", f"images/{base}-{w}.webp"
        if os.path.exists(src) and not os.path.exists(dst):
            im = Image.open(src); h = round(im.size[1] * w / im.size[0])
            im.resize((w, h), Image.LANCZOS).save(dst, "WEBP", quality=76, method=6)

def add_srcset(t, rel):
    depth = rel.count("/")
    pre = "../" * depth
    sizes = "(max-width: 800px) 100vw, 760px" if rel.startswith("blog/") and depth >= 2 else "(max-width: 700px) 92vw, (max-width: 1100px) 46vw, 560px"
    def sub(m):
        tag = m.group(0)
        if "srcset=" in tag: return tag
        ms = re.search(r'\ssrc="((?:\.\./)*)images/([a-z0-9-]+)\.webp"', tag)
        if not ms: return tag
        base = ms.group(2)
        if base not in RESIZE or not os.path.exists(f"images/{base}-{RESIZE[base]}.webp"): return tag
        w = RESIZE[base]; full = Image.open(f"images/{base}.webp").size[0]
        pre2 = ms.group(1)
        add = f' srcset="{pre2}images/{base}-{w}.webp {w}w, {pre2}images/{base}.webp {full}w" sizes="{sizes}"'
        return tag.replace(ms.group(0), ms.group(0) + add, 1)
    return re.sub(r"<img\b[^>]*>", sub, t)

# --------------------------------------------------------------------------- page building
def card_blog(s, p):
    g = P[s]; base, alt = IMGS[g["img"]]; CAT = g.get("cat", globals()["CAT"])
    v = f"{p}images/{base}-{RESIZE[base]}.webp" if base in RESIZE else f"{p}images/{base}.webp"
    return (f'<article class="post-card rv">\n<a href="{p}blog/{CAT}/{s}/" tabindex="-1" aria-hidden="true"><img src="{v}" alt="{esc(alt)}" width="800" height="533" loading="lazy" decoding="async"></a>\n<div>\n'
            f'<h2><a href="{p}blog/{CAT}/{s}/">{cap(g["h"])}</a></h2>\n<p>{g["dek"]}</p>\n<a class="more arrow" href="{p}blog/{CAT}/{s}/">Read more </a>\n</div>\n</article>\n')


def build_pages():
    for s in ORDER:
        g = P[s]; t = rd(TPL); path = f"/blog/{CAT}/{s}/"; base, alt = IMGS[g["img"]]
        body = g["body"]
        heads = re.findall(r"<h2>(.*?)</h2>", body)
        for h in heads: body = body.replace(f"<h2>{h}</h2>", f'<h2 id="{slugify(h)}">{h}</h2>', 1)
        m = mins(body)
        t = re.sub(r"<title>.*?</title>", f"<title>{esc(g['t'])}</title>", t, flags=re.S)
        for pat in [r'(<meta name="description" content=")[^"]*', r'(<meta property="og:description" content=")[^"]*', r'(<meta name="twitter:description" content=")[^"]*']:
            t = re.sub(pat, lambda x: x.group(1) + esc(g["d"]), t)
        for pat in [r'(<meta property="og:title" content=")[^"]*', r'(<meta name="twitter:title" content=")[^"]*']:
            t = re.sub(pat, lambda x: x.group(1) + esc(g["t"]), t)
        for pat in [r'(<link rel="canonical" href=")[^"]*', r'(<meta property="og:url" content=")[^"]*', r'(<link rel="alternate" hreflang="[^"]*" href=")[^"]*']:
            t = re.sub(pat, lambda x: x.group(1) + URL + path, t)
        # relative asset paths: template is depth 2, new pages are depth 3
        t = t.replace('href="../../', 'href="../../../').replace('src="../../', 'src="../../../')
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BlogPosting", "@id": URL + path + "#post", "headline": g["h"], "description": g["d"], "inLanguage": "en-IN",
             "mainEntityOfPage": {"@type": "WebPage", "@id": URL + path}, "image": [f"{URL}/images/{base}.webp"],
             "datePublished": DATE, "dateModified": DATE, "wordCount": len(re.sub(r"<[^>]+>", " ", body).split()),
             "author": {"@type": "Organization", "name": "Raahee Corp", "url": URL + "/"},
             "publisher": {"@type": "Organization", "name": "Raahee Corp", "logo": {"@type": "ImageObject", "url": URL + "/icon-512.png", "width": 512, "height": 512}},
             "about": {"@type": "ApartmentComplex", "name": "Raahee Parna", "url": URL + "/", "address": {"@type": "PostalAddress", "addressLocality": "Dudulgaon", "addressRegion": "Maharashtra", "postalCode": "412105", "addressCountry": "IN"}},
             "keywords": f"Raahee Parna, {g['tag']}, Dudulgaon, Moshi, Pune"},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": URL + q}
                for i, (n, q) in enumerate([("Raahee Parna", "/"), ("Blog", "/blog/"), (CATNAME, f"/blog/{CAT}/"), (g["h"], path)])]}]}
        t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda x: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + "\n  </script>", t, count=1, flags=re.S)
        # breadcrumb UI
        t = re.sub(r'<nav class="crumbs".*?</nav>', f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../../../">Raahee Parna</a> &rsaquo; <a href="../../">Blog</a> &rsaquo; <a href="../">{CATNAME}</a> &rsaquo; <span>{esc(cap(g["tag"]))}</span></nav>', t, count=1, flags=re.S)
        others = [o for o in ORDER if o != s][:3]
        rel = "".join(f'<li><a href="../{o}/">{cap(P[o]["h"])}</a></li>' for o in others)
        art = f'''<article class="article">
      <h1>{cap(g["h"])}</h1>
      <p class="meta">By Raahee Corp &middot; <time datetime="{DATE}">26 November 2026</time> &middot; {m} min read</p>
      <figure><img src="../../../images/{base}.webp" alt="{esc(alt)}" width="1600" height="1066" fetchpriority="high"></figure>
      {body}
      <aside class="callout" aria-labelledby="cta-h">
        <h2 id="cta-h">Interested in Raahee Parna?</h2>
        <p>Get the price list, floor plans and brochure for 2, 2.5 and 3 BHK homes in Dudulgaon, Moshi, Pune.</p>
        <a class="btn btn--primary arrow" href="../../../#contact">Register your interest</a>
      </aside>
      <section class="related" aria-labelledby="rel-h">
        <h2 id="rel-h">More about Raahee Parna</h2>
        <ul>{rel}<li><a href="../../">All Raahee Parna guides</a></li></ul>
      </section>
    </article>'''
        t = re.sub(r'<article class="article">.*?</article>', lambda x: art, t, count=1, flags=re.S)
        wr(f"blog/{CAT}/{s}/index.html", t)
    # category page cloned from the blog hub
    t = rd("blog/index.html"); path = f"/blog/{CAT}/"
    title = "Raahee Parna Price, Plans & RERA | Dudulgaon"
    desc = "Raahee Parna, Dudulgaon near Moshi: price list, floor plans and carpet areas, MahaRERA details, amenities and a full project overview."
    t = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", t, flags=re.S)
    for pat in [r'(<meta name="description" content=")[^"]*', r'(<meta property="og:description" content=")[^"]*', r'(<meta name="twitter:description" content=")[^"]*']:
        t = re.sub(pat, lambda x: x.group(1) + esc(desc), t)
    for pat in [r'(<meta property="og:title" content=")[^"]*', r'(<meta name="twitter:title" content=")[^"]*']:
        t = re.sub(pat, lambda x: x.group(1) + esc(title), t)
    for pat in [r'(<link rel="canonical" href=")[^"]*', r'(<meta property="og:url" content=")[^"]*', r'(<link rel="alternate" hreflang="[^"]*" href=")[^"]*']:
        t = re.sub(pat, lambda x: x.group(1) + URL + path, t)
    t = t.replace('href="../', 'href="../../').replace('src="../', 'src="../../')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": CATNAME, "url": URL + path, "inLanguage": "en-IN",
         "hasPart": [{"@type": "BlogPosting", "headline": P[s]["h"], "url": f"{URL}/blog/{CAT}/{s}/"} for s in ORDER]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": URL + q} for i, (n, q) in enumerate([("Raahee Parna", "/"), ("Blog", "/blog/"), (CATNAME, path)])]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda x: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + "\n  </script>", t, count=1, flags=re.S)
    t = re.sub(r'<nav class="crumbs".*?</nav>', f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../../">Raahee Parna</a> &rsaquo; <a href="../">Blog</a> &rsaquo; <span>{CATNAME}</span></nav>', t, count=1, flags=re.S)
    t = re.sub(r"<h1>.*?</h1>", "<h1>Raahee Parna Dudulgaon: price list, floor plans, RERA and amenities</h1>", t, count=1, flags=re.S)
    t = re.sub(r'<p class="eyebrow">.*?</p>', '<p class="eyebrow">Project guides</p>', t, count=1, flags=re.S)
    t = re.sub(r'(<header class="blog-hero">.*?</h1>\s*)<p>.*?</p>', lambda x: x.group(1) + "<p>Price list, floor plans and carpet areas, MahaRERA details, amenities and an overview of Raahee Parna by Raahee Corp in Dudulgaon, Moshi, Pune. All figures come from the current price list and plans and are indicative.</p>", t, count=1, flags=re.S)
    cards = "".join(card_blog(s, "../../") for s in ORDER)
    t = re.sub(r'(<section class="posts"[^>]*>\s*).*?(\s*</section>)', lambda x: x.group(1) + cards + x.group(2), t, count=1, flags=re.S)
    wr(f"blog/{CAT}/index.html", t)

# --------------------------------------------------------------------------- site-wide edits
def head_fonts(t, p):
    t = re.sub(r'\s*<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*>', "", t)
    t = re.sub(r'\s*<link (?:rel="stylesheet" )?href="https://fonts\.googleapis\.com/css2[^>]*>', "", t)
    if "roboto-latin.woff2" not in t:
        t = t.replace("</head>", f'  <link rel="preload" as="font" type="font/woff2" crossorigin href="{p}fonts/roboto-latin.woff2">\n</head>', 1)
    return t


def sitewide():
    pages = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(("node_modules/", "dist/", "scripts/"))]
    for f in pages:
        t = rd(f); o = t; depth = f.count("/"); p = "../" * depth
        t = head_fonts(t, p)
        # cache-busting
        t = re.sub(r'((?:href|src)="(?:\.\./)*(?:css|js)/[A-Za-z0-9._-]+\.(?:css|js))(?:\?v=[^"]*)?"', lambda m: m.group(1) + f'?v={VER}"', t)
        # footer: link the HTML site map
        if "sitemap/" not in t:
            t = re.sub(r'(<li><a href="((?:\.\./)*)blog/">Blog</a></li>)', lambda m: m.group(1) + f'<li><a href="{m.group(2)}sitemap/">Site map</a></li>', t, count=1)
        t = t.replace('alt="MahaRERA QR code, registration number', 'alt="Raahee Parna: MahaRERA QR code, registration number')
        t = add_srcset(t, f)
        if t != o: wr(f, t)


def home():
    t = rd("index.html")
    # brand in the H1 through the logo alt
    t = t.replace('<h1 class="hero__title"><img class="hero__logo" src="images/logo-teal.webp" alt="Raahee Parna"', '<h1 class="hero__title"><img class="hero__logo" src="images/logo-teal.webp" alt="Raahee Parna Dudulgaon"')
    if 'id="guides"' not in t:
        cards = [("raahee-parna-price-list", "river", "Price list", "Raahee Parna price list", "Unit-wise total packages for 2, 2.5 and 3 BHK homes, from ₹58.53 lakh."),
                 ("raahee-parna-floor-plans", "aerial", "Floor plans", "Floor plans and carpet areas", "Typical B, C and D wing plans, with carpet areas for every home type."),
                 ("raahee-parna-dudulgaon-overview", "pool", "Project overview", "Raahee Parna Dudulgaon overview", "3.5 acres, 686 homes in 7 towers, 40+ amenities near Moshi, Pune.")]
        li = ""
        for s, im, tag, title, dek in cards:
            base, alt = IMGS[im]; v = f"images/{base}-{RESIZE[base]}.webp" if base in RESIZE else f"images/{base}.webp"
            li += (f'<li class="gl-card"><a href="blog/{CAT}/{s}/"><span class="gl-im"><img src="{v}" width="800" height="533" loading="lazy" decoding="async" alt="{esc(alt)}"><em>{tag}</em></span>'
                   f'<span class="gl-tx"><strong>{title}</strong><span>{dek}</span><span class="gl-foot"><b>Read guide &rarr;</b></span></span></a></li>')
        quick = "".join(f'<a href="blog/{CAT}/{s}/">{lab}</a>' for s, lab in [("raahee-parna-rera-details", "RERA details"), ("raahee-parna-amenities", "Amenities"), ("raahee-parna-price-list", "Price list"), ("raahee-parna-floor-plans", "Floor plans"), ("raahee-parna-dudulgaon-overview", "Project overview")])
        sec = f'''    <!-- GUIDES -->
    <section class="section" id="guides" aria-labelledby="h-guides" style="padding-top:0">
      <div class="wrap">
        <p class="eyebrow">Free guides</p>
        <h2 class="h2" id="h-guides">Raahee Parna guides for Dudulgaon home buyers</h2>
        <p class="gl-sub">Plain-spoken guides on the price list, floor plans, RERA details and life in Dudulgaon, so you can decide with confidence.</p>
        <ul class="gl-grid">{li}</ul>
        <p class="gl-quick">{quick}<a href="blog/">All guides</a></p>
      </div>
    </section>

'''
        t = t.replace("    <!-- FAQ -->", sec + "    <!-- FAQ -->", 1)
    wr("index.html", t)


def hub():
    t = rd("blog/index.html")
    if f"blog/{CAT}/" not in t and f'{CAT}/{ORDER[0]}/' not in t:
        cards = "".join(card_blog(s, "../") for s in ORDER)
        t = re.sub(r'(<section class="posts"[^>]*>\s*)', lambda x: x.group(1) + cards, t, count=1)
        wr("blog/index.html", t)
    # related links on the original posts
    for f in glob.glob("blog/*/index.html"):
        d = os.path.basename(os.path.dirname(f))
        if d == CAT: continue
        t = rd(f)
        if f"../{CAT}/" not in t and "</ul>\n      </section>\n    </article>" in t:
            extra = f'<li><a href="../{CAT}/raahee-parna-price-list/">Raahee Parna price list: 2, 2.5 and 3 BHK in Dudulgaon, Moshi</a></li><li><a href="../{CAT}/raahee-parna-floor-plans/">Raahee Parna floor plans and carpet areas: B, C and D wings</a></li>'
            t = t.replace("</ul>\n      </section>\n    </article>", extra + "</ul>\n      </section>\n    </article>", 1)
            wr(f, t)


def sitemap_page():
    t = rd("blog/index.html"); path = "/sitemap/"
    t = t.replace('href="../', 'href="../').replace("<body>", "<body>", 1)
    title = "Site Map | Raahee Parna, Dudulgaon"
    desc = "Site map of Raahee Parna, Dudulgaon near Moshi, Pune: the project page, price list, floor plans, RERA details, amenities, FAQ and every guide in one place."
    t = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", t, flags=re.S)
    for pat in [r'(<meta name="description" content=")[^"]*', r'(<meta property="og:description" content=")[^"]*', r'(<meta name="twitter:description" content=")[^"]*']:
        t = re.sub(pat, lambda x: x.group(1) + esc(desc), t)
    for pat in [r'(<meta property="og:title" content=")[^"]*', r'(<meta name="twitter:title" content=")[^"]*']:
        t = re.sub(pat, lambda x: x.group(1) + esc(title), t)
    for pat in [r'(<link rel="canonical" href=")[^"]*', r'(<meta property="og:url" content=")[^"]*', r'(<link rel="alternate" hreflang="[^"]*" href=")[^"]*']:
        t = re.sub(pat, lambda x: x.group(1) + URL + path, t)
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": "Site map", "url": URL + path},
          {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Raahee Parna", "item": URL + "/"}, {"@type": "ListItem", "position": 2, "name": "Site map", "item": URL + path}]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda x: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + "\n  </script>", t, count=1, flags=re.S)
    t = re.sub(r'<nav class="crumbs".*?</nav>', '<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Raahee Parna</a> &rsaquo; <span>Site map</span></nav>', t, count=1, flags=re.S)
    blog_posts = [("../blog/club-parna-lifestyle-amenities-dudulgaon/", "Inside Raahee Parna: Club Parna, the Pool and 40+ Amenities"),
                  ("../blog/getting-around-from-raahee-parna-dudulgaon/", "Getting Around from Raahee Parna: Dudulgaon's Schools, Hospitals and Hubs"),
                  ("../blog/buying-a-home-in-moshi-pune-with-raahee-parna/", "Buying a Home in Moshi, Pune: Where Raahee Parna in Dudulgaon Fits In"),
                  ("../blog/choosing-where-to-live-in-pune-raahee-parna/", "Where to Live in Pune: A Practical Checklist and How Raahee Parna Compares")]
    sec = lambda h, items: f'<section class="smap__sec"><h2>{h}</h2><ul>' + "".join(f'<li><a href="{u}">{n}</a></li>' for u, n in items) + "</ul></section>"
    main_ = [("../", "Raahee Parna: home page"), ("../#homes", "2, 2.5 & 3 BHK homes"), ("../#pricing", "Price list"), ("../#plans", "Floor plans"), ("../#amenities", "Amenities"), ("../#location", "Location"), ("../#faq", "FAQ"), ("../#contact", "Contact and enquiry")]
    proj = [(f"../blog/{CAT}/", "All project guides")] + [(f"../blog/{CAT}/{s}/", cap(P[s]["h"])) for s in ORDER]
    body = f'<div class="smap">{sec("Raahee Parna, Dudulgaon", main_)}{sec("Project guides", proj)}{sec("Journal", [("../blog/", "All guides")] + blog_posts)}</div>'
    t = t.replace(' aria-current="page"', "")
    t = re.sub(r'<header class="blog-hero">.*?</header>', '<header class="blog-hero"><p class="eyebrow">Find anything</p><h1>Raahee Parna Dudulgaon site map</h1><p>Every page of Raahee Parna in one place.</p></header>', t, count=1, flags=re.S)
    t = re.sub(r'<section class="posts"[^>]*>.*?</section>', lambda x: body, t, count=1, flags=re.S)
    wr("sitemap/index.html", t)


def css():
    c = rd("css/site.css")
    if "roboto-latin" not in c:
        ff = rd(os.path.join(FONT_SRC, "fonts.css"))
        c = ff + c
    if ".gl-grid" not in c:
        c += """
/* guides section + tables + site map (added with the SEO upgrade) */
.gl-sub{max-width:620px;color:var(--muted);margin:-.2em 0 1.4em}
.gl-grid{list-style:none;margin:0;padding:4px 2px 10px;display:grid;grid-auto-flow:column;grid-auto-columns:84%;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
.gl-grid::-webkit-scrollbar{display:none}
.gl-card{scroll-snap-align:center;display:flex}
.gl-card a{display:flex;flex-direction:column;width:100%;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-l);overflow:hidden;text-decoration:none;color:var(--ink);transition:transform .3s,box-shadow .3s}
.gl-card a:hover{transform:translateY(-4px);box-shadow:var(--shadow)}
.gl-im{position:relative;display:block;aspect-ratio:3/2;overflow:hidden;background:var(--teal-d)}
.gl-im img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s}
.gl-card a:hover .gl-im img{transform:scale(1.05)}
.gl-im em{position:absolute;left:12px;top:12px;font-style:normal;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:var(--lime);color:var(--ink);padding:.35em .8em;border-radius:999px}
.gl-tx{display:flex;flex-direction:column;gap:.4em;padding:18px 20px 18px;flex:1}
.gl-tx strong{font-size:1.15rem;line-height:1.25;color:var(--ink)}
.gl-tx>span{font-size:.93rem;line-height:1.55;color:var(--muted)}
.gl-foot{margin-top:auto;padding-top:.7em;border-top:1px dashed var(--line)}
.gl-foot b{color:var(--teal-d);font-size:.9rem}
.gl-quick{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0}
.gl-quick a{font-size:.85rem;font-weight:500;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:.45em 1em;text-decoration:none;transition:background .2s,border-color .2s}
.gl-quick a:hover{background:var(--tint-lime);border-color:var(--green)}
@media(min-width:800px){.gl-grid{grid-auto-flow:row;grid-auto-columns:auto;grid-template-columns:repeat(3,1fr);overflow:visible;gap:22px}}
.tw{overflow-x:auto;margin:0 0 1.4em;-webkit-overflow-scrolling:touch}
.article table.compare{width:100%;border-collapse:collapse;font-size:.95rem;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-m);overflow:hidden}
.article table.compare th,.article table.compare td{padding:.7em .9em;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
.article table.compare th{background:var(--tint-lime);font-weight:500}
.article ol{margin:0 0 1.3em;padding-left:1.3em}.article ol li{margin-bottom:.45em}
.smap{display:grid;gap:22px;padding:24px 0 48px}.smap__sec h2{font-size:1.25rem;margin:0 0 .5em}.smap__sec ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}.smap__sec a{color:var(--teal-d)}
@media(min-width:800px){.smap{grid-template-columns:repeat(3,1fr)}}
"""
    wr("css/site.css", c)


def fonts():
    os.makedirs("fonts", exist_ok=True)
    for n in ("roboto-latin.woff2", "roboto-latin-ext.woff2"):
        if not os.path.exists(f"fonts/{n}"): shutil.copy(os.path.join(FONT_SRC, n), f"fonts/{n}")


def sitemap_xml():
    sm = rd("sitemap.xml")
    add = [f"/blog/{CAT}/", "/sitemap/"] + [f"/blog/{CAT}/{s}/" for s in ORDER]
    for u in add:
        if URL + u not in sm:
            sm = sm.replace("</urlset>", f'  <url><loc>{URL}{u}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    sm = re.sub(r"(<loc>https://raaheeparna\.com/(?:blog/)?</loc>\s*<lastmod>)[^<]*", lambda m: m.group(1) + DATE, sm)
    wr("sitemap.xml", sm)


def build_mjs():
    b = rd("scripts/build.mjs")
    for entry in ("fonts", "sitemap"):
        if f'"{entry}",' not in b:
            b = b.replace('  "css",', f'  "css",\n  "{entry}",', 1)
    wr("scripts/build.mjs", b)


def htaccess():
    h = rd(".htaccess")
    h = h.replace('ExpiresByType text/css "access plus 1 month"', 'ExpiresByType text/css "access plus 1 day"').replace('ExpiresByType application/javascript "access plus 1 month"', 'ExpiresByType application/javascript "access plus 1 day"')
    if "font/woff2" not in h:
        h = h.replace('  ExpiresByType image/x-icon "access plus 1 year"', '  ExpiresByType image/x-icon "access plus 1 year"\n  ExpiresByType font/woff2 "access plus 1 year"')
    wr(".htaccess", h)


if __name__ == "__main__":
    fonts(); make_variants(); css(); build_mjs(); htaccess()
    build_pages(); home(); hub(); sitemap_page(); sitewide(); sitemap_xml()
    print("done")
