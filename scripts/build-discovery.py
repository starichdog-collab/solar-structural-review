#!/usr/bin/env python3
"""Build discovery XML from the three authoritative, already-published HTML pages.

This script never generates or rewrites HTML, images, contacts or application code.
Run from any directory. --check validates the prospective XML without writing it.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta, timezone
from email.utils import format_datetime
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "preparation.html", "report-reading.html")
ORIGIN = "https://solar.dooja.co.kr"
KST = timezone(timedelta(hours=9))
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ATOM_NS = "http://www.w3.org/2005/Atom"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
DROP = {"script", "style", "svg", "button", "input", "select", "option", "textarea", "canvas", "iframe", "object", "embed"}
KEEP = {
    "h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li",
    "dl", "dt", "dd", "blockquote", "table", "caption", "thead", "tbody",
    "tfoot", "tr", "th", "td", "a", "img", "figure", "figcaption", "strong",
    "em", "b", "i", "u", "s", "sub", "sup", "br", "hr", "pre", "code",
    "div", "span", "section", "article", "aside", "small", "details", "summary", "time",
}


@dataclass
class Node:
    tag: str
    attrs: dict[str, str | None] = field(default_factory=dict)
    children: list["Node | str"] = field(default_factory=list)

    def text(self) -> str:
        return "".join(child if isinstance(child, str) else child.text() for child in self.children)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()


class Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def absolute_url(value: str, base: str, *, image=False) -> str | None:
    value = value.strip()
    if not value:
        return None
    result = urljoin(base, value)
    scheme = urlsplit(result).scheme.lower()
    allowed = {"http", "https"} if image else {"http", "https", "mailto", "tel"}
    return result if scheme in allowed else None


def absolute_srcset(value: str, base: str) -> str | None:
    candidates = []
    for candidate in value.split(","):
        fields = candidate.strip().split()
        if not fields or len(fields) > 2:
            continue
        url = absolute_url(fields[0], base, image=True)
        if not url:
            continue
        if len(fields) == 2 and not re.fullmatch(r"(?:\d+w|(?:\d+(?:\.\d+)?|\.\d+)x)", fields[1]):
            continue
        candidates.append(url + (" " + fields[1] if len(fields) == 2 else ""))
    return ", ".join(candidates) or None


def sanitize(node: Node | str, base: str) -> str:
    if isinstance(node, str):
        return escape(node, quote=False)
    if node.tag in DROP:
        return ""
    children = "".join(sanitize(child, base) for child in node.children)
    tag = {"legend": "h3", "label": "span"}.get(node.tag, node.tag)
    # Main/form/fieldset/noscript wrappers add no feed functionality. Keep their text.
    if tag not in KEEP:
        return children
    attrs = {}
    for name in ("id", "title"):
        if node.attrs.get(name):
            attrs[name] = node.attrs[name]
    if tag == "a" and node.attrs.get("href"):
        url = absolute_url(node.attrs["href"], base)
        if url:
            attrs["href"] = url
    if tag == "img":
        url = absolute_url(node.attrs.get("src") or "", base, image=True)
        if not url:
            return ""
        attrs["src"] = url
        attrs["alt"] = node.attrs.get("alt") or ""
        for name in ("width", "height"):
            if (node.attrs.get(name) or "").isdigit():
                attrs[name] = node.attrs[name]
        if node.attrs.get("srcset"):
            srcset = absolute_srcset(node.attrs["srcset"], base)
            if srcset:
                attrs["srcset"] = srcset
    if tag in {"th", "td"}:
        for name in ("colspan", "rowspan"):
            if (node.attrs.get(name) or "").isdigit():
                attrs[name] = node.attrs[name]
        if tag == "th" and node.attrs.get("scope") in {"row", "col", "rowgroup", "colgroup"}:
            attrs["scope"] = node.attrs["scope"]
    if tag == "ol":
        if re.fullmatch(r"-?\d+", node.attrs.get("start") or ""):
            attrs["start"] = node.attrs["start"]
        if "reversed" in node.attrs:
            attrs["reversed"] = "reversed"
    if tag == "time" and node.attrs.get("datetime"):
        attrs["datetime"] = node.attrs["datetime"]
    attr_text = "".join(f' {name}="{escape(str(value), quote=True)}"' for name, value in attrs.items())
    if tag in VOID:
        return f"<{tag}{attr_text}>"
    return f"<{tag}{attr_text}>{children}</{tag}>"


def json_nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from json_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from json_nodes(child)


def parse_date(value: str) -> datetime:
    if len(value) == 10:
        return datetime.combine(datetime.strptime(value, "%Y-%m-%d").date(), time(), KST)
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return result if result.tzinfo else result.replace(tzinfo=KST)


def load_page(filename: str) -> dict:
    doc = Document((ROOT / filename).read_text(encoding="utf-8"))
    nodes = list(doc.root.walk())
    heads = [node for node in nodes if node.tag == "head"]
    assert len(heads) == 1, f"One head required: {filename}"
    head_nodes = list(heads[0].walk())
    titles = [node.text().strip() for node in head_nodes if node.tag == "title"]
    canonical = [node.attrs.get("href") for node in head_nodes if node.tag == "link" and node.attrs.get("rel") == "canonical"]
    descriptions = [node.attrs.get("content") for node in head_nodes if node.tag == "meta" and node.attrs.get("name") == "description"]
    mains = [node for node in nodes if node.tag == "main"]
    assert len(titles) == len(canonical) == len(descriptions) == len(mains) == 1, f"Ambiguous document: {filename}"
    url = canonical[0]
    expected = ORIGIN + ("/" if filename == "index.html" else "/" + filename)
    assert url == expected, f"Unexpected canonical in {filename}: {url}"
    metadata = []
    for node in nodes:
        if node.tag == "script" and node.attrs.get("type") == "application/ld+json":
            metadata.extend(json_nodes(json.loads(node.text())))
    webpages = [item for item in metadata if "WebPage" in ([item.get("@type")] if isinstance(item.get("@type"), str) else (item.get("@type") or [])) and item.get("url") == url]
    assert len(webpages) == 1, f"One authoritative WebPage required: {filename}"
    published = webpages[0]["datePublished"]
    modified = webpages[0]["dateModified"]
    assert parse_date(published) <= parse_date(modified), f"Dates reversed: {filename}"
    body = sanitize(mains[0], url).strip()
    assert len(Document(body).root.text().strip()) > max(300, len(descriptions[0]) * 2), f"Feed only contains an excerpt: {filename}"
    # Every retained URL must be usable when the feed is read away from the site.
    for node in Document(body).root.walk():
        assert node.tag not in DROP | {"header", "footer", "main", "form", "fieldset"}, f"Non-content feed markup in {filename}"
        for attr in ("href", "src"):
            if node.attrs.get(attr):
                assert urlsplit(node.attrs[attr]).scheme in {"http", "https", "mailto", "tel"}, f"Relative {attr}: {filename}"
        if node.attrs.get("srcset"):
            assert all(urlsplit(part.strip().split()[0]).scheme in {"http", "https"} for part in node.attrs["srcset"].split(",")), f"Relative srcset: {filename}"
    return dict(filename=filename, title=titles[0], url=url, excerpt=descriptions[0], published=published, modified=modified, body=body)


def xml_bytes(root: ET.Element) -> bytes:
    ET.indent(root, space="  ")
    data = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    ET.fromstring(data)
    return data


def build() -> tuple[dict[str, bytes], list[dict]]:
    pages = [load_page(name) for name in PAGES]
    assert len({page["url"] for page in pages}) == len(PAGES)
    ET.register_namespace("", SITEMAP_NS)
    ET.register_namespace("atom", ATOM_NS)
    sitemap = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    for page in pages:
        node = ET.SubElement(sitemap, f"{{{SITEMAP_NS}}}url")
        ET.SubElement(node, f"{{{SITEMAP_NS}}}loc").text = page["url"]
        ET.SubElement(node, f"{{{SITEMAP_NS}}}lastmod").text = page["modified"]
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    for name, value in (
        ("title", "두자 태양광 구조검토 자료실"),
        ("link", ORIGIN + "/"),
        ("description", "구조검토 준비자료 정리와 구조계산서 이해를 돕는 두자(Dooja)의 공개 기술자료"),
        ("language", "ko-KR"),
        ("lastBuildDate", format_datetime(max(parse_date(page["modified"]) for page in pages))),
    ):
        ET.SubElement(channel, name).text = value
    ET.SubElement(channel, f"{{{ATOM_NS}}}link", href=ORIGIN + "/feed.xml", rel="self", type="application/rss+xml")
    for page in pages:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = page["title"]
        ET.SubElement(item, "link").text = page["url"]
        ET.SubElement(item, "description").text = page["body"]
        ET.SubElement(item, "pubDate").text = format_datetime(parse_date(page["published"]))
        ET.SubElement(item, "guid", isPermaLink="true").text = page["url"]
    output = {"sitemap.xml": xml_bytes(sitemap), "feed.xml": xml_bytes(rss)}
    assert len(output["feed.xml"]) < 10 * 1024 * 1024, "Feed exceeds Naver's size limit"
    assert len(ET.fromstring(output["sitemap.xml"])) == len(PAGES)
    assert len(ET.fromstring(output["feed.xml"]).findall("./channel/item")) == len(PAGES)
    return output, pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate and report without changing files")
    args = parser.parse_args()
    output, pages = build()
    if not args.check:
        for filename, data in output.items():
            (ROOT / filename).write_bytes(data)
    print(json.dumps({
        "mode": "check" if args.check else "write",
        "pages": len(pages),
        "bytes": {filename: len(data) for filename, data in output.items()},
        "items": [{"url": page["url"], "full_body_characters": len(page["body"]), "published": page["published"], "modified": page["modified"]} for page in pages],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
