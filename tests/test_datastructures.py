from datastructures import (
    CONF_NAMES,
    SCHOOL_ABBREVS,
    SCHOOL_DATA_BY_ABBREV,
    SCHOOL_DATA_BY_NAME,
)


def test_derived_data():
    """Ensure that our derived data transformations worked.

    These are just a quick sanity check to make sure we end up with the data
    format we intended when we derive alternate structures from
    SCHOOL_DATA_BY_ABBREV
    """
    assert SCHOOL_DATA_BY_ABBREV['wof']['name'] == 'wofford'
    assert SCHOOL_DATA_BY_NAME['wofford']['abbrev'] == 'wof'
    assert len(SCHOOL_DATA_BY_NAME) == len(SCHOOL_DATA_BY_ABBREV)
    assert 'vt' in SCHOOL_ABBREVS
    assert 'acc' in CONF_NAMES


def test_school_data_structure():
    """Verify main structure is all lowercase with no extra spaces."""

    # We'll eventually have code to regenerate this data structure, but we're fixing it
    # manually as issues arise, mostly in abbrevs. Until it's automated, test our edits.
    for k, data in SCHOOL_DATA_BY_ABBREV.items():
        assert k == k.lower().strip()
        assert k == k.lower().strip()
        for key, value in data.items():
            assert key == key.lower().strip()
            if type(value) == str:
                assert value == value.lower().strip()
