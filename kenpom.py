#!/usr/bin/env python

"""
Scrape KenPom data for quick display.

TODO:
* Decompose the BS `TAG` data into data (eg team.name.text => team.name).
* Documentation of inputs (ALL, comma-delimited, etc)
* Allow for displaying up to N (top 25, 100 etc).
* Provide some kind of configuration object to drive display of columns.
  Probably have a `filter_data` method that takes display config (which
  rows (conf, top 25) and columns (team, rank, W-L, etc) and returns
  appropriate data for display.

"""

from collections import deque, namedtuple
import sys

from bs4 import BeautifulSoup, SoupStrainer
import requests

URL = 'https://kenpom.com/'
DATA_ROW_COL_COUNT = 22
KenPom = namedtuple('KenPom', [
    'Empty', 'rank', 'name', 'conf', 'record', 'eff_margin', 'offense', 'off_rank', 'defense', 'def_rank',
    'tempo', 'tempo_rank', 'luck', 'luck_rank',
    'sos_eff_margin', 'sos_eff_margin_rank', 'sos_off', 'sos_off_rank', 'sos_def', 'sos_def_rank',
    'sos_non_conf', 'sos_non_conf_rank',
])


def fetch_content(url):
    """Fetch the HTML content from the URL."""

    page = requests.get(url)
    if page.status_code == 200:
        return page.content
    else:
        print('Error in getting page')
        sys.exit(1)


def parse_data(html_content):
    """Parse raw HTML into a more useful data structure."""

    soup = BeautifulSoup(html_content, 'html.parser', parse_only=SoupStrainer('tr'))
    data = []
    for row in soup:
        # Consume entire iterator, we'll filter columns later.
        elements = deque(row.children)

        # We're relying on the fact that data-based rows have 22 cols and header rows do not
        if len(elements) != DATA_ROW_COL_COUNT:
            continue
        data.append(KenPom(*elements))

    return data


def filter_data(data, conf):
    """Filter data before we display.

    Currently only filters by conference, may add filtering by Top 25/100,
    columns (config which columnar data is displayed).
    """
    max_name_len = 4
    filtered_data = []
    for team in data:
        if conf == ['ALL'] or team.conf.text in conf:
            curr_team_len = len(team.name.text) + 1
            max_name_len = curr_team_len if curr_team_len > max_name_len else max_name_len
            filtered_data.append(team)

    meta_data = {
        'conf_filter': conf,
        'max_name_len': max_name_len,
        'num_teams': len(filtered_data),
    }
    return filtered_data, meta_data


def write_to_console(data, meta_data):
    """Dump the data to standard out."""

    print()  # provide white-space around output
    show_conf = meta_data['conf_filter'] == ['ALL']
    for team in data:
        print('{team:>{len}} {rank:>5} {record:>6}  {conf}'.format(
            len=meta_data['max_name_len'],
            team=team.name.text.replace('.', ''),  # dot in University St. looks funny in right-justified output
            rank=team.rank.text,
            record=team.record.text,
            conf=team.conf.text if show_conf else ''
        ))
    return data, meta_data


def main():
    """Get args, fetch data, filter data, display data"""
    args = sys.argv[1] if len(sys.argv) == 2 else None
    conferences = args or input('Conference list: ') or 'ALL'
    conferences = [c.upper() for c in conferences.split(',')]
    page_content = fetch_content(URL)
    all_data = parse_data(page_content)
    data, meta_data = filter_data(all_data, conferences)
    write_to_console(data, meta_data)


if __name__ == '__main__':
    main()
