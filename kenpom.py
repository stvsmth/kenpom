#!/usr/bin/env python

"""Scrape KenPom data for quick display.

TODO:
* Clean up arg handling, but retain option for user_input on no args
  (essential for easy use in primary use case: iPhone/PyTo).
* Use conf list for input validation? Maybe generate list via an arg (--list).
* Provide configuration object to drive display of columns. We currently
  only show rank, W/L, and conference.
"""
from bs4 import BeautifulSoup, SoupStrainer
from cachetools import cached, TTLCache
from datastructures import (
    KenPom,
    KenPomDict,
    MetaData,
    CONF_NAMES,
    SCHOOL_DATA_BY_NAME,
    SCHOOL_DATA_BY_ALIAS,
)
from typing import List, Tuple
from urllib.parse import unquote_plus
import requests
import sys

URL = "https://kenpom.com/"
NUM_SCHOOLS = 353  # Total number of NCAA D1 schools
DATA_ROW_COL_COUNT = 22  # Number of data elements in tr elements w/ data we want
SHORTEST_SCHOOL_NAME = 4  # Used as starting point to compute width of terminal output


def main():
    """Get args, fetch data, filter data, display data."""
    interactive = True
    while interactive:
        as_of, raw_data = fetch_and_parse_data()
        user_input, interactive = get_args(sys.argv)
        if user_input.lower() in ("q", "quit", "exit"):
            break
        data, meta_data = filter_data(raw_data, user_input)
        write_to_console(data, meta_data, as_of)


@cached(cache=TTLCache(maxsize=20000, ttl=600))
def fetch_and_parse_data():
    """Convenience method that allows us to cache results.

    Caching the results allow us to let a long-running process (such as PyTo on
    the phone) get relatively up-to-date results. Note that as of 2020-02-07 the
    total size of raw data was 18500 bytes, so we may need to double-check this
    after each season to ensure Kenpom hasn't dumped more data.
    """
    page_content = fetch_content(URL)
    raw_data, as_of = parse_data(page_content)
    return as_of, raw_data


def get_args(args: List[str]) -> Tuple[str, bool]:
    """Pull args from command-line, or prompt user if no args."""
    if len(args) == 2:
        interactive = False
        user_input = args[1]
    else:
        interactive = True
        user_input = (
            input("\nTop `n`, code(s), conference(s), or schools(s) [25]: ") or "25"
        )

    # Convert All input to our integer equivalent
    if user_input.lower() == "all":
        user_input = "0"
    return user_input, interactive


def fetch_content(url: str) -> str:
    """Fetch the HTML content from the URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode("utf-8")


def parse_data(html_content: str) -> Tuple[KenPomDict, str]:
    """Parse raw HTML into a more useful data structure.

    Note: The parse data currently returns all strings. For now we're just ingesting
    the data and printing in different format(s). At some point in the future we may
    type the data, such that the `rank` data item is an integer, the efficiency
    margin data is float, etc.
    """
    as_of_html = BeautifulSoup(html_content, "lxml").find_all(class_="update")
    as_of = as_of_html[0].text.strip() if as_of_html else ""

    # Join the total # of games line onto the date line.
    as_of = as_of.replace("\n", " ")

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

        # Get alias to use as data key, allow user to search on this
        school_alias = SCHOOL_DATA_BY_NAME[school_name.lower()]["alias"]
        text_items.append(school_alias.upper())

        data[school_alias] = KenPom(*text_items)

    return data, as_of


def _get_filters(user_input: str) -> Tuple[List[str], int]:
    """Return filters based on user input.

    This is a brute force not-so-pretty way of handling top-N filters along with
    name-based filters.
    """
    # IF we're filtering by N, we only have one parameter, and it should convert
    # to an int cleanly; otherwise, we're dealing with a list (possibly of 1 item)
    # of strings representing names (conf, school, or alias). Normalize that data
    # to lower case and handle some input requirements for spaces.
    try:
        top_filter = int(user_input)
        assert top_filter >= 0, "Top `n` must be zero or greater."
        return [], top_filter
    except ValueError:
        # Normalize the user input from command-line (or `input`)
        input_as_list = [c.lower() for c in user_input.split(",")]

        # Remove any quotes used in school name input
        input_as_list = [u.replace('"', "").replace("'", "") for u in input_as_list]

        # Decode any encoded input (mostly + for space) because sometimes we start
        # typing and don't want to go back and surround input with quotes
        input_as_list = [unquote_plus(i) for i in input_as_list]
        return input_as_list, -1


def filter_data(data: KenPomDict, user_input: str) -> Tuple[KenPomDict, MetaData]:
    """Filter data for display."""
    names, top_filter = _get_filters(user_input)

    if top_filter == 0:
        filtered_data = data

    elif top_filter > 0:
        filtered_data = {k: v for k, v in data.items() if v.rank <= top_filter}

    elif aliases := SCHOOL_DATA_BY_ALIAS.keys() & set(names):
        filtered_data = {k: v for k, v in data.items() if k in aliases}

    elif conf_names := CONF_NAMES.intersection(set(names)):
        filtered_data = {k: v for k, v in data.items() if v.conf.lower() in conf_names}

    else:
        filtered_data = {
            k: v for k, v in data.items() for n in names if n in v.name.lower()
        }

    # Keep track of the longest school name. We'll need this to handle
    # right-justified formatting in our console output.
    max_name_len = (
        max({len(v.name) for v in filtered_data.values()}) if filtered_data else 0
    )

    meta_data = {
        "max_name_len": max_name_len,
        "names": names,
        "num_teams": len(filtered_data),
        "top_filter": top_filter,
    }
    return filtered_data, meta_data


def write_to_console(
    data: KenPomDict, meta: MetaData, as_of: str
) -> Tuple[KenPomDict, MetaData]:
    """Dump the data to standard out."""
    print()  # provide white-space around output
    for team in list(data.values()):
        print(
            "{team:>{len}}  {alias:>5} {rank:>5} {record:>6}  {conf}".format(
                len=meta["max_name_len"],
                alias=team.alias,
                team=team.name,
                rank=team.rank,
                record=team.record,
                conf=team.conf,
            )
        )
    print("\n", as_of, "\n")
    return data, meta


if __name__ == "__main__":
    main()
