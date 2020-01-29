#!/usr/bin/env python

"""Scrape KenPom data for quick display.

TODO:
* Provide some kind of configuration object to drive display of columns.
  Probably have a `filter_data` method that takes display config (which
  rows (conf, top 25) and columns (team, rank, W-L, etc) and returns
  appropriate data for display.
"""

from collections import deque, namedtuple
import sys

from bs4 import BeautifulSoup, SoupStrainer
import requests

URL = "https://kenpom.com/"
DATA_ROW_COL_COUNT = 22
KenPom = namedtuple(
    "KenPom",
    [
        "rank",
        "name",
        "conf",
        "record",
        "eff_margin",
        "offense",
        "off_rank",
        "defense",
        "def_rank",
        "tempo",
        "tempo_rank",
        "luck",
        "luck_rank",
        "sos_eff_margin",
        "sos_eff_margin_rank",
        "sos_off",
        "sos_off_rank",
        "sos_def",
        "sos_def_rank",
        "sos_non_conf",
        "sos_non_conf_rank",
    ],
)


def main():
    """Get args, fetch data, filter data, display data."""

    args = sys.argv[1] if len(sys.argv) == 2 else None
    conferences = args or input("Top `n` or conference list: ") or "ALL"
    conferences = conferences.split(",")
    page_content = fetch_content(URL)
    all_data, as_of = parse_data(page_content)
    data, meta_data = filter_data(all_data, conferences, as_of)
    write_to_console(data, meta_data)


def fetch_content(url):
    """Fetch the HTML content from the URL."""

    page = requests.get(url)
    if page.status_code == 200:
        return page.content
    else:
        print("Error in getting page")
        sys.exit(1)


def parse_data(html_content):
    """Parse raw HTML into a more useful data structure.

    Note: The parse data currently returns all strings. For now we're just ingesting
    the data and printing in different format(s). At some point in the future we may
    type the data, such that the `rank` data item is an integer, the efficiency
    margin data is float, etc.
    """

    as_of_html = BeautifulSoup(html_content, "html.parser").find_all(class_="update")
    as_of = as_of_html[0].text if as_of_html else ""

    soup = BeautifulSoup(html_content, "html.parser", parse_only=SoupStrainer("tr"))
    data = []
    for row in soup:
        # Consume entire iterator, we'll filter columns later.
        elements = deque(row.children)

        # Rely on the fact that data-based rows have 22 cols and header rows do not
        if len(elements) != DATA_ROW_COL_COUNT:
            continue
        # Note, we strip out any "blank" column as well (such as the first column)
        elements = [e.text for e in elements if hasattr(e, "text")]
        data.append(KenPom(*elements))

    return data, as_of


def _get_filters(conf):
    """Return filters based on user input.

    This is a brute force not-so-pretty way of handling
    top-N filters along with conference-based filters.

    We'll clean this up in the future.
    """

    conf = [c.upper() for c in conf]
    try:
        top_filter = int(conf[0])
        do_all = False
        assert top_filter >= 1, "Must use a positive integer"
    except ValueError:
        top_filter = None
        do_all = True if conf[0] == "ALL" else False

    return conf, top_filter, do_all


def filter_data(data, conf, as_of):
    """Filter data before we display.

    Currently only filters by conference, may add filtering by Top 25/100,
    columns (config which columnar data is displayed).
    """

    conf, top_filter, do_all = _get_filters(conf)
    max_name_len = 4
    filtered_data = []

    for team in data:
        if do_all or top_filter or team.conf.upper() in conf:
            curr_team_len = len(team.name) + 1
            max_name_len = (
                curr_team_len if curr_team_len > max_name_len else max_name_len
            )
            filtered_data.append(team)

            if len(filtered_data) == top_filter:
                break
    show_conf = True if len(conf) > 1 or top_filter is not None else False
    meta_data = {
        "as_of": as_of,
        "conf_filter": conf,
        "max_name_len": max_name_len,
        "num_teams": len(filtered_data),
        "show_conf": show_conf,
        "top_filter": top_filter,
    }
    return filtered_data, meta_data


def write_to_console(data, meta_data):
    """Dump the data to standard out."""

    print()  # provide white-space around output
    for team in data:
        print(
            "{team:>{len}} {rank:>5} {record:>6}  {conf}".format(
                len=meta_data["max_name_len"],
                team=team.name.replace(
                    ".", ""
                ),  # dot in North Carolina St. looks funny in right-justified output
                rank=team.rank,
                record=team.record,
                conf=team.conf if meta_data["show_conf"] else "",
            )
        )
    print()  # provide white-space around output
    print(meta_data["as_of"])
    return data, meta_data


if __name__ == "__main__":
    main()
