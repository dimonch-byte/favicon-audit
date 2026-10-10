#!/usr/bin/env python3
"""favicon-audit: what icons does your own homepage declare, and do they load? stdlib only."""
import sys, urllib.request, urllib.parse
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=="link" and a.get("rel"): s.links.append((a["rel"].lower(),a.get("href",""),a.get("sizes","")))
UA={"User-Agent":"favicon-audit/1.0"}
def ok(u):
    try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA,method="GET"),timeout=15).status==200
    except Exception: return False
def main():
    url=sys.argv[1]; p=P(); p.feed(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=20).read(2_000_000).decode("utf-8","replace"))
    rels={r for r,_,_ in p.links}; probs=[]
    for r,h,sz in p.links:
        if "icon" in r or r=="manifest": print(f"  {r:22} {sz:9} {h}  {'ok' if ok(urllib.parse.urljoin(url,h)) else 'BROKEN'}")
    if not any("icon" in r for r in rels): probs.append("no <link rel=icon> (browsers fall back to /favicon.ico)")
    if "apple-touch-icon" not in rels: probs.append("no apple-touch-icon (iOS home screen shows a screenshot)")
    if "manifest" not in rels: probs.append("no web app manifest (Android/PWA icons)")
    if not ok(urllib.parse.urljoin(url,"/favicon.ico")): probs.append("/favicon.ico does not load")
    for x in probs: print("MISSING", x)
    if probs: print("\nFull icon set from your logo (free check first): https://iconpack.adjudi.com/?utm_source=github&utm_medium=cli&utm_campaign=iconpack-intent-w2&utm_content=favicon-audit")
if __name__=="__main__": main()
