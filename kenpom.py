#!/usr/bin/env python

"""Scrape KenPom data for quick display.

TODO:
* Clean up arg handling, but retain option for user_input on no args
  (essential for easy use in primary use case: iPhone/Pythonista).
* Use conf list for input validation? 2) Generate list via an arg (--list)
* Provide configuration object to drive display of columns. We currently
  only show rank, W/L, and (sometimes) conference.
"""

from bs4 import BeautifulSoup, SoupStrainer
from const import KenPom, CONF_LIST
from urllib.parse import unquote_plus
import requests
import sys

URL = "https://kenpom.com/"
NUM_SCHOOLS = 353  # Total number of NCAA D1 schools
DATA_ROW_COL_COUNT = 22  # Number of data elements in tr elements w/ data we want
SHORTEST_SCHOOL_NAME = 4  # Used as starting point to compute width or terminal output


def main():
    """Get args, fetch data, filter data, display data."""
    while True:
        try:
            user_input = get_args(sys.argv)
            if user_input.lower() in ("q", "quit", "exit"):
                break
            page_content = fetch_content(URL)
            raw_data, as_of = parse_data(page_content)
            data, meta_data = filter_data(raw_data, user_input, as_of)
            write_to_console(data, meta_data)
        except KeyboardInterrupt:
            pass


def get_args(args):
    """Pull args from command-line, or prompt user if no args."""
    if len(args) == 2:
        return args[1]
    else:
        return input("Top `n`, 0 for all, school(s), or conference(s) [25]: ") or "25"


def fetch_content(url):
    """Fetch the HTML content from the URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.content


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
    for elements in soup:
        # Rely on the fact that relevant rows have 22 cols and other tr elements don't
        if len(elements) != DATA_ROW_COL_COUNT:
            continue
        # Note, we strip out any "blank" column as well (such as the first column)
        elements = [e.text for e in elements if hasattr(e, "text")]
        data.append(KenPom(*elements))

    return data, as_of


def _get_filters(user_input):
    """Return filters based on user input.

    This is a brute force not-so-pretty way of handling top-N filters along with
    name-based filters. There are probably all kinds of input that could cause
    issues. But I'm the only user right now.
    """
    # IF we're filtering by N, we only have one parameter, and it should convert
    # to an int cleanly; otherwise, we're dealing with a list (possibly of 1 item)
    # of conference codes (acc,sec) or (possibly partial) school names (vil,kans)
    try:
        top_filter = int(user_input)
        assert top_filter >= 0, "Top `n` must be zero or greater."
        return [], top_filter
    except ValueError:
        # Normalize the user input from command-line (or `input`)
        user_input = [c.upper() for c in user_input.split(",")]

        # Remove any quotes used in school name input
        user_input = [u.replace('"', "").replace("'", "") for u in user_input]

        # Decode any encoded input (mostly + for space) because sometimes we start
        # typing and don't want to go back and surround input with quotes
        user_input = [unquote_plus(i) for i in user_input]
        return user_input, -1


def filter_data(data, user_input, as_of):
    """Filter data before we display."""
    filtered_data = []
    names, top_filter = _get_filters(user_input)

    # Keep track of the longest school name. We'll need this to handle
    # right-justified formatting in our console output.
    max_name_len = SHORTEST_SCHOOL_NAME

    is_top_search = top_filter >= 0
    is_conf_search = CONF_LIST.intersection(set(names))
    is_name_search = not is_top_search and not is_conf_search

    for team in data:
        if is_conf_search:
            is_included = team.conf.upper() in names
        elif is_name_search:
            is_included = any([n in team.name.upper() for n in names])
        else:
            is_included = False

        if is_top_search or is_included:
            curr_team_len = len(team.name) + 1
            max_name_len = (
                curr_team_len if curr_team_len > max_name_len else max_name_len
            )
            filtered_data.append(team)

            if len(filtered_data) == top_filter:
                break

    show_conf = any([is_top_search, is_name_search, is_conf_search and len(names) > 1])
    meta_data = {
        "as_of": as_of,
        "name_filter": names,  # not currently used, but I think we want it
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
                ),  # dot in Florida St. looks funny in right-justified output
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
