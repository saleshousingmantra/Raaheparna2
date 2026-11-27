#!/usr/bin/env python3
"""Add four locality guides for Raahee Parna (run AFTER scripts/improve.py, from the repo root).

    python3 scripts/improve.py && python3 scripts/add_locality.py

Every place name and travel time comes from the project's location map (approximate, as already
published in the "Getting around from Raahee Parna" guide). Nothing is invented; each place links to
Google Maps so readers can check live directions.
"""
import os, re, json, html, urllib.parse
import improve as I
from improve import rd, wr, esc, cap, slugify, mins, URL, DATE, P, IMGS, RESIZE, ORDER as PROJ_ORDER

CAT = "locality"
CATNAME = "Dudulgaon locality guides"
IMGS["map"] = ("location-map", "Location map of Raahee Parna in Dudulgaon near Moshi, Pune with nearby schools, hospitals and IT parks")


def gmaps(name):
    q = urllib.parse.quote_plus(f"{name} Dudulgaon Pune")
    return f'<a href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener" aria-label="Open {name} in Google Maps">Map</a>'


def table(rows, hdr=("Place", "Approx. travel time")):
    t = f'<div class="tw"><table class="compare"><thead><tr><th>{hdr[0]}</th><th>{hdr[1]}</th><th>Map</th></tr></thead><tbody>'
    for n, tm in rows: t += f"<tr><td>{n}</td><td>{tm}</td><td>{gmaps(n)}</td></tr>"
    return t + "</tbody></table></div>"

SRC = ("<p><strong>How we compiled this guide:</strong> place names and travel times come from the Raahee Parna location map and are approximate. "
       "Traffic changes every trip, so use the Google Maps links to check live directions, and confirm details with each place before you decide.</p>")

L = {}
L["schools-and-colleges-near-raahee-parna"] = dict(
    cat=CAT, img="map", tag="Schools and colleges",
    t="Schools and Colleges near Raahee Parna, Dudulgaon",
    h="Schools and colleges near Raahee Parna, Dudulgaon",
    d="Schools and colleges near Raahee Parna, Dudulgaon, Moshi: Aditya International School 3–5 min, colleges from 2–3 min. Approximate times and map links.",
    dek="Schools and colleges around Raahee Parna in Dudulgaon, with approximate travel times and Google Maps links.",
    body=f'''<p>For most families, the school run decides whether a home works day to day. Raahee Parna sits in Dudulgaon, near Moshi in PCMC, Pune, and several schools and colleges are a short drive away. Here is what lies around the project.</p>
<h2>Schools near Raahee Parna</h2>
{table([("Aditya International School", "about 3–5 minutes"), ("New Orchid International School", "about 4–7 minutes"), ("Priyadarshani School", "about 7–10 minutes"), ("Radcliffe School, Chovisawadi", "about 8–12 minutes"), ("Silver Birch International School", "about 8–12 minutes"), ("City Pride School", "about 8–12 minutes"), ("Apex International School, Wadmukhwadi", "about 10–15 minutes"), ("RKL Galaxy International School, Wadmukhwadi", "about 10–15 minutes")])}
<h2>Colleges and universities</h2>
{table([("Rajmata Jijau Shikshan Prasarak Mandal College of Pharmacy, Dudulgaon", "about 2–3 minutes"), ("MIT Arts, Commerce and Science College", "about 5–10 minutes"), ("Modern College of Pharmacy", "about 5–10 minutes"), ("Dnyanvilas College of Engineering", "about 5–10 minutes"), ("Dr D Y Patil Technical Campus", "about 15–20 minutes"), ("Ajeenkya DY Patil University", "about 20–30 minutes")])}
<h2>How to choose a school</h2>
<ul><li>Visit at drop-off time to see the real traffic and the school's own transport.</li><li>Ask about the board, admission process and fees directly with the school.</li><li>Check whether a school bus serves Dudulgaon and Raahee Parna.</li></ul>
<h2>Plan your own route</h2>
<p>Try the route from <a href="https://www.google.com/maps/search/?api=1&amp;query=Raahee+Parna+Dudulgaon+Pune" target="_blank" rel="noopener">Raahee Parna on Google Maps</a> to the schools on your shortlist at your usual travel time. For more about the area, read <a href="../../getting-around-from-raahee-parna-dudulgaon/">getting around from Raahee Parna</a> and the <a href="../../raahee-parna/raahee-parna-dudulgaon-overview/">Raahee Parna project overview</a>.</p>
{SRC}''')

L["hospitals-near-raahee-parna"] = dict(
    cat=CAT, img="map", tag="Hospitals",
    t="Hospitals near Raahee Parna, Dudulgaon, Moshi",
    h="Hospitals near Raahee Parna, Dudulgaon, Moshi",
    d="Hospitals near Raahee Parna, Dudulgaon: Kamlesh and Jijau hospitals 3–5 min, Dhanashree in Moshi 5–7 min, and larger facilities within 20 min. Map links.",
    dek="Hospitals and healthcare around Raahee Parna in Dudulgaon, with approximate travel times and Google Maps links.",
    body=f'''<p>Knowing where the nearest hospital is matters when you choose a home. Raahee Parna in Dudulgaon, near Moshi, has several hospitals within a short drive, and larger facilities are a little farther.</p>
<h2>Hospitals close to Raahee Parna</h2>
{table([("Kamlesh Multispeciality Hospital", "about 3–5 minutes"), ("Jijau Mother and Child Care Hospital", "about 3–5 minutes"), ("Dhanashree Multispeciality Hospital, Moshi", "about 5–7 minutes"), ("Bliss Hospital", "about 5–10 minutes"), ("Tulip Hospital", "about 5–10 minutes"), ("Sunrise Hospital", "about 5–10 minutes"), ("Accord Hospitals", "about 15–20 minutes")])}
<h2>What to check before you rely on a hospital</h2>
<ul><li>Confirm the specialities, emergency services and opening hours directly with the hospital.</li><li>Ask which insurance and cashless plans each hospital accepts.</li><li>Save the nearest hospital's number and location on your phone before you move in.</li></ul>
<h2>Plan your own route</h2>
<p>Check live directions from <a href="https://www.google.com/maps/search/?api=1&amp;query=Raahee+Parna+Dudulgaon+Pune" target="_blank" rel="noopener">Raahee Parna on Google Maps</a>, ideally once at peak hour and once off-peak. Read the <a href="../schools-and-colleges-near-raahee-parna/">schools and colleges guide</a> and <a href="../../getting-around-from-raahee-parna-dudulgaon/">getting around from Raahee Parna</a> for the rest of the neighbourhood.</p>
{SRC}''')

L["shopping-and-malls-near-raahee-parna"] = dict(
    cat=CAT, img="map", tag="Shopping",
    t="Shopping and Malls near Raahee Parna, Dudulgaon",
    h="Shopping and malls near Raahee Parna, Dudulgaon",
    d="Shopping near Raahee Parna, Dudulgaon: DMart and Reliance Trends 5–10 min, Town Plaza, Silverian Mall and Spine City Mall 10–15 min. Map links.",
    dek="Everyday shopping and malls around Raahee Parna in Dudulgaon, with approximate travel times and Google Maps links.",
    body=f'''<p>Daily errands and weekend outings both depend on how close the shops are. From Raahee Parna in Dudulgaon, everyday stores are a short drive and the larger malls are a modest trip.</p>
<h2>Everyday shopping</h2>
{table([("DMart", "about 5–10 minutes"), ("Reliance Trends", "about 5–10 minutes"), ("Reliance Digital", "about 5–10 minutes")])}
<h2>Malls for a bigger day out</h2>
{table([("Town Plaza", "about 10–15 minutes"), ("Silverian Mall", "about 10–15 minutes"), ("Spine City Mall", "about 10–15 minutes")])}
<h2>Making the most of it</h2>
<ul><li>Plan the weekly shop for off-peak hours to avoid queues and parking trouble.</li><li>Check store timings and offers directly, since they change often.</li><li>Walk the streets near the project during a visit to see the local markets for yourself.</li></ul>
<h2>Plan your own route</h2>
<p>Check live directions from <a href="https://www.google.com/maps/search/?api=1&amp;query=Raahee+Parna+Dudulgaon+Pune" target="_blank" rel="noopener">Raahee Parna on Google Maps</a>. For the other amenities nearby, read the <a href="../hospitals-near-raahee-parna/">hospitals guide</a> and <a href="../../club-parna-lifestyle-amenities-dudulgaon/">what Club Parna offers inside the campus</a>.</p>
{SRC}''')

L["it-parks-and-jobs-near-raahee-parna"] = dict(
    cat=CAT, img="map", tag="IT parks and jobs",
    t="IT Parks and Jobs near Raahee Parna, Dudulgaon",
    h="IT parks and employment hubs near Raahee Parna, Dudulgaon",
    d="Employment hubs near Raahee Parna, Dudulgaon: The Business Gate 5–10 min, Charholi IT Park 10–15 min, Talwade IT Park 30–40 min. Map links.",
    dek="IT parks and job hubs around Raahee Parna in Dudulgaon, with approximate travel times and Google Maps links.",
    body=f'''<p>For working buyers, the commute is part of the price of a home. Raahee Parna in Dudulgaon is close to a few employment hubs in the PCMC belt, while Pune's larger IT hubs are farther away.</p>
<h2>Employment hubs near Raahee Parna</h2>
{table([("The Business Gate", "about 5–10 minutes"), ("Charholi IT Park", "about 10–15 minutes"), ("Talwade IT Park", "about 30–40 minutes"), ("Hinjewadi IT Park", "about 60–70 minutes, depending on traffic"), ("Kharadi", "about 60–70 minutes, depending on traffic")])}
<h2>Who this location suits</h2>
<p>The location suits people who work in the PCMC belt or have flexible hours. If your office is in Hinjewadi or Kharadi, test the commute at peak hour before you decide, because traffic changes the time a great deal.</p>
<h2>Test your own commute</h2>
<ol><li>Open <a href="https://www.google.com/maps/search/?api=1&amp;query=Raahee+Parna+Dudulgaon+Pune" target="_blank" rel="noopener">Raahee Parna on Google Maps</a> and set your office as the destination.</li><li>Check the time at your usual leaving hour, not just off-peak.</li><li>Ask colleagues who live in Moshi and Charholi how they travel.</li></ol>
<p>Read the <a href="../schools-and-colleges-near-raahee-parna/">schools and colleges guide</a> and the <a href="../../buying-a-home-in-moshi-pune-with-raahee-parna/">guide to buying a home in Moshi</a> for the rest of the picture.</p>
{SRC}''')

LORDER = list(L)
for s in LORDER: P[s] = L[s]


def build_pages():
    for s in LORDER:
        g = L[s]; t = rd(I.TPL); path = f"/blog/{CAT}/{s}/"; base, alt = IMGS[g["img"]]
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
        t = re.sub(r'<nav class="crumbs".*?</nav>', f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../../../">Raahee Parna</a> &rsaquo; <a href="../../">Blog</a> &rsaquo; <a href="../">{CATNAME}</a> &rsaquo; <span>{esc(cap(g["tag"]))}</span></nav>', t, count=1, flags=re.S)
        others = [o for o in LORDER if o != s][:3]
        rel = "".join(f'<li><a href="../{o}/">{cap(L[o]["h"])}</a></li>' for o in others)
        rel += '<li><a href="../../raahee-parna/raahee-parna-dudulgaon-overview/">Raahee Parna Dudulgaon: project overview</a></li>'
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
        <h2 id="rel-h">More about Dudulgaon</h2>
        <ul>{rel}<li><a href="../">All Dudulgaon locality guides</a></li></ul>
      </section>
    </article>'''
        t = re.sub(r'<article class="article">.*?</article>', lambda x: art, t, count=1, flags=re.S)
        wr(f"blog/{CAT}/{s}/index.html", t)
    # category page cloned from the blog hub
    t = rd("blog/index.html"); path = f"/blog/{CAT}/"
    title = "Dudulgaon Locality Guides | Raahee Parna"
    desc = "Locality guides for Raahee Parna, Dudulgaon near Moshi: schools and colleges, hospitals, shopping and IT parks, with approximate times and map links."
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
         "hasPart": [{"@type": "BlogPosting", "headline": L[s]["h"], "url": f"{URL}/blog/{CAT}/{s}/"} for s in LORDER]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": URL + q} for i, (n, q) in enumerate([("Raahee Parna", "/"), ("Blog", "/blog/"), (CATNAME, path)])]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda x: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + "\n  </script>", t, count=1, flags=re.S)
    t = re.sub(r'<nav class="crumbs".*?</nav>', f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../../">Raahee Parna</a> &rsaquo; <a href="../">Blog</a> &rsaquo; <span>{CATNAME}</span></nav>', t, count=1, flags=re.S)
    t = re.sub(r"<h1>.*?</h1>", "<h1>Raahee Parna Dudulgaon locality guides: schools, hospitals, shopping and jobs</h1>", t, count=1, flags=re.S)
    t = re.sub(r'<p class="eyebrow">.*?</p>', '<p class="eyebrow">Locality guides</p>', t, count=1, flags=re.S)
    t = re.sub(r'(<header class="blog-hero">.*?</h1>\s*)<p>.*?</p>', lambda x: x.group(1) + "<p>What lies around Raahee Parna in Dudulgaon, near Moshi: schools and colleges, hospitals, shopping and employment hubs. Times are approximate, from the project's location map, and every place links to Google Maps.</p>", t, count=1, flags=re.S)
    intro = ('<section class="posts-intro wrap"><p>Choosing a home is about more than the flat itself. These four guides cover what lies around Raahee Parna in Dudulgaon, near Moshi in PCMC, Pune: the schools and colleges your children and students would use, the hospitals for everyday and emergency care, the shops and malls for daily needs and weekend plans, and the employment hubs that matter for your commute. Every place name and travel time comes from the Raahee Parna location map and is approximate, so use the Google Maps link beside each place to check live directions at your usual travel hour. '
             'Start with the guide that matters most to your household, then read the <a href="../getting-around-from-raahee-parna-dudulgaon/">getting around guide</a> for the full picture, and see the <a href="../raahee-parna/raahee-parna-dudulgaon-overview/">project overview</a>, <a href="../raahee-parna/raahee-parna-price-list/">price list</a> and <a href="../raahee-parna/raahee-parna-rera-details/">RERA details</a> when you are ready to compare homes.</p></section>')
    t = re.sub(r'(<section class="posts"[^>]*>)', lambda x: intro + x.group(1), t, count=1)
    cards = "".join(I.card_blog(s, "../../") for s in LORDER)
    t = re.sub(r'(<section class="posts"[^>]*>\s*).*?(\s*</section>)', lambda x: x.group(1) + cards + x.group(2), t, count=1, flags=re.S)
    wr(f"blog/{CAT}/index.html", t)


def mobile_css():
    c = rd("css/site.css")
    if "compare-mobile" not in c:
        c += """
/* compare-mobile: let table cells wrap on phones so every column is visible */
@media(max-width:640px){.article table.compare th,.article table.compare td{white-space:normal;padding:.6em .55em;font-size:.86rem;vertical-align:top}.article table.compare td:last-child{white-space:nowrap}}
"""
        wr("css/site.css", c)


def link_everywhere():
    # blog hub: locality cards after the project cards
    t = rd("blog/index.html")
    if f"blog/{CAT}/" not in t and f"{CAT}/{LORDER[0]}/" not in t:
        cards = "".join(I.card_blog(s, "../") for s in LORDER)
        t = re.sub(r'(<section class="posts"[^>]*>\s*)', lambda x: x.group(1) + cards, t, count=1)
        wr("blog/index.html", t)
    # HTML site map page
    t = rd("sitemap/index.html")
    if f"blog/{CAT}/" not in t:
        items = [(f"../blog/{CAT}/", "All locality guides")] + [(f"../blog/{CAT}/{s}/", cap(L[s]["h"])) for s in LORDER]
        sec = '<section class="smap__sec"><h2>Dudulgaon locality guides</h2><ul>' + "".join(f'<li><a href="{u}">{n}</a></li>' for u, n in items) + "</ul></section>"
        t = t.replace('<section class="smap__sec"><h2>Journal</h2>', sec + '<section class="smap__sec"><h2>Journal</h2>', 1)
        wr("sitemap/index.html", t)
    # home: quick links
    t = rd("index.html")
    if f"blog/{CAT}/" not in t:
        q = "".join(f'<a href="blog/{CAT}/{s}/">{lab}</a>' for s, lab in [("schools-and-colleges-near-raahee-parna", "Schools nearby"), ("hospitals-near-raahee-parna", "Hospitals nearby"), ("shopping-and-malls-near-raahee-parna", "Shopping nearby"), ("it-parks-and-jobs-near-raahee-parna", "IT parks and jobs")])
        t = t.replace('<a href="blog/">All guides</a></p>', q + '<a href="blog/">All guides</a></p>', 1)
        wr("index.html", t)
    # sitemap.xml
    sm = rd("sitemap.xml")
    for u in [f"/blog/{CAT}/"] + [f"/blog/{CAT}/{s}/" for s in LORDER]:
        if URL + u not in sm:
            sm = sm.replace("</urlset>", f'  <url><loc>{URL}{u}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    wr("sitemap.xml", sm)
    # existing "getting around" guide links to the four new guides
    f = "blog/getting-around-from-raahee-parna-dudulgaon/index.html"; t = rd(f)
    if f"../../blog/{CAT}/" not in t and f"../{CAT}/" not in t:
        extra = "".join(f'<li><a href="../{CAT}/{s}/">{cap(L[s]["h"])}</a></li>' for s in LORDER)
        t = t.replace("</ul>\n      </section>\n    </article>", extra + "</ul>\n      </section>\n    </article>", 1)
        wr(f, t)


if __name__ == "__main__":
    mobile_css(); build_pages(); link_everywhere(); I.sitewide()
    print("locality guides built:", LORDER)
