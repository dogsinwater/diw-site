#!/usr/bin/env python3
"""One-time: map every old WordPress URL to its new home -> redirects.txt"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
old = [l.strip().strip("/") for l in Path(sys.argv[1]).read_text().split() if l.strip()]
live = {p.stem for p in (ROOT / "content/guides").glob("*.md")} | {"contact", "privacy-policy", "about", "terms", "gear", "guides", "topics", "affiliate-disclaimer"}
M = {
 "a-boating-adventure-with-your-dog": "preparing-for-a-boat-trip-with-your-dog", "planning-a-pet-friendly-boat-trip": "preparing-for-a-boat-trip-with-your-dog",
 "how-to-make-your-boat-ride-a-splash-with-your-pooch": "preparing-for-a-boat-trip-with-your-dog", "7-tips-for-enjoying-a-stress-free-boat-ride-with-your-dog": "preparing-for-a-boat-trip-with-your-dog",
 "creative-dog-friendly-boat-activities": "preparing-for-a-boat-trip-with-your-dog", "doggy-boat-toys": "preparing-for-a-boat-trip-with-your-dog",
 "a-sailors-guide-to-dog-safety-at-sea": "the-dos-and-donts-of-boating-with-dogs", "going-on-a-cruise-adventure-with-your-dog": "the-dos-and-donts-of-boating-with-dogs",
 "paddleboarding-with-your-furry-friend": "kayaks-for-a-paddling-adventure-with-your-dog",
 "dog-safety-near-open-water": "checklist-for-ensuring-your-dogs-safety-in-and-around-water",
 "doggy-life-jackets-ensuring-your-furry-friends-safety-on-a-boat": "doggy-life-jackets", "top-5-dog-life-vests-in-the-market-and-why-they-are-important": "doggy-life-jackets",
 "safely-exploring-water-trails-with-your-dog": "ensuring-your-dogs-safety-in-moving-water",
 "how-to-keep-dogs-cool-with-water": "protecting-your-dog-from-heatstroke-at-the-beach",
 "how-to-train-your-dog-to-swim-safely-at-the-beach": "teaching-your-dog-to-swim-via-doggy-paddle", "dive-into-water-adventures-with-your-canine-companion": "teaching-your-dog-to-swim-via-doggy-paddle",
 "chihuahuas-and-their-fear-of-water-solutions": "how-to-bathe-a-dog-who-hates-water", "fun-facts-about-dogs-and-water": "unraveling-the-mechanics-of-how-dogs-swim",
 "a-beach-adventure-with-your-dog": "doggy-beach-day", "tips-for-a-perfect-beach-day-with-your-furry-friend": "doggy-beach-day",
 "how-to-protect-your-pet-at-the-beach": "doggy-beach-day", "keep-your-furry-friend-safe-at-the-beach-tips-for-dog-owners": "doggy-beach-day",
 "fun-and-healthy-snacks-for-your-dogs-beach-day": "packing-for-the-beach-a-dog-owners-checklist", "the-ultimate-guide-to-a-perfect-dog-friendly-beach-picnic": "packing-for-the-beach-a-dog-owners-checklist",
 "dog-friendly-beaches-for-the-ultimate-canine-vacation": "doggy-beach-etiquette-how-to-respect-other-beachgoers",
 "how-to-handle-potential-dangers-for-dogs-at-the-lake": "avoiding-hazards-ensuring-your-dogs-safety-at-the-lake",
 "splashing-around-fun-activities-for-your-dog-at-the-lake": "must-have-items-for-a-lake-day-with-your-dog", "10-must-have-items-for-a-perfect-day-at-the-lake-with-your-dog": "must-have-items-for-a-lake-day-with-your-dog",
 "top-picks-for-dog-friendly-lakes": "must-have-items-for-a-lake-day-with-your-dog", "the-benefits-of-freshwater-swimming-for-your-dog": "must-have-items-for-a-lake-day-with-your-dog",
 "how-to-create-a-safe-and-enjoyable-backyard-pool-for-your-furry-friends": "how-to-keep-your-dog-safe-near-pools", "a-pool-adventure-with-your-dog": "how-to-keep-your-dog-safe-near-pools",
 "how-to-build-a-dog-friendly-pond": "how-to-keep-your-dog-safe-near-pools",
 "post-swim-toys": "pool-toys-for-dogs-who-love-water", "how-to-host-the-ultimate-pool-party-for-your-dog": "pool-toys-for-dogs-who-love-water", "the-importance-of-washing-your-dogs-toys": "pool-toys-for-dogs-who-love-water",
 "ensuring-your-dogs-health-post-swim": "essential-post-swimming-practices-for-your-dog", "paws-and-coats": "dive-in-but-keep-your-pups-skin-healthy",
 "doggy-beach-games-to-enhance-your-bond": "10-water-games-your-dog-will-love",
 "the-ultimate-guide-to-creating-the-perfect-agility-course-kit-diy-for-lakeside-or-beach-fun-for-a-dog": "10-water-games-your-dog-will-love",
 "water-sport-competitions-for-dogs": "world-of-dog-dock-diving", "snowy-photo-shoot-capturing-your-dogs-beauty-in-the-winter-scenery": "how-to-photograph-your-swimming-dog",
 "dogs-really-need-winter-coats": "how-to-keep-your-dog-warm-after-a-winter-swim",
 "build-a-dog-friendly-snow-fort": "how-to-train-your-dog-to-love-playing-in-the-snow", "a-snow-adventure-with-my-dog": "how-to-train-your-dog-to-love-playing-in-the-snow",
 "letting-your-dog-eat-snow": "how-to-train-your-dog-to-love-playing-in-the-snow",
 "thanksgiving-hazards-for-dogs-a-comprehensive-guide-for-pet-owners": "", "gps-tracker-for-dogs": "gear", "teaching-your-dog-search-and-rescue-skills": "world-of-dog-dock-diving",
 "blog": "guides", "shop": "gear", "affiliate-disclosure": "affiliate-disclaimer", "terms-and-conditions": "terms", "advertise-with-us": "contact",
 "my-bookmarks": "", "customize-interests": "", "cart": "gear", "checkout": "gear", "my-account": "",
}
lines = ["# Old WordPress URLs -> new site (Cloudflare _redirects format). Generated by scripts/make_redirects.py"]
missing = []
for s in old:
    if s in live:
        continue
    if s.startswith("shop/"):
        dest = "gear"
    elif s in M:
        dest = M[s]
    else:
        missing.append(s); continue
    d = "/" + (dest + "/" if dest else "")
    lines += [f"/{s}/ {d} 301", f"/{s} {d} 301"]
lines += ["# WordPress leftovers", "/home/ / 301", "/feed/ /sitemap.xml 301", "/wp-admin/* / 301", "/wp-login.php / 301",
          "/category/* /topics/ 301", "/tag/* /guides/ 301", "/author/* /about/ 301", "/product/* /gear/ 301",
          "/product-category/* /gear/ 301", "/shop/* /gear/ 301"]
(ROOT / "redirects.txt").write_text("\n".join(lines) + "\n")
print(f"{len(old)} old URLs -> {len([l for l in lines if l.startswith('/')])} rules; unmapped: {missing}")
