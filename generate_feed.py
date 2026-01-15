#!/usr/bin/env python3
"""Generate an RSS feed from the Weeklypedia archive."""

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.request import urlopen
from xml.dom import minidom

ARCHIVE_URL = "https://weekly.hatnote.com/archive/en/index.html"
BASE_URL = "https://weekly.hatnote.com/archive/en/"
FEED_TITLE = "Weeklypedia"
FEED_DESCRIPTION = "The most edited Wikipedia articles and discussions from the last week"
FEED_LINK = "https://weekly.hatnote.com/"


def fetch_archive():
    """Fetch the archive index page."""
    with urlopen(ARCHIVE_URL) as response:
        return response.read().decode("utf-8")


def parse_issues(html):
    """Extract issue links and dates from the archive HTML."""
    # Pattern matches links like: <a href="20260109/weeklypedia_20260109.html">January 9, 2026</a>
    pattern = r'<a href="(\d{8}/weeklypedia_\d{8}\.html)">([^<]+)</a>'
    matches = re.findall(pattern, html)

    issues = []
    for path, date_text in matches:
        date_match = re.search(r"(\d{8})", path)
        if date_match:
            date_str = date_match.group(1)
            try:
                pub_date = datetime.strptime(date_str, "%Y%m%d")
                issues.append({
                    "url": BASE_URL + path,
                    "title": f"Weeklypedia - {date_text.strip()}",
                    "date": pub_date,
                    "date_text": date_text.strip(),
                })
            except ValueError:
                continue

    return issues


def generate_rss(issues, max_items=50):
    """Generate RSS 2.0 XML from issue list."""
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = FEED_TITLE
    ET.SubElement(channel, "link").text = FEED_LINK
    ET.SubElement(channel, "description").text = FEED_DESCRIPTION
    ET.SubElement(channel, "language").text = "en"

    if issues:
        last_build = issues[0]["date"].strftime("%a, %d %b %Y 12:00:00 GMT")
        ET.SubElement(channel, "lastBuildDate").text = last_build

    for issue in issues[:max_items]:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = issue["title"]
        ET.SubElement(item, "link").text = issue["url"]
        ET.SubElement(item, "guid").text = issue["url"]
        pub_date = issue["date"].strftime("%a, %d %b %Y 12:00:00 GMT")
        ET.SubElement(item, "pubDate").text = pub_date
        ET.SubElement(item, "description").text = (
            f"Weekly summary of the most edited Wikipedia articles and discussions "
            f"for the week ending {issue['date_text']}."
        )

    # Pretty print
    xml_str = ET.tostring(rss, encoding="unicode")
    dom = minidom.parseString(xml_str)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + dom.documentElement.toprettyxml(indent="  ")


def main():
    print("Fetching Weeklypedia archive...")
    html = fetch_archive()

    print("Parsing issues...")
    issues = parse_issues(html)
    print(f"Found {len(issues)} issues")

    print("Generating RSS feed...")
    rss_xml = generate_rss(issues)

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

    print("Written to feed.xml")


if __name__ == "__main__":
    main()
