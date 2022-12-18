"""Tests for kenpom scraping, using locally stored data.

We consume many dict_values via list in these tests. It just feels wrong to use
a test for positioning using keyed entries. I know dicts are ordered these days,
but it still feels funny to rely on that, especially in tests.
"""

from contextlib import contextmanager
from io import StringIO
from kenpom import (
    parse_data,
    filter_data,
    write_to_console,
    NUM_SCHOOLS,
    _massage_school_name,
)
from pathlib import Path
import os
import sys

NUM_ACC_TEAMS = 15
NUM_SEC_TEAMS = 14
NUM_TEAMS_W_VALLEY_IN_NAME = 3
NUM_HEADER_LINES = 2
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
    all_data, _ = PARSED_CONTENT

    # Quick check to make sure our data is in sync with ranks, if something goes
    # haywire, this test can tell us where in the sequence of schools it went sideways.
    # In particular, if the test fails, we're missing the school BEFORE the name of the
    # school in the failing test.
    values = list(all_data.values())
    for i, team in zip(range(NUM_SCHOOLS), values):
        assert i + 1 == team.rank

    # Test both above and below the first "page break". Do a full check of every
    # column on one of these to ensure we have the correct mappings
    all_data = list(all_data.values())
    num_40 = all_data[39]
    assert num_40.name == "Utah St"
    assert num_40.rank == 40

    num_41 = all_data[40]
    assert num_41.rank == 41
    assert num_41.name == "Oregon"
    assert num_41.conf == "P12"
    assert num_41.record == "6-5"
    assert num_41.eff_margin == 15.35
    assert num_41.offense == 110.9
    assert num_41.off_rank == 35
    assert num_41.defense == 95.6
    assert num_41.def_rank == 59

    assert num_41.tempo == 67.2
    assert num_41.tempo_rank == 243
    assert num_41.luck == -0.040
    assert num_41.luck_rank == 259

    assert num_41.sos_eff_margin == 9.03
    assert num_41.sos_eff_margin_rank == 16
    assert num_41.sos_off == 106.1
    assert num_41.sos_off_rank == 22
    assert num_41.sos_def == 97.0
    assert num_41.sos_def_rank == 13

    assert num_41.sos_non_conf == 6.49
    assert num_41.sos_non_conf_rank == 34
    # Not in KenPom, we added when we parsed
    assert num_41.alias == "ORE"


def test_filter_data_conf_capitalization():
    all_data, _ = PARSED_CONTENT
    upper, _ = filter_data(all_data, "meac")
    lower, _ = filter_data(all_data, "MEAC")
    mixed, _ = filter_data(all_data, "Meac")
    assert upper == lower == mixed


def test_filter_handles_top_n():

    # Be sure this we work on double-digit numbers, otherwise
    # There's a subtle logic bug that could end up printing 2 teams
    # instead of 25. Strings being iterable and all that.
    all_data, _ = PARSED_CONTENT

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
    all_data, _ = PARSED_CONTENT

    data, _ = filter_data(all_data, "utah")
    assert len(data) == 1

    data, _ = filter_data(all_data, "amer")
    assert len(data) == 1


def test_bogus_input():
    all_data, _ = PARSED_CONTENT

    data, _ = filter_data(all_data, "foobar")
    assert len(data) == 0


def test_filter_data_school_by_name():
    all_data, _ = PARSED_CONTENT
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
    assert data[0].name == "Wyoming"
    assert data[1].name == "Wofford"

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
    all_data, _ = PARSED_CONTENT
    data, _ = filter_data(all_data, "mich,msu")
    assert len(data) == 2


def test_filter_data_school_aliases():
    all_data, _ = PARSED_CONTENT
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

    with captured_output() as (out, _):
        write_to_console(data, meta_data, as_of)
        out_text = out.getvalue()
    as_lines = out_text.split("\n")

    assert (
        as_lines[NUM_SCHOOLS + 1].strip()
        == "IUPUI  IUPUI   363  363 / 361    2-9  Horz"
    )


def test_write_to_console_top_5():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "5")

    assert len(data) == 5
    some_data = list(data.values())

    # make sure we have some output where we expect (offset by 1, so #2, #4)
    assert some_data[1].name == "Houston"
    assert some_data[3].name == "UCLA"

    with captured_output() as (out, _):
        write_to_console(data, meta_data, as_of)
        out_text = out.getvalue()

    # check the formatting of at least one line
    as_lines = out_text.split("\n")
    assert "     Kansas     KU     5   13 /   9   10-1   B12" == as_lines[6]


def test_write_to_console_multi_conference():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "ACC,SEC")

    assert len(data) == NUM_SEC_TEAMS + NUM_ACC_TEAMS

    # Make sure some random values are where we expect
    some_data = list(data.values())
    assert some_data[8].name == "Virginia Tech"
    assert some_data[24].name == "Georgia Tech"

    with captured_output() as (out, _):
        write_to_console(data, meta_data, as_of)
        out_text = out.getvalue()

    # Make sure the formatting for at least one line is as expected.
    # ... note there are 2 lines of header, so offset by 2
    as_lines = out_text.split("\n")
    assert "      Virginia    UVA    11   12 /  26    8-1   ACC" == as_lines[4]


def test_write_to_console_basic_conference():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, "acc")

    with captured_output() as (out, _):
        write_to_console(data, meta_data, as_of)
        out_text = out.getvalue()

    as_lines = out_text.split("\n")

    # Check formatting, values, be sure we have at least one team ranked > #20
    # so we know that we're bypassing the intermittent headers include long (NC)
    # and short team names (Duke), which define width of output.
    assert as_lines[2] == "      Virginia    UVA    11   12 /  26    8-1   ACC"
    assert as_lines[3] == "          Duke   DUKE    14   17 /  21   10-2   ACC"
    assert as_lines[4] == "North Carolina    UNC    20   10 /  55    8-4   ACC"
    assert as_lines[5] == " Virginia Tech     VT    25   18 /  53   11-1   ACC"

    assert NUM_ACC_TEAMS == len(as_lines) - NUM_FOOTER_LINES - NUM_HEADER_LINES
    assert as_lines[18] == "Data includes 84 of 97 games played on Saturday, December 17"


def test_massage_school_name():
    assert _massage_school_name("Gonzaga 1") == "Gonzaga"
    assert _massage_school_name("Gonzaga") == "Gonzaga"
    assert _massage_school_name("Boise St. 4") == "Boise St"
    assert _massage_school_name("One Two Three 245") == "One Two Three"
    assert _massage_school_name("") == ""


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
