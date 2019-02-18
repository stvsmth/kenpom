"""
Tests for kenpom scraping, using locally stored data

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

from captured_output import captured_output
from kenpom import parse_data, filter_data, write_to_console


NUM_ACC_TEAMS = 15


def mock_fetch_content():
    with open('test.html', 'r') as f:
        data = f.read()
        return data


def test_parse_data():
    page_content = mock_fetch_content()
    all_data, as_of = parse_data(page_content)

    # Test the first row, all columns to make sure we're matched
    assert 'Virginia' == all_data[1].name
    assert '2' == all_data[1].rank
    assert 'ACC' == all_data[1].conf
    assert '22-2' == all_data[1].record
    assert '+34.46' == all_data[1].eff_margin
    assert '120.8' == all_data[1].offense
    assert '5' == all_data[1].off_rank
    assert '86.3' == all_data[1].defense
    assert '3' == all_data[1].def_rank

    assert '59.4' == all_data[1].tempo
    assert '353' == all_data[1].tempo_rank
    assert '+.030' == all_data[1].luck
    assert '110' == all_data[1].luck_rank

    assert '+7.96' == all_data[1].sos_eff_margin
    assert '36' == all_data[1].sos_eff_margin_rank
    assert '107.9' == all_data[1].sos_off
    assert '43' == all_data[1].sos_off_rank
    assert '100.0' == all_data[1].sos_def
    assert '33' == all_data[1].sos_def_rank

    assert '-3.07' == all_data[1].sos_non_conf
    assert '264' == all_data[1].sos_non_conf_rank

    # ... sentimental check
    assert 'Virginia Tech' == all_data[11].name
    assert '12' == all_data[11].rank
    assert '329' == all_data[11].sos_non_conf_rank

    # Quick test row before the header
    assert 'Lipscomb' == all_data[39].name
    assert '40' == all_data[39].rank
    assert '27' == all_data[39].sos_non_conf_rank

    # Quick test row after the header
    assert 'TCU' == all_data[40].name
    assert '41' == all_data[40].rank
    assert '185' == all_data[40].sos_non_conf_rank


def test_write_to_console():
    page_content = mock_fetch_content()
    all_data, as_of = parse_data(page_content)
    data, meta_data = filter_data(all_data, ['ACC'], as_of)

    with captured_output() as (out, err):
        write_to_console(data, meta_data)
        out_text = out.getvalue()

    acc_teams = out_text.strip().split('\n')
    # There are 15 teams in the ACC, plus two lines for the as_of data
    assert NUM_ACC_TEAMS + 2 == len(acc_teams), 'Conference filter broken'

    # Check formatting, values, be sure to test team > #20
    # so we know that we're bypassing the intermittent headers
    # include longest (NCST) and short team names (Duke), which
    # define width of output.
    assert '               Duke     1   23-2' in out_text
    assert '           Virginia     2   22-2' in out_text
    assert '      Virginia Tech    12   20-5' in out_text
    assert '  North Carolina St    35   18-8' in out_text
    assert '        Wake Forest   187   9-15' in out_text

    assert 'Data includes 17 of 18 games played on Sunday, February 17' in out_text
