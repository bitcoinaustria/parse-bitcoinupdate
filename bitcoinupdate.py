#!/usr/bin/env python
# -*- coding: utf8 -*-
# This short script parses the RSS feed from bitcoinupdate.com and returns a nicely formatted
# block of HTML for the most recent entry.
# 
# Author: Harald Schilly <hsy@bitcoin-austria.at>
# License: Apache 2.0

import requests as req
from dateutil.parser import parse as date_parser
from xml.dom.minidom import parseString as parse_xml

output = r"""
%(title)s
===
%(description)s

[Link zur aktuellen Folge](%(href)s)
"""

rss_url = "http://bitcoinupdate.com/podcast.php"
rss_data = req.get(rss_url)
if rss_data.status_code != 200:
    raise Exception("status code not 200: %s" % rss_data.status_code)

rss = parse_xml(rss_data.text.encode("utf8"))

def get_val(el, what):
    n = el.getElementsByTagName(what)[0]
    return n.childNodes[0].data

most_recent_date = None
title, description, href = None, None, None

items = rss.getElementsByTagName("item")
for item in items:
    pubDate = get_val(item, "pubDate")
    t = get_val(item, "title")
    d = get_val(item, "description")
    h = get_val(item, "link")

    date = date_parser(pubDate)
    if most_recent_date is None or date > most_recent_date:
        title, description, href = t, d, h
        most_recent_date = date

out = (output % locals()).encode('utf-8')
print(out)
