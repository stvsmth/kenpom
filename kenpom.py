#!/usr/bin/env python

"""Scrape KenPom data for quick display.

TODO:
* Use conf list for input validation? Maybe generate list via an arg (--conf-list).
* Provide configuration object to drive display of columns? Default list is
  pretty useful (lacks, tempo, luck, SOS).
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
import argparse
import requests

URL = "https://kenpom.com/"
NUM_SCHOOLS = 357  # Total number of NCAA D1 schools
DATA_ROW_COL_COUNT = 22  # Number of data elements in tr elements w/ data we want
HEADER_LEN = 37  # Number of `-` chars to print underneath the output header text
CACHE_IN_SECS = 600


def main():
    """Get args, fetch data, filter data, display data."""
    args = parse_args()
    user_input = args or get_input(args.indent)

    if args.filter:
        user_input = args.filter

    while user_input not in ("q", "quit", "exit"):
        as_of, raw_data = fetch_and_parse_data()
        data, meta_data = filter_data(raw_data, user_input)
        write_to_console(data, meta_data, as_of, args.indent)
        user_input = "quit" if not args.filter else get_input(args.indent)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.usage = f"""
    List, in KenPom ranked order, Division 1 men's college basketball
    teams given some filter. Filters include top-n teams, conference,
    team name, team alias (aka ESPN ticker symbol).

    If no filter is provided, the program will go into a loop prompting
    you for a new filter after each run. While running with in the loop
    we only update data about every {CACHE_IN_SECS // 60} minutes.

    Example filters:
    7        List top 7 teams
    acc,sec  List all teams from the ACC and SEC conferences
    vt,woff  Compare teams by alias: Virginia Tech and Wofford
    Valley   List all teams with `valley` in the school name

    School names with spaces in them can be quoted or use the + sign in
    lieu of a space. That is, both of the following will work.

      "virginia tech",wofford
      virginia+tech, wofford"""

    parser.add_argument(
        dest="filter",
        nargs="?",
        default="25",
        help="one or more (comma-separated) search terms, defaults to 25",
    )
    parser.add_argument(
        "--indent",
        type=int,
        metavar="N",
        default=0,
        help="offset console input by `N` spaces",
    )

    return parser.parse_args()


@cached(cache=TTLCache(maxsize=20000, ttl=CACHE_IN_SECS))
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


def get_input(indent: int) -> str:
    """Pull args from command-line, or prompt user if no args.

    Keep the user input as a string, we'll type it later.
    """
    left_pad = indent * " " if indent else ""
    user_input = (
        input(f"\n{left_pad}Top `n`, code(s), conference(s), or school(s) [25]: ")
        or "25"
    )

    # Convert All input to our numerical/str equivalent
    user_input = user_input.lower()
    if user_input == "all":
        user_input = "0"
    return user_input


def fetch_content(url: str) -> str:
    """Fetch the HTML content from the URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode("utf-8")


def parse_data(html_content: str) -> Tuple[KenPomDict, str]:
    """Parse raw HTML into a more useful data structure.

    We also append one data item: `alias`. This allows us to search by the oft-
    used school alias (KU, UK, UMBC, aka score ticker symbol).
    """
    as_of_html = BeautifulSoup(html_content, "lxml").find_all(class_="update")
    as_of = as_of_html[0].text.strip() if as_of_html else ""

    # Join the total # of games and date info onto one line.
    as_of = as_of.replace("\n", " ")

    soup = BeautifulSoup(html_content, "lxml", parse_only=SoupStrainer("tr"))
    data = dict()
    for elements in soup:
        # Rely on the fact that relevant rows have distinct, known number of items
        if len(elements) != DATA_ROW_COL_COUNT:
            continue

        # Grab just text vales from our html elements
        text_items = [e.text.strip() for e in elements if hasattr(e, "text")]

        # Replace the trailing dot in `Boise St.` so right-justified text looks better
        text_items[1] = school_name = text_items[1].replace(".", "")

        # Get alias to use as data key, allow user to search on this
        school_alias = SCHOOL_DATA_BY_NAME[school_name.lower()]["alias"]
        text_items.append(school_alias.upper())

        data[school_alias] = KenPom(*text_items)

    return data, as_of


def _get_filters(user_input: str) -> Tuple[List[str], int]:
    """Return filters based on user input.

    This is an ugly way of handling top-N filters vs. name-based filters. Will
    eventually clean this up, but haven't needed to change it so far.
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
    """Filter which schools we will display based on user input."""
    names, top_filter = _get_filters(user_input)

    if top_filter == 0:
        filtered_data = data

    elif top_filter > 0:
        filtered_data = {k: v for k, v in data.items() if v.rank <= top_filter}

    elif aliases := SCHOOL_DATA_BY_ALIAS.keys() & set(names):
        filtered_data = {k: v for k, v in data.items() if k in aliases}

    elif conf_names := CONF_NAMES.intersection(set(names)):
        filtered_data = {k: v for k, v in data.items() if v.conf.lower() in conf_names}

    else:  # full school name
        filtered_data = {
            k: v for k, v in data.items() for n in names if n in v.name.lower()
        }

    # Keep track of the longest school name. We'll need this to handle
    # right-justified formatting in our console output. If there's no
    # filtered_data then we have bogus input, so we need to guard against
    # the evil `None` rearing its ugly head.
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
    data: KenPomDict, meta: MetaData, as_of: str, indent: int = 0
) -> Tuple[KenPomDict, MetaData]:
    """Dump the data to standard out."""

    left_pad = indent * " " if indent else ""
    str_template = (
        "{left_pad}{team:>{len}}  {alias:>5} {rank:>5}  {off_rank:>3} /{def_rank:>4} "
        "{record:>6} {conf:>5}"
    )
    # Header text ...
    print(
        str_template.format(
            len=meta["max_name_len"],
            left_pad=left_pad,
            alias="Code",
            team="Team",
            rank="Rank",
            off_rank="Off",
            def_rank="Def",
            record="Rec",
            conf="Conf",
        )
    )
    # -----------------------------------
    print(left_pad + (meta["max_name_len"] + HEADER_LEN) * "-")

    # Data ...
    for team in list(data.values()):
        print(
            str_template.format(
                len=meta["max_name_len"],
                left_pad=left_pad,
                alias=team.alias,
                team=team.name,
                rank=team.rank,
                off_rank=team.off_rank,
                def_rank=team.def_rank,
                record=team.record,
                conf=team.conf,
            )
        )
    # Footer (as of date)
    print(f"\n{left_pad}{as_of}\n")

    return data, meta


if __name__ == "__main__":
    main()
