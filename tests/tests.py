"""
Tests for kenpom scraping, using locally stored data

Expected Output for ACC
           Virginia     1   15-0
               Duke     2   14-2
      Virginia Tech     7   14-1
     North Carolina     9   12-4
  North Carolina St    23   14-2
         Louisville    25   11-5
         Florida St    26   13-4
           Syracuse    35   12-5
            Clemson    47   10-6
       Georgia Tech    62   10-6
         Pittsburgh    68   12-5
           Miami FL    69    9-7
         Notre Dame    80   11-5
     Boston College   119    9-6
        Wake Forest   161    7-8

"""

from captured_output import captured_output
from kenpom import parse_data, filter_data, write_to_console


def mock_fetch_content():
    with open('test.html', 'r') as f:
        data = f.read()
        return data


def test_parse_data():
    page_content = mock_fetch_content()
    all_data = parse_data(page_content)

    # Test the first row, all columns to make sure we're matched
    assert 'Virginia' == all_data[0].name
    assert '1' == all_data[0].rank
    assert 'ACC' == all_data[0].conf
    assert '15-0' == all_data[0].record
    assert '+32.80' == all_data[0].eff_margin
    assert '117.9' == all_data[0].offense
    assert '6' == all_data[0].off_rank
    assert '85.1' == all_data[0].defense
    assert '2' == all_data[0].def_rank

    assert '61.0' == all_data[0].tempo
    assert '353' == all_data[0].tempo_rank
    assert '+.054' == all_data[0].luck
    assert '80' == all_data[0].luck_rank

    assert '+1.22' == all_data[0].sos_eff_margin
    assert '128' == all_data[0].sos_eff_margin_rank
    assert '102.4' == all_data[0].sos_off
    assert '227' == all_data[0].sos_off_rank
    assert '101.2' == all_data[0].sos_def
    assert '62' == all_data[0].sos_def_rank

    assert '-2.92' == all_data[0].sos_non_conf
    assert '261' == all_data[0].sos_non_conf_rank

    # ... sentimental check
    assert 'Virginia Tech' == all_data[6].name
    assert '7' == all_data[6].rank
    assert '323' == all_data[6].sos_non_conf_rank

    # Quick test row before the header
    assert 'Wofford' == all_data[39].name
    assert '40' == all_data[39].rank
    assert '17' == all_data[39].sos_non_conf_rank

    # Quick test row after the header
    assert 'Butler' == all_data[40].name
    assert '41' == all_data[40].rank
    assert '65' == all_data[40].sos_non_conf_rank


def test_write_to_console():
    page_content = mock_fetch_content()
    all_data = parse_data(page_content)
    data, meta_data = filter_data(all_data, ['ACC'])

    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    acc_teams = out_text.strip().split('\n')
    assert 15 == len(acc_teams), 'Conference filter broken'

    # Check formatting, values, be sure to test team > #20
    # so we know that we're bypassing the intermittent headers
    # include longest (NCST) and short team names (Duke), which
    # define width of output.
    assert '           Virginia     1   15-0' in out_text
    assert '               Duke     2   14-2' in out_text
    assert '      Virginia Tech     7   14-1' in out_text
    assert '  North Carolina St    23   14-2' in out_text
    assert '        Wake Forest   161    7-8' in out_text
