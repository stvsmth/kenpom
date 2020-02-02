from datastructures import (
    SCHOOL_ABBREVS,
    SCHOOL_NAMES,
    _school_abbrevs,
    _school_names,
)
from kenpom import (
    translate_abbrevs_to_names,
    translate_names_to_abbrevs,
    NUM_SCHOOLS,
)


def test_translate_names_to_abbrevs():
    assert [] == translate_abbrevs_to_names(["FOO"])
    assert ["kansas"] == translate_abbrevs_to_names(["KU"])
    assert ["kansas"] == translate_abbrevs_to_names(["ku"])
    assert ["duke", "virginia"] == translate_abbrevs_to_names(["DUKE", "uva"])
    assert ["virginia tech", "wofford"] == translate_abbrevs_to_names(["VT", "WOF"])


def test_translate_abbrevs_to_names():
    assert [] == translate_abbrevs_to_names([""])
    assert ["KU"] == translate_names_to_abbrevs(["Kansas"])
    assert ["DUKE", "UVA"] == translate_names_to_abbrevs(["duke", "Virginia"])
    assert ["VT", "WOF"] == translate_names_to_abbrevs(["virginia Tech", "Wofford"])


def test_for_duplicates_and_bad_d1_count():
    num_abbrevs = len(SCHOOL_ABBREVS)
    num_names = len(SCHOOL_NAMES)

    if num_abbrevs == num_names:
        assert num_names == NUM_SCHOOLS, "Looks like school added or removed"
    else:
        for item in (_school_abbrevs, _school_names):
            seen = {}
            dupes = []
            for x in list(item):
                if x not in seen:
                    seen[x] = 1
                else:
                    if seen[x] == 1:
                        dupes.append(x)
                    seen[x] += 1

            msg = "names, abbrev mismatch {} != {}. Dupe: {}".format(
                num_names, num_abbrevs, dupes
            )
            assert num_abbrevs == num_names, msg
