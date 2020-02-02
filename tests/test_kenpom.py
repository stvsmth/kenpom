"""Tests for kenpom scraping, using locally stored data."""

from contextlib import contextmanager
from datastructures import CONF_DATA
from io import StringIO
from kenpom import (
    parse_data,
    filter_data,
    write_to_console,
    NUM_SCHOOLS,
)
from pathlib import Path
import os
import sys

NUM_ACC_TEAMS = len(CONF_DATA["acc"])
NUM_SEC_TEAMS = len(CONF_DATA["sec"])
NUM_TEAMS_W_VALLEY_IN_NAME = 3


def _fetch_test_content():
    """Get a local copy of HTML file.

    We do some path manipulations so the tests can be run via py.test from any
    directory.
    """
    this_dir = Path(__file__).resolve().parent
    test_html_path = os.path.join(this_dir, "test.html")
    with open(test_html_path, "r") as f:
        data = f.read()
        return data


# FIXME: Fixture Me!!!
# Parsing content is REALLY expensive (much more so than reading content)
PARSED_CONTENT = parse_data(_fetch_test_content())


def test_parse_data():
    all_data, as_of = PARSED_CONTENT

    # Quick check to make sure our data is in sync with ranks, if something goes
    # haywire, this test can tell us where in the sequence of schools it went sideways.
    for i in range(NUM_SCHOOLS):
        team = all_data[i]
        assert str(i + 1) == team.rank, team

    # Test both above and below the first "page break". Do a full check of every
    # column on one of these, to ensure we have the correct mappings
    num_40 = all_data[39]
    assert "Northern Iowa" == num_40.name
    assert "40" == num_40.rank

    num_41 = all_data[40]
    assert "41" == num_41.rank
    assert "Florida" == num_41.name
    assert "SEC" == num_41.conf
    assert "13-8" == num_41.record
    assert "+15.42" == num_41.eff_margin
    assert "111.4" == num_41.offense
    assert "30" == num_41.off_rank
    assert "96.0" == num_41.defense
    assert "70" == num_41.def_rank

    assert "65.6" == num_41.tempo
    assert "295" == num_41.tempo_rank
    assert "-.032" == num_41.luck
    assert "243" == num_41.luck_rank

    assert "+7.76" == num_41.sos_eff_margin
    assert "27" == num_41.sos_eff_margin_rank
    assert "106.8" == num_41.sos_off
    assert "15" == num_41.sos_off_rank
    assert "99.1" == num_41.sos_def
    assert "42" == num_41.sos_def_rank

    assert "+5.90" == num_41.sos_non_conf
    assert "35" == num_41.sos_non_conf_rank
    # Not in KenPom, we added when we parsed
    assert "FLA" == num_41.abbrev


def test_filter_data_conf_capitalization():
    all_data, as_of = PARSED_CONTENT
    upper, _ = filter_data(all_data, "meac", as_of)
    lower, _ = filter_data(all_data, "MEAC", as_of)
    mixed, _ = filter_data(all_data, "Meac", as_of)
    assert upper == lower == mixed


def test_filter_handles_top_n():

    # Be sure this we work on double-digit numbers, otherwise
    # There's a subtle logic bug that could end up printing 2 teams
    # instead of 25. Strings being iterable and all that.
    all_data, as_of = PARSED_CONTENT

    data, _ = filter_data(all_data, "0", as_of)
    assert len(data) == NUM_SCHOOLS

    data, _ = filter_data(all_data, "1", as_of)
    assert len(data) == 1

    data, _ = filter_data(all_data, "7", as_of)
    assert len(data) == 7

    data, _ = filter_data(all_data, "25", as_of)
    assert len(data) == 25

    data, _ = filter_data(all_data, "111", as_of)
    assert len(data) == 111


def test_filter_data_ensure_abbrev_superiority():
    all_data, as_of = PARSED_CONTENT

    data, _ = filter_data(all_data, "utah", as_of)
    assert len(data) == 1

    data, _ = filter_data(all_data, "amer", as_of)
    assert len(data) == 1


def test_filter_data_school_by_name():
    all_data, as_of = PARSED_CONTENT
    data, _ = filter_data(all_data, "valley", as_of)

    assert len(data) == NUM_TEAMS_W_VALLEY_IN_NAME
    names = [x.name for x in data]
    assert "Utah Valley" in names
    assert "UT Rio Grande Valley" in names
    assert "Mississippi Valley St" in names

    # Check for multiple names input
    data, _ = filter_data(all_data, "wyoming,wofford", as_of)
    assert len(data) == 2
    assert data[0].name == "Wofford"
    assert data[1].name == "Wyoming"

    # Check for quoting (single and double) and url encoding
    data, _ = filter_data(all_data, "'Virginia Tech'", as_of)
    assert len(data) == 1
    assert data[0].name == "Virginia Tech"

    data, _ = filter_data(all_data, '"Virginia Tech"', as_of)
    assert len(data) == 1
    assert data[0].name == "Virginia Tech"

    data, _ = filter_data(all_data, "virginia+tech", as_of)
    assert len(data) == 1
    assert data[0].name == "Virginia Tech"


def test_filter_data_abbrev_vs_name():
    all_data, as_of = PARSED_CONTENT
    data, _ = filter_data(all_data, "mich,msu", as_of)
    assert len(data) == 2


def test_filter_data_school_abbrevs():
    all_data, as_of = PARSED_CONTENT
    data, _ = filter_data(all_data, "vt,wof", as_of)

    assert len(data) == 2
    assert data[0].name == "Virginia Tech"
    assert data[1].name == "Wofford"

    data, _ = filter_data(all_data, "VT,WOF", as_of)
    assert len(data) == 2
    assert data[0].name == "Virginia Tech"
    assert data[1].name == "Wofford"

    data, _ = filter_data(all_data, "Vt,Wof", as_of)
    assert len(data) == 2
    assert data[0].name == "Virginia Tech"
    assert data[1].name == "Wofford"


def test_write_to_console_all():
    all_data, as_of = PARSED_CONTENT

    data, meta_data = filter_data(all_data, "0", as_of)

    # Grab just # 4 for cleaner diff on test failure.
    data = data[3:4]
    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    text_without_footer = out_text.split("\n")[1]
    assert "San Diego St     4   23-0  MWC" in text_without_footer


def test_write_to_console_top_5():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "5", as_of)

    assert len(data) == 5
    assert data[1].name == "Duke"
    assert data[4].name == "Gonzaga"

    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    assert "San Diego St     4   23-0  MWC" in out_text


def test_write_to_console_multi_conference():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "ACC,SEC", as_of)

    assert len(data) == NUM_SEC_TEAMS + NUM_ACC_TEAMS
    assert data[16].name == "South Carolina"
    assert data[19].name == "Clemson"
    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    assert "Duke     2   18-3  ACC" in out_text


def test_write_to_console_basic_conference():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "acc", as_of)

    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    acc_teams = out_text.strip().split("\n")
    # There are 15 teams in the ACC, plus two lines for the as_of data
    assert NUM_ACC_TEAMS + 2 == len(acc_teams), "Conference filter broken"

    # Check formatting, values, be sure to test team > #20
    # so we know that we're bypassing the intermittent headers
    # include longest (NCST) and short team names (Duke), which
    # define width of output.

    assert "           Duke     2   18-3" in out_text
    assert "     Louisville     8   19-3" in out_text
    assert "     Florida St    18   18-3" in out_text
    assert "       Syracuse    53   13-9" in out_text
    assert "       Virginia    54   14-6" in out_text
    assert "     Notre Dame    57   13-8" in out_text
    assert "       NC State    70   14-8" in out_text
    assert "     Pittsburgh    79   13-8" in out_text
    assert "  Virginia Tech    84   14-8" in out_text
    assert "   Georgia Tech    91  10-12" in out_text
    assert "        Clemson    95  11-10" in out_text
    assert " North Carolina    97  10-11" in out_text
    assert "    Wake Forest   104  10-11" in out_text
    assert "       Miami FL   117   11-9" in out_text
    assert " Boston College   162  11-11" in out_text

    assert "Data through games of Saturday, February 1" in out_text


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
