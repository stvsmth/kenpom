from kenpom import parse_data


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
