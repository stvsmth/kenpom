from datastructures import (
    SCHOOL_DATA_BY_NAME,
    SCHOOL_DATA_BY_ALIAS,
    CONF_NAMES,
    SCHOOL_ALIASES,
)


def test_derived_data():
    """Ensure that our derived data transformations worked.

    These are just a quick sanity check to make sure we end up with the data
    format we intended when we derive alternate structures from
    SCHOOL_DATA_BY_ALIAS
    """
    assert SCHOOL_DATA_BY_ALIAS['wof']['name'] == 'wofford'
    assert SCHOOL_DATA_BY_NAME['wofford']['alias'] == 'wof'
    assert len(SCHOOL_DATA_BY_NAME) == len(SCHOOL_DATA_BY_ALIAS)
    assert 'vt' in SCHOOL_ALIASES
    assert 'acc' in CONF_NAMES


def test_school_data_structure():
    """Verify main structure is all lowercase with no extra spaces."""

    # We'll eventually have code to regenerate this data structure, but we're fixing it
    # manually as issues arise, mostly in aliases. Until it's automated, test our edits.
    for k, data in SCHOOL_DATA_BY_ALIAS.items():
        assert k == k.lower().strip()
        assert k == k.lower().strip()
        for key, value in data.items():
            assert key == key.lower().strip()
            if type(value) == str:
                assert value == value.lower().strip()
