#!/usr/bin/env python3
"""Notify Naver of published, changed canonical pages. Defaults to a dry run.

After a successful deployment:
  python scripts/notify-indexnow.py / /preparation.html /report-reading.html --submit

Only submit pages that were actually added or changed. Acceptance is not a
promise of crawling, indexing, or ranking. No automatic retries are performed.
Official protocol: https://searchadvisor.naver.com/guide/indexnow-request
The verification key in dist/ is intentionally public, as IndexNow requires.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", help="Published canonical URLs or paths")
    parser.add_argument("--submit", action="store_true", help="Send one API request")
    parser.add_argument("--receipt", type=Path, help="Save the response receipt locally")
    args = parser.parse_args()

    public = Path(__file__).resolve().parents[1]
    canonical_urls = {
        node.text
        for node in ET.parse(public / "sitemap.xml").findall(
            ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
        )
    }
    urls = list(dict.fromkeys(urllib.parse.urljoin("https://solar.dooja.co.kr/", item) for item in args.urls))
    if any(url not in canonical_urls for url in urls):
        parser.error("Every URL must be a canonical URL already present in the sitemap.")

    keys = [
        path for path in public.glob("*.txt")
        if re.fullmatch(r"[a-fA-F0-9-]{8,128}", path.stem)
        and path.read_text(encoding="utf-8").strip() == path.stem
    ]
    if len(keys) != 1:
        parser.error("Expected exactly one published IndexNow verification file.")

    key = keys[0].stem
    payload = {
        "host": "solar.dooja.co.kr",
        "key": key,
        "keyLocation": f"https://solar.dooja.co.kr/{key}.txt",
        "urlList": urls,
    }
    if not args.submit:
        print(json.dumps({"mode": "dry-run", "urls": urls, "verification_file_ready": True}, ensure_ascii=False))
        return 0

    receipt = {"requested_at": datetime.now(timezone.utc).isoformat(), "urls": urls}
    request = urllib.request.Request(
        "https://searchadvisor.naver.com/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Dooja-Resources-IndexNow/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            receipt.update(http_status=response.status, response=response.read(8192).decode("utf-8", "replace"))
    except urllib.error.HTTPError as error:
        receipt.update(http_status=error.code, response=error.read(8192).decode("utf-8", "replace"))
    except (urllib.error.URLError, TimeoutError) as error:
        receipt.update(http_status=None, error=str(error), note="Request receipt could not be confirmed; do not retry blindly.")

    receipt["accepted"] = receipt["http_status"] in (200, 202)
    receipt["key_verification_pending"] = receipt["http_status"] == 202
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))
    return 0 if receipt["accepted"] else 1


if __name__ == "__main__":
    sys.exit(main())
