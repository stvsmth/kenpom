# KenPom scraper 🏀

A little bit of Python to scrape the front page of the wonderfully useful
[KenPom](https://kenpom.com) site for NCAA basketball statistics. This tool assumes
you are comfortable on the command-line.

Why scrape? Well, if your team rarely haunts the top 25 and/or your curious how your
team ranks against other non-ranked teams, KenPom is one way to compare relative
strengths.  I find I this tool particularly useful on my iPhone with
[Pythonista](http://omz-software.com/pythonista/).

This tool is tested against all version >= Python 3.6. While I would love to make use
of Python 3.7+ features, Pythonista is currently stuck on Python 3.6.

![tests](https://github.com/stvsmth/kenpom/workflows/tests/badge.svg)

## Installation

This is tool primarily uses [requests](https://requests.readthedocs.io/en/master/)
and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). While not
required, using virtual environments is almost always the smart thing to do. Also, we
use some pre-commit hooks to keep things formatted nicely and avoid some silly mistakes.

```bash
git clone https://github.com/stvsmth/kenpom.git
python3 -m venv kenpom
cd kenpom && source bin/activate
pip install -r requirements.txt
pre-commit install
pytest tests
```

## Usage

You can pass filtering options in via command-line arguments or as prompted. We'll
filter on conference(s), school names(s), or the top `n` schools. With no input we
simply print the top 25 teams. Conference and school names are case insensitive. While
conference names must match exactly, school names will match on any string. For example,
`irgini` will match schools with `Virginia` in the name.

#### Conference name vs school name searches
Conference searches take precedence over school name searches.

You will probably forget this and never even care. Unless, that is, you're fond of
American University (for which searching `amer` will return the American Athletic
Conference schools) or short search strings like `be` (Big East). Generally speaking,
you should **use five characters or more for school name searches**. You've been warned.

#### Basic usage

Without any command line options, we'll prompt you for one of three values: `n` for
a top-`n` search, a conference code, or a school name. The default is a top-25 search.

    (kenpom) $ python kenpom.py
    Top `n`, 0 for all, school(s), or conference(s) [25]:

            Kansas     1   17-3  B12
              Duke     2   17-3  ACC
            Baylor     3   18-1  B12
            [snip]   ...    ...  ...
        Texas Tech    24   13-7  B12
           Rutgers    25   16-5  B10

    Data through games of Thursday, January 30

We'll be leaving out the footer for the remaining examples.

#### Searching for schools by name(s)

This is probably the most useful mode. Your team is playing Duke? How do they match up?

    (kenpom) $ python kenpom.py duke,woff

        Duke     2   17-3  ACC
     Wofford   147   14-8  SC

#### Searching for schools by full name(s)

Searching for schools by full name, when that name includes a space, requires some care.
You can quote the school name(s) using single or double quotes:

    (kenpom) $ python kenpom.py "virginia tech",'florida st'

        Florida St    21   17-3  ACC
     Virginia Tech    72   14-7  ACC

Or you can use a plus sign (+) in lieu of a space. This is handy if you start typing and
are too lazy to go back and add a leading quote.

    (kenpom) $ python kenpom.py virginia+tech

     Virginia Tech    72   14-7  ACC

#### Schools in one or more conferences

    (kenpom) $ python kenpom.py sec,acc

                Duke     2   17-3  ACC
          Louisville    10   17-3  ACC
          Florida St    18   17-3  ACC
            Kentucky    25   15-4  SEC
               [snip]  ...    ...  ...
      Boston College   166  10-10  ACC
          Vanderbilt   183   8-11  SEC

#### Fetch the top `n` teams

    (kenpom) $ python kenpom.py 7

            Kansas     1   17-3  B12
              Duke     2   17-3  ACC
           Gonzaga     3   21-1  WCC
            Baylor     4   17-1  B12
            Dayton     5   18-2  A10
     West Virginia     6   16-3  B12
       Michigan St     7   15-5  B10

#### Fetch all rankings

    (kenpom) $ python kenpom.py 0

         Kansas     1   17-3  B12
           Duke     2   17-3  ACC
        Gonzaga     3   21-1  WCC
         [snip]   ...    ...  ...
     Chicago St   353   4-18  WAC
