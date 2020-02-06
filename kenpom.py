#!/usr/bin/env python

"""Scrape KenPom data for quick display.

TODO:
* Clean up arg handling, but retain option for user_input on no args
  (essential for easy use in primary use case: iPhone/PyTo).
* Use conf list for input validation? 2) Generate list via an arg (--list)
* Provide configuration object to drive display of columns. We currently
  only show rank, W/L, and conference.
"""

from bs4 import BeautifulSoup, SoupStrainer
from datastructures import (
    KenPom,
    CONF_NAMES,
    SCHOOL_DATA_BY_NAME,
    SCHOOL_DATA_BY_ABBREV,
)
from urllib.parse import unquote_plus
import requests
import sys

URL = "https://kenpom.com/"
NUM_SCHOOLS = 353  # Total number of NCAA D1 schools
DATA_ROW_COL_COUNT = 22  # Number of data elements in tr elements w/ data we want
SHORTEST_SCHOOL_NAME = 4  # Used as starting point to compute width or terminal output


def main():
    """Get args, fetch data, filter data, display data."""
    page_content = fetch_content(URL)
    raw_data, as_of = parse_data(page_content)
    interactive = True
    print("   ", as_of)
    while interactive:
        user_input, interactive = get_args(sys.argv)
        if user_input.lower() in ("q", "quit", "exit"):
            break
        data, meta_data = filter_data(raw_data, user_input)
        write_to_console(data, meta_data)


def get_args(args):
    """Pull args from command-line, or prompt user if no args."""
    if len(args) == 2:
        interactive = False
        user_input = args[1]
    else:
        interactive = True
        user_input = (
            input("    Top `n`, 0 for all, school(s), or conference(s) [25]: ") or "25"
        )

    # Convert All input to our integer equivalent
    if user_input.lower() == "all":
        user_input = "0"
    return user_input, interactive


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
    as_of_html = BeautifulSoup(html_content, "lxml").find_all(class_="update")
    as_of = as_of_html[0].text if as_of_html else ""
    # Remove the total # of games indicator.
    as_of = as_of.split("\n")[0]

    soup = BeautifulSoup(html_content, "lxml", parse_only=SoupStrainer("tr"))
    data = dict()
    for elements in soup:
        # Rely on the fact that relevant rows have distinct, known number of items
        if len(elements) != DATA_ROW_COL_COUNT:
            continue

        # Grab just text vales from our html elements
        text_items = [e.text.strip() for e in elements if hasattr(e, "text")]

        # Replace the trailing period in `Boise St.` so justified text looks better
        text_items[1] = school_name = text_items[1].replace(".", "")

        # Get abbrev to use as data key, allow user to search on this
        school_abbrev = SCHOOL_DATA_BY_NAME[school_name.lower()]["abbrev"]
        text_items.append(school_abbrev.upper())

        data[school_abbrev] = KenPom(*text_items)

    return data, as_of


def _get_filters(user_input):
    """Return filters based on user input.

    This is a brute force not-so-pretty way of handling top-N filters along with
    name-based filters.
    """
    # IF we're filtering by N, we only have one parameter, and it should convert
    # to an int cleanly; otherwise, we're dealing with a list (possibly of 1 item)
    # of strings representing names (conf, school, or abbrev). Normalize that data
    # to lower case and handle some input requirements for spaces.
    try:
        top_filter = int(user_input)
        assert top_filter >= 0, "Top `n` must be zero or greater."
        return [], top_filter
    except ValueError:
        # Normalize the user input from command-line (or `input`)
        user_input = [c.lower() for c in user_input.split(",")]

        # Remove any quotes used in school name input
        user_input = [u.replace('"', "").replace("'", "") for u in user_input]

        # Decode any encoded input (mostly + for space) because sometimes we start
        # typing and don't want to go back and surround input with quotes
        user_input = [unquote_plus(i) for i in user_input]
        return user_input, -1


def filter_data(data, user_input):
    """Filter data for display."""
    names, top_filter = _get_filters(user_input)

    if top_filter == 0:
        filtered_data = data

    elif top_filter > 0:
        filtered_data = {k: v for k, v in data.items() if v.rank <= top_filter}

    elif abbrevs := SCHOOL_DATA_BY_ABBREV.keys() & set(names):
        filtered_data = {k: v for k, v in data.items() if k in abbrevs}

    elif conf_names := CONF_NAMES.intersection(set(names)):
        filtered_data = {k: v for k, v in data.items() if v.conf.lower() in conf_names}

    else:
        filtered_data = {
            k: v for k, v in data.items() for n in names if n in v.name.lower()
        }

    # Keep track of the longest school name. We'll need this to handle
    # right-justified formatting in our console output.
    max_name_len = max({len(v.name) for v in filtered_data.values()})

    meta_data = {
        "max_name_len": max_name_len,
        "names": names,
        "num_teams": len(filtered_data),
        "top_filter": top_filter,
    }
    return filtered_data, meta_data


def write_to_console(data, meta_data):
    """Dump the data to standard out."""
    print()  # provide white-space around output
    for team in list(data.values()):
        print(
            "   {team:>{len}} {rank:>5} {record:>6}  {conf}".format(
                len=meta_data["max_name_len"],
                team=team.name,
                rank=team.rank,
                record=team.record,
                conf=team.conf,
            )
        )
    print()  # provide white-space around output
    return data, meta_data


if __name__ == "__main__":
    main()
