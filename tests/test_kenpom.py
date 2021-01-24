"""Tests for kenpom scraping, using locally stored data.

We consume many dict_values via list in these tests. It just feels wrong to use
a test for positioning using keyed entries. I know dicts are ordered these days,
but it still feels funny to rely on that, especially in tests.
"""

from contextlib import contextmanager
from io import StringIO
from kenpom import parse_data, filter_data, write_to_console, NUM_SCHOOLS, get_args
from pathlib import Path
import os
import sys

NUM_ACC_TEAMS = 15
NUM_SEC_TEAMS = 14
NUM_TEAMS_W_VALLEY_IN_NAME = 3
NUM_HEADER_LINES = 1
NUM_FOOTER_LINES = 4


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


PARSED_CONTENT = parse_data(_fetch_test_content())


def test_parse_data():
    all_data, as_of = PARSED_CONTENT

    # Quick check to make sure our data is in sync with ranks, if something goes
    # haywire, this test can tell us where in the sequence of schools it went sideways.
    values = list(all_data.values())
    for i, team in zip(range(NUM_SCHOOLS), values):
        assert i + 1 == team.rank

    # Test both above and below the first "page break". Do a full check of every
    # column on one of these to ensure we have the correct mappings
    all_data = list(all_data.values())
    num_40 = all_data[39]
    assert "LSU" == num_40.name
    assert 40 == num_40.rank

    num_41 = all_data[40]
    assert 41 == num_41.rank
    assert "Rutgers" == num_41.name
    assert "B10" == num_41.conf
    assert "8-6" == num_41.record
    assert 16.86 == num_41.eff_margin
    assert 110.1 == num_41.offense
    assert 55 == num_41.off_rank
    assert 93.3 == num_41.defense
    assert 40 == num_41.def_rank

    assert 69.2 == num_41.tempo
    assert 167 == num_41.tempo_rank
    assert 0.013 == num_41.luck
    assert 155 == num_41.luck_rank

    assert 15.14 == num_41.sos_eff_margin
    assert 5 == num_41.sos_eff_margin_rank
    assert 111.8 == num_41.sos_off
    assert 2 == num_41.sos_off_rank
    assert 96.7 == num_41.sos_def
    assert 30 == num_41.sos_def_rank

    assert -6.45 == num_41.sos_non_conf
    assert 278 == num_41.sos_non_conf_rank
    # Not in KenPom, we added when we parsed
    assert "RUTG" == num_41.alias


def test_filter_data_conf_capitalization():
    all_data, as_of = PARSED_CONTENT
    upper, _ = filter_data(all_data, "meac")
    lower, _ = filter_data(all_data, "MEAC")
    mixed, _ = filter_data(all_data, "Meac")
    assert upper == lower == mixed


def test_filter_handles_top_n():

    # Be sure this we work on double-digit numbers, otherwise
    # There's a subtle logic bug that could end up printing 2 teams
    # instead of 25. Strings being iterable and all that.
    all_data, as_of = PARSED_CONTENT

    # data, _ = filter_data(all_data, "0")
    # assert len(data) == NUM_SCHOOLS

    data, _ = filter_data(all_data, "1")
    assert len(data) == 1

    data, _ = filter_data(all_data, "7")
    assert len(data) == 7

    data, _ = filter_data(all_data, "25")
    assert len(data) == 25

    data, _ = filter_data(all_data, "111")
    assert len(data) == 111


def test_filter_data_ensure_alias_superiority():
    all_data, as_of = PARSED_CONTENT

    data, _ = filter_data(all_data, "utah")
    assert len(data) == 1

    data, _ = filter_data(all_data, "amer")
    assert len(data) == 1


def test_bogus_input():
    all_data, as_of = PARSED_CONTENT

    data, _ = filter_data(all_data, "foobar")
    assert len(data) == 0


def test_filter_data_school_by_name():
    all_data, as_of = PARSED_CONTENT
    data, _ = filter_data(all_data, "valley")

    assert len(data) == NUM_TEAMS_W_VALLEY_IN_NAME
    names = [x.name for x in list(data.values())]
    assert "Utah Valley" in names
    assert "UT Rio Grande Valley" in names
    assert "Mississippi Valley St" in names

    # Check for multiple names input
    data, _ = filter_data(all_data, "wyoming,wofford")
    assert len(data) == 2
    data = list(data.values())
    assert data[0].name == "Wofford"
    assert data[1].name == "Wyoming"

    # Check for quoting (single and double) and url encoding
    data, _ = filter_data(all_data, "'Virginia Tech'")
    assert len(data) == 1
    assert data["vt"].name == "Virginia Tech"

    data, _ = filter_data(all_data, '"Virginia Tech"')
    assert len(data) == 1
    assert data["vt"].name == "Virginia Tech"

    data, _ = filter_data(all_data, "virginia+tech")
    assert len(data) == 1
    assert data["vt"].name == "Virginia Tech"


def test_filter_data_alias_vs_name():
    all_data, as_of = PARSED_CONTENT
    data, _ = filter_data(all_data, "mich,msu")
    assert len(data) == 2


def test_filter_data_school_aliases():
    all_data, as_of = PARSED_CONTENT
    data, _ = filter_data(all_data, "vt,wof")
    data = list(data.values())

    assert len(data) == 2
    assert data[0].name == "Virginia Tech"
    assert data[1].name == "Wofford"

    data, _ = filter_data(all_data, "VT,WOF")
    data = list(data.values())
    assert len(data) == 2
    assert data[0].name == "Virginia Tech"
    assert data[1].name == "Wofford"

    data, _ = filter_data(all_data, "Vt,Wof")
    data = list(data.values())
    assert len(data) == 2
    assert data[0].name == "Virginia Tech"
    assert data[1].name == "Wofford"


def test_write_to_console_all():
    all_data, as_of = PARSED_CONTENT

    data, meta_data = filter_data(all_data, "0")
    assert len(data) == NUM_SCHOOLS

    with captured_output() as (out, err):
        write_to_console(data, meta_data, as_of)
        out_text = out.getvalue()
    as_lines = out_text.split("\n")

    assert " Mississippi Valley St   MVSU   357   0-13  SWAC" == as_lines[357]


def test_write_to_console_top_5():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "5")

    assert len(data) == 5
    some_data = list(data.values())

    # make sure we have some output where we expect
    assert some_data[1].name == "Baylor"
    assert some_data[3].name == "Iowa"

    with captured_output() as (out, err):
        write_to_console(data, meta_data, as_of)
        out_text = out.getvalue()

    # check the formatting of at least one line
    as_lines = out_text.split("\n")

    assert "Villanova   NOVA     5   10-1  BE" == as_lines[5]


def test_write_to_console_multi_conference():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "ACC,SEC")

    assert len(data) == NUM_SEC_TEAMS + NUM_ACC_TEAMS

    # Make sure some random values are where we expect
    some_data = list(data.values())
    assert some_data[16].name == "Georgia Tech"
    assert some_data[19].name == "NC State"
    with captured_output() as (out, err):
        write_to_console(data, meta_data, as_of)
        out_text = out.getvalue()

    # Make sure the formatting for at least one line is as expected.
    as_lines = out_text.split("\n")
    assert "      Virginia    UVA     9   10-2  ACC" == as_lines[1]


def test_write_to_console_basic_conference():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "acc")

    with captured_output() as (out, err):
        write_to_console(data, meta_data, as_of)
        out_text = out.getvalue()

    as_lines = out_text.split("\n")

    # Check formatting, values, be sure we have at least one team ranked > #20
    # so we know that we're bypassing the intermittent headers include long (NC)
    # and short team names (Duke), which define width of output.
    assert "      Virginia    UVA     9   10-2  ACC" == as_lines[1]
    assert "    Florida St    FSU    15    9-2  ACC" == as_lines[2]
    assert "          Duke   DUKE    32    5-5  ACC" == as_lines[3]
    assert "North Carolina    UNC    34   10-5  ACC" == as_lines[4]

    assert NUM_ACC_TEAMS == len(as_lines) - NUM_FOOTER_LINES - NUM_HEADER_LINES
    assert " Data includes 17 of 27 games played on Sunday, January 24 " == as_lines[17]


def test_get_args_from_args():
    assert get_args(["prog", "all"]) == ("0", False)
    assert get_args(["prog", "7"]) == ("7", False)
    assert get_args(["prog", "ucla,penn"]) == ("ucla,penn", False)


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
