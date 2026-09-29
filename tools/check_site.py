#!/usr/bin/env python3
"""Checks the Lune support site without a network: every page exists and is well-formed, links resolve,
languages link to each other, and nothing loads from another site except Tally on the feedback pages.
Run from the repository root: python3 tools/check_site.py"""
import os
import re
import sys
from html.parser import HTMLParser

LANGUAGES = {"": "en", "zh-hant/": "zh-Hant", "zh-hans/": "zh-Hans"}
PAGES = ["", "privacy/", "terms/", "feedback/"]
FORM_FILE = "feedback-form.js"
errors = []


def fail(message):
    errors.append(message)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.links = []          # <a href>
        self.resources = []      # (tag, url) that the browser loads by itself
        self.metas = {}
        self.classes = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        for name in (attrs.get("class") or "").split():
            self.classes.add(name)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag in ("script", "img", "iframe", "source", "audio", "video", "embed") and attrs.get("src"):
            self.resources.append((tag, attrs["src"]))
        if tag == "link" and attrs.get("href"):
            self.resources.append((tag, attrs["href"]))
        if tag == "meta":
            key = attrs.get("http-equiv") or attrs.get("name")
            if key:
                self.metas[key.lower()] = attrs.get("content", "")


def check_page(folder, page):
    path = os.path.join(folder + page, "index.html")
    if not os.path.isfile(path):
        fail(f"missing page: {path}")
        return
    text = open(path, encoding="utf-8").read()
    parsed = Page()
    parsed.feed(text)
    language = LANGUAGES[folder]
    if parsed.lang != language:
        fail(f"{path}: <html lang> is {parsed.lang!r}, expected {language!r}")
    if "content-security-policy" not in parsed.metas:
        fail(f"{path}: no Content-Security-Policy")
    if parsed.metas.get("referrer") != "no-referrer":
        fail(f"{path}: no referrer policy")
    is_feedback = page == "feedback/"
    for tag, url in parsed.resources:
        if re.match(r"^(https?:)?//", url):
            fail(f"{path}: loads {url} from another site")
        if tag == "script" and not (is_feedback and url.endswith(FORM_FILE)):
            fail(f"{path}: script {url} (only the feedback pages load {FORM_FILE})")
    if "tally.so" in text and not is_feedback:
        fail(f"{path}: mentions tally.so outside the feedback pages")
    if re.search(r"tally\.so/(embed|r)/\w", text):
        fail(f"{path}: a Tally form ID belongs only in {FORM_FILE}")
    targets = set()
    for href in parsed.links:
        if href.startswith(("mailto:", "https://", "http://", "#")):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), href))
        targets.add(target)
        if not os.path.isfile(os.path.join(target, "index.html") if os.path.isdir(target) else target):
            fail(f"{path}: broken link {href}")
    # Each page links to the same page in every language (its own included).
    for other in LANGUAGES:
        if os.path.normpath(other + page or ".") not in targets:
            fail(f"{path}: no link to {other + page or 'the English home page'}")
    if page == "terms/" and "draft-notice" not in parsed.classes:
        fail(f"{path}: the Terms of Use must say DRAFT until the lawyer's review")
    if is_feedback:
        if "no-health-details" not in parsed.classes:
            fail(f"{path}: must ask for no health details")
        if 'id="feedback-form"' not in text or "form-pending" not in parsed.classes:
            fail(f"{path}: needs the #feedback-form holder with its form-pending note")
    if page == "privacy/" and "Tally" not in text:
        fail(f"{path}: the privacy policy must name Tally")


def check_form_file():
    text = open(FORM_FILE, encoding="utf-8").read()
    if len(re.findall(r'var LUNE_TALLY_FORM_ID = "[^"]*";', text)) != 1:
        fail(f"{FORM_FILE}: expected exactly one LUNE_TALLY_FORM_ID")


def main():
    for folder in LANGUAGES:
        for page in PAGES:
            check_page(folder, page)
    check_form_file()
    for required in ("styles.css", ".nojekyll"):
        if not os.path.isfile(required):
            fail(f"missing {required}")
    form_id = re.search(r'LUNE_TALLY_FORM_ID = "([^"]*)"', open(FORM_FILE, encoding="utf-8").read())
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problem(s)")
    print(f"{len(LANGUAGES) * len(PAGES)} pages OK.")
    if not form_id or not form_id.group(1):
        print(f"Note: {FORM_FILE} has no Tally form ID yet; the feedback pages show their 'not available yet' note.")


if __name__ == "__main__":
    main()
