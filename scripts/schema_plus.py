#!/usr/bin/env python3
"""Richer structured data for Tanish Urbania, Raahee Parna and United Athila (facts already on each page only).
Usage: python3 schema_plus.py tanish|raahee|ua"""
import re, json, sys, os, glob, html
from PIL import Image

SITES = {
  "tanish": dict(root="/home/user/tanish-urbania", url="https://tanish-urbania.com", org="#developer", cx="#project"),
  "raahee": dict(root="/home/user/Raaheparna2", url="https://raaheeparna.com", org="#developer", cx="#project"),
  "ua": dict(root="/home/user/united-athila-dhanori", url="https://unitedathiladhanori.com", org="#organization", cx="#residence"),
}
name = sys.argv[1]; C = SITES[name]; os.chdir(C["root"]); URL = C["url"]
ORG = URL + "/" + C["org"]; CX = URL + "/" + C["cx"]
PAT = r'(<script type="application/ld\+json">)(.*?)(</script>)'

def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t): open(p, "w", encoding="utf-8").write(t)
def node(g, i):
    for x in g:
        if x.get("@id") == i: return x
def typ(x, t): return t in (x["@type"] if isinstance(x["@type"], list) else [x["@type"]])
def addtype(x, *ts):
    cur = x["@type"] if isinstance(x["@type"], list) else [x["@type"]]
    for t in ts:
        if t not in cur: cur.append(t)
    x["@type"] = cur if len(cur) > 1 else cur[0]
def page_h1(f):
    s = rd(f); m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    h = re.sub(r"<[^>]+>", " ", re.sub(r'<span class="h1-brand">.*?</span>', "", m.group(1)))
    return re.sub(r"\s+", " ", html.unescape(h)).strip()
def itemlist(id_, nm, files):
    items = []
    for i, (f, u) in enumerate(files):
        items.append({"@type": "ListItem", "position": i + 1, "name": page_h1(f), "url": URL + u})
    return {"@type": "ItemList", "@id": URL + "/#" + id_, "name": nm, "itemListElement": items}
def imgnode(n, f, cap):
    w, h = Image.open(f).size; u = f"{URL}/{f}"
    return {"@type": "ImageObject", "@id": f"{URL}/#img-{n}", "url": u, "contentUrl": u, "width": w, "height": h, "caption": cap, "inLanguage": "en-IN"}
def apt(name_, lo, hi, extra=None, bedrooms=None, desc=None):
    a = {"@type": "Apartment", "@id": f"{URL}/#apt-{re.sub(r'[^a-z0-9]+', '-', name_.lower())}", "name": name_,
         "floorSize": {"@type": "QuantitativeValue", "minValue": lo, "maxValue": hi, "unitCode": "FTK", "unitText": "sq ft (approx.)"}, "containedInPlace": {"@id": CX}}
    if bedrooms: a["numberOfBedrooms"] = bedrooms
    if desc: a["description"] = desc
    return a

def load():
    t = rd("index.html"); m = re.search(PAT, t, re.S); return t, m, json.loads(m.group(2))
def save(t, m, d): wr("index.html", t[:m.start()] + m.group(1) + json.dumps(d, ensure_ascii=False, indent=2) + m.group(3) + t[m.end():])
def push(g, *ns):
    have = {x.get("@id") for x in g if "@id" in x}
    for n in ns:
        if n["@id"] not in have: g.append(n)

# ---------------------------------------------------------------- Tanish Urbania
if name == "tanish":
    t, m, d = load(); g = d["@graph"]; org = node(g, ORG); cx = node(g, CX)
    brand = {"@type": "Brand", "@id": URL + "/#brand", "name": "Tanish Urbania", "slogan": "Urban Life. Redefined.", "logo": URL + "/android-chrome-512x512.png"}
    push(g, brand)
    org["brand"] = {"@id": brand["@id"]}; cx["brand"] = {"@id": brand["@id"]}
    org["contactPoint"] = {"@type": "ContactPoint", "contactType": "sales", "telephone": "+917264011256", "areaServed": "IN", "availableLanguage": ["en", "hi", "mr"]}
    addtype(cx, "Residence")
    cx["numberOfBuildings"] = 12
    cx["additionalProperty"] = [{"@type": "PropertyValue", "name": "Residential wings", "value": 12}, {"@type": "PropertyValue", "name": "Architecture", "value": "YW Architects"}]
    cx["amenityFeature"] = [{"@type": "LocationFeatureSpecification", "name": "Landscaped zones with well-distributed open areas", "value": True},
                            {"@type": "LocationFeatureSpecification", "name": "Wing placement for open space, daylight and cross ventilation", "value": True},
                            {"@type": "LocationFeatureSpecification", "name": "Generous balconies", "value": True}]
    a2 = apt("2 BHK at Tanish Urbania", 720, 770, bedrooms=2, desc="2 BHK homes of approximately 720 to 770 sq ft with generous balconies, cross ventilation and daylight. Price on request.")
    a3 = apt("3 BHK at Tanish Urbania", 920, 980, bedrooms=3, desc="3 BHK homes of approximately 920 to 980 sq ft with spacious living, generous balconies, cross ventilation and daylight. Price on request.")
    push(g, a2, a3); cx["containsPlace"] = [{"@id": a2["@id"]}, {"@id": a3["@id"]}]
    pl = node(g, URL + "/#place")
    if pl and "containedInPlace" not in pl: pl["containedInPlace"] = {"@type": "City", "name": "Pune", "address": {"@type": "PostalAddress", "addressRegion": "Maharashtra", "addressCountry": "IN"}}
    # richer navigation list: project pages + guides
    il = node(g, URL + "/#projectpages")
    files = [(f, "/" + f[:-10]) for f in sorted(glob.glob("blog/project/*/index.html"))] + [(f, "/" + f[:-10]) for f in sorted(glob.glob("blog/*/*/index.html")) if "/project/" not in f]
    g[g.index(il)] = itemlist("projectpages", "Tanish Urbania project pages and guides", files)
    save(t, m, d)
    for f in glob.glob("blog/**/index.html", recursive=True):
        s = rd(f)
        if "/#complex" in s: wr(f, s.replace(URL + "/#complex", CX))

# ---------------------------------------------------------------- Raahee Parna
if name == "raahee":
    t, m, d = load(); g = d["@graph"]; org = node(g, ORG); cx = node(g, CX)
    brand = {"@type": "Brand", "@id": URL + "/#brand", "name": "Raahee Parna", "logo": URL + "/images/logo-teal.webp"}
    push(g, brand); cx["brand"] = {"@id": brand["@id"]}; org["brand"] = {"@id": brand["@id"]}
    addtype(cx, "Residence")
    place = {"@type": "Place", "@id": URL + "/#place", "name": "Raahee Parna, Dudulgaon, near Moshi, PCMC, Pune", "hasMap": "https://www.google.com/maps/search/?api=1&query=Raahee+Parna+Dudulgaon+Pune",
             "address": {"@type": "PostalAddress", "addressLocality": "Dudulgaon", "addressRegion": "Maharashtra", "postalCode": "412105", "addressCountry": "IN"},
             "containedInPlace": {"@type": "City", "name": "Pune", "address": {"@type": "PostalAddress", "addressRegion": "Maharashtra", "addressCountry": "IN"}}}
    push(g, place); cx["containedInPlace"] = {"@id": place["@id"]}
    imgs = [imgnode("river", "images/hero-river.webp", "Raahee Parna towers by the Indrayani River, Dudulgaon, near Moshi, Pune"),
            imgnode("pool", "images/pool.webp", "Club Parna swimming pool at Raahee Parna, Dudulgaon"),
            imgnode("aerial", "images/aerial-1.webp", "Aerial view of Raahee Parna in Dudulgaon, Pune")]
    push(g, *imgs)
    files = [(f, "/" + f[:-10]) for f in sorted(glob.glob("blog/raahee-parna/*/index.html"))] + [(f, "/" + f[:-10]) for f in sorted(glob.glob("blog/locality/*/index.html"))]
    push(g, itemlist("projectpages", "Raahee Parna project pages and locality guides", files))
    wp = node(g, URL + "/#webpage")
    if wp: wp["about"] = {"@id": CX}; wp["primaryImageOfPage"] = {"@id": imgs[0]["@id"]}
    save(t, m, d)

# ---------------------------------------------------------------- United Athila
if name == "ua":
    t, m, d = load(); g = d["@graph"]; org = node(g, ORG); cx = node(g, CX)
    brand = {"@type": "Brand", "@id": URL + "/#brand", "name": "United Athila", "logo": URL + "/images/logo/united-athila-logo.png"}
    push(g, brand); cx["brand"] = {"@id": brand["@id"]}; org["brand"] = {"@id": brand["@id"]}
    imgs = [imgnode("courtyard", "images/gallery/towers-courtyard-view.webp", "United Athila, Dhanori: towers and landscaped courtyard (artist's impression)"),
            imgnode("pool", "images/gallery/pool-amenity-deck.webp", "United Athila, Dhanori: swimming pool and amenity deck (artist's impression)"),
            imgnode("facade", "images/gallery/towers-facade.webp", "United Athila, Dhanori: central tower facade (artist's impression)")]
    push(g, *imgs)
    cx["associatedMedia"] = [{"@id": i["@id"]} for i in imgs]
    a2 = apt("2 BHK at United Athila", 779, 843, desc="2 BHK homes of 779 to 843 sq ft carpet at United Athila, Dhanori. From ₹84.58 lakh (all-inclusive, indicative).")
    a25 = apt("2.5 BHK at United Athila", 806, 899, desc="2.5 BHK homes of 806 to 899 sq ft carpet at United Athila, Dhanori. From ₹90.22 lakh (all-inclusive, indicative).")
    a3 = apt("3 BHK at United Athila", 918, 1059, bedrooms=3, desc="3 BHK homes of 918 to 1,059 sq ft carpet at United Athila, Dhanori. From ₹99.63 lakh (all-inclusive, indicative).")
    a2["numberOfBedrooms"] = 2
    for a in (a2, a25, a3): a["floorSize"]["unitText"] = "sq ft carpet"
    push(g, a2, a25, a3); cx["containsPlace"] = [{"@id": a["@id"]} for a in (a2, a25, a3)]
    files = [(f, "/" + f[:-10]) for f in sorted(glob.glob("blog/united-athila/*/index.html"))] + [(f, "/" + f[:-10]) for f in sorted(glob.glob("blog/*/*/index.html")) if "/united-athila/" not in f]
    push(g, itemlist("projectpages", "United Athila project pages and guides", files))
    wp = node(g, URL + "/#webpage")
    if wp:
        addtype(wp, "RealEstateListing"); wp.setdefault("datePosted", "2026-11-26"); wp["about"] = {"@id": CX}; wp["primaryImageOfPage"] = {"@id": imgs[0]["@id"]}
    save(t, m, d)
print(name, "done")
