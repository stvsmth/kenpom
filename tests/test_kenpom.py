"""Tests for kenpom scraping, using locally stored data.

Expected Output for ACC

               Duke     1   23-2
           Virginia     2   22-2
     North Carolina     8   20-5
      Virginia Tech    12   20-5
         Louisville    14   18-8
         Florida St    20   20-5
            Clemson    30  15-10
  North Carolina St    35   18-8
           Syracuse    43   17-8
           Miami FL    74  11-14
         Notre Dame    79  13-12
         Pittsburgh    81  12-14
       Georgia Tech   109  11-15
     Boston College   112  13-11
        Wake Forest   187   9-15

Data includes 17 of 18 games played on Sunday, February 17
"""

from contextlib import contextmanager
from io import StringIO
from kenpom import parse_data, filter_data, write_to_console
from pathlib import Path
import os
import sys


NUM_ACC_TEAMS = 15
NUM_AMER_TEAMS = 12


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


# Read the file once for these tests
PARSED_CONTENT = parse_data(_fetch_test_content())


def test_parse_data():
    all_data, as_of = PARSED_CONTENT

    # Test the first row, all columns to make sure we're matched
    assert "Virginia" == all_data[1].name
    assert "2" == all_data[1].rank
    assert "ACC" == all_data[1].conf
    assert "22-2" == all_data[1].record
    assert "+34.46" == all_data[1].eff_margin
    assert "120.8" == all_data[1].offense
    assert "5" == all_data[1].off_rank
    assert "86.3" == all_data[1].defense
    assert "3" == all_data[1].def_rank

    assert "59.4" == all_data[1].tempo
    assert "353" == all_data[1].tempo_rank
    assert "+.030" == all_data[1].luck
    assert "110" == all_data[1].luck_rank

    assert "+7.96" == all_data[1].sos_eff_margin
    assert "36" == all_data[1].sos_eff_margin_rank
    assert "107.9" == all_data[1].sos_off
    assert "43" == all_data[1].sos_off_rank
    assert "100.0" == all_data[1].sos_def
    assert "33" == all_data[1].sos_def_rank

    assert "-3.07" == all_data[1].sos_non_conf
    assert "264" == all_data[1].sos_non_conf_rank

    # ... sentimental check
    assert "Virginia Tech" == all_data[11].name
    assert "12" == all_data[11].rank
    assert "329" == all_data[11].sos_non_conf_rank

    # Quick test row before the header
    assert "Lipscomb" == all_data[39].name
    assert "40" == all_data[39].rank
    assert "27" == all_data[39].sos_non_conf_rank

    # Quick test row after the header
    assert "TCU" == all_data[40].name
    assert "41" == all_data[40].rank
    assert "185" == all_data[40].sos_non_conf_rank


def test_filter_data_conf_capitalization():
    all_data, as_of = PARSED_CONTENT
    data, _ = filter_data(all_data, ["amer"], as_of)

    # Test using `amer` since KenPom doesn't capitalize all conference names
    # (only the acronyms, which are most ... eg American Athletic Conference
    # is displayed as `Amer`.
    assert len(data) == NUM_AMER_TEAMS
    assert data[0].name == "Houston"
    assert data[1].name == "Cincinnati"


def test_write_to_console_all():
    all_data, as_of = PARSED_CONTENT

    data, meta_data = filter_data(all_data, ["ALL"], as_of)

    # Grab just # 4 for cleaner diff on test failure.
    data = data[3:4]
    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    text_without_footer = out_text.split("\n")[1]
    assert "Michigan St     4   21-5  B10" in text_without_footer


def test_write_to_console_top_5():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, ["5"], as_of)

    assert len(data) == 5
    assert data[1].name == "Virginia"
    assert data[4].name == "Kentucky"

    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    assert "Michigan St     4   21-5  B10" in out_text


def test_write_to_console_multi_conference():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, ["ACC", "Amer"], as_of)

    assert len(data) == NUM_AMER_TEAMS + NUM_ACC_TEAMS
    assert data[19].name == "Tulsa"
    assert data[24].name == "Wake Forest"
    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    assert "South Florida   103   17-8  Amer" in out_text


def test_write_to_console_basic_conference():
    all_data, as_of = PARSED_CONTENT
    data, meta_data = filter_data(all_data, ["ACC"], as_of)

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
    assert "               Duke     1   23-2" in out_text
    assert "           Virginia     2   22-2" in out_text
    assert "      Virginia Tech    12   20-5" in out_text
    assert "  North Carolina St    35   18-8" in out_text
    assert "        Wake Forest   187   9-15" in out_text

    assert "Data includes 17 of 18 games played on Sunday, February 17" in out_text


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
