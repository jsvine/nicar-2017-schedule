#!/usr/bin/env python
import requests
import lxml.html
import itertools
from collections import OrderedDict
import argparse
import json
import csv
import sys
import re

SCHEDULE_URL = "https://ire.org/conferences/nicar2017/schedule/"
DATES = [
    "2017-03-01",
    "2017-03-02",
    "2017-03-03",
    "2017-03-04",
    "2017-03-05"
]

def extract_speakers(description):
    """
    If speakers are listed in the first paragraph of the description,
    extract them.
    """
    speaker_pat = re.compile(r"^(Speakers?: ([^\n]+))?(.*)$", re.DOTALL)
    match = re.match(speaker_pat, description)
    graf, names, rest = match.groups()
    return names, rest.strip()

def convert_time(ts):
    """
    Convert IRE time string (e.g., "12:30 p.m.", "8 a.m.") to 24-hour time. Assmes that nothing's happening between midnight and 1am.
    """
    nums, suffix = ts.split(" ")
    if suffix == "p.m.":
        is_pm = True
    elif suffix == "a.m.":
        is_pm = False
    else:
        raise ValueError("Can't parse " + ts)
    if nums.count(":") == 0:
        nums += ":00"
    hours, minutes = list(map(int, nums.split(":")))
    hours += (is_pm and hours != 12) * 12
    return "{0:02d}:{1:02d}".format(hours, minutes)

def calculate_length(start, end):
    s_hours, s_mins = list(map(int, start.split(":")))
    e_hours, e_mins = list(map(int, end.split(":")))
    return (((e_hours * 60) + e_mins) - ((s_hours * 60) + s_mins)) / 60

def parse_session(el, date):
    """
    Given an HTML element containing one session and the date of the session,
    extract the key information.
    """
    s_type = el.cssselect(".col-10")[0].text_content().strip()
    s_title = el.cssselect(".title3")[0].text_content().strip()
    s_href = el.cssselect(".title3 a")[0].attrib["href"]
    s_id = "/".join(s_href.split("/")[-3:-1])
    grafs = el.cssselect(".col-60 p")
    s_desc = "\n\n".join(p.text_content().strip() for p in grafs).strip()
    s_desc_compact = re.sub(r"\n\n+", "\n\n", s_desc)
    s_speakers, s_description = extract_speakers(s_desc_compact)
    details = el.cssselect(".meta p")
    s_room, s_time = (p.text_content().strip() for p in details)
    time_start, time_end = map(convert_time, s_time.split(" - "))
    return OrderedDict([
        ("title", s_title),
        ("type", s_type),
        ("description", s_description),
        ("speakers", s_speakers),
        ("date", date),
        ("time_start", time_start),
        ("time_end", time_end),
        ("length_in_hours", round(calculate_length(time_start, time_end), 3)),
        ("room", s_room),
        ("event_id", s_id),
        ("event_url", "https://ire.org" + s_href),
    ])
    
def parse_day(el, date):
    """
    Given an HTML element containing a day's worth of sessions,
    pass each session element to the parser and return the results.
    """
    session_els = list(el)
    sessions_data = [ parse_session(s, date) for s in session_els ]
    return sessions_data

def fix_encoding(string):
    """
    Fix embedded utf-8 bytestrings.
    Solution via http://bit.ly/1DEpdmQ
    """
    pat = r"[\xc2-\xf4][\x80-\xbf]+"
    fix = lambda m: m.group(0).encode("latin-1").decode("utf-8")
    return re.sub(pat, fix, string.decode("utf-8"))

def get_sessions():
    """
    Fetch and parse the schedule HTML from the NICAR webpage.
    """
    html = fix_encoding(requests.get(SCHEDULE_URL).content)
    dom = lxml.html.fromstring(html)
    day_els = dom.cssselect("ul.listview.pane")
    days_zipped = zip(day_els, DATES)
    sessions_nested = [ parse_day(el, date) for el, date in days_zipped ]
    sessions = list(itertools.chain.from_iterable(sessions_nested))
    return sessions

def main():
    """
    Get the data and print it.
    """
    sessions = get_sessions()
    json.dump(sessions, sys.stdout, indent=4)

if __name__ == "__main__":
    main()
