
import unittest

from kenpom import parse_data


def mock_fetch_content():
    with open('test.html', 'r') as f:
        data = f.read()
        return data


class KenpomTestCase(unittest.TestCase):

    def test_parse_data(self):
        page_content = mock_fetch_content()
        all_data = parse_data(page_content)

        # Test the first row, all columns to make sure we're matched
        self.assertEqual('Virginia', all_data[0].name)
        self.assertEqual('1', all_data[0].rank)
        self.assertEqual('ACC', all_data[0].conf)
        self.assertEqual('15-0', all_data[0].record)
        self.assertEqual('+32.80', all_data[0].eff_margin)
        self.assertEqual('117.9', all_data[0].offense)
        self.assertEqual('6', all_data[0].off_rank)
        self.assertEqual('85.1', all_data[0].defense)
        self.assertEqual('2', all_data[0].def_rank)

        self.assertEqual('61.0', all_data[0].tempo)
        self.assertEqual('353', all_data[0].tempo_rank)
        self.assertEqual('+.054', all_data[0].luck)
        self.assertEqual('80', all_data[0].luck_rank)

        self.assertEqual('+1.22', all_data[0].sos_eff_margin)
        self.assertEqual('128', all_data[0].sos_eff_margin_rank)
        self.assertEqual('102.4', all_data[0].sos_off)
        self.assertEqual('227', all_data[0].sos_off_rank)
        self.assertEqual('101.2', all_data[0].sos_def)
        self.assertEqual('62', all_data[0].sos_def_rank)

        self.assertEqual('-2.92', all_data[0].sos_non_conf)
        self.assertEqual('261', all_data[0].sos_non_conf_rank)

        # ... sentimental check
        self.assertEqual('Virginia Tech', all_data[6].name)
        self.assertEqual('7', all_data[6].rank)
        self.assertEqual('323', all_data[6].sos_non_conf_rank)

        # Quick test row before the header
        self.assertEqual('Wofford', all_data[39].name)
        self.assertEqual('40', all_data[39].rank)
        self.assertEqual('17', all_data[39].sos_non_conf_rank)

        # Quick test row after the header
        self.assertEqual('Butler', all_data[40].name)
        self.assertEqual('41', all_data[40].rank)
        self.assertEqual('65', all_data[40].sos_non_conf_rank)


if __name__ == '__main__':
    unittest.main()
